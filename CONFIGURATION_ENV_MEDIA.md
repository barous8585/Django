# 🔐 Configuration .env et Gestion des Médias - Guide Complet

## ✅ CE QUI A ÉTÉ FAIT

### 1. **Configuration des Variables d'Environnement**

#### Fichier `config.env` créé
```bash
# Copiez ce fichier en .env à la racine du projet
Django/
├── .env  ← Créez ce fichier manuellement (non versionné)
└── config.env  ← Template fourni
```

**Variables configurées :**
- ✅ `SECRET_KEY` - Nouvelle clé secrète Django générée
- ✅ `DEBUG` - Mode debug
- ✅ `ALLOWED_HOSTS` - Hosts autorisés
- ✅ `SMS_PROVIDER` - Configuration SMS (Twilio, etc.)
- ✅ `ORANGE_MONEY_API_KEY` - API Orange Money
- ✅ `MAX_UPLOAD_SIZE` - Taille max des fichiers (5MB)
- ✅ `ALLOWED_EXTENSIONS` - Extensions autorisées (jpg, png, pdf)

#### `.gitignore` mis à jour
```
.env
.env.local
config.env
media/
```
**Important : Le fichier .env ne sera JAMAIS commité sur Git**

---

### 2. **Gestion Avancée des Fichiers Médias**

#### Nouveau fichier `core/validators.py`
**3 validateurs créés :**

1. **`validate_file_extension()`**
   - Vérifie l'extension du fichier
   - Accepte : jpg, jpeg, png, pdf
   - Rejette tout autre format

2. **`validate_file_size()`**
   - Limite : 5MB par défaut
   - Configurable via .env

3. **`validate_image()`**
   - Vérifie que le fichier est une vraie image
   - Utilise Pillow pour validation

4. **`compress_image()`**
   - Compression automatique des images
   - Redimensionne si > 1920px de largeur
   - Qualité JPEG à 85% (optimal)
   - Économise de l'espace disque

5. **`get_file_info()`**
   - Récupère infos : nom, taille, extension

#### Modèle `Participation` amélioré
```python
preuve_paiement = models.ImageField(
    upload_to='preuves_paiement/%Y/%m/',  # Organisé par année/mois
    validators=[validate_file_extension, validate_file_size, validate_image],
    help_text="Formats acceptés: JPG, PNG (max 5MB)"
)
```

**Fonctionnalités :**
- ✅ Validation automatique à l'upload
- ✅ Compression automatique après sauvegarde
- ✅ Organisation par date (année/mois)
- ✅ Messages d'erreur clairs

---

### 3. **Visualiseur de Preuves de Paiement**

#### Nouvelle page `/api/proof/{id}/`
**Fonctionnalités :**
- ✅ **Affichage plein écran** de la preuve
- ✅ **Zoom** : +/- et reset
- ✅ **Mode plein écran** (F11)
- ✅ **Détails complets** : utilisateur, montant, référence, date
- ✅ **Validation en un clic** depuis la page
- ✅ **Rejet** avec message
- ✅ **Informations fichier** : nom, taille, format

#### Admin Django amélioré
**Nouvelles colonnes :**
- ✅ Bouton "🔍 Voir" dans la liste
- ✅ "Visualiseur" dans le détail de la participation
- ✅ Preview de l'image directement dans l'admin
- ✅ Lien vers le visualiseur plein écran

---

## 🌐 COMMENT UTILISER

### Étape 1 : Créer le fichier .env

```bash
# À la racine du projet Django/
cd /Users/thiernoousmanebarry/Desktop/Django

# Copier le template
cp config.env .env

# Éditer avec vos vraies valeurs
nano .env  # ou avec votre éditeur
```

### Étape 2 : Tester l'upload de preuve

#### Via l'Admin Django
1. Aller sur http://127.0.0.1:8000/admin/
2. Connexion : `+224620000000` / `admin123`
3. Aller dans **Participations** → **Ajouter une participation**
4. Remplir les champs
5. **Upload une image** (JPG/PNG, max 5MB)
6. Sauvegarder

#### Validation des preuves
1. Liste des participations : http://127.0.0.1:8000/admin/core/participation/
2. Cliquer sur **"🔍 Voir"** dans la colonne Preuve
3. Page du visualiseur s'ouvre
4. Utiliser les boutons **Zoom** : `+` `-` `100%` `⛶`
5. Cliquer **"✓ Valider le paiement"** pour valider

### Étape 3 : Via l'API REST

**Upload d'une participation avec preuve :**

```bash
curl -X POST http://127.0.0.1:8000/api/participations/ \
  -H "Content-Type: multipart/form-data" \
  -F "conteneur=1" \
  -F "montant=50000" \
  -F "reference_paiement=OM123456789" \
  -F "preuve_paiement=@/chemin/vers/photo.jpg"
```

---

## 📂 STRUCTURE DES FICHIERS MÉDIAS

```
Django/
├── media/
│   └── preuves_paiement/
│       ├── 2026/
│       │   ├── 02/         # Février 2026
│       │   │   ├── photo_1.jpg
│       │   │   ├── photo_2.jpg
│       │   │   └── ...
│       │   ├── 03/         # Mars 2026
│       │   └── ...
│       └── 2027/
│           └── ...
```

**Avantages :**
- Organisation automatique par date
- Facile à archiver/nettoyer
- Évite les conflits de noms

---

## 🔒 SÉCURITÉ

