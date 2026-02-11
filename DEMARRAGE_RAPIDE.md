# 🚀 GUIDE DE DÉMARRAGE RAPIDE

**Date** : 11 Février 2026  
**Version** : 3.0 - Système Complet  

---

## ⚡ TESTER EN 2 MINUTES

### 1️⃣ Vérifier que le serveur tourne

```bash
# Le serveur doit être actif sur :
http://127.0.0.1:8000/
http://0.0.0.0:8000/
```

Si pas actif, lancer :
```bash
cd /Users/thiernoousmanebarry/Desktop/Django
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

---

### 2️⃣ Test Login ADMIN

1. **Ouvrir** : http://127.0.0.1:8000/login/
2. **Entrer** : `+224620000000`
3. **Code OTP** : Regarder dans le navigateur (affiché dans le message de succès)
4. **Entrer le code** : 6 chiffres
5. **Résultat attendu** : Redirection automatique vers `/admin-panel/`

**✅ Vous devez voir** :
- Titre : "🏦 PANNEAU ADMINISTRATEUR"
- Statistiques : Conteneurs, Participations, Utilisateurs
- Menu : Administration / Gestion / Statistiques
- **Marge plateforme visible** (si commandes existent)

**❌ Si redirection vers `/dashboard/`** :
→ Problème : vider le cache du navigateur (`Cmd+Shift+R` sur Mac)

---

### 3️⃣ Test Login COMMERÇANT

1. **Ouvrir une nouvelle fenêtre privée** (Incognito)
2. **Aller sur** : http://127.0.0.1:8000/login/
3. **Entrer** : `+224620123456`
4. **Code OTP** : Affiché dans le message
5. **Entrer le code**
6. **Résultat attendu** : Redirection vers `/commercant/dashboard/`

**✅ Vous devez voir** :
- Titre : "👤 MON ESPACE COMMERÇANT"
- Boutons : "➕ Participer" / "📜 Historique" / "👤 Profil"
- **Uniquement SES statistiques** (pas celles des autres)
- **PAS de marge plateforme visible**

---

### 4️⃣ Test Participation Commerçant

1. **Connecté comme commerçant** (`+224620123456`)
2. **Cliquer** : "➕ Participer à un Conteneur"
3. **Sélectionner** : Conteneur CHINE-GUINEE
4. **Montant** : `5000000` GNF
5. **Référence** : `OM20260211TEST`
6. **Photo** : Uploader une image quelconque (reçu Orange Money)
7. **Soumettre**

**✅ Résultat attendu** :
- Message : "Participation enregistrée avec succès !"
- Statut : "⏳ En attente de validation"
- Visible dans "📜 Historique"

---

### 5️⃣ Test Validation Admin

1. **Connecté comme admin** (`+224620000000`)
2. **Aller sur** : http://127.0.0.1:8000/admin/
3. **Login** : `+224620000000` / `admin123`
4. **Aller dans** : Core → Participations
5. **Sélectionner** la participation du test 4
6. **Cocher** : "Valide"
7. **Sauvegarder**

**✅ Résultat attendu** :
- Participation validée ✅
- Montant du conteneur mis à jour (+5M GNF)
- Barre de progression actualisée
- Visible chez le commerçant comme "✅ Validée"

---

## 🧪 COMPTES DE TEST

### Administrateur

```
Téléphone : +224620000000
Rôle : Admin (is_staff=True)
Redirection : /admin-panel/
Django Admin : ✅ Accès complet
Mot de passe Django : admin123
```

### Commerçant

```
Téléphone : +224620123456
Rôle : Commerçant (is_staff=False)
Redirection : /commercant/dashboard/
Django Admin : ❌ Pas d'accès
```

---

## 📱 URLS PRINCIPALES

### Pages Publiques
- Accueil : http://127.0.0.1:8000/
- Login : http://127.0.0.1:8000/login/
- Conteneurs : http://127.0.0.1:8000/api/conteneurs/
- Fournisseurs : http://127.0.0.1:8000/api/fournisseurs/

### Admin (Staff uniquement)
- Dashboard Admin : http://127.0.0.1:8000/admin-panel/
- Django Admin : http://127.0.0.1:8000/admin/
- Dashboard Stats : http://127.0.0.1:8000/dashboard/

### Commerçant (Connecté)
- Dashboard : http://127.0.0.1:8000/commercant/dashboard/
- Participer : http://127.0.0.1:8000/commercant/participer/
- Historique : http://127.0.0.1:8000/commercant/historique/
- Profil : http://127.0.0.1:8000/commercant/profil/

---

## 🔧 COMMANDES UTILES

### Démarrer le serveur
```bash
cd /Users/thiernoousmanebarry/Desktop/Django
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### Créer un nouveau commerçant
```bash
python manage.py shell
```
```python
from django.contrib.auth import get_user_model
User = get_user_model()

commercant = User.objects.create(
    telephone='+224620999999',
    username='+224620999999',
    is_staff=False
)
print(f"Commerçant créé : {commercant.telephone}")
exit()
```

### Créer un nouveau conteneur
```bash
python manage.py shell
```
```python
from core.models import Conteneur
from decimal import Decimal

conteneur = Conteneur.objects.create(
    nom="DUBAI-GUINEE-2026",
    description="Électronique et Accessoires",
    objectif=Decimal('50000000'),
    devise='USD',
    etape='collecte',
    capacite_max_cbm=Decimal('76.00')
)
print(f"Conteneur créé : {conteneur.nom}")
exit()
```

