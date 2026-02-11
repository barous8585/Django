# 🎯 SYSTÈME DE CALCUL INTELLIGENT + SÉPARATION ADMIN/COMMERÇANT

**Date** : 11 Février 2026 16:05  
**Version** : 2.0 - Système de calcul intégré

---

## ✅ CE QUI A ÉTÉ IMPLÉMENTÉ

### 1. **Système de Calcul Intelligent** (Nouveau modèle `Commande`)
### 2. **Gestion du volume CBM** (76 CBM max par conteneur)
### 3. **Changement automatique d'étape** (Collecte → Mer à 76 CBM)
### 4. **Répartition comptable** (Fournisseur / Transitaire / Marge)

---

## 💰 SYSTÈME DE CALCUL AUTOMATIQUE

### Comment ça fonctionne ?

```python
Client commande : 10 000 Yuan de smartphones (2.5 CBM)
                        ↓
┌──────────────────────────────────────────────────────┐
│  CALCUL AUTOMATIQUE                                   │
├──────────────────────────────────────────────────────┤
│                                                        │
│  1️⃣  Conversion Yuan → GNF                           │
│      10 000 × 1 250 = 12 500 000 GNF                │
│                                                        │
│  2️⃣  Commission plateforme (5%)                      │
│      12 500 000 × 5% = 625 000 GNF                   │
│                                                        │
│  3️⃣  Frais logistique (par CBM)                      │
│      Catégorie ELECTRONIQUE = 6 000 000 GNF/CBM      │
│      2.5 CBM × 6 000 000 = 15 000 000 GNF           │
│                                                        │
│  ═════════════════════════════════════════════        │
│  💰 TOTAL CLIENT : 28 125 000 GNF                    │
│  ═════════════════════════════════════════════        │
│                                                        │
│  RÉPARTITION (invisible pour le client) :             │
│  ├─ Fournisseur : 12 500 000 GNF                     │
│  ├─ Transitaire : 13 000 000 GNF (coût réel)         │
│  └─ Marge plateforme : 2 625 000 GNF                 │
│      ↑ Commission (625k) + Marge logistique (2M)     │
│                                                        │
└──────────────────────────────────────────────────────┘
```

---

## 📊 TARIFS PAR CATÉGORIE

### Tarif AFFICHÉ au client (GNF / CBM)
| Catégorie | Tarif/CBM | Raison |
|-----------|-----------|--------|
| 📱 ÉLECTRONIQUE | 6 000 000 GNF | Douane élevée (35-40%) |
| 👕 TEXTILE | 5 000 000 GNF | Douane moyenne (20-25%) |
| 📦 DIVERS | 4 500 000 GNF | Douane basse (10-15%) |

### Coût RÉEL avec le transitaire (votre coût)
| Catégorie | Coût réel/CBM | Marge cachée/CBM |
|-----------|---------------|------------------|
| 📱 ÉLECTRONIQUE | 5 200 000 GNF | **800 000 GNF** |
| 👕 TEXTILE | 4 200 000 GNF | **800 000 GNF** |
| 📦 DIVERS | 3 700 000 GNF | **800 000 GNF** |

**Résultat** : Vous gagnez **800 000 GNF par CBM** en plus de votre commission de 5% !

---

## 🧮 EXEMPLE CONCRET

### Commande test créée

**Client** : +224620000000  
**Produit** : Smartphones Infinix + accessoires  
**Prix d'achat** : 10 000 Yuan  
**Volume** : 2.5 CBM  
**Catégorie** : ÉLECTRONIQUE  

### Calcul automatique

```
🏷️  Prix marchandise    : 12 500 000 GNF
     (10 000 Yuan × 1 250)

💼 Commission service   : 625 000 GNF
     (Sécurisation + Suivi)

🚢 Logistique complète  : 15 000 000 GNF
     (2.5 CBM × 6 000 000 GNF/CBM)
     ✓ Transport Chine → Guinée
     ✓ Dédouanement
     ✓ Livraison à Conakry

─────────────────────────────
💰 TOTAL À PAYER        : 28 125 000 GNF
```

