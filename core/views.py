from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import Conteneur, Participation, Portefeuille, Transaction, TauxDeChange, Fournisseur
from .serializers import (
    ConteneurSerializer, ParticipationSerializer, UtilisateurSerializer,
    PortefeuilleSerializer, TransactionSerializer, TauxDeChangeSerializer,
    OTPRequestSerializer, OTPVerifySerializer, FournisseurSerializer
)
from .validators import get_file_info

Utilisateur = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def demander_otp(request):
    serializer = OTPRequestSerializer(data=request.data)
    if serializer.is_valid():
        telephone = serializer.validated_data['telephone']
        
        utilisateur, created = Utilisateur.objects.get_or_create(
            telephone=telephone,
            defaults={'username': telephone}
        )
        
        otp_code = utilisateur.generate_otp()
        
        return Response({
            'message': f'Code OTP envoyé au {telephone}',
            'otp_code': otp_code,
            'debug': True
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verifier_otp(request):
    serializer = OTPVerifySerializer(data=request.data)
    if serializer.is_valid():
        telephone = serializer.validated_data['telephone']
        otp_code = serializer.validated_data['otp_code']
        
        try:
            utilisateur = Utilisateur.objects.get(telephone=telephone)
        except Utilisateur.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        
        if utilisateur.verify_otp(otp_code):
            if not hasattr(utilisateur, 'portefeuille'):
                Portefeuille.objects.create(utilisateur=utilisateur)
            
            refresh = RefreshToken.for_user(utilisateur)
            
            redirect_url = '/admin-panel/' if utilisateur.is_staff or utilisateur.is_superuser else '/commercant/dashboard/'
            
            return Response({
                'message': 'Connexion réussie',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'utilisateur': UtilisateurSerializer(utilisateur).data,
                'redirect_url': redirect_url,
                'is_admin': utilisateur.is_staff or utilisateur.is_superuser
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Code OTP invalide ou expiré'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConteneurViewSet(viewsets.ModelViewSet):
    queryset = Conteneur.objects.filter(annule=False)
    serializer_class = ConteneurSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html' or request.META.get('HTTP_ACCEPT', '').startswith('text/html'):
            conteneurs = self.get_queryset()
            total_objectif = conteneurs.aggregate(total=Sum('objectif'))['total'] or 0
            total_collecte = conteneurs.aggregate(total=Sum('montant_actuel'))['total'] or 0
            
            return render(request, 'api/conteneurs.html', {
                'title': '📦 Conteneurs',
                'description': 'Liste des conteneurs de marchandises',
                'conteneurs': conteneurs,
                'total_objectif': total_objectif,
                'total_collecte': total_collecte,
            })
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html' or request.META.get('HTTP_ACCEPT', '').startswith('text/html'):
            conteneur = self.get_object()
            participations = conteneur.participation_set.all()
            progression = conteneur.get_progression()
            objectif_gnf = conteneur.get_objectif_en_gnf()
            montant_manquant = max(0, objectif_gnf - conteneur.montant_actuel)
            montant_moyen = conteneur.montant_actuel / participations.count() if participations.count() > 0 else 0
            
            return render(request, 'api/conteneur_detail.html', {
                'title': f'📦 {conteneur.nom}',
                'description': f'Détails du conteneur {conteneur.nom}',
                'conteneur': conteneur,
                'participations': participations,
                'progression': progression,
                'objectif_gnf': objectif_gnf,
                'montant_manquant': montant_manquant,
                'montant_moyen': montant_moyen,
                'total_participants': participations.count(),
                'participations_validees': participations.filter(valide=True).count(),
                'participations_attente': participations.filter(valide=False).count(),
            })
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        conteneur = self.get_object()
        conteneur.annuler_et_rembourser()
        return Response({'message': 'Conteneur annulé et remboursements effectués'})

class ParticipationViewSet(viewsets.ModelViewSet):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html' or request.META.get('HTTP_ACCEPT', '').startswith('text/html'):
            participations = self.get_queryset()
            validees = participations.filter(valide=True).count()
            en_attente = participations.filter(valide=False).count()
            
            return render(request, 'api/participations.html', {
                'title': '🤝 Participations',
                'description': 'Liste des participations aux conteneurs',
                'participations': participations,
                'validees': validees,
                'en_attente': en_attente,
            })
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Participation.objects.all()
            return Participation.objects.filter(utilisateur=self.request.user)
        return Participation.objects.all()
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(utilisateur=self.request.user)
        else:
            serializer.save()

class PortefeuilleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PortefeuilleSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html' or request.META.get('HTTP_ACCEPT', '').startswith('text/html'):
            portefeuilles = Portefeuille.objects.all()
            solde_total = portefeuilles.aggregate(total=Sum('solde'))['total'] or 0
            solde_moyen = solde_total / portefeuilles.count() if portefeuilles.count() > 0 else 0
            
            return render(request, 'api/portefeuilles.html', {
                'title': '💰 Portefeuilles',
                'description': 'Liste des portefeuilles utilisateurs',
                'portefeuilles': portefeuilles,
                'solde_total': solde_total,
                'solde_moyen': solde_moyen,
            })
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Portefeuille.objects.filter(utilisateur=self.request.user)
        return Portefeuille.objects.all()

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html' or request.META.get('HTTP_ACCEPT', '').startswith('text/html'):
            transactions = Transaction.objects.all()
            depots = transactions.filter(type_transaction='depot').count()
            retraits = transactions.filter(type_transaction='retrait').count()
            remboursements = transactions.filter(type_transaction='remboursement').count()
            
            return render(request, 'api/transactions.html', {
                'title': '📝 Transactions',
                'description': 'Historique des transactions',
                'transactions': transactions[:50],
                'depots': depots,
                'retraits': retraits,
                'remboursements': remboursements,
            })
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Transaction.objects.filter(portefeuille__utilisateur=self.request.user)
        return Transaction.objects.all()

class TauxDeChangeViewSet(viewsets.ModelViewSet):
    queryset = TauxDeChange.objects.all()
    serializer_class = TauxDeChangeSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html' or request.META.get('HTTP_ACCEPT', '').startswith('text/html'):
            taux = self.get_queryset()
            actifs = taux.filter(actif=True).count()
            inactifs = taux.filter(actif=False).count()
            
            return render(request, 'api/taux_change.html', {
                'title': '💱 Taux de Change',
                'description': 'Taux de conversion des devises',
                'taux': taux,
                'actifs': actifs,
                'inactifs': inactifs,
            })
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def actifs(self, request):
        taux_actifs = TauxDeChange.objects.filter(actif=True)
        serializer = self.get_serializer(taux_actifs, many=True)
        return Response(serializer.data)


class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.filter(verifie=True)
    serializer_class = FournisseurSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html' or request.META.get('HTTP_ACCEPT', '').startswith('text/html'):
            fournisseurs = self.get_queryset()
            
            categorie_filter = request.GET.get('categorie', '')
            pays_filter = request.GET.get('pays', '')
            
            if categorie_filter:
                fournisseurs = fournisseurs.filter(categorie=categorie_filter)
            if pays_filter:
                fournisseurs = fournisseurs.filter(pays_origine=pays_filter)
            
            stats = {
                'total': Fournisseur.objects.filter(verifie=True).count(),
                'textile': fournisseurs.filter(categorie='TEXTILE').count(),
                'electro': fournisseurs.filter(categorie='ELECTRO').count(),
                'beaute': fournisseurs.filter(categorie='BEAUTE').count(),
                'maison': fournisseurs.filter(categorie='MAISON').count(),
            }
            
            return render(request, 'api/fournisseurs.html', {
                'title': '🏭 Catalogue Fournisseurs Certifiés',
                'description': 'Fournisseurs vérifiés pour l\'import Chine/Dubaï/Turquie',
                'fournisseurs': fournisseurs,
                'stats': stats,
                'categorie_filter': categorie_filter,
                'pays_filter': pays_filter,
            })
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html' or request.META.get('HTTP_ACCEPT', '').startswith('text/html'):
            fournisseur = self.get_object()
            
            return render(request, 'api/fournisseur_detail.html', {
                'title': f'🏭 {fournisseur.nom}',
                'description': fournisseur.specialite,
                'fournisseur': fournisseur,
            })
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def par_categorie(self, request):
        categorie = request.query_params.get('categorie')
        if categorie:
            fournisseurs = self.queryset.filter(categorie=categorie)
            serializer = self.get_serializer(fournisseurs, many=True)
            return Response(serializer.data)
        return Response({'error': 'Paramètre categorie requis'}, status=400)
