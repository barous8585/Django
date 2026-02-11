# 🌐 GUIDE D'ACCÈS EXTERNE - Tontine Digitale

## ✅ CONFIGURATION RÉALISÉE

### 1. **Vider le cache du navigateur** 
Pour voir les dernières modifications (correction des liens) :

**Sur Mac (Safari/Chrome)** :
- Appuyer sur **`Cmd + Shift + R`** (rechargement forcé)

**Ou manuellement** :
1. Safari : Développement → Vider les caches
2. Chrome : ⋮ (menu) → Plus d'outils → Effacer les données de navigation

---

### 2. **Serveur accessible depuis d'autres appareils**

Le serveur Django a été configuré pour accepter les connexions depuis :
- ✅ Votre Mac : `localhost` et `127.0.0.1`
- ✅ Autres appareils sur le même réseau WiFi : `192.168.43.153`
- ✅ Toutes les interfaces : `0.0.0.0`

---

## 🔗 COMMENT PARTAGER L'APPLICATION

### **Depuis votre Mac**
Utilisez : http://127.0.0.1:8000/

### **Depuis un autre appareil (téléphone, tablette, autre ordinateur)**

**IMPORTANT** : L'appareil doit être sur le **même réseau WiFi** que votre Mac !

#### **Étape 1 : Trouver l'adresse IP de votre Mac**

Votre adresse IP actuelle : **192.168.43.153**

Pour vérifier (si elle change) :
```bash
ipconfig getifaddr en0
# ou
ipconfig getifaddr en1
```

#### **Étape 2 : Accéder depuis un autre appareil**

Sur le téléphone/tablette/ordinateur, ouvrir le navigateur et taper :

```
http://192.168.43.153:8000/
```

**URLs disponibles** :
- Page d'accueil : `http://192.168.43.153:8000/`
- Catalogue fournisseurs : `http://192.168.43.153:8000/api/fournisseurs/`
- Conteneurs : `http://192.168.43.153:8000/api/conteneurs/`
- Admin : `http://192.168.43.153:8000/admin/`

---

## 📱 EXEMPLE D'UTILISATION

### **Depuis un iPhone/Android**

1. **Connectez-vous au même WiFi** que le Mac
   - Nom du réseau : (votre WiFi actuel)

2. **Ouvrez Safari ou Chrome** sur le téléphone

3. **Tapez dans la barre d'adresse** :
   ```
   http://192.168.43.153:8000/
   ```

4. **Vous verrez** la page d'accueil de l'application

5. **Naviguez** :
   - Cliquez sur "🏭 Fournisseurs Certifiés"
   - Explorez le catalogue
   - Testez les filtres

---

## 🔒 SÉCURITÉ

### **Configuration actuelle (DÉVELOPPEMENT)**
- ✅ DEBUG activé
- ✅ Accessible uniquement sur le réseau local (WiFi)
- ✅ Pas d'accès depuis Internet

### **Recommandations**

**Pour le développement (maintenant)** :
- ✅ Configuration actuelle suffisante
- ✅ Accessible uniquement sur votre réseau WiFi privé
- ✅ Impossible d'y accéder depuis Internet

**Pour la production (déploiement futur)** :
- ⏳ Mettre `DEBUG=False`
- ⏳ Utiliser un nom de domaine
- ⏳ Activer HTTPS (certificat SSL)
- ⏳ Configurer un pare-feu
- ⏳ Utiliser un serveur de production (Gunicorn/uWSGI)

---

## 🛠️ COMMANDES UTILES

### **Démarrer le serveur en mode externe**
```bash
cd /Users/thiernoousmanebarry/Desktop/Django
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### **Démarrer en mode local uniquement**
```bash
python manage.py runserver
# ou
python manage.py runserver 127.0.0.1:8000
```

### **Trouver votre IP locale**
```bash
# Sur Mac
ipconfig getifaddr en0  # WiFi
ipconfig getifaddr en1  # Ethernet