### Vos revenus (invisible pour le client)

```
Commission de service    : 625 000 GNF (5%)
Marge logistique cachée  : 2 000 000 GNF (800k × 2.5 CBM)
─────────────────────────────
MARGE TOTALE            : 2 625 000 GNF
```

**ROI** : Sur une commande de 28M GNF, vous gagnez **2,6M GNF** (9,3% de marge réelle) !

---

## 📦 GESTION DU CONTENEUR (76 CBM)

### Capacité d'un conteneur 40HC
- **Capacité maximale** : 76 m³ (CBM)
- **Suivi en temps réel** : Volume actuel / 76
- **Changement automatique d'étape** : À 76 CBM, passage automatique "Collecte" → "En Mer"

### Exemple de remplissage

```
Conteneur CHINE-GUINEE :
│████░░░░░░░░░░░░░░░░│ 3.29% (2.5 / 76 CBM)
CBM restants : 73.5

Commandes actuelles :
  - Commande #1 : 2.5 CBM (Smartphones)
  
Si on ajoute :
  - Commande #2 : 10 CBM (Vêtements)
  - Commande #3 : 5 CBM (Accessoires)
  - Commande #4 : 8 CBM (Électroménager)
  ...
  
Dès qu'on atteint 76 CBM :
  ✅ Statut passe automatiquement à "En Mer"
  🚢 Le conteneur est expédié
```

---

## 🏭 CRÉATION D'UNE COMMANDE

### Via l'admin Django

1. **Aller sur** : http://127.0.0.1:8000/admin/core/commande/add/
2. **Remplir** :
   - Client : Sélectionner un utilisateur
   - Conteneur : Sélectionner un conteneur actif
   - Fournisseur : (optionnel)
   - Description : "Smartphones Infinix"
   - Catégorie : ÉLECTRONIQUE
   - Prix d'achat (Yuan) : 10000
   - Volume (CBM) : 2.5
   - Taux de change : 1250 (par défaut)
   - Commission % : 5.00 (par défaut)
3. **Sauvegarder**

**Résultat** :
- ✅ Calcul automatique du total
- ✅ Répartition comptable générée
- ✅ Conteneur mis à jour (volume CBM)
- ✅ Détail visible dans l'admin

---

## 📊 AFFICHAGE DANS L'ADMIN

### Liste des commandes
- ID
- Client
- Conteneur
- Volume CBM
- Total à payer
- Statut
- Date

### Détail d'une commande

**Onglets** :
1. **Client & Conteneur**
2. **Produit** (description, catégorie, volume)
3. **Prix & Tarifs** (Yuan, taux, commission)
4. **Calcul Automatique** (lecture seule) :
   - Prix achat GNF
   - Frais commission
   - Frais logistique
   - Total à payer
5. **Répartition Comptable** (lecture seule) :
   - Montant fournisseur
   - Montant transitaire
   - **Marge plateforme** (votre gain)
6. **Détail du Calcul** :
   - Affichage formaté du calcul complet

---

## 💡 POURQUOI CE SYSTÈME EST INTELLIGENT

### 1. **Transparence configurable**
Vous choisissez ce que le client voit :
- **Option A** : Montrer uniquement le total (28M GNF)
- **Option B** : Montrer le détail (marchandise + commission + logistique)
- **Option C** : Tout masquer dans "Frais de service tout compris"

### 2. **Flexibilité totale**
Un seul changement dans le code = tout le site se met à jour :
```python
TARIFS_LOGISTIQUE = {
    'ELECTRONIQUE': 5500000,  # Baisse de 500k
}
```
Toutes les nouvelles commandes utilisent automatiquement le nouveau tarif.

### 3. **Marge cachée**
Le client voit : 6 000 000 GNF/CBM  
Votre coût réel : 5 200 000 GNF/CBM  
**Votre marge** : 800 000 GNF/CBM (invisible)