### Fichiers .env
- ❌ **JAMAIS** commiter .env sur Git
- ✅ Toujours dans `.gitignore`
- ✅ Utiliser `.env.example` pour le template
- ✅ Droits d'accès : `chmod 600 .env`

### Validation des uploads
- ✅ Extensions validées (pas d'executable)
- ✅ Taille limitée (évite DoS)
- ✅ Validation MIME type (vraie image)
- ✅ Compression automatique (économie d'espace)

### URLs sécurisées
- ✅ `/api/proof/{id}/` nécessite `@staff_member_required`
- ✅ Seuls les admins peuvent voir les preuves

---

## 🎯 URLS DISPONIBLES

### Visualisation des preuves
- **Visualiseur** : http://127.0.0.1:8000/api/proof/1/
  (Remplacer `1` par l'ID de la participation)

### API Upload
- **POST** : http://127.0.0.1:8000/api/participations/
  - Content-Type: `multipart/form-data`
  - Champs: `conteneur`, `montant`, `reference_paiement`, `preuve_paiement`

### Admin Django
- **Liste** : http://127.0.0.1:8000/admin/core/participation/
- **Détail** : http://127.0.0.1:8000/admin/core/participation/{id}/change/

---

## 📋 CHECKLIST D'INSTALLATION

### Pour le développement
- [x] ✅ Fichier `config.env` créé (template)
- [ ] ⏳ Créer `.env` manuellement (copier config.env)
- [x] ✅ `.gitignore` mis à jour
- [x] ✅ `settings.py` utilise decouple
- [x] ✅ Validateurs créés
- [x] ✅ Compression automatique activée
- [x] ✅ Visualiseur de preuves opérationnel

### Pour la production
- [ ] ⏳ Remplir VRAIES valeurs dans .env :
  - [ ] `SECRET_KEY` unique
  - [ ] `DEBUG=False`
  - [ ] `ALLOWED_HOSTS` (domaine production)
  - [ ] `SMS_API_KEY` (Twilio)
  - [ ] `ORANGE_MONEY_API_KEY`
- [ ] ⏳ Configurer serveur de fichiers (Nginx/S3)
- [ ] ⏳ Backup automatique du dossier media/
- [ ] ⏳ CDN pour les fichiers statiques/media

---

## 🚀 TEST RAPIDE

### Test 1 : Variables d'environnement
```bash
source .venv/bin/activate
python manage.py shell

>>> from django.conf import settings
>>> settings.SECRET_KEY  # Doit afficher la clé du .env
>>> settings.MAX_UPLOAD_SIZE  # Doit afficher 5242880
```

### Test 2 : Upload d'une preuve
1. Aller sur http://127.0.0.1:8000/admin/core/participation/add/
2. Uploader une image > 5MB → Doit refuser
3. Uploader un fichier .exe → Doit refuser
4. Uploader une image JPG < 5MB → Doit accepter

### Test 3 : Visualiseur
1. Créer une participation avec preuve
2. Aller sur `/api/proof/1/`
3. Tester les boutons zoom
4. Cliquer **"✓ Valider"** → Doit rediriger vers admin

---

## 📝 PROCHAINES ÉTAPES

### Configuration SMS (Priorité 1)
```env
# Dans .env
SMS_PROVIDER=twilio
SMS_API_KEY=votre_cle_twilio
SMS_API_SECRET=votre_secret_twilio
```

### Configuration Orange Money (Priorité 2)
```env
ORANGE_MONEY_API_KEY=votre_cle_api
ORANGE_MONEY_API_SECRET=votre_secret
ORANGE_MONEY_BASE_URL=https://api.orange.com/
```

### Migration PostgreSQL (Priorité 3)
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=tontine_db
DB_USER=tontine_user
DB_PASSWORD=VotreMotDePasseSecurisé
DB_HOST=localhost
DB_PORT=5432
```

---

## 🛠️ COMMANDES UTILES

```bash
# Vérifier la taille du dossier media
du -sh media/

# Lister toutes les preuves uploadées
find media/preuves_paiement -type f

# Compter les images
find media/preuves_paiement -type f | wc -l

# Nettoyer les images de test (ATTENTION !)
# rm -rf media/preuves_paiement/test/
```

---

## 📊 STATISTIQUES

- **Fichiers créés** : 5 nouveaux fichiers
  - `config.env`
  - `core/validators.py`
  - `core/proof_views.py`
  - `templates/api/proof_viewer.html`
  - Migration 0002
  
- **Fichiers modifiés** : 4 fichiers
  - `settings.py` (utilise decouple)
  - `models.py` (validateurs + compression)
  - `admin.py` (boutons visualiseur)
  - `urls.py` (route proof)

- **Fonctionnalités ajoutées** : 8
  1. Variables d'environnement
  2. Validation extensions
  3. Validation taille
  4. Validation image
  5. Compression automatique
  6. Visualiseur zoom
  7. Validation en un clic
  8. Organisation par date

---

## 🎉 CONCLUSION

**Vous avez maintenant :**
- ✅ Configuration sécurisée avec .env
- ✅ Validation complète des uploads
- ✅ Compression automatique des images
- ✅ Visualiseur professionnel avec zoom
- ✅ Validation/rejet en un clic
- ✅ Organisation automatique par date

**Prêt pour :**
- ✅ Recevoir les preuves Orange Money
- ✅ Valider les paiements visuellement
- ✅ Production (après remplir vraies valeurs .env)

**Fichier de référence :** `config.env` (template à copier en .env)

🚀 **Serveur actif : http://127.0.0.1:8000/**
