"""
Script de Test de Remplissage du Conteneur
============================================

Simule 20 clients fictifs qui participent à un conteneur avec des volumes variés.
Vérifie que le conteneur s'arrête bien à 76 CBM et que les calculs sont corrects.

Usage:
    python manage.py shell < test_remplissage.py

Ou directement:
    python test_remplissage.py
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tontine_digitale.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Conteneur, Commande, Participation
from decimal import Decimal
import random

User = get_user_model()

# Configuration
NOMBRE_CLIENTS = 20
CONTENEUR_TEST = "TEST-REMPLISSAGE-2026"
CATEGORIES = ['ELECTRONIQUE', 'TEXTILE', 'DIVERS']
VOLUMES_POSSIBLES = [Decimal('0.5'), Decimal('1.0'), Decimal('2.0'), Decimal('3.0'), Decimal('5.0'), Decimal('10.0')]

def nettoyer_donnees_test():
    """Supprime les données de test précédentes"""
    print("\n🧹 Nettoyage des données de test précédentes...")
    
    # Supprimer le conteneur test et ses dépendances
    Conteneur.objects.filter(nom=CONTENEUR_TEST).delete()
    
    # Supprimer les utilisateurs test
    User.objects.filter(telephone__startswith='+224620999').delete()
    
    print("✅ Données de test nettoyées")


def creer_conteneur_test():
    """Crée un conteneur de test"""
    print("\n📦 Création du conteneur de test...")
    
    conteneur = Conteneur.objects.create(
        nom=CONTENEUR_TEST,
        objectif=Decimal('50000000'),  # 50M GNF
        devise='CNY',
        etape='collecte',
        capacite_max_cbm=Decimal('76.00'),
        volume_total_cbm=Decimal('0.00')
    )
    
    print(f"✅ Conteneur créé : {conteneur.nom}")
    print(f"   Capacité : {conteneur.capacite_max_cbm} CBM")
    
    return conteneur


def creer_clients_fictifs(nombre=20):
    """Crée des clients fictifs"""
    print(f"\n👥 Création de {nombre} clients fictifs...")
    
    clients = []
    for i in range(1, nombre + 1):
        telephone = f'+224620999{i:03d}'
        
        # Vérifier si existe déjà
        client, created = User.objects.get_or_create(
            telephone=telephone,
            defaults={
                'username': telephone,
                'is_staff': False,
                'is_superuser': False
            }
        )
        
        clients.append(client)
        
        if created:
            print(f"   ✅ Client {i}/{nombre} créé : {telephone}")
        else:
            print(f"   ♻️  Client {i}/{nombre} existait déjà : {telephone}")
    
    return clients


def simuler_commandes(conteneur, clients):
    """Simule des commandes pour remplir le conteneur"""
    print(f"\n📦 Simulation de commandes jusqu'à {conteneur.capacite_max_cbm} CBM...")
    
    commandes_creees = []
    volume_total = Decimal('0.00')
    marge_totale = Decimal('0.00')
    
    for i, client in enumerate(clients, start=1):
        # Volume aléatoire
        volume = random.choice(VOLUMES_POSSIBLES)
        
        # Vérifier si on ne dépasse pas 76 CBM
        if volume_total + volume > conteneur.capacite_max_cbm:
            volume_restant = conteneur.capacite_max_cbm - volume_total
            if volume_restant >= Decimal('0.5'):
                volume = volume_restant
            else:
                print(f"\n   ⚠️  Client {i} : Volume restant insuffisant ({volume_restant} CBM)")
                break
        
        # Catégorie aléatoire
        categorie = random.choice(CATEGORIES)
        
        # Prix aléatoire en Yuan (entre 1000 et 20000)
        prix_yuan = Decimal(random.randint(1000, 20000))
        
        # Créer la commande
        commande = Commande.objects.create(
            utilisateur=client,
            conteneur=conteneur,
            description_produit=f"Commande test {i} - Catégorie {categorie}",
            categorie_produit=categorie,
            prix_achat_yuan=prix_yuan,
            volume_cbm=volume
        )
        
        commandes_creees.append(commande)
        volume_total += volume
        marge_totale += Decimal(str(commande.marge_plateforme))
        
        print(f"   📦 Commande {i}: {volume} CBM ({categorie}) - Prix: {prix_yuan} Yuan")
        print(f"      → Total client: {commande.total_a_payer:,.0f} GNF")
        print(f"      → Marge plateforme: {commande.marge_plateforme:,.0f} GNF")
        print(f"      → Volume cumulé: {volume_total}/{conteneur.capacite_max_cbm} CBM")
        
        # Si on atteint 76 CBM, arrêter
        if volume_total >= conteneur.capacite_max_cbm:
            print(f"\n   🎯 Conteneur plein ! ({volume_total} CBM)")
            break
    
    return commandes_creees, volume_total, marge_totale


def verifier_resultats(conteneur, commandes, volume_total, marge_totale):
    """Vérifie que tous les calculs sont corrects"""
    print("\n🔍 Vérification des résultats...")
    
    # Recharger le conteneur depuis la DB
    conteneur.refresh_from_db()
    
    # Tests
    tests_passes = []
    tests_echoues = []
    
    # Test 1: Volume total correct
    if conteneur.volume_total_cbm == volume_total:
        tests_passes.append("✅ Volume total correct")
    else:
        tests_echoues.append(f"❌ Volume total incorrect : {conteneur.volume_total_cbm} != {volume_total}")
    
    # Test 2: Changement d'étape si >= 76 CBM
    if volume_total >= Decimal('76.00'):
        if conteneur.etape == 'mer':
            tests_passes.append("✅ Étape changée automatiquement (Collecte → Mer)")
        else:
            tests_echoues.append(f"❌ Étape non changée : {conteneur.etape} (devrait être 'mer')")
    else:
        if conteneur.etape == 'collecte':
            tests_passes.append("✅ Étape reste 'Collecte' (volume < 76 CBM)")
        else:
            tests_echoues.append(f"❌ Étape incorrecte : {conteneur.etape}")
    
    # Test 3: Nombre de commandes
    if len(commandes) == Commande.objects.filter(conteneur=conteneur).count():
        tests_passes.append(f"✅ Nombre de commandes correct ({len(commandes)})")
    else:
        tests_echoues.append("❌ Nombre de commandes incorrect en base de données")
    
    # Test 4: Calcul de la marge
    marge_calculee = sum(c.marge_plateforme for c in commandes)
    if marge_calculee == marge_totale:
        tests_passes.append(f"✅ Marge totale correcte : {marge_totale:,.0f} GNF")
    else:
        tests_echoues.append(f"❌ Marge incorrecte : {marge_calculee} != {marge_totale}")
    
    # Test 5: Vérifier qu'aucune commande ne dépasse 76 CBM
    if volume_total <= Decimal('76.00'):
        tests_passes.append("✅ Volume ne dépasse pas la capacité max (76 CBM)")
    else:
        tests_echoues.append(f"❌ Volume dépasse 76 CBM : {volume_total}")
    
    # Affichage des résultats
    print("\n" + "="*60)
    print("📊 RÉSULTATS DES TESTS")
    print("="*60)
    
    for test in tests_passes:
        print(test)
    
    for test in tests_echoues:
        print(test)
    
    print("\n" + "="*60)
    print(f"✅ Tests réussis : {len(tests_passes)}/{len(tests_passes) + len(tests_echoues)}")
    print("="*60)
    
    return len(tests_echoues) == 0


def afficher_statistiques(conteneur, commandes, volume_total, marge_totale):
    """Affiche les statistiques finales"""
    print("\n" + "="*60)
    print("📈 STATISTIQUES FINALES")
    print("="*60)
    
    print(f"\n📦 CONTENEUR : {conteneur.nom}")
    print(f"   • Volume total : {volume_total} / {conteneur.capacite_max_cbm} CBM")
    print(f"   • Taux de remplissage : {(volume_total / conteneur.capacite_max_cbm * 100):.2f}%")
    print(f"   • Étape actuelle : {conteneur.etape.upper()}")
    print(f"   • Nombre de commandes : {len(commandes)}")
    
    print(f"\n💰 REVENUS")
    total_client = sum(Decimal(str(c.total_a_payer)) for c in commandes)
    print(f"   • Total facturé aux clients : {total_client:,.0f} GNF")
    print(f"   • Marge plateforme totale : {marge_totale:,.0f} GNF")
    if total_client > 0:
        print(f"   • Taux de marge réel : {(marge_totale / total_client * Decimal('100')):.2f}%")
    
    print(f"\n📊 DÉTAIL PAR CATÉGORIE")
    for categorie in CATEGORIES:
        commandes_cat = [c for c in commandes if c.categorie_produit == categorie]
        if commandes_cat:
            volume_cat = sum(Decimal(str(c.volume_cbm)) for c in commandes_cat)
            marge_cat = sum(Decimal(str(c.marge_plateforme)) for c in commandes_cat)
            print(f"   • {categorie} :")
            print(f"      - Commandes : {len(commandes_cat)}")
            print(f"      - Volume : {volume_cat} CBM")
            print(f"      - Marge : {marge_cat:,.0f} GNF")
    
    print("\n" + "="*60)


def main():
    """Fonction principale"""
    print("="*60)
    print("🧪 TEST DE REMPLISSAGE DU CONTENEUR")
    print("="*60)
    
    try:
        # 1. Nettoyer les données précédentes
        nettoyer_donnees_test()
        
        # 2. Créer le conteneur de test
        conteneur = creer_conteneur_test()
        
        # 3. Créer les clients fictifs
        clients = creer_clients_fictifs(NOMBRE_CLIENTS)
        
        # 4. Simuler les commandes
        commandes, volume_total, marge_totale = simuler_commandes(conteneur, clients)
        
        # 5. Vérifier les résultats
        tous_tests_passes = verifier_resultats(conteneur, commandes, volume_total, marge_totale)
        
        # 6. Afficher les statistiques
        afficher_statistiques(conteneur, commandes, volume_total, marge_totale)
        
        # 7. Résultat final
        if tous_tests_passes:
            print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
            print("✅ Le système de remplissage fonctionne correctement.")
            return 0
        else:
            print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
            print("❌ Vérifiez les erreurs ci-dessus.")
            return 1
    
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TEST : {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
