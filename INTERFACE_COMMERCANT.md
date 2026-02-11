# 📱 INTERFACE COMMERÇANT - Guide Complet

**Date** : 11 Février 2026  
**Sujet** : Séparation Admin vs Commerçant

---

## 🎯 LE PROBLÈME

**Question** : "Les commerçants, à partir de leur téléphone, comment vont-ils faire ? Ils sont sensés voir tout ce que moi l'administrateur vois ?"

**Réponse** : NON ! Les commerçants ne doivent PAS voir la même chose que l'administrateur.

---

## ✅ SOLUTION IMPLÉMENTÉE : 2 INTERFACES SÉPARÉES

### 1. **Interface ADMIN** (vous uniquement)
**URL** : http://127.0.0.1:8000/admin/  
**Accès** : Utilisateurs avec `is_staff=True` ou `is_superuser=True`

**Permissions ADMIN** :
- ✅ Voir TOUS les conteneurs
- ✅ Voir TOUTES les participations
- ✅ Valider les paiements
- ✅ Créer/Modifier/Supprimer des conteneurs
- ✅ Gérer les taux de change
- ✅ Gérer les fournisseurs
- ✅ Voir les portefeuilles de tous
- ✅ Annuler des conteneurs
- ✅ Export CSV/Excel
- ✅ Dashboard avec statistiques globales

---

### 2. **Interface COMMERÇANT** (utilisateurs normaux)
**URL** : http://127.0.0.1:8000/commercant/dashboard/  
**Accès** : Utilisateurs avec `is_staff=False`

**Permissions COMMERÇANT** :
- ✅ Voir UNIQUEMENT ses propres participations
- ✅ Voir UNIQUEMENT les conteneurs actifs (collecte)
- ✅ Participer à un conteneur
- ✅ Voir son portefeuille personnel
- ✅ Voir le catalogue fournisseurs
- ✅ Contacter l'admin
- ❌ **NE PEUT PAS** valider de paiements
- ❌ **NE PEUT PAS** voir les autres commerçants
- ❌ **NE PEUT PAS** modifier les conteneurs
- ❌ **NE PEUT PAS** gérer les fournisseurs

---

## 📱 INTERFACE COMMERÇANT CRÉÉE

### Pages disponibles

#### 1. **Dashboard Commerçant** (`/commercant/dashboard/`)
**Affichage** :
- Photo de profil (initiales du téléphone)
- Numéro de téléphone
- **Solde du portefeuille** (gros, visible, en haut)
- **Actions rapides** :
  - 📦 Voir les conteneurs
  - 🤝 Participer à un conteneur
  - 🏭 Catalogue fournisseurs
  - 📜 Historique
- **Mes participations actives** avec :
  - Nom du conteneur
  - Statut (✓ Validé ou ⏳ En attente)
  - Jauge de progression
  - Mon investissement
  - Objectif total
  - Étape actuelle
- **Mes statistiques** :
  - Total investi
  - Nombre de participations
  - Nombre de conteneurs actifs
  - Participations validées

**Navigation bottom** (fixe) :
- 🏠 Accueil
- 📦 Conteneurs
- 🏭 Fournisseurs
- 👤 Profil

---

#### 2. **Participer** (`/commercant/participer/`)
**Affichage** :
- Liste des conteneurs **disponibles** uniquement (étape "Collecte", non annulés)
- Pour chaque conteneur :
  - Nom
  - Objectif
  - Progression
  - Bouton "Participer"

---

#### 3. **Historique** (`/commercant/historique/`)
**Affichage** :
- Toutes mes participations (passées et présentes)
- Mes transactions (20 dernières)

---

#### 4. **Profil** (`/commercant/profil/`)
**Affichage** :
- Mes informations
- Solde portefeuille
- Total investi
- Nombre de conteneurs terminés
- Bouton "Modifier mon profil"
- Bouton "Déconnexion"

---

## 🔐 SYSTÈME DE REDIRECTION AUTOMATIQUE

### Après connexion OTP :

```python
@login_required
def redirect_after_login(request):
    user = request.user
    
    # Admin → Dashboard admin
    if user.is_staff or user.is_superuser:
        return redirect('/admin-panel/')
    
    # Commerçant → Dashboard commerçant
    return redirect('/commercant/dashboard/')
```

**Résultat** :
- **Vous (admin)** : Login → `/admin-panel/` (dashboard admin)
- **Commerçant** : Login → `/commercant/dashboard/` (dashboard commerçant)

