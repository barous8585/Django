from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import validate_file_extension, validate_file_size, validate_image, compress_image
import random
import string
import os

class Utilisateur(AbstractUser):
    telephone = models.CharField(max_length=15, unique=True, verbose_name="Numéro de téléphone")
    otp_code = models.CharField(max_length=6, blank=True, null=True, verbose_name="Code OTP")
    otp_created_at = models.DateTimeField(blank=True, null=True, verbose_name="Date création OTP")
    is_phone_verified = models.BooleanField(default=False, verbose_name="Téléphone vérifié")
    
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return self.telephone
    
    def generate_otp(self):
        self.otp_code = ''.join(random.choices(string.digits, k=6))
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp_code
    
    def verify_otp(self, code):
        if not self.otp_code or not self.otp_created_at:
            return False
        
        time_diff = timezone.now() - self.otp_created_at
        if time_diff.total_seconds() > 300:
            return False
        
        if self.otp_code == code:
            self.is_phone_verified = True
            self.otp_code = None
            self.otp_created_at = None
            self.save()
            return True
        return False


class Portefeuille(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, verbose_name="Utilisateur", related_name="portefeuille")
    solde = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Solde (GNF)")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_mise_a_jour = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Portefeuille"
        verbose_name_plural = "Portefeuilles"
    
    def __str__(self):
        return f"Portefeuille de {self.utilisateur.telephone} - {self.solde} GNF"
    
    def crediter(self, montant):
        self.solde += montant
        self.save()
    
    def debiter(self, montant):
        if self.solde >= montant:
            self.solde -= montant
            self.save()
            return True
        return False


class TauxDeChange(models.Model):
    DEVISE_CHOICES = [
        ('USD', 'Dollar américain'),
        ('CNY', 'Yuan chinois'),
        ('EUR', 'Euro'),
    ]
    
    devise = models.CharField(max_length=3, choices=DEVISE_CHOICES, verbose_name="Devise")
    taux_gnf = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Taux vers GNF")
    date_application = models.DateTimeField(auto_now_add=True, verbose_name="Date d'application")
    actif = models.BooleanField(default=True, verbose_name="Taux actif")
    
    class Meta:
        verbose_name = "Taux de change"
        verbose_name_plural = "Taux de change"
        ordering = ['-date_application']
    
    def __str__(self):
        return f"1 {self.devise} = {self.taux_gnf} GNF"