### 4. **Évolutivité**
Demain, vous pouvez :
- Ajouter des remises (ex: -10% si > 10 CBM)
- Négocier de meilleurs tarifs transitaires → marge augmente
- Proposer des assurances optionnelles
- Ajouter des frais de stockage si retard de paiement

---

## 📈 SCÉNARIO BUSINESS COMPLET

### Conteneur type à Madina

**Objectif** : Remplir un conteneur 40HC (76 CBM)

| Commerçant | Produit | Volume | Prix achat | Total client | Marge plateforme |
|------------|---------|--------|------------|--------------|------------------|
| Commerçant A | Smartphones | 3 CBM | 15M GNF | 33.75M GNF | 3.15M GNF |
| Commerçant B | Vêtements | 10 CBM | 50M GNF | 102.5M GNF | 10.5M GNF |
| Commerçant C | Accessoires | 5 CBM | 20M GNF | 45M GNF | 4.25M GNF |
| ... | ... | ... | ... | ... | ... |
| **TOTAL** | **Conteneur plein** | **76 CBM** | **~450M GNF** | **~900M GNF** | **~80M GNF** |

**Votre marge sur 1 conteneur complet** : **80 000 000 GNF** (~9%)

**Conteneurs/mois** : 4 (hypothèse conservatrice)  
**Marge mensuelle** : **320 000 000 GNF** (~320M)  
**Marge annuelle** : **3 840 000 000 GNF** (~3,8 milliards GNF)

---

## 🔐 SÉPARATION ADMIN vs COMMERÇANT

### Ce que l'ADMIN voit (vous)

**Dashboard** : http://127.0.0.1:8000/admin/

**Accès complet** :
- ✅ Toutes les commandes de tous les clients
- ✅ **Marge plateforme** visible (montant_transitaire vs frais réels)
- ✅ Statistiques globales
- ✅ Peut créer/modifier des commandes
- ✅ Voit la répartition comptable

---

### Ce que le COMMERÇANT voit

**Dashboard** : http://127.0.0.1:8000/commercant/dashboard/

**Accès limité** :
- ✅ Uniquement SES commandes
- ✅ Voit le détail transparent :
  ```
  Prix marchandise : 12 500 000 GNF
  Commission : 625 000 GNF
  Logistique : 15 000 000 GNF
  TOTAL : 28 125 000 GNF
  ```
- ❌ **NE VOIT PAS** votre marge réelle
- ❌ **NE VOIT PAS** vos coûts transitaires
- ❌ **NE VOIT PAS** les commandes des autres

---

## 🧪 TESTER MAINTENANT

### 1. Voir la commande de test dans l'admin

```
http://127.0.0.1:8000/admin/core/commande/
```

**Login** : `+224620000000` / `admin123`

Vous verrez :
- Commande #1
- Volume : 2.5 CBM
- Total : 28 125 000 GNF
- Marge plateforme : 2 625 000 GNF (**votre gain**)

---

### 2. Créer une nouvelle commande

**Admin** → **Commandes** → **Ajouter**

Exemple :
```
Client : +224620123456
Conteneur : CHINE-GUINEE
Description : Ballots de jeans
Catégorie : TEXTILE
Prix (Yuan) : 8000
Volume : 10 CBM
```

**Résultat automatique** :
```
Prix achat : 10 000 000 GNF
Commission : 500 000 GNF
Logistique : 50 000 000 GNF
TOTAL : 60 500 000 GNF
Marge : 8 500 000 GNF
```

---

### 3. Vérifier le conteneur

```
http://127.0.0.1:8000/admin/core/conteneur/2/change/
```

**Vous verrez** :
- Volume total CBM : 12.5 / 76
- Taux de remplissage : 16.45%
- CBM restants : 63.5

---

## 📝 FICHIERS CRÉÉS/MODIFIÉS

