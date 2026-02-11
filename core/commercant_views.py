from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Participation, Portefeuille, Conteneur
from django.db.models import Sum, Count

@login_required
def commercant_dashboard(request):
    """
    Dashboard pour les commerçants (utilisateurs non-staff)
    """
    user = request.user
    
    # Rediriger les admins vers l'admin panel
    if user.is_staff or user.is_superuser:
        return redirect('/admin-panel/')
    
    # Récupérer ou créer le portefeuille
    portefeuille, created = Portefeuille.objects.get_or_create(utilisateur=user)
    
    # Récupérer les participations de l'utilisateur
    participations = Participation.objects.filter(
        utilisateur=user
    ).select_related('conteneur').order_by('-date_participation')
    
    # Statistiques
    stats = {
        'total_investi': participations.filter(valide=True).aggregate(
            total=Sum('montant')
        )['total'] or 0,
        'nb_participations': participations.count(),
        'valides': participations.filter(valide=True).count(),
        'nb_conteneurs': participations.values('conteneur').distinct().count(),
    }
    
    context = {
        'user': user,
        'portefeuille': portefeuille,
        'participations': participations,
        'stats': stats,
    }
    
    return render(request, 'commercant_dashboard.html', context)


@login_required
def commercant_participer(request):
    """
    Page pour participer à un conteneur
    """
    user = request.user
    
    # Rediriger les admins
    if user.is_staff or user.is_superuser:
        return redirect('/admin-panel/')
    
    # Conteneurs disponibles (en collecte, non annulés)
    conteneurs = Conteneur.objects.filter(
        etape='collecte',
        annule=False
    ).order_by('-date_creation')
    
    context = {
        'user': user,
        'conteneurs': conteneurs,
    }
    
    return render(request, 'commercant_participer.html', context)


@login_required
def commercant_historique(request):
    """
    Historique complet des participations et transactions
    """
    user = request.user
    
    # Rediriger les admins
    if user.is_staff or user.is_superuser:
        return redirect('/admin-panel/')
    
    # Toutes les participations
    participations = Participation.objects.filter(
        utilisateur=user
    ).select_related('conteneur').order_by('-date_participation')
    
    # Transactions du portefeuille
    portefeuille = Portefeuille.objects.get(utilisateur=user)
    transactions = portefeuille.transactions.all()[:20]  # 20 dernières
    
    context = {
        'user': user,
        'participations': participations,
        'transactions': transactions,
    }
    
    return render(request, 'commercant_historique.html', context)


@login_required
def commercant_profil(request):
    """
    Profil de l'utilisateur commerçant
    """
    user = request.user
    
    # Rediriger les admins
    if user.is_staff or user.is_superuser:
        return redirect('/admin-panel/')
    
    portefeuille = Portefeuille.objects.get(utilisateur=user)
    
    # Stats globales
    total_investi = Participation.objects.filter(
        utilisateur=user,
        valide=True
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    nb_conteneurs_termines = Participation.objects.filter(
        utilisateur=user,
        conteneur__etape='port'
    ).values('conteneur').distinct().count()
    
    context = {
        'user': user,
        'portefeuille': portefeuille,
        'total_investi': total_investi,
        'nb_conteneurs_termines': nb_conteneurs_termines,
    }
    
    return render(request, 'commercant_profil.html', context)