---

## 👥 COMMENT CRÉER UN COMMERÇANT

### Méthode 1 : Via l'admin Django

1. Aller sur : http://127.0.0.1:8000/admin/core/utilisateur/add/
2. Remplir :
   - Téléphone : `+224620123456`
   - Mot de passe : (optionnel, utilisera OTP)
   - **NE PAS** cocher "Membre du personnel" (is_staff)
   - **NE PAS** cocher "Statut super-utilisateur" (is_superuser)
   - Cocher "Téléphone vérifié" (pour test)
3. Sauvegarder

**Résultat** : Utilisateur normal (commerçant)

---

### Méthode 2 : Via API OTP

```bash
# 1. Demander OTP
curl -X POST http://127.0.0.1:8000/api/auth/demander-otp/ \
  -H "Content-Type: application/json" \
  -d '{"telephone": "+224620123456"}'

# Réponse : {"message": "Code OTP envoyé", "otp_code": "123456"}

# 2. Vérifier OTP
curl -X POST http://127.0.0.1:8000/api/auth/verifier-otp/ \
  -H "Content-Type: application/json" \
  -d '{"telephone": "+224620123456", "otp_code": "123456"}'

# Réponse : {"access": "token_jwt...", "refresh": "..."}
```

**Résultat** : Utilisateur créé automatiquement, `is_staff=False`

---

## 📊 COMPARAISON ADMIN vs COMMERÇANT

| Fonctionnalité | Admin | Commerçant |
|----------------|-------|------------|
| Voir tous les conteneurs | ✅ | ❌ (seulement actifs) |
| Voir toutes les participations | ✅ | ❌ (seulement les siennes) |
| Créer un conteneur | ✅ | ❌ |
| Participer à un conteneur | ✅ | ✅ |
| Valider des paiements | ✅ | ❌ |
| Voir son portefeuille | ✅ | ✅ |
| Voir tous les portefeuilles | ✅ | ❌ |
| Gérer les fournisseurs | ✅ | ❌ (lecture seule) |
| Gérer les taux de change | ✅ | ❌ |
| Annuler un conteneur | ✅ | ❌ |
| Export CSV/Excel | ✅ | ❌ |
| Dashboard global | ✅ | ❌ |
| Dashboard personnel | ❌ | ✅ |

---

## 🌐 URLS COMPLÈTES

### URLs Admin
- `/admin/` - Admin Django natif
- `/admin-panel/` - Dashboard admin personnalisé
- `/dashboard/` - Stats & exports

### URLs Commerçant
- `/commercant/dashboard/` - Dashboard personnel
- `/commercant/participer/` - Rejoindre un conteneur
- `/commercant/historique/` - Mes participations
- `/commercant/profil/` - Mon profil

### URLs Communes
- `/` - Page d'accueil
- `/login/` - Connexion OTP
- `/api/conteneurs/` - Liste conteneurs (filtrée selon rôle)
- `/api/fournisseurs/` - Catalogue fournisseurs
- `/contact/` - Page de contact

---

## 📱 EXPÉRIENCE UTILISATEUR COMMERÇANT

### Scénario complet :

#### 1. **Première connexion**
```
Commerçant ouvre : http://192.168.43.153:8000/
↓
Clique "Se connecter"
↓
Entre son numéro : +224620123456
↓
Reçoit code OTP par SMS : 654321
↓
Entre le code
↓
Redirigé automatiquement vers : /commercant/dashboard/
```

#### 2. **Sur le dashboard**
**Affichage mobile-friendly** :
- En haut : Son solde portefeuille (gros chiffre)
- 4 boutons d'action rapide
- Liste de ses participations avec jauges
- Ses statistiques

#### 3. **Participer à un conteneur**
```
Dashboard → Bouton "Participer" (🤝)
↓
Liste des conteneurs disponibles
↓
Clique sur "CHINE-GUINEE"
↓
Voit les détails + bouton "Je participe"
↓
Formulaire :
  - Montant : 5 000 000 GNF
  - Référence Orange Money : OM123456
  - Upload preuve : photo_recu.jpg
↓
Submit
↓
Retour au dashboard avec message :
  "⏳ Votre participation est en attente de validation"
```

#### 4. **Après validation par l'admin**
```
Dashboard commerçant se met à jour :
  - Statut passe de "⏳ En attente" à "✓ Validé"
  - La jauge du conteneur se remplit
  - Son investissement total augmente
```

---