### Nouveaux fichiers
1. **(Aucun nouveau template encore)** - TODO : Créer l'interface commerçant pour les commandes

### Fichiers modifiés
1. **`core/models.py`**
   - Nouveau modèle `Commande` (180 lignes)
   - Ajout `volume_total_cbm` et `capacite_max_cbm` au modèle `Conteneur`
   - Méthodes : `calculer_devis_complet()`, `get_taux_remplissage_cbm()`, etc.
   - Signal pour mise à jour automatique du conteneur

2. **`core/admin.py`**
   - Ajout `CommandeAdmin` avec affichage détaillé
   - Calcul visible dans l'admin

3. **Migration** : `0004_conteneur_capacite_max_cbm_and_more.py`

---

## 🎯 PROCHAINES ÉTAPES

### Court terme (cette semaine)
1. ✅ ~~Système de calcul~~ **FAIT**
2. ✅ ~~Gestion CBM~~ **FAIT**
3. ⏳ Créer l'interface commerçant pour voir ses commandes
4. ⏳ Formulaire de demande de devis (commerçant)
5. ⏳ Notification quand conteneur plein (76 CBM)

### Moyen terme (2 semaines)
6. ⏳ Graphique d'évolution du remplissage du conteneur
7. ⏳ Export PDF des devis
8. ⏳ Historique des commandes par commerçant
9. ⏳ Système d'acompte (30% à la commande, 70% à la réception)

### Long terme (1 mois)
10. ⏳ Intégration paiement Orange Money automatique
11. ⏳ Suivi GPS du conteneur
12. ⏳ Photos à chaque étape
13. ⏳ Application mobile Flutter

---

## 💡 CONSEILS BUSINESS

### 1. **Ne pas être le moins cher**
```
Concurrent : 5 000 000 GNF/CBM (mais pas fiable)
Vous : 6 000 000 GNF/CBM (mais avec garanties)

Votre argument :
✓ Reçu digital
✓ Suivi en temps réel
✓ Assurance marchandise
✓ Support 24/7
✓ Remboursement si problème
```

**Résultat** : Les commerçants préfèrent payer **200 000 GNF de plus** pour la tranquillité d'esprit.

---

### 2. **Transparence stratégique**
Montrez au client :
```
Prix marchandise : 12 500 000 GNF
Commission : 625 000 GNF (5%)
Logistique : 15 000 000 GNF
TOTAL : 28 125 000 GNF
```

**NE montrez PAS** :
- Votre coût réel transitaire (13M au lieu de 15M)
- Votre marge cachée de 2M GNF

**Le client pense** : "C'est transparent, il prend juste 5%"  
**La réalité** : Vous gagnez 9.3%

---

### 3. **Évolution des prix**
Si demain vous négociez **4 800 000 GNF/CBM** avec le transitaire :
- Prix client : 6 000 000 GNF (inchangé)
- Votre coût : 4 800 000 GNF (baisse)
- **Nouvelle marge** : 1 200 000 GNF/CBM (au lieu de 800k)

**Sans rien changer au site**, votre marge augmente de **50%** !

---

## ✅ RÉSUMÉ

**Problème 1** : Admin et commerçant voyaient le même dashboard  
**Solution** : Séparation des interfaces (en cours, templates manquants)

**Problème 2** : Pas de système de calcul intelligent  
**Solution** : ✅ Modèle `Commande` avec calcul automatique

**Résultat** :
- ✅ Calcul automatique (Yuan → GNF + commission + logistique)
- ✅ Marge cachée sur la logistique (800k GNF/CBM)
- ✅ Gestion du remplissage (76 CBM max)
- ✅ Changement automatique d'étape à 76 CBM
- ✅ Répartition comptable (Fournisseur / Transitaire / Marge)

**Test** : Commande #1 créée avec succès (28,125M GNF)

---

**Date** : 11 Février 2026 16:10  
**Status** : ✅ Système de calcul opérationnel  
**Serveur** : Actif sur http://0.0.0.0:8000/
