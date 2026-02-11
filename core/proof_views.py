from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Participation
from .validators import get_file_info
import os

@staff_member_required
def proof_viewer(request, participation_id):
    participation = get_object_or_404(Participation, id=participation_id)
    
    # Gérer les actions de validation/rejet
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'validate':
            participation.valide = True
            participation.save()
            participation.conteneur.mettre_a_jour_montant()
            messages.success(request, f'Participation de {participation.utilisateur.telephone} validée avec succès!')
            return redirect('/admin/core/participation/')
        
        elif action == 'reject':
            messages.warning(request, f'Participation de {participation.utilisateur.telephone} rejetée.')
            return redirect('/admin/core/participation/')
    
    # Informations sur le fichier
    file_info = {}
    if participation.preuve_paiement and os.path.exists(participation.preuve_paiement.path):
        file_info = get_file_info(participation.preuve_paiement)
    
    context = {
        'title': f'Preuve de Paiement - {participation.utilisateur.telephone}',
        'description': f'Validation de la participation de {participation.montant} GNF',
        'participation': participation,
        'file_info': file_info,
    }
    
    return render(request, 'api/proof_viewer.html', context)