### Créer une commande test
```bash
python manage.py shell
```
```python
from core.models import Commande, Conteneur
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()
client = User.objects.get(telephone='+224620123456')
conteneur = Conteneur.objects.first()

commande = Commande.objects.create(
    client=client,
    conteneur=conteneur,
    description='Test smartphones',
    categorie='ELECTRONIQUE',
    prix_achat_yuan=Decimal('10000'),
    volume_cbm=Decimal('2.5')
)
print(f"Commande créée : {commande.total_a_payer} GNF")
exit()
```

---

## 🐛 RÉSOLUTION DE PROBLÈMES

### Problème 1 : Redirection incorrecte après login

**Symptôme** : Admin redirigé vers `/dashboard/` au lieu de `/admin-panel/`

**Solution** :
1. Vider le cache du navigateur : `Cmd+Shift+R` (Mac) ou `Ctrl+Shift+R` (Windows)
2. Ou fermer complètement le navigateur et rouvrir
3. Ou utiliser une fenêtre privée/incognito

---

### Problème 2 : "TemplateDoesNotExist"

**Symptôme** : Erreur lors de l'accès à `/commercant/dashboard/`

**Vérifier** :
```bash
ls -la /Users/thiernoousmanebarry/Desktop/Django/templates/api/
```

**Doit contenir** :
- `commercant_dashboard.html`
- `commercant_participer.html`
- `commercant_historique.html`
- `commercant_profil.html`

---

### Problème 3 : Jauge ne s'actualise pas

**Cause** : Participation créée mais pas validée

**Solution** :
1. Aller dans Django Admin : `/admin/core/participation/`
2. Sélectionner la participation
3. **Cocher "Valide"**
4. Sauvegarder
5. Rafraîchir la page du conteneur

---

### Problème 4 : Code OTP invalide

**Cause** : Code expiré (5 min) ou mal saisi

**Solution** :
1. Cliquer "Renvoyer le code"
2. Utiliser le nouveau code affiché
3. Copier-coller le code depuis la console si besoin

---

## 📊 VÉRIFIER QUE TOUT FONCTIONNE

### Check-list Backend

```bash
# 1. Serveur actif ?
curl http://127.0.0.1:8000/

# 2. API Conteneurs ?
curl http://127.0.0.1:8000/api/conteneurs/?format=json

# 3. API Participations ?
curl http://127.0.0.1:8000/api/participations/?format=json

# 4. API Fournisseurs ?
curl http://127.0.0.1:8000/api/fournisseurs/?format=json

# 5. Taux de change ?
curl http://127.0.0.1:8000/api/taux-change/?format=json
```

**Résultats attendus** : Code 200 avec données JSON

---

### Check-list Frontend

1. ✅ Page d'accueil charge : http://127.0.0.1:8000/
2. ✅ Login charge : http://127.0.0.1:8000/login/
3. ✅ Admin panel charge : http://127.0.0.1:8000/admin-panel/
4. ✅ Dashboard commerçant charge : http://127.0.0.1:8000/commercant/dashboard/
5. ✅ Liste conteneurs charge : http://127.0.0.1:8000/api/conteneurs/
6. ✅ Liste fournisseurs charge : http://127.0.0.1:8000/api/fournisseurs/

---

## 💰 TESTER LE SYSTÈME DE CALCUL

### Scénario : Commande de 10k Yuan de Smartphones (2.5 CBM)

**Input** :
```
Prix achat : 10 000 Yuan
Volume : 2.5 CBM
Catégorie : ELECTRONIQUE
Taux de change : 1 250 GNF/Yuan
Commission : 5%
Tarif logistique : 6 000 000 GNF/CBM
```

**Output attendu** :
```
Prix achat GNF : 12 500 000 GNF (10k × 1250)
Commission : 625 000 GNF (5%)
Logistique : 15 000 000 GNF (6M × 2.5)
TOTAL CLIENT : 28 125 000 GNF

Répartition (visible uniquement admin) :
- Fournisseur : 12 500 000 GNF
- Transitaire : 13 000 000 GNF (coût réel : 5.2M × 2.5)
- Marge plateforme : 2 625 000 GNF (9.3%)
```

**Comment tester** :
1. Connecté comme admin
2. Aller dans Django Admin : `/admin/core/commande/add/`
3. Remplir avec les valeurs ci-dessus
4. Sauvegarder
5. **Vérifier** : Total à payer = 28 125 000 GNF
6. **Vérifier** : Marge plateforme = 2 625 000 GNF

---

## 🎯 OBJECTIF FINAL

**Vous devez avoir** :
1. ✅ 2 dashboards séparés (Admin vs Commerçant)
2. ✅ Redirection automatique selon le rôle
3. ✅ Calcul automatique des commandes
4. ✅ Marge plateforme cachée pour le commerçant
5. ✅ Système de participation avec upload de preuve
6. ✅ Validation admin avec mise à jour auto

**Si tout fonctionne** :
→ La plateforme est prête pour les tests utilisateurs réels !

---

## 📞 SUPPORT

**En cas de problème** :
1. Vérifier les logs du serveur Django
2. Vérifier la console du navigateur (F12)
3. Consulter les fichiers de documentation :
   - `RECAPITULATIF_COMPLET.md`
   - `SYSTEME_CALCUL_INTELLIGENT.md`
   - `SEPARATION_ROLES.md`

---

**Date** : 11 Février 2026  
**Version** : 3.0  
**Statut** : ✅ Prêt pour tests
