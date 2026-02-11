# 🚀 GUIDE DE DÉPLOIEMENT EN PRODUCTION

**Date** : 11 Février 2026  
**Version** : 3.1 - Prêt pour Production  

---

## 📋 TABLE DES MATIÈRES

1. [Prérequis](#prérequis)
2. [Configuration Locale](#configuration-locale)
3. [Déploiement sur Railway](#déploiement-railway)
4. [Déploiement sur Render](#déploiement-render)
5. [Configuration PostgreSQL](#configuration-postgresql)
6. [Sécurité Renforcée](#sécurité-renforcée)
7. [Tests de Remplissage](#tests-de-remplissage)
8. [Monitoring & Maintenance](#monitoring)

---

## ✅ PRÉREQUIS

### Ce qui est déjà fait
- [x] Application Django fonctionnelle
- [x] Séparation Admin vs Commerçant
- [x] Système de calcul intelligent
- [x] Gestion conteneur 76 CBM
- [x] Upload de preuves de paiement

### Ce qu'il te faut
- [ ] Compte GitHub (pour versionner ton code)
- [ ] Compte Railway OU Render (pour héberger)
- [ ] Numéro de téléphone pour SMS réels (Orange Money API)

---

## 🔧 CONFIGURATION LOCALE

### 1. Mettre à jour `.env`

```bash
# .env (Production)
SECRET_KEY=votre-clé-secrète-ultra-longue-ici
DEBUG=False
ALLOWED_HOSTS=ton-app.up.railway.app,ton-domaine.com

# PostgreSQL (fourni par Railway/Render)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Sécurité
ADMIN_REQUIRE_2FA=True

# SMS (optionnel pour l'instant)
SMS_PROVIDER=debug
SMS_API_KEY=
SMS_API_SECRET=

# Orange Money (optionnel)
ORANGE_MONEY_API_KEY=
ORANGE_MONEY_API_SECRET=
```

### 2. Générer une SECRET_KEY sécurisée

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copie la clé générée dans ton `.env`.

### 3. Installer les dépendances de production

```bash
pip install -r requirements.txt
```

### 4. Tester localement avec PostgreSQL (optionnel)

Si tu veux tester PostgreSQL en local :

```bash
# Installer PostgreSQL
brew install postgresql@14  # Mac
# ou apt-get install postgresql  # Linux

# Démarrer PostgreSQL
brew services start postgresql@14

# Créer une base de test
createdb tontine_test

# Dans .env
DATABASE_URL=postgresql://localhost/tontine_test

# Migrer
python manage.py migrate
```

---

## 🚂 DÉPLOIEMENT SUR RAILWAY

### Pourquoi Railway ?
- ✅ Gratuit pour commencer (500h/mois)
- ✅ PostgreSQL inclus automatiquement
- ✅ Déploiement en 1 clic depuis GitHub
- ✅ HTTPS automatique
- ✅ Domaine personnalisé gratuit

### Étapes

#### 1. Créer un compte Railway
- Va sur : https://railway.app/
- Connecte-toi avec GitHub

#### 2. Pousser ton code sur GitHub

```bash
# Dans ton terminal
cd /Users/thiernoousmanebarry/Desktop/Django

# Initialiser Git (si pas déjà fait)
git init
git add .
git commit -m "🚀 Préparation déploiement production v3.1"

# Créer le repo sur GitHub
# Puis :
git remote add origin https://github.com/ton-username/tontine-digitale.git
git branch -M main
git push -u origin main
```

#### 3. Créer un nouveau projet Railway

1. Clique sur "New Project"
2. Sélectionne "Deploy from GitHub repo"
3. Choisis ton repo `tontine-digitale`
4. Railway détecte automatiquement Django

#### 4. Ajouter PostgreSQL

1. Dans ton projet Railway, clique "New"
2. Sélectionne "Database" → "Add PostgreSQL"
3. Railway crée automatiquement une base de données
4. La variable `DATABASE_URL` est automatiquement ajoutée

#### 5. Configurer les variables d'environnement

Dans Railway, va dans "Variables" et ajoute :

```
SECRET_KEY=ta-clé-générée-avant
DEBUG=False
ALLOWED_HOSTS=ton-app.up.railway.app
ADMIN_REQUIRE_2FA=True
```

#### 6. Déployer

Railway déploie automatiquement à chaque push sur GitHub !

```bash
# Ton app sera disponible sur :
https://ton-app.up.railway.app/
```

#### 7. Créer un superutilisateur en production

```bash
# Dans Railway, va dans ton service Django
# Clique sur "Console"
# Exécute :
python manage.py createsuperuser
```

---

## 🎨 DÉPLOIEMENT SUR RENDER

### Pourquoi Render ?
- ✅ Plan gratuit généreux
- ✅ PostgreSQL inclus
- ✅ Meilleure stabilité que Railway
- ✅ Logs détaillés

### Étapes

#### 1. Créer un compte Render
- Va sur : https://render.com/
- Connecte-toi avec GitHub

#### 2. Créer une base PostgreSQL

1. Clique "New" → "PostgreSQL"
2. Nom : `tontine-db`
3. Plan : Free
4. Crée la base
5. Copie l'URL de connexion (Internal Database URL)

#### 3. Créer le Web Service

1. Clique "New" → "Web Service"
2. Connecte ton repo GitHub
3. Configuration :
   - **Name** : `tontine-digitale`
   - **Environment** : Python 3
   - **Build Command** : `pip install -r requirements.txt && python manage.py collectstatic --no-input`
   - **Start Command** : `gunicorn tontine_digitale.wsgi`
   - **Plan** : Free

#### 4. Variables d'environnement

Dans "Environment", ajoute :

```
SECRET_KEY=ta-clé
DEBUG=False
DATABASE_URL=postgresql://user:pass@host/db (copié depuis la DB)
ALLOWED_HOSTS=ton-app.onrender.com
PYTHON_VERSION=3.11.10
```

#### 5. Déployer

Render déploie automatiquement. Ton app sera sur :

```
https://ton-app.onrender.com/
```

---

## 🗄️ CONFIGURATION POSTGRESQL

### Migration SQLite → PostgreSQL

Tes données locales (SQLite) ne sont PAS automatiquement transférées.

#### Option 1 : Recommencer à zéro (recommandé)

```bash
# En production, simplement exécuter :
python manage.py migrate
python manage.py createsuperuser
```

#### Option 2 : Transférer les données (si nécessaire)

```bash
# 1. Exporter les données locales
python manage.py dumpdata --natural-foreign --natural-primary \
  -e contenttypes -e auth.Permission --indent 2 > data.json

# 2. En production, importer
python manage.py loaddata data.json
```

### Vérifier que PostgreSQL fonctionne

```bash
# En production (Railway/Render console)
python manage.py dbshell

# Tu dois voir :
psql (14.x)
Type "help" for help.
tontine_db=>
```

---

## 🔐 SÉCURITÉ RENFORCÉE

### Ce qui est déjà activé (automatique en production)

Lorsque `DEBUG=False`, ton `settings.py` active automatiquement :

✅ **Force HTTPS** : Toutes les connexions sont cryptées  
✅ **Cookies sécurisés** : Session et CSRF protégés  
✅ **HSTS** : Force HTTPS pendant 1 an  
✅ **Protection XSS** : Contre les injections JavaScript  
✅ **X-Frame-Options** : Empêche l'embedding malveillant  
✅ **Sessions courtes** : 1 heure max  

### Protéger la marge cachée

La **marge plateforme** (différence entre tarif client et coût réel) est déjà masquée pour les commerçants.

**Vérifie** :
1. Un commerçant connecté ne peut PAS accéder à `/admin/`
2. Un commerçant ne voit PAS `marge_plateforme` dans l'API
3. Un commerçant ne voit PAS les commandes des autres

**Test** :
```bash
# Se connecter comme commerçant
curl -X POST https://ton-app.com/api/auth/verifier-otp/ \
  -H "Content-Type: application/json" \
  -d '{"telephone": "+224620123456", "otp_code": "123456"}'

# Essayer d'accéder à l'admin (doit échouer)
curl https://ton-app.com/admin/ \
  -H "Authorization: Bearer TOKEN_COMMERCANT"

# Résultat attendu : 403 Forbidden
```

### Double authentification Admin

Même les admins doivent passer par OTP pour se connecter.

**Pour activer** (déjà dans `settings.py`) :
```python
ADMIN_REQUIRE_2FA = True
```

**Comportement** :
1. Admin entre son numéro → Reçoit OTP
2. Valide le code → Accès à `/admin-panel/`
3. Si pas de validation OTP, accès refusé même avec `is_staff=True`

---

## 🧪 TESTS DE REMPLISSAGE

### Script de test inclus : `test_remplissage.py`

Ce script simule 20 clients qui commandent jusqu'à remplir un conteneur de 76 CBM.

### Exécuter le test

#### En local :
```bash
cd /Users/thiernoousmanebarry/Desktop/Django
python test_remplissage.py
```

#### En production :
```bash
# Railway : Console
python test_remplissage.py

# Render : Shell
python test_remplissage.py
```

### Ce que le test vérifie

✅ **Volume total correct** : Somme des volumes = conteneur.volume_total_cbm  
✅ **Changement d'étape** : À 76 CBM → étape = "mer"  
✅ **Pas de dépassement** : Volume ≤ 76 CBM  
✅ **Calcul de la marge** : Somme des marges = marge totale  
✅ **Nombre de commandes** : Toutes enregistrées en DB  

### Résultats attendus

```
🧪 TEST DE REMPLISSAGE DU CONTENEUR
============================================================

🧹 Nettoyage des données de test précédentes...
✅ Données de test nettoyées

📦 Création du conteneur de test...
✅ Conteneur créé : TEST-REMPLISSAGE-2026

👥 Création de 20 clients fictifs...
   ✅ Client 1/20 créé : +224620999001
   ...

📦 Simulation de commandes jusqu'à 76.0 CBM...
   📦 Commande 1: 3.0 CBM (ELECTRONIQUE) - Prix: 15000 Yuan
      → Total client: 37,500,000 GNF
      → Marge plateforme: 3,150,000 GNF
      → Volume cumulé: 3.0/76.0 CBM
   ...
   🎯 Conteneur plein ! (76.0 CBM)

🔍 Vérification des résultats...
============================================================
📊 RÉSULTATS DES TESTS
============================================================
✅ Volume total correct
✅ Étape changée automatiquement (Collecte → Mer)
✅ Nombre de commandes correct (18)
✅ Marge totale correcte : 60,800,000 GNF
✅ Volume ne dépasse pas la capacité max (76 CBM)

============================================================
✅ Tests réussis : 5/5
============================================================

📈 STATISTIQUES FINALES
============================================================

📦 CONTENEUR : TEST-REMPLISSAGE-2026
   • Volume total : 76.0 / 76.0 CBM
   • Taux de remplissage : 100.00%
   • Étape actuelle : MER
   • Nombre de commandes : 18

💰 REVENUS
   • Total facturé aux clients : 675,000,000 GNF
   • Marge plateforme totale : 60,800,000 GNF
   • Taux de marge réel : 9.01%

📊 DÉTAIL PAR CATÉGORIE
   • ELECTRONIQUE :
      - Commandes : 7
      - Volume : 28.0 CBM
      - Marge : 22,400,000 GNF
   • TEXTILE :
      - Commandes : 6
      - Volume : 30.0 CBM
      - Marge : 24,000,000 GNF
   • DIVERS :
      - Commandes : 5
      - Volume : 18.0 CBM
      - Marge : 14,400,000 GNF

============================================================

🎉 TOUS LES TESTS SONT PASSÉS !
✅ Le système de remplissage fonctionne correctement.
```

---

## 📊 MONITORING & MAINTENANCE

### Logs en production

#### Railway :
```bash
# Voir les logs en temps réel
railway logs

# Ou dans l'interface web : Deployments → View Logs
```

#### Render :
```bash
# Interface web : Logs (en temps réel)
```

### Commandes utiles en production

```bash
# Voir l'état de la base de données
python manage.py dbshell

# Voir les utilisateurs
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.count()

# Voir les conteneurs actifs
>>> from core.models import Conteneur
>>> Conteneur.objects.filter(etape='collecte').count()

# Voir la marge totale
>>> from core.models import Commande
>>> from django.db.models import Sum
>>> Commande.objects.aggregate(Sum('marge_plateforme'))
```

### Backups PostgreSQL

#### Railway :
Backups automatiques quotidiens (plan gratuit : 3 jours de rétention)

#### Render :
Backups manuels :
```bash
# Dans la DB Render, clique "Backups" → "Create Backup"
```

### Métriques à surveiller

| Métrique | Seuil | Action |
|----------|-------|--------|
| Temps de réponse | > 3s | Optimiser queries DB |
| Erreurs 500 | > 5/jour | Vérifier logs |
| Utilisation DB | > 80% | Upgrade plan |
| CPU | > 90% | Upgrade plan |

---

## 🚀 CHECK-LIST FINALE AVANT LANCEMENT

### Configuration
- [ ] `SECRET_KEY` changée (pas la valeur par défaut)
- [ ] `DEBUG=False` en production
- [ ] `ALLOWED_HOSTS` configuré avec ton domaine
- [ ] `DATABASE_URL` pointe vers PostgreSQL
- [ ] Variables d'environnement configurées (Railway/Render)

### Base de données
- [ ] Migrations exécutées (`python manage.py migrate`)
- [ ] Superutilisateur créé
- [ ] Taux de change initialisés
- [ ] Au moins 1 conteneur de test créé

### Sécurité
- [ ] HTTPS activé (automatique sur Railway/Render)
- [ ] Cookies sécurisés activés
- [ ] Session timeout configuré (1h)
- [ ] Double authentification admin testée

### Tests
- [ ] Script de remplissage exécuté avec succès
- [ ] Login Admin testé en production
- [ ] Login Commerçant testé en production
- [ ] Upload de preuve de paiement testé
- [ ] Validation admin testée

### Fonctionnalités
- [ ] Séparation Admin/Commerçant vérifiée
- [ ] Calcul automatique testé (10k Yuan = 28.125M GNF)
- [ ] Marge cachée invisible pour commerçant
- [ ] Changement d'étape à 76 CBM testé
- [ ] API OTP fonctionne (codes reçus)

---

## 📞 EN CAS DE PROBLÈME

### Erreur : "Bad Request (400)"
**Cause** : `ALLOWED_HOSTS` incorrect  
**Solution** : Ajoute ton domaine dans `.env` :
```
ALLOWED_HOSTS=ton-app.up.railway.app,ton-domaine.com
```

### Erreur : "could not connect to server"
**Cause** : `DATABASE_URL` incorrect  
**Solution** : Copie l'URL exacte depuis Railway/Render DB settings

### Erreur : "Static files not found"
**Cause** : `collectstatic` pas exécuté  
**Solution** :
```bash
python manage.py collectstatic --no-input
```

### Les images uploadées disparaissent
**Cause** : Railway/Render effacent les fichiers à chaque redéploiement  
**Solution** : Utiliser un service de stockage externe :
- Cloudinary (gratuit jusqu'à 25GB)
- AWS S3
- Voir guide : `CONFIGURATION_STOCKAGE_MEDIA.md` (à créer)

---

## 🎉 FÉLICITATIONS !

Si tu es arrivé ici, ta plateforme est **EN PRODUCTION** ! 🚀

**URLs importantes** :
- App : https://ton-app.up.railway.app/
- Login : https://ton-app.up.railway.app/login/
- Admin : https://ton-app.up.railway.app/admin/

**Prochaines étapes** :
1. Configurer un vrai service SMS (au lieu de OTP debug)
2. Intégrer Orange Money API pour validation automatique
3. Ajouter des notifications push (Firebase)
4. Développer l'app mobile (Flutter)

---

**Date** : 11 Février 2026  
**Version** : 3.1  
**Statut** : ✅ Prêt pour déploiement
