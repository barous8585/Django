from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Conteneur, Participation, Utilisateur, Portefeuille, Transaction, TauxDeChange, Fournisseur

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'telephone', 'username', 'is_phone_verified', 'date_joined']
        read_only_fields = ['id', 'is_phone_verified', 'date_joined']

class OTPRequestSerializer(serializers.Serializer):
    telephone = serializers.CharField(max_length=15)

class OTPVerifySerializer(serializers.Serializer):
    telephone = serializers.CharField(max_length=15)
    otp_code = serializers.CharField(max_length=6)

class PortefeuilleSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer(read_only=True)
    
    class Meta:
        model = Portefeuille
        fields = ['id', 'utilisateur', 'solde', 'date_creation', 'date_mise_a_jour']
        read_only_fields = ['id', 'solde', 'date_creation', 'date_mise_a_jour']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'type_transaction', 'montant', 'conteneur', 'description', 'date_transaction']
        read_only_fields = ['id', 'date_transaction']

class TauxDeChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TauxDeChange
        fields = ['id', 'devise', 'taux_gnf', 'date_application', 'actif']
        read_only_fields = ['id', 'date_application']

class ParticipationSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer(read_only=True)
    preuve_paiement_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Participation
        fields = ['id', 'conteneur', 'utilisateur', 'montant', 'reference_paiement', 
                  'preuve_paiement', 'preuve_paiement_url', 'valide', 'date_participation']
        read_only_fields = ['id', 'utilisateur', 'valide', 'date_participation']
    
    def get_preuve_paiement_url(self, obj):
        if obj.preuve_paiement:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.preuve_paiement.url)
        return None

class ConteneurSerializer(serializers.ModelSerializer):
    progression = serializers.SerializerMethodField()
    objectif_gnf = serializers.SerializerMethodField()
    participations = ParticipationSerializer(many=True, read_only=True, source='participation_set')
    
    class Meta:
        model = Conteneur
        fields = ['id', 'nom', 'objectif', 'devise', 'objectif_gnf', 'montant_actuel', 
                  'etape', 'progression', 'annule', 'date_creation', 'participations']
        read_only_fields = ['id', 'montant_actuel', 'date_creation']
    
    def get_progression(self, obj):
        return obj.get_progression()
    
    def get_objectif_gnf(self, obj):
        return float(obj.get_objectif_en_gnf())


class FournisseurSerializer(serializers.ModelSerializer):
    badge_icon = serializers.SerializerMethodField()
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)
    pays_display = serializers.CharField(source='get_pays_origine_display', read_only=True)
    
    class Meta:
        model = Fournisseur
        fields = ['id', 'nom', 'categorie', 'categorie_display', 'badges_confiance', 
                  'badge_icon', 'specialite', 'moq', 'argument_vente', 
                  'annees_experience', 'pays_origine', 'pays_display', 'verifie', 'date_ajout']
        read_only_fields = ['id', 'date_ajout']
    
    def get_badge_icon(self, obj):
        return obj.get_badge_icon()
