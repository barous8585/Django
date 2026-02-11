# 🚂 GUIDE DÉPLOIEMENT RAILWAY - PAS À PAS

**Date** : 11 Février 2026  
**Tu es ici** : Interface Railway "What would you like to create?"

---

## 📍 ÉTAPE 1 : CHOISIR "GitHub Repository"

Sur l'écran que tu vois actuellement, **clique sur** :

```
🐙 GitHub Repository
```

**Pourquoi ?** Railway va se connecter à ton repo GitHub pour déployer automatiquement.

---

## 📍 ÉTAPE 2 : Connecter GitHub (si première fois)

Si c'est ta première fois sur Railway :

1. Railway va te demander d'autoriser l'accès à GitHub
2. **Clique** : "Authorize Railway"
3. **Sélectionne** : "All repositories" ou juste ton organisation

**Résultat** : Railway peut maintenant accéder à tes repos.

---

## 📍 ÉTAPE 3 : Créer le Repo sur GitHub

### Option A : Via GitHub.com (Recommandé)

1. **Ouvre** : https://github.com/new
2. **Repository name** : `tontine-digitale`
3. **Description** : "Plateforme de groupage de conteneurs pour commerçants en Guinée"
4. **Public ou Private** : À toi de choisir (Private recommandé)
5. **NE PAS** cocher "Initialize with README"
6. **Cliquer** : "Create repository"

### Option B : Via ligne de commande

```bash
# Créer le repo sur GitHub avec gh CLI
gh repo create tontine-digitale --private --source=. --remote=origin

# Ou manuellement après avoir créé sur GitHub.com :
git remote add origin https://github.com/TON-USERNAME/tontine-digitale.git
git branch -M main
git push -u origin main
```

---

## 📍 ÉTAPE 4 : Pousser le Code

Dans ton terminal :

```bash
cd /Users/thiernoousmanebarry/Desktop/Django

# Vérifier le commit
git log --oneline -1

# Ajouter le remote (remplace TON-USERNAME)
git remote add origin https://github.com/TON-USERNAME/tontine-digitale.git

# Pousser
git push -u origin main
```

**Identifiants GitHub** :
- Username : Ton nom d'utilisateur GitHub
- Password : Token personnel (pas ton mot de passe !)

**Créer un token** : https://github.com/settings/tokens
- Coche : `repo` (full control)
- Copie le token et utilise-le comme mot de passe

---

## 📍 ÉTAPE 5 : Retour sur Railway

1. **Rafraîchir** la liste des repos dans Railway
2. **Chercher** : `tontine-digitale`
3. **Sélectionner** le repo
4. **Cliquer** : "Deploy now"

**Railway va** :
- ✅ Détecter que c'est un projet Django
- ✅ Lire `requirements.txt`
- ✅ Installer les dépendances
- ✅ Exécuter le `Procfile`
- ✅ Déployer automatiquement !

---

## 📍 ÉTAPE 6 : Ajouter PostgreSQL

Dans ton projet Railway :

1. **Cliquer** : "+ New" (en haut à droite)
2. **Sélectionner** : "Database"
3. **Choisir** : "Add PostgreSQL"
4. **Railway crée** la base de données automatiquement

**Important** : La variable `DATABASE_URL` est **automatiquement ajoutée** à ton service Django !

---

## 📍 ÉTAPE 7 : Configurer les Variables d'Environnement

Dans Railway, aller dans ton service Django :

1. **Cliquer** sur le service (rectangle avec Django)
2. **Onglet** : "Variables"
3. **Ajouter** ces variables :

```bash
# OBLIGATOIRE
SECRET_KEY=<COPIE_LA_CLE_CI_DESSOUS>
DEBUG=False
ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}}

# SÉCURITÉ
ADMIN_REQUIRE_2FA=True

# CLOUDINARY (optionnel pour l'instant)
USE_CLOUDINARY=False

# SMS (mode debug pour l'instant)
SMS_PROVIDER=debug
```

### Générer SECRET_KEY

Dans ton terminal local :
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Copie** la clé générée et colle-la dans `SECRET_KEY` sur Railway.

---

## 📍 ÉTAPE 8 : Attendre le Déploiement

Railway affiche les logs en temps réel :

```
Building...
Installing dependencies...
Collecting Django==5.2.11
...
Build completed successfully!
Starting server...
Server running on http://0.0.0.0:8000
```

**Durée** : 2-5 minutes

---

## 📍 ÉTAPE 9 : Obtenir l'URL de ton Site

1. Dans Railway, **cliquer** sur le service Django
2. **Onglet** : "Settings"
3. **Section** : "Networking"
4. **Cliquer** : "Generate Domain"

**Railway génère** une URL automatique :
```
https://tontine-digitale-production-abc123.up.railway.app/
```

**C'est ton URL publique !** 🎉

---

## 📍 ÉTAPE 10 : Exécuter les Migrations

Dans Railway, aller dans ton service Django :

1. **Cliquer** sur le service
2. **Onglet** : "⚡ Console" (ou "Deployments" → ⋮ → "Open Shell")
3. **Exécuter** :

```bash
# Migrer la base de données
python manage.py migrate

# Créer le superutilisateur admin
python manage.py createsuperuser
# Téléphone: +224620000000
# Mot de passe: admin123 (change-le !)

# Créer les taux de change
python manage.py shell
```

