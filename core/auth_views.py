from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

def login_view(request):
    """
    Affiche le formulaire de connexion OTP
    """
    return render(request, 'auth/login.html')


@login_required
def redirect_after_login(request):
    """
    Redirige l'utilisateur selon son rôle après connexion
    """
    user = request.user
    
    # Si admin/staff → dashboard admin
    if user.is_staff or user.is_superuser:
        return redirect('/admin-panel/')
    
    # Sinon → dashboard commerçant
    return redirect('/commercant/dashboard/')


@staff_member_required
def admin_dashboard_view(request):
    """
    Dashboard pour les administrateurs uniquement
    """
    from core.models import Conteneur, Participation, Portefeuille, Transaction, Utilisateur
    
    context = {
        'total_conteneurs': Conteneur.objects.filter(annule=False).count(),
        'total_participations': Participation.objects.count(),
        'total_utilisateurs': Utilisateur.objects.count(),
        'total_portefeuilles': Portefeuille.objects.count(),
        'participations_attente': Participation.objects.filter(valide=False).count(),
    }
    
    return render(request, 'auth/admin_panel.html', context)
