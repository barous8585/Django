from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Utilisateur, Conteneur, Participation, Portefeuille, Transaction, TauxDeChange, Fournisseur, Commande

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ['telephone', 'username', 'is_phone_verified', 'date_joined']
    list_filter = ['is_phone_verified', 'date_joined']
    search_fields = ['telephone', 'username']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('telephone', 'username', 'password')}),
        ('Vérification', {'fields': ('is_phone_verified', 'otp_code', 'otp_created_at')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telephone', 'username', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login', 'otp_code', 'otp_created_at']

@admin.register(Portefeuille)
class PortefeuilleAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'afficher_solde', 'date_creation', 'date_mise_a_jour']
    search_fields = ['utilisateur__telephone']
    readonly_fields = ['date_creation', 'date_mise_a_jour']
    
    def afficher_solde(self, obj):
        return format_html('<strong>{} GNF</strong>', obj.solde)
    afficher_solde.short_description = 'Solde'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['portefeuille', 'type_transaction', 'montant', 'conteneur', 'date_transaction']
    list_filter = ['type_transaction', 'date_transaction']
    search_fields = ['portefeuille__utilisateur__telephone', 'description']
    readonly_fields = ['date_transaction']

@admin.register(TauxDeChange)
class TauxDeChangeAdmin(admin.ModelAdmin):
    list_display = ['devise', 'taux_gnf', 'date_application', 'actif']
    list_filter = ['devise', 'actif', 'date_application']
    list_editable = ['actif']
    ordering = ['-date_application']