Dans le shell Python :
```python
from core.models import TauxDeChange
from decimal import Decimal

TauxDeChange.objects.create(devise='USD', taux_gnf=Decimal('8650'), actif=True)
TauxDeChange.objects.create(devise='EUR', taux_gnf=Decimal('9500'), actif=True)
TauxDeChange.objects.create(devise='CNY', taux_gnf=Decimal('1200'), actif=True)
print("✅ Taux créés")
exit()
```

---

## 📍 ÉTAPE 11 : TESTER !

### Test 1 : Accéder au site

Ouvrir : `https://ton-app.up.railway.app/`

**Tu dois voir** : La page d'accueil

---

### Test 2 : Login Admin

1. Aller sur : `https://ton-app.up.railway.app/login/`
2. Entrer : `+224620000000`
3. Code OTP affiché (mode debug)
4. Valider
5. **Résultat** : Redirection vers `/admin-panel/`

---

### Test 3 : Django Admin

1. Aller sur : `https://ton-app.up.railway.app/admin/`
2. Login : `+224620000000` / `admin123`
3. **Tu dois voir** : Interface Django Admin

---

## 📍 ÉTAPE 12 : Configurer Cloudinary (Important)

### Pourquoi ?
Les images uploadées vont **disparaître** à chaque redéploiement sans Cloudinary.

### Comment ?

1. **Créer compte** : https://cloudinary.com/users/register/free
2. **Noter** : Cloud name, API Key, API Secret
3. **Dans Railway, Variables** :
   ```
   USE_CLOUDINARY=True
   CLOUDINARY_CLOUD_NAME=ton-cloud-name
   CLOUDINARY_API_KEY=123456789012345
   CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz123
   ```
4. **Railway redéploie** automatiquement

**Résultat** : Les images sont maintenant sauvegardées sur Cloudinary ! ✅

---

## 📍 ÉTAPE 13 : Créer des Données de Test

Dans Railway Console :

```bash
python manage.py shell
```

```python
from core.models import Conteneur
from decimal import Decimal

# Créer 2 conteneurs actifs
Conteneur.objects.create(
    nom="CHINE-GUINEE-FEV2026",
    objectif=Decimal('50000000'),
    devise='CNY',
    etape='collecte',
    capacite_max_cbm=Decimal('76.00')
)

Conteneur.objects.create(
    nom="DUBAI-GUINEE-FEV2026",
    objectif=Decimal('40000000'),
    devise='USD',
    etape='collecte',
    capacite_max_cbm=Decimal('76.00')
)

print("✅ 2 conteneurs créés")
exit()
```

---

## 📍 ÉTAPE 14 : Inviter les Premiers Commerçants

Partage l'URL avec 5 commerçants de confiance :

```
🚀 Nouvelle plateforme de groupage de conteneurs !

Accès : https://ton-app.up.railway.app/

Comment ça marche :
1. Se connecter avec ton numéro
2. Choisir un conteneur
3. Envoyer la preuve Orange Money
4. Suivre l'avancement en temps réel

Support : +224 620 000 000
```

---

## ✅ CHECK-LIST FINALE

Avant de lancer officiellement :

- [ ] Site accessible sur Railway
- [ ] PostgreSQL connecté
- [ ] Migrations exécutées
- [ ] Superuser créé
- [ ] Taux de change ajoutés
- [ ] Cloudinary configuré (important !)
- [ ] 2 conteneurs de test créés
- [ ] Login admin testé
- [ ] Login commerçant testé
- [ ] Upload preuve testé
- [ ] Validation admin testée

---

## 🚨 EN CAS DE PROBLÈME

### Erreur : "Bad Request (400)"

**Cause** : `ALLOWED_HOSTS` incorrect

**Solution** : Dans Railway Variables :
```
ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}}
```

Railway remplace automatiquement `${{RAILWAY_PUBLIC_DOMAIN}}` par ton domaine.

---

### Erreur : "could not connect to database"

**Cause** : PostgreSQL pas encore prêt

**Solution** : Attendre 30 secondes et redéployer (⋮ → Restart)

---

### Les migrations ne passent pas

**Dans Railway Console** :
```bash
python manage.py migrate --run-syncdb
```

---

### Les images ne s'affichent pas

**Cause** : Cloudinary pas configuré

**Solution** : Voir ÉTAPE 12 ci-dessus

---

## 📊 MONITORING

### Voir les logs en temps réel

Dans Railway :
1. Cliquer sur le service
2. Onglet "Deployments"
3. Cliquer sur le déploiement actif
4. Logs s'affichent en temps réel

---

### Vérifier la base de données

Dans Railway Console :
```bash
python manage.py dbshell
```

```sql
-- Voir les utilisateurs
SELECT telephone, is_staff FROM core_utilisateur;

-- Voir les conteneurs
SELECT nom, etape, volume_total_cbm FROM core_conteneur;

-- Quitter
\q
```

---

## 🎉 FÉLICITATIONS !

Si tu es arrivé ici, ta plateforme est **EN LIGNE** ! 🚀

**Prochaines étapes** :
1. Tester avec 5 commerçants
2. Collecter feedback
3. Corriger bugs
4. Lancer officiellement !

**Ton URL** : https://ton-app.up.railway.app/

---

**Date** : 11 Février 2026  
**Statut** : ✅ Déployé sur Railway  
**Support** : Voir `DEPLOIEMENT.md` pour plus de détails
