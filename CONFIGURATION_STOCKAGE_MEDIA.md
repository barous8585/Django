# 📸 CONFIGURATION STOCKAGE MÉDIA (Cloudinary)

**Problème** : Les images uploadées par les commerçants disparaissent à chaque redéploiement sur Railway/Render.

**Solution** : Utiliser Cloudinary pour stocker les preuves de paiement.

---

## 🎯 Pourquoi Cloudinary ?

- ✅ **Gratuit** : 25 GB de stockage
- ✅ **Simple** : Configuration en 10 minutes
- ✅ **CDN** : Images servies rapidement partout dans le monde
- ✅ **Optimisation automatique** : Compression, redimensionnement
- ✅ **Sécurisé** : HTTPS automatique

---

## 🚀 INSTALLATION (10 minutes)

### 1. Créer un compte Cloudinary

1. Aller sur : https://cloudinary.com/users/register/free
2. S'inscrire (gratuit)
3. Noter tes identifiants :
   - **Cloud name** : `ton-cloud-name`
   - **API Key** : `123456789012345`
   - **API Secret** : `abcdefghijklmnopqrstuvwxyz`

---

### 2. Installer les dépendances

```bash
pip install cloudinary django-cloudinary-storage
```

---

### 3. Mettre à jour `requirements.txt`

Ajouter ces lignes :
```
cloudinary==1.41.0
django-cloudinary-storage==0.3.0
```

---

### 4. Configurer `settings.py`

Ajouter en haut du fichier (après les imports) :

```python
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Cloudinary Configuration
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME', default=''),
    api_key=config('CLOUDINARY_API_KEY', default=''),
    api_secret=config('CLOUDINARY_API_SECRET', default=''),
    secure=True
)
```

Modifier la section `INSTALLED_APPS` :

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'cloudinary_storage',  # ⭐ AVANT django.contrib.staticfiles
    'cloudinary',          # ⭐ NOUVEAU
    'core',
]
```

Modifier la configuration des médias (remplacer l'ancienne section MEDIA) :

```python
# Media files (avec Cloudinary)
if config('USE_CLOUDINARY', default=False, cast=bool):
    # Production : Cloudinary
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': config('CLOUDINARY_API_KEY'),
        'API_SECRET': config('CLOUDINARY_API_SECRET'),
    }
else:
    # Développement : Local
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'
```

---

### 5. Ajouter les variables d'environnement

#### En local (`.env`) :
```bash
USE_CLOUDINARY=False
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

#### En production (Railway/Render) :
```bash
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=ton-cloud-name
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz
```

---

## ✅ TESTER

### En local (avant déploiement)

1. Mettre `USE_CLOUDINARY=True` dans `.env`
2. Uploader une preuve de paiement
3. Vérifier sur Cloudinary Dashboard que l'image apparaît

### En production

1. Après déploiement, uploader une preuve
2. Aller sur : https://cloudinary.com/console/media_library
3. L'image doit apparaître dans "Media Library"
4. Redéployer l'app → l'image reste accessible ✅

---

## 🔍 VÉRIFICATION

### URLs des images

**Avant Cloudinary** :
```
http://127.0.0.1:8000/media/preuves_paiement/2026/02/recu.jpg
```

**Après Cloudinary** :
```
https://res.cloudinary.com/ton-cloud-name/image/upload/v123456/preuves_paiement/2026/02/recu.jpg
```

---

## 💡 AVANTAGES SUPPLÉMENTAIRES

### Transformation d'images automatique

Cloudinary peut redimensionner automatiquement :

```python
# Dans models.py, tu peux ajouter :
from cloudinary.models import CloudinaryField

class Participation(models.Model):
    # Remplacer :
    # preuve_paiement = models.ImageField(upload_to='preuves_paiement/%Y/%m/')
    
    # Par :
    preuve_paiement = CloudinaryField(
        'image',
        folder='preuves_paiement',
        transformation={
            'width': 800,
            'height': 600,
            'crop': 'limit',
            'quality': 'auto:good'
        }
    )
```

**Résultat** : Toutes les images sont automatiquement redimensionnées et optimisées !

---

## 📊 QUOTAS GRATUITS

| Ressource | Quota Gratuit |
|-----------|---------------|
| Stockage | 25 GB |
| Bande passante | 25 GB/mois |
| Transformations | 25 000/mois |
| Images | Illimité |

**Estimation** : 
- 1 preuve = ~500 KB
- 50 000 preuves = 25 GB
- Largement suffisant pour commencer !

---

## 🆘 EN CAS DE PROBLÈME

### Erreur : "cloudinary_storage not found"

**Solution** :
```bash
pip install django-cloudinary-storage
pip freeze > requirements.txt
```

### Les images n'apparaissent pas

**Vérifier** :
1. `USE_CLOUDINARY=True` en production
2. Variables `CLOUDINARY_*` correctement configurées
3. Cloudinary Dashboard → Media Library (images doivent apparaître)

### Erreur : "Invalid cloud_name"

**Cause** : Cloud name incorrect

**Solution** : Aller sur Cloudinary Dashboard → copier le bon "Cloud name"

---

## ✅ CHECK-LIST

- [ ] Compte Cloudinary créé
- [ ] `cloudinary` et `django-cloudinary-storage` installés
- [ ] `settings.py` modifié (imports + INSTALLED_APPS + MEDIA config)
- [ ] Variables d'environnement ajoutées (local + production)
- [ ] Test upload en local (avec `USE_CLOUDINARY=True`)
- [ ] Déployé en production avec variables Cloudinary
- [ ] Test upload en production
- [ ] Images persistantes après redéploiement ✅

---

**Temps total** : 10-15 minutes  
**Coût** : Gratuit (plan Free)  
**Résultat** : Les preuves de paiement ne disparaissent plus jamais ! 🎉
