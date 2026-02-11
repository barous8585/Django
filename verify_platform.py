#!/usr/bin/env python
"""
Script de vérification complète de la plateforme Tontine Digitale
"""

import os
import sys
import django

# Configuration Django
sys.path.append('/Users/thiernoousmanebarry/Desktop/Django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tontine_digitale.settings')
django.setup()

from core.models import Conteneur, Participation, Utilisateur, Portefeuille, TauxDeChange, Fournisseur, Transaction
from django.contrib.admin.sites import site

print("="*80)
print(" 🔍 VÉRIFICATION COMPLÈTE DE LA PLATEFORME TONTINE DIGITALE")
print("="*80)
print()

# 1. Vérifier la base de données
print("📊 1. ÉTAT DE LA BASE DE DONNÉES")
print("-" * 80)
print(f"✅ Utilisateurs          : {Utilisateur.objects.count()}")
print(f"✅ Conteneurs            : {Conteneur.objects.count()}")
print(f"✅ Participations        : {Participation.objects.count()}")
print(f"✅ Portefeuilles         : {Portefeuille.objects.count()}")
print(f"✅ Transactions          : {Transaction.objects.count()}")
print(f"✅ Taux de change        : {TauxDeChange.objects.count()}")
print(f"✅ Fournisseurs          : {Fournisseur.objects.count()}")
print()

# 2. Vérifier les taux de change
print("💱 2. TAUX DE CHANGE")
print("-" * 80)
for taux in TauxDeChange.objects.all():
    statut = "✅ Actif" if taux.actif else "⚠️  Inactif"
    print(f"{statut} | {taux.devise:4s} : 1 = {taux.taux_gnf:10.2f} GNF")
print()

# 3. Vérifier les conteneurs
print("📦 3. CONTENEURS")
print("-" * 80)
for conteneur in Conteneur.objects.all():
    print(f"Nom         : {conteneur.nom}")
    print(f"Devise      : {conteneur.get_devise_display()}")
    print(f"Objectif    : {conteneur.objectif} {conteneur.devise}")
    print(f"Objectif GNF: {conteneur.get_objectif_en_gnf():.2f} GNF")
    print(f"Collecté    : {conteneur.montant_actuel:.2f} GNF")
    print(f"Progression : {conteneur.get_progression():.2f}%")
    print(f"Étape       : {conteneur.get_etape_display()}")
    print(f"Annulé      : {'Oui' if conteneur.annule else 'Non'}")
    print()

# 4. Vérifier les fournisseurs par catégorie
print("🏭 4. FOURNISSEURS PAR CATÉGORIE")
print("-" * 80)
categories = ['TEXTILE', 'ELECTRO', 'BEAUTE', 'MAISON']
for cat in categories:
    count = Fournisseur.objects.filter(categorie=cat, verifie=True).count()
    emoji = {'TEXTILE': '👕', 'ELECTRO': '📱', 'BEAUTE': '💄', 'MAISON': '🏠'}[cat]
    print(f"{emoji} {cat:10s}: {count} fournisseurs")
print()

# 5. Vérifier les modèles enregistrés dans l'admin
print("⚙️  5. MODÈLES ADMIN DJANGO")
print("-" * 80)
registered_models = [model.__name__ for model in site._registry.keys()]
for model_name in sorted(registered_models):
    print(f"✅ {model_name}")
print()

# 6. Test de conversion de devise
print("🧮 6. TEST DE CONVERSION DE DEVISE")
print("-" * 80)
if TauxDeChange.objects.filter(devise='USD', actif=True).exists():
    taux = TauxDeChange.objects.get(devise='USD', actif=True)
    montant_usd = 1000
    montant_gnf = montant_usd * float(taux.taux_gnf)
    print(f"✅ {montant_usd} USD = {montant_gnf:,.2f} GNF (taux: {taux.taux_gnf})")
else:
    print("⚠️  Aucun taux de change USD actif")
print()

# 7. Vérifier les participations validées
print("🤝 7. PARTICIPATIONS")
print("-" * 80)
total_participations = Participation.objects.count()
validees = Participation.objects.filter(valide=True).count()
en_attente = Participation.objects.filter(valide=False).count()
print(f"Total        : {total_participations}")
print(f"✅ Validées  : {validees}")
print(f"⏳ En attente: {en_attente}")
print()

# 8. Résumé de santé de la plateforme
print("💚 8. SANTÉ DE LA PLATEFORME")
print("-" * 80)

errors = []

if Utilisateur.objects.count() == 0:
    errors.append("❌ Aucun utilisateur créé")
else:
    print("✅ Utilisateurs créés")

if TauxDeChange.objects.filter(actif=True).count() == 0:
    errors.append("⚠️  Aucun taux de change actif")
else:
    print("✅ Taux de change configurés")

if Fournisseur.objects.count() < 20:
    errors.append(f"⚠️  Seulement {Fournisseur.objects.count()} fournisseurs (attendu: 20)")
else:
    print("✅ Catalogue fournisseurs complet (20)")

if Conteneur.objects.count() == 0:
    errors.append("⚠️  Aucun conteneur créé")
else:
    print("✅ Conteneurs créés")

print()

# 9. URLs à tester
print("🌐 9. URLS À TESTER MANUELLEMENT")
print("-" * 80)
urls = [
    ("Page d'accueil", "http://127.0.0.1:8000/"),
    ("Catalogue fournisseurs", "http://127.0.0.1:8000/api/fournisseurs/"),
    ("Conteneurs", "http://127.0.0.1:8000/api/conteneurs/"),
    ("Participations", "http://127.0.0.1:8000/api/participations/"),
    ("Dashboard", "http://127.0.0.1:8000/dashboard/"),
    ("Admin Django", "http://127.0.0.1:8000/admin/"),
    ("Contact", "http://127.0.0.1:8000/contact/"),
]

for nom, url in urls:
    print(f"• {nom:30s}: {url}")
print()

# 10. Résumé final
print("="*80)
if errors:
    print("⚠️  AVERTISSEMENTS DÉTECTÉS:")
    for error in errors:
        print(f"  {error}")
else:
    print("✅ PLATEFORME EN PARFAIT ÉTAT")
print("="*80)
print()
print("📝 Prochaines étapes:")
print("  1. Tester manuellement toutes les URLs ci-dessus")
print("  2. Vérifier la navigation entre les pages")
print("  3. Tester la création/modification depuis l'admin")
print("  4. Vider le cache du navigateur (Cmd+Shift+R)")
print()