## 🔒 SÉCURITÉ

### Protections implémentées :

1. **Décorateur `@login_required`**
   - Toutes les pages commerçant nécessitent connexion
   - Redirection automatique vers `/login/` si non connecté

2. **Vérification du rôle**
   ```python
   if user.is_staff or user.is_superuser:
       return redirect('/admin-panel/')
   ```
   - Empêche les admins d'accéder aux pages commerçant
   - Empêche les commerçants d'accéder aux pages admin

3. **Filtrage des données**
   ```python
   # Commerçant voit UNIQUEMENT ses participations
   participations = Participation.objects.filter(utilisateur=user)
   
   # Admin voit TOUT
   participations = Participation.objects.all()
   ```

4. **Décorateur `@staff_member_required`**
   - Dashboard admin accessible UNIQUEMENT aux staff
   - Retourne 403 Forbidden si commerçant essaie d'accéder

---

## 🧪 TESTS À EFFECTUER

### Test 1 : Créer un commerçant
```bash
# Via shell Django
python manage.py shell
>>> from core.models import Utilisateur
>>> u = Utilisateur.objects.create_user(
...     telephone='+224620999999',
...     username='commercant1'
... )
>>> u.is_staff = False
>>> u.is_phone_verified = True
>>> u.save()
>>> print(f"Commerçant créé : {u.telephone}")
```

### Test 2 : Se connecter comme commerçant
1. Aller sur : http://127.0.0.1:8000/login/
2. Téléphone : +224620999999
3. Code OTP : (celui affiché en console)
4. Vérifier redirection vers `/commercant/dashboard/`

### Test 3 : Tenter d'accéder à l'admin
1. Connecté comme commerçant
2. Essayer d'aller sur : http://127.0.0.1:8000/admin/
3. **Attendu** : Redirection vers login admin ou 403 Forbidden

---

## 📂 FICHIERS CRÉÉS

1. **`templates/commercant_dashboard.html`** (381 lignes)
   - Dashboard principal commerçant
   - Design mobile-first
   - Navigation bottom fixe

2. **`core/commercant_views.py`** (130 lignes)
   - 4 vues : dashboard, participer, historique, profil
   - Redirection automatique des admins
   - Filtrage des données par utilisateur

3. **`core/auth_views.py`** (modifié)
   - Ajout fonction `redirect_after_login()`
   - Redirection selon rôle

4. **`tontine_digitale/urls.py`** (modifié)
   - 4 nouvelles routes commerçant

---

## 🚀 PROCHAINES ÉTAPES

### 1. **Créer les templates manquants** (TODO)
- `commercant_participer.html`
- `commercant_historique.html`
- `commercant_profil.html`

### 2. **Ajouter le formulaire de participation** (TODO)
Dans `commercant_participer.html` :
- Upload photo preuve
- Référence Orange Money
- Montant

### 3. **Tester avec de vrais commerçants**
- Créer 5 comptes commerçants
- Leur demander de tester depuis leur téléphone
- Recueillir les feedbacks

### 4. **Application mobile** (Futur)
- Flutter qui consomme l'API
- Notifications push
- Caméra pour preuves

---

## 💡 CONSEIL IMPORTANT

### Pour le MVP (test initial) :
1. **Créez 2-3 comptes commerçants de test**
2. **Testez le parcours complet** depuis mobile
3. **Vérifiez que :**
   - Ils ne voient PAS les données des autres
   - Ils ne peuvent PAS accéder à l'admin
   - La navigation est fluide
   - Les jauges s'actualisent

### Pour la production :
1. **Activez les SMS réels** (Twilio)
2. **Intégrez Orange Money** pour paiements
3. **Déployez sur un serveur** (accès Internet)
4. **Formez les premiers commerçants** à Madina

---

## ✅ RÉSUMÉ

**Problème** : Les commerçants verraient tout comme l'admin  
**Solution** : 2 interfaces séparées avec permissions différentes  
**Résultat** :
- ✅ Admin voit TOUT et peut TOUT faire
- ✅ Commerçant voit UNIQUEMENT ses données
- ✅ Redirection automatique selon le rôle
- ✅ Dashboard mobile-friendly pour commerçants
- ✅ Sécurité par décorateurs Django

**Prochaine action** : Créer les templates manquants et tester !

---

**Date** : 11 Février 2026 16:00  
**Status** : ✅ Structure créée, templates à compléter  
**Documentation** : `INTERFACE_COMMERCANT.md`