class Conteneur(models.Model):
    ETAPE_CHOICES = [
        ('collecte', 'Collecte'),
        ('mer', 'En Mer'),
        ('port', 'Au Port'),
    ]
    
    DEVISE_CHOICES = [
        ('GNF', 'Franc Guinéen'),
        ('USD', 'Dollar américain'),
        ('CNY', 'Yuan chinois'),
    ]
    
    nom = models.CharField(max_length=200, verbose_name="Nom du conteneur")
    objectif = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Objectif")
    devise = models.CharField(max_length=3, choices=DEVISE_CHOICES, default='GNF', verbose_name="Devise")
    montant_actuel = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Montant actuel (GNF)")
    
    # Gestion du volume CBM (capacité conteneur 40HC = 76 CBM)
    volume_total_cbm = models.DecimalField(max_digits=8, decimal_places=3, default=0, verbose_name="Volume total (CBM)")
    capacite_max_cbm = models.DecimalField(max_digits=8, decimal_places=3, default=76, verbose_name="Capacité max (CBM)", help_text="76 CBM pour un conteneur 40HC")
    
    etape = models.CharField(max_length=20, choices=ETAPE_CHOICES, default='collecte', verbose_name="Étape")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    annule = models.BooleanField(default=False, verbose_name="Annulé")
    
    class Meta:
        verbose_name = "Conteneur"
        verbose_name_plural = "Conteneurs"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.nom} - {self.get_progression()}%"
    
    def get_progression(self):
        objectif_gnf = self.get_objectif_en_gnf()
        if objectif_gnf > 0:
            return round((self.montant_actuel / objectif_gnf) * 100, 2)
        return 0
    
    def get_objectif_en_gnf(self):
        if self.devise == 'GNF':
            return self.objectif
        
        try:
            taux = TauxDeChange.objects.filter(devise=self.devise, actif=True).latest('date_application')
            return self.objectif * taux.taux_gnf
        except TauxDeChange.DoesNotExist:
            return self.objectif
    
    def mettre_a_jour_montant(self):
        """
        Met à jour le montant actuel ET le volume CBM total
        Change automatiquement l'étape si le conteneur est plein
        """
        # Mise à jour montant (participations validées)
        total = self.participation_set.filter(valide=True).aggregate(
            models.Sum('montant')
        )['montant__sum'] or 0
        self.montant_actuel = total
        
        # Mise à jour volume CBM (commandes liées)
        volume_total = self.commandes.aggregate(
            models.Sum('volume_cbm')
        )['volume_cbm__sum'] or 0
        self.volume_total_cbm = volume_total
        
        # Changement automatique d'étape si conteneur rempli
        if self.volume_total_cbm >= self.capacite_max_cbm and self.etape == 'collecte':
            self.etape = 'mer'  # Passage automatique à "En Mer"
        
        self.save()
    
    def get_taux_remplissage_cbm(self):
        """
        Retourne le pourcentage de remplissage du conteneur (en CBM)
        """
        if self.capacite_max_cbm > 0:
            return round((self.volume_total_cbm / self.capacite_max_cbm) * 100, 2)
        return 0
    
    def cbm_restants(self):
        """
        Retourne le nombre de CBM encore disponibles
        """
        return float(self.capacite_max_cbm) - float(self.volume_total_cbm)
    
    def peut_accepter_commande(self, volume_cbm):
        """
        Vérifie si une commande de X CBM peut être ajoutée
        """
        return (self.volume_total_cbm + volume_cbm) <= self.capacite_max_cbm
        self.save()
    
    def annuler_et_rembourser(self):
        self.annule = True
        self.save()
        
        for participation in self.participation_set.filter(valide=True):
            portefeuille = participation.utilisateur.portefeuille
            portefeuille.crediter(participation.montant)
            
            Transaction.objects.create(
                portefeuille=portefeuille,
                type_transaction='remboursement',
                montant=participation.montant,
                conteneur=self,
                description=f"Remboursement conteneur annulé: {self.nom}"
            )


class Participation(models.Model):
    conteneur = models.ForeignKey(Conteneur, on_delete=models.CASCADE, verbose_name="Conteneur")
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, verbose_name="Utilisateur")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant (GNF)")
    reference_paiement = models.CharField(max_length=100, verbose_name="Référence Orange Money")
    preuve_paiement = models.ImageField(
        upload_to='preuves_paiement/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Preuve de paiement",
        validators=[validate_file_extension, validate_file_size, validate_image],
        help_text="Formats acceptés: JPG, PNG (max 5MB)"
    )
    valide = models.BooleanField(default=False, verbose_name="Paiement validé")
    date_participation = models.DateTimeField(auto_now_add=True, verbose_name="Date de participation")
    
    class Meta:
        verbose_name = "Participation"
        verbose_name_plural = "Participations"
        ordering = ['-date_participation']
    
    def __str__(self):
        statut = "✓" if self.valide else "✗"
        return f"{self.utilisateur.telephone} - {self.montant} GNF [{statut}]"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Compresser l'image après sauvegarde
        if self.preuve_paiement:
            image_path = self.preuve_paiement.path
            if os.path.exists(image_path):
                compress_image(image_path)


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('depot', 'Dépôt'),
        ('retrait', 'Retrait'),
        ('participation', 'Participation conteneur'),
        ('remboursement', 'Remboursement'),
    ]
    
    portefeuille = models.ForeignKey(Portefeuille, on_delete=models.CASCADE, verbose_name="Portefeuille", related_name="transactions")
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    montant = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant (GNF)")
    conteneur = models.ForeignKey(Conteneur, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Conteneur")
    description = models.TextField(verbose_name="Description")
    date_transaction = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-date_transaction']
    
    def __str__(self):
        return f"{self.type_transaction} - {self.montant} GNF ({self.date_transaction.strftime('%d/%m/%Y')})"


class Fournisseur(models.Model):
    CATEGORIE_CHOICES = [
        ('TEXTILE', 'Mode & Textile'),
        ('ELECTRO', 'Électronique & Accessoires'),
        ('BEAUTE', 'Beauté & Cosmétiques'),
        ('MAISON', 'Maison & Quincaillerie'),
    ]
    
    PAYS_CHOICES = [
        ('CHINE', 'Chine'),
        ('DUBAI', 'Dubaï'),
        ('TURQUIE', 'Turquie'),
    ]
    
    nom = models.CharField(max_length=200, verbose_name="Nom du fournisseur")
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, verbose_name="Catégorie")
    badges_confiance = models.CharField(max_length=200, verbose_name="Badges de confiance")
    specialite = models.TextField(verbose_name="Spécialité de produits")
    moq = models.CharField(max_length=100, verbose_name="MOQ (Commande minimum)")
    argument_vente = models.TextField(verbose_name="Argument de vente pour Madina")
    annees_experience = models.IntegerField(default=0, verbose_name="Années d'expérience")
    pays_origine = models.CharField(max_length=20, choices=PAYS_CHOICES, default='CHINE', verbose_name="Pays d'origine")
    verifie = models.BooleanField(default=True, verbose_name="Fournisseur vérifié")
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    
    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['categorie', 'nom']
    
    def __str__(self):
        return f"{self.nom} ({self.get_categorie_display()})"
    
    def get_badge_icon(self):
        if 'Verified' in self.badges_confiance:
            return '✓'
        elif 'Gold' in self.badges_confiance:
            return '🥇'
        elif 'Trade Assurance' in self.badges_confiance:
            return '🛡️'
        return '⭐'


