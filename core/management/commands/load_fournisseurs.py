from django.core.management.base import BaseCommand
from core.models import Fournisseur

class Command(BaseCommand):
    help = 'Charge les 20 fournisseurs certifiés dans la base de données'
    
    def handle(self, *args, **options):
        fournisseurs_data = [
            {
                "nom": "Guangzhou SK Fashion",
                "categorie": "TEXTILE",
                "badges_confiance": "Verified & 12 ans exp.",
                "specialite": "Ballots de Jeans & T-shirts",
                "moq": "100 pièces",
                "argument_vente": "Tailles adaptées au marché africain.",
                "annees_experience": 12,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Quanzhou Winner Bags",
                "categorie": "TEXTILE",
                "badges_confiance": "Trade Assurance",
                "specialite": "Sacs à dos & sacs à main",
                "moq": "50 pièces",
                "argument_vente": "Très robuste, idéal pour les écoliers.",
                "annees_experience": 8,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Jinjiang Footwear Co.",
                "categorie": "TEXTILE",
                "badges_confiance": "Gold Plus Member",
                "specialite": "Sneakers & Chaussures sport",
                "moq": "1 carton (12 paires)",
                "argument_vente": "Copies de haute qualité et modèles génériques.",
                "annees_experience": 10,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Foshan Children's Wear",
                "categorie": "TEXTILE",
                "badges_confiance": "Usine inspectée (SGS)",
                "specialite": "Vêtements pour bébés/enfants",
                "moq": "1 ballot mixte",
                "argument_vente": "Coton bio, résiste aux lavages fréquents.",
                "annees_experience": 15,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Suzhou Wedding Dress",
                "categorie": "TEXTILE",
                "badges_confiance": "Top Rated",
                "specialite": "Robes de fête & tissus wax",
                "moq": "5 pièces",
                "argument_vente": "Idéal pour les événements et mariages.",
                "annees_experience": 7,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Shenzhen Digital Tech",
                "categorie": "ELECTRO",
                "badges_confiance": "Verified Supplier",
                "specialite": "Smartphones & Tablettes",
                "moq": "10 unités",
                "argument_vente": "Fournit des marques comme Infinix/Tecno.",
                "annees_experience": 9,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Guangdong Cable Pro",
                "categorie": "ELECTRO",
                "badges_confiance": "10 ans d'ancienneté",
                "specialite": "Chargeurs & Câbles USB",
                "moq": "100 unités",
                "argument_vente": "Câbles tressés (incassables), forte demande.",
                "annees_experience": 10,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Yiwu Solar Power",
                "categorie": "ELECTRO",
                "badges_confiance": "Trade Assurance",
                "specialite": "Panneaux solaires & Lampes",
                "moq": "5 kits",
                "argument_vente": "Solution pour les zones à faible courant.",
                "annees_experience": 6,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Zhongshan LED Lighting",
                "categorie": "ELECTRO",
                "badges_confiance": "Verified & CE",
                "specialite": "Ampoules & Projecteurs",
                "moq": "1 carton",
                "argument_vente": "Basse consommation, très rentable.",
                "annees_experience": 11,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Ningbo Home Audio",
                "categorie": "ELECTRO",
                "badges_confiance": "Gold Plus Member",
                "specialite": "Enceintes Bluetooth / Radio",
                "moq": "20 unités",
                "argument_vente": "Très puissant, avec lecture carte SD/USB.",
                "annees_experience": 8,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Xuchang Human Hair",
                "categorie": "BEAUTE",
                "badges_confiance": "15 ans exp. (Top)",
                "specialite": "Mèches, Perruques & Tissages",
                "moq": "10 paquets",
                "argument_vente": "Cheveux 100% naturels (Brésilien/Indien).",
                "annees_experience": 15,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Guangzhou Skin Care",
                "categorie": "BEAUTE",
                "badges_confiance": "ISO 9001 Certified",
                "specialite": "Crèmes & Laits corporels",
                "moq": "1 carton",
                "argument_vente": "Produits sans hydroquinone (Vérifiés).",
                "annees_experience": 12,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Jinhua Cosmetic Tools",
                "categorie": "BEAUTE",
                "badges_confiance": "Trade Assurance",
                "specialite": "Kits Maquillage & Pinceaux",
                "moq": "50 kits",
                "argument_vente": "Très léger à transporter dans le conteneur.",
                "annees_experience": 7,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Yiwu Jewelry King",
                "categorie": "BEAUTE",
                "badges_confiance": "Verified Supplier",
                "specialite": "Bijoux fantaisie & Parures",
                "moq": "100 pièces",
                "argument_vente": "Petit prix, grosse marge à la revente.",
                "annees_experience": 9,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Beauty Nail Tech",
                "categorie": "BEAUTE",
                "badges_confiance": "Verified",
                "specialite": "Vernis & Lampes UV",
                "moq": "1 carton mixte",
                "argument_vente": "Matériel pro pour les salons de coiffure.",
                "annees_experience": 5,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Foshan Furniture Co.",
                "categorie": "MAISON",
                "badges_confiance": "Usine inspectée",
                "specialite": "Matelas & Chaises pliantes",
                "moq": "10 unités",
                "argument_vente": "Gain de place énorme dans le conteneur.",
                "annees_experience": 14,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Zhongshan Cookware",
                "categorie": "MAISON",
                "badges_confiance": "Trade Assurance",
                "specialite": "Marmites & Poêles (Inox)",
                "moq": "1 set complet",
                "argument_vente": "Qualité lourde, ne brûle pas les aliments.",
                "annees_experience": 13,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Ningbo Small Apps",
                "categorie": "MAISON",
                "badges_confiance": "Gold Member",
                "specialite": "Mixeurs & Bouilloires",
                "moq": "20 unités",
                "argument_vente": "Moteur renforcé pour usage intensif.",
                "annees_experience": 10,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Guangdong Plastic Ind.",
                "categorie": "MAISON",
                "badges_confiance": "20 ans exp.",
                "specialite": "Seaux & Bassines empilables",
                "moq": "1 lot (50 pcs)",
                "argument_vente": "Incassable, indispensable dans chaque foyer.",
                "annees_experience": 20,
                "pays_origine": "CHINE"
            },
            {
                "nom": "Yiwu Tools Master",
                "categorie": "MAISON",
                "badges_confiance": "Verified Supplier",
                "specialite": "Outillage (Marteaux, Perceuses)",
                "moq": "1 kit complet",
                "argument_vente": "Idéal pour les quincailleries de quartier.",
                "annees_experience": 11,
                "pays_origine": "CHINE"
            }
        ]
        
        # Supprimer les anciens fournisseurs (optionnel)
        Fournisseur.objects.all().delete()
        
        # Ajouter les nouveaux
        count = 0
        for data in fournisseurs_data:
            Fournisseur.objects.create(**data)
            count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'✓ {count} fournisseurs chargés avec succès!')
        )