@admin.register(Conteneur)
class ConteneurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'afficher_progression', 'devise', 'objectif', 'montant_actuel', 'etape', 'annule', 'date_creation']
    list_filter = ['etape', 'devise', 'annule', 'date_creation']
    search_fields = ['nom']
    readonly_fields = ['montant_actuel', 'date_creation']
    actions = ['annuler_conteneurs']
    
    def afficher_progression(self, obj):
        progression = obj.get_progression()
        couleur = '#28a745' if progression >= 100 else '#ffc107' if progression >= 50 else '#dc3545'
        return format_html(
            '<div style="width:100px; background-color:#e9ecef; border-radius:5px;">'
            '<div style="width:{}%; background-color:{}; height:20px; border-radius:5px; text-align:center; color:white; font-weight:bold;">'
            '{}%'
            '</div></div>',
            min(progression, 100), couleur, progression
        )
    afficher_progression.short_description = 'Progression'
    
    def annuler_conteneurs(self, request, queryset):
        for conteneur in queryset:
            conteneur.annuler_et_rembourser()
        self.message_user(request, f'{queryset.count()} conteneur(s) annulé(s) et remboursé(s)')
    annuler_conteneurs.short_description = "Annuler et rembourser les conteneurs sélectionnés"

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'conteneur', 'montant', 'reference_paiement', 'afficher_preuve', 'valide', 'date_participation']
    list_filter = ['valide', 'date_participation', 'conteneur']
    search_fields = ['utilisateur__telephone', 'reference_paiement']
    list_editable = ['valide']
    actions = ['valider_paiements']
    readonly_fields = ['afficher_preuve_grande', 'afficher_lien_viewer']
    
    def afficher_preuve(self, obj):
        if obj.preuve_paiement:
            return format_html(
                '<a href="/api/proof/{}/" target="_blank" style="background: #667eea; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none;">🔍 Voir</a>',
                obj.id
            )
        return format_html('<span style="color: #dc3545;">❌ Aucune</span>')
    afficher_preuve.short_description = 'Preuve'
    
    def afficher_lien_viewer(self, obj):
        if obj.preuve_paiement:
            return format_html(
                '<a href="/api/proof/{}/" target="_blank" style="background: #28a745; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; display: inline-block; margin: 10px 0;">🔍 Ouvrir le Visualiseur de Preuve</a>',
                obj.id
            )
        return "Aucune preuve de paiement uploadée"
    afficher_lien_viewer.short_description = 'Visualiseur'
    
    def afficher_preuve_grande(self, obj):
        if obj.preuve_paiement:
            return format_html(
                '<div style="text-align: center;">'
                '<img src="{}" style="max-width:500px; height:auto; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);" />'
                '<p style="margin-top: 10px; color: #666;">Cliquez sur "Visualiseur" pour une vue complète avec zoom</p>'
                '</div>',
                obj.preuve_paiement.url
            )
        return "Aucune preuve de paiement"
    afficher_preuve_grande.short_description = 'Preuve de paiement'
    
    def valider_paiements(self, request, queryset):
        participations_validees = queryset.update(valide=True)
        
        conteneurs = set(queryset.values_list('conteneur', flat=True))
        for conteneur_id in conteneurs:
            conteneur = Conteneur.objects.get(id=conteneur_id)
            conteneur.mettre_a_jour_montant()
        
        self.message_user(
            request,
            f'{participations_validees} paiement(s) validé(s) avec succès. Les conteneurs ont été mis à jour.'
        )
    
    valider_paiements.short_description = "Valider les paiements sélectionnés"


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'afficher_badge', 'moq', 'annees_experience', 'pays_origine', 'verifie', 'date_ajout']
    list_filter = ['categorie', 'pays_origine', 'verifie', 'annees_experience']
    search_fields = ['nom', 'specialite', 'badges_confiance']
    list_editable = ['verifie']
    ordering = ['categorie', 'nom']
    
    fieldsets = (
        ('Informations Générales', {
            'fields': ('nom', 'categorie', 'pays_origine', 'annees_experience', 'verifie')
        }),
        ('Produits & Confiance', {
            'fields': ('badges_confiance', 'specialite', 'moq')
        }),
        ('Marketing', {
            'fields': ('argument_vente',)
        }),
        ('Dates', {
            'fields': ('date_ajout',)
        }),
    )
    
    readonly_fields = ['date_ajout']
    
    def afficher_badge(self, obj):
        icon = obj.get_badge_icon()
        badges = obj.badges_confiance
        
        if 'Verified' in badges:
            couleur = '#28a745'
        elif 'Gold' in badges:
            couleur = '#ffc107'
        elif 'Trade Assurance' in badges:
            couleur = '#007bff'
        else:
            couleur = '#6c757d'
        
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{} {}</span>',
            couleur, icon, badges
        )
    afficher_badge.short_description = 'Badges de Confiance'


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'utilisateur', 'conteneur', 'volume_cbm', 'total_a_payer', 'statut', 'date_creation']
    list_filter = ['statut', 'categorie_produit', 'date_creation']
    search_fields = ['utilisateur__telephone', 'description_produit']
    list_editable = ['statut']
    readonly_fields = ['prix_achat_gnf', 'frais_commission', 'frais_logistique', 'total_a_payer', 
                       'montant_fournisseur', 'montant_transitaire', 'marge_plateforme', 
                       'date_creation', 'date_modification', 'afficher_calcul_detaille']
    
    fieldsets = (
        ('Client & Conteneur', {
            'fields': ('utilisateur', 'conteneur', 'fournisseur', 'statut')
        }),
        ('Produit', {
            'fields': ('description_produit', 'categorie_produit', 'volume_cbm')
        }),
        ('Prix & Tarifs', {
            'fields': ('prix_achat_yuan', 'taux_change', 'commission_pct')
        }),
        ('Calcul Automatique (Lecture seule)', {
            'fields': ('prix_achat_gnf', 'frais_commission', 'frais_logistique', 'total_a_payer'),
            'classes': ('collapse',)
        }),
        ('Répartition Comptable (Lecture seule)', {
            'fields': ('montant_fournisseur', 'montant_transitaire', 'marge_plateforme'),
            'classes': ('collapse',)
        }),
        ('Détail du Calcul', {
            'fields': ('afficher_calcul_detaille',),
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def afficher_calcul_detaille(self, obj):
        if obj.id:
            return format_html('<pre>{}</pre>', obj.get_detail_calcul())
        return "Sauvegardez d'abord pour voir le calcul"
    afficher_calcul_detaille.short_description = '📊 Détail du calcul'