class Commande(models.Model):
    """
    Modèle pour les commandes individuelles avec calcul automatique
    Commission 5% + Frais logistique par CBM
    """
    CATEGORIE_CHOICES = [
        ('ELECTRONIQUE', 'Électronique'),
        ('TEXTILE', 'Textile & Vêtements'),
        ('DIVERS', 'Divers'),
    ]
    
    STATUT_CHOICES = [
        ('devis', 'Devis en cours'),
        ('confirme', 'Confirmé'),
        ('paye', 'Payé'),
        ('expedie', 'Expédié'),
        ('recu', 'Reçu'),
    ]
    
    # Relations
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='commandes')
    conteneur = models.ForeignKey(Conteneur, on_delete=models.SET_NULL, null=True, blank=True, related_name='commandes')
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Informations produit
    description_produit = models.TextField(verbose_name="Description du produit")
    categorie_produit = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default='DIVERS')
    
    # Prix et volume
    prix_achat_yuan = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix d'achat (Yuan)")
    volume_cbm = models.DecimalField(max_digits=8, decimal_places=3, verbose_name="Volume (CBM)", help_text="Mètres cubes")
    
    # Taux et tarifs
    taux_change = models.DecimalField(max_digits=10, decimal_places=2, default=1250, verbose_name="Taux Yuan → GNF")
    commission_pct = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, verbose_name="Commission (%)")
    
    # Montants calculés (mis à jour automatiquement)
    prix_achat_gnf = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Prix achat (GNF)")
    frais_commission = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Commission plateforme")
    frais_logistique = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Frais logistique")
    total_a_payer = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Total à payer (GNF)")
    
    # Répartition pour comptabilité
    montant_fournisseur = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Part fournisseur")
    montant_transitaire = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Part transitaire")
    marge_plateforme = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Marge plateforme")
    
    # Statut et dates
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='devis')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Commande {self.id} - {self.utilisateur.telephone} - {self.volume_cbm} CBM"
    
    def calculer_devis_complet(self):
        """
        Calcul intelligent du devis complet
        Retourne un dictionnaire avec tous les montants
        """
        # Tarifs logistique par catégorie (en GNF par CBM)
        TARIFS_LOGISTIQUE = {
            'ELECTRONIQUE': 6000000,  # Plus cher (douane élevée)
            'TEXTILE': 5000000,
            'DIVERS': 4500000,
        }
        
        # Tarif négocié avec transitaire (votre coût réel)
        TARIF_REEL_TRANSITAIRE = {
            'ELECTRONIQUE': 5200000,  # Vous négociez moins cher
            'TEXTILE': 4200000,
            'DIVERS': 3700000,
        }
        
        # 1. Conversion Yuan → GNF
        prix_achat_gnf = float(self.prix_achat_yuan) * float(self.taux_change)
        
        # 2. Commission de service (5% sur la marchandise)
        frais_commission = prix_achat_gnf * (float(self.commission_pct) / 100)
        
        # 3. Frais logistique (tarif client)
        tarif_client = TARIFS_LOGISTIQUE.get(self.categorie_produit, 5000000)
        frais_logistique_total = float(self.volume_cbm) * tarif_client
        
        # 4. Coût réel transitaire (votre coût)
        tarif_reel = TARIF_REEL_TRANSITAIRE.get(self.categorie_produit, 4200000)
        cout_reel_transitaire = float(self.volume_cbm) * tarif_reel
        
        # 5. Marge cachée sur la logistique
        marge_logistique = frais_logistique_total - cout_reel_transitaire
        
        # 6. Marge totale plateforme
        marge_totale = frais_commission + marge_logistique
        
        # 7. Total client
        total_a_payer = prix_achat_gnf + frais_commission + frais_logistique_total
        
        return {
            'prix_achat_gnf': prix_achat_gnf,
            'frais_commission': frais_commission,
            'frais_logistique': frais_logistique_total,
            'total_a_payer': total_a_payer,
            'montant_fournisseur': prix_achat_gnf,
            'montant_transitaire': cout_reel_transitaire,
            'marge_plateforme': marge_totale,
            'tarif_cbm_client': tarif_client,
            'tarif_cbm_reel': tarif_reel,
            'marge_par_cbm': tarif_client - tarif_reel,
        }
    
    def save(self, *args, **kwargs):
        """
        Calcul automatique avant sauvegarde
        """
        devis = self.calculer_devis_complet()
        
        self.prix_achat_gnf = devis['prix_achat_gnf']
        self.frais_commission = devis['frais_commission']
        self.frais_logistique = devis['frais_logistique']
        self.total_a_payer = devis['total_a_payer']
        self.montant_fournisseur = devis['montant_fournisseur']
        self.montant_transitaire = devis['montant_transitaire']
        self.marge_plateforme = devis['marge_plateforme']
        
        super().save(*args, **kwargs)
    
    def get_detail_calcul(self):
        """
        Retourne un texte explicatif du calcul (pour affichage client)
        """
        devis = self.calculer_devis_complet()
        return f"""
📦 Détail de votre commande :
─────────────────────────────
🏷️  Prix marchandise    : {devis['prix_achat_gnf']:,.0f} GNF
     ({self.prix_achat_yuan} Yuan × {self.taux_change})

💼 Commission service   : {devis['frais_commission']:,.0f} GNF
     (Sécurisation + Suivi)

🚢 Logistique complète  : {devis['frais_logistique']:,.0f} GNF
     ({self.volume_cbm} CBM × {devis['tarif_cbm_client']:,.0f} GNF/CBM)
     ✓ Transport Chine → Guinée
     ✓ Dédouanement
     ✓ Livraison à Conakry

─────────────────────────────
💰 TOTAL À PAYER        : {devis['total_a_payer']:,.0f} GNF
"""


# Signals pour mise à jour automatique

@receiver(post_save, sender=Participation)
def mettre_a_jour_conteneur_apres_participation(sender, instance, created, **kwargs):
    """
    Met à jour automatiquement le montant_actuel du conteneur 
    quand une participation est créée ou modifiée
    """
    if instance.valide:  # Seulement si la participation est validée
        instance.conteneur.mettre_a_jour_montant()


@receiver(post_save, sender=Commande)
def mettre_a_jour_conteneur_apres_commande(sender, instance, created, **kwargs):
    """
    Met à jour automatiquement le volume CBM du conteneur
    quand une commande est créée ou modifiée
    """
    if instance.conteneur:
        instance.conteneur.mettre_a_jour_montant()


@receiver(post_save, sender=Utilisateur)
def creer_portefeuille_utilisateur(sender, instance, created, **kwargs):
    """
    Crée automatiquement un portefeuille quand un utilisateur est créé
    """
    if created:
        Portefeuille.objects.get_or_create(utilisateur=instance)