# Ou voir toutes les interfaces
ifconfig | grep "inet "
```

### **Vérifier que le serveur écoute**
```bash
lsof -i :8000
```

---

## 🐛 DÉPANNAGE

### **Problème : "Site inaccessible" depuis un autre appareil**

**Solution 1 : Vérifier le WiFi**
- ✅ Les deux appareils sont sur le même réseau WiFi
- ✅ Pas de réseau "invité" (Guest) qui isole les appareils

**Solution 2 : Vérifier le pare-feu Mac**
```bash
# Ouvrir les Préférences Système
# → Sécurité et confidentialité
# → Pare-feu
# → Autoriser Python ou désactiver temporairement
```

**Solution 3 : Vérifier l'IP**
```bash
# Votre IP peut changer si vous redémarrez le routeur
ipconfig getifaddr en0
```

**Solution 4 : Redémarrer le serveur**
```bash
# Arrêter le serveur actuel (Ctrl+C)
# Puis relancer :
python manage.py runserver 0.0.0.0:8000
```

---

### **Problème : Cache du navigateur (ancien contenu)**

**Solutions** :

**Mac (Safari)** :
1. `Cmd + Shift + R` (rechargement forcé)
2. Ou : Développement → Vider les caches

**Mac (Chrome)** :
1. `Cmd + Shift + R` (rechargement forcé)
2. Ou : Menu ⋮ → Plus d'outils → Effacer les données de navigation

**iPhone/Android** :
1. Fermer complètement le navigateur
2. Rouvrir et recharger la page
3. Ou : Mode navigation privée

---

### **Problème : L'IP change souvent**

Si votre routeur WiFi change souvent l'IP de votre Mac, vous pouvez :

**Solution 1 : IP statique (recommandé)**
1. Ouvrir Préférences Système → Réseau
2. WiFi → Avancé → TCP/IP
3. Configurer IPv4 : Manuellement
4. IP : `192.168.43.153` (garder la même)
5. Masque : `255.255.255.0`
6. Routeur : (l'IP de votre routeur, généralement `192.168.43.1`)

**Solution 2 : Utiliser le nom d'hôte Mac**
```
http://nom-du-mac.local:8000/
```
(Remplacer "nom-du-mac" par le nom de votre Mac)

---

## 📊 ÉTAT ACTUEL DU SERVEUR

```
✅ Serveur actif : http://0.0.0.0:8000/
✅ Port : 8000
✅ Adresse IP locale : 192.168.43.153
✅ Réseau : WiFi (même réseau requis)
✅ ALLOWED_HOSTS : localhost, 127.0.0.1, 192.168.43.153, 0.0.0.0
```

---

## 🎯 TESTER L'ACCÈS EXTERNE

### **Checklist**

**Depuis votre Mac** :
- [ ] http://127.0.0.1:8000/ → Fonctionne
- [ ] http://localhost:8000/ → Fonctionne
- [ ] http://192.168.43.153:8000/ → Fonctionne

**Depuis un téléphone (même WiFi)** :
- [ ] http://192.168.43.153:8000/ → Doit fonctionner
- [ ] Cliquer sur "Fournisseurs" → Doit afficher le catalogue
- [ ] Cliquer sur "← Retour Accueil" → Doit revenir à l'accueil (plus d'erreur 401)

**Depuis un autre ordinateur (même WiFi)** :
- [ ] http://192.168.43.153:8000/ → Doit fonctionner

---

## 🚀 DÉPLOIEMENT INTERNET (FUTUR)

Pour rendre l'application accessible depuis Internet (pas seulement WiFi local), vous devrez :

### **Option 1 : Tunnel local (temporaire, gratuit)**
- **Ngrok** : https://ngrok.com/
  ```bash
  ngrok http 8000
  # Donne une URL publique temporaire
  ```

### **Option 2 : Hébergement cloud (production)**
- **Heroku** (facile, gratuit limité)
- **DigitalOcean** ($5/mois)
- **AWS / Google Cloud** (flexible)
- **PythonAnywhere** (spécialisé Python)

### **Option 3 : VPS personnel**
- Louer un serveur
- Configurer Nginx + Gunicorn
- Acheter un nom de domaine
- Installer un certificat SSL

---

## 📝 RÉSUMÉ RAPIDE

### **Pour développer localement (vous seul)**
```bash
python manage.py runserver
```
Accès : http://127.0.0.1:8000/

### **Pour tester avec d'autres (même WiFi)**
```bash
python manage.py runserver 0.0.0.0:8000
```
Accès depuis autres appareils : http://192.168.43.153:8000/

### **Pour vider le cache navigateur**
```
Mac : Cmd + Shift + R
```

---

**Date de configuration** : 11 Février 2026 10:20  
**Adresse IP actuelle** : 192.168.43.153  
**Port** : 8000  
**Status** : ✅ Accessible sur le réseau local WiFi
