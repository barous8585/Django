# 📱 PARTAGE RAPIDE - Comment accéder au site depuis votre téléphone

## ⚡ EN 3 ÉTAPES SIMPLES

### **ÉTAPE 1 : Vérifiez votre WiFi**
Les 2 appareils doivent être sur le **MÊME WiFi** :
- ✅ Votre Mac : connecté au WiFi
- ✅ Votre téléphone : connecté au **même** WiFi

---

### **ÉTAPE 2 : Notez l'adresse**
Sur votre téléphone, tapez cette adresse dans Safari/Chrome :

```
http://192.168.43.153:8000/
```

**Ou scannez ce QR code** (à générer sur : https://www.qr-code-generator.com/)

---

### **ÉTAPE 3 : Naviguez**
- 🏠 Vous verrez la page d'accueil
- 🏭 Cliquez sur "Fournisseurs Certifiés"
- 📦 Explorez les 20 fournisseurs
- ✨ Testez les filtres par catégorie

---

## 🔄 VIDER LE CACHE (si vous ne voyez pas les changements)

### **Sur Mac (votre navigateur actuel)**
```
Appuyez sur : Cmd + Shift + R
```

### **Sur iPhone**
1. Fermer Safari complètement (balayer vers le haut depuis le bas)
2. Rouvrir Safari
3. Recharger la page

### **Sur Android**
1. Menu (⋮) → Paramètres → Confidentialité
2. Effacer les données de navigation
3. Recharger la page

---

## 🎯 TESTER

### **Depuis votre Mac**
http://127.0.0.1:8000/

### **Depuis votre téléphone** (même WiFi)
http://192.168.43.153:8000/

### **Depuis un autre ordinateur** (même WiFi)
http://192.168.43.153:8000/

---

## ⚠️ IMPORTANT

**Ce qui fonctionne** :
- ✅ Accès depuis n'importe quel appareil sur votre WiFi
- ✅ Votre famille/amis dans la même maison

**Ce qui NE fonctionne PAS** :
- ❌ Accès depuis Internet (4G/5G)
- ❌ Accès depuis un autre WiFi

**Pour un accès Internet complet**, il faudra déployer sur un serveur cloud (Heroku, DigitalOcean, etc.).

---

## 🆘 PROBLÈME ?

### **"Site inaccessible" sur le téléphone**
1. ✅ Même WiFi que le Mac ?
2. ✅ Serveur Django lancé ?
3. ✅ Adresse correcte ? `http://192.168.43.153:8000/`

### **Cache navigateur (ancien contenu)**
- Mac : `Cmd + Shift + R`
- iPhone : Fermer/rouvrir Safari
- Android : Vider le cache

### **L'IP a changé ?**
```bash
# Sur votre Mac, dans le Terminal :
ipconfig getifaddr en0
```
Utilisez la nouvelle IP affichée.

---

## 📞 CONTACT

**Serveur actif sur** :
- Local : http://127.0.0.1:8000/
- Réseau : http://192.168.43.153:8000/

**Documentation complète** : `ACCES_EXTERNE.md`

---

✅ **Tout est configuré ! Testez maintenant depuis votre téléphone !**
