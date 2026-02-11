# 📁 Structure du Projet Tontine Digitale (Dernière Mise à Jour - 10/02/2026)

```
Django/
│
├── 📂 .venv/                          # Environnement virtuel Python
│   └── Django 5.2.11 + DRF 3.16.1 + JWT + Pillow + openpyxl + Chart.js
│
├── 📂 media/                          # 📸 Fichiers uploadés par les utilisateurs
│   └── preuves_paiement/             # Captures d'écran Orange Money
│
├── 📂 templates/                      # 🎨 Templates HTML
│   ├── home.html                     # Page d'accueil
│   ├── dashboard.html                # Dashboard avec graphiques Chart.js
│   ├── 📂 api/
│   │   ├── base_v2.html             # Template de base (mode sombre, recherche, filtres)
│   │   ├── conteneurs.html          # Liste conteneurs + filtres
│   │   ├── conteneur_detail.html    # Détail d'un conteneur
│   │   ├── participations.html      # Liste participations + filtres
│   │   ├── portefeuilles.html       # Liste portefeuilles
│   │   ├── transactions.html        # Liste transactions + filtres
│   │   └── taux_change.html         # Taux de change
│   └── 📂 auth/
│       ├── login.html               # ⭐ Connexion OTP (2 étapes) - NOUVEAU
│       └── admin_panel.html         # ⭐ Panneau admin personnalisé - NOUVEAU
│
├── 📄 manage.py                       # 🎯 Centre de commande Django
├── 📄 db.sqlite3                      # 🗄️ Base de données SQLite
├── 📄 .gitignore                      # Fichiers ignorés par Git
├── 📄 STRUCTURE.md                    # 📖 Ce fichier
├── 📄 TODO.md                         # ⭐ Liste complète des tâches - NOUVEAU
│
├── 📂 tontine_digitale/               # ⚙️ Configuration globale
│   ├── settings.py                    # 🔧 Paramètres
│   │   ├── AUTH_USER_MODEL: 'core.Utilisateur'
│   │   ├── MEDIA_ROOT & MEDIA_URL (preuves de paiement)
│   │   ├── REST_FRAMEWORK: JWT Authentication
│   │   ├── LANGUAGE_CODE: 'fr-fr'
│   │   └── TIME_ZONE: 'Africa/Dakar'
│   │
│   ├── urls.py                        # 🛣️ Routes principales
│   │   ├── /                → home
│   │   ├── /login/          → Connexion OTP ⭐ NOUVEAU
│   │   ├── /admin/          → Interface Django Admin
│   │   ├── /admin-panel/    → Panneau Admin personnalisé ⭐ NOUVEAU
│   │   ├── /dashboard/      → Dashboard graphique
│   │   ├── /api/            → API REST
│   │   └── /media/          → Fichiers uploadés
│   │
│   ├── asgi.py, wsgi.py, __init__.py
│
└── 📂 core/                           # 🧠 Application métier

    ├── 🏗️ models.py (6 modèles)
    │   │
    │   ├── 👤 Utilisateur (AbstractUser)
    │   │   ├── telephone: Numéro unique (USERNAME_FIELD)
    │   │   ├── otp_code: Code à 6 chiffres
    │   │   ├── otp_created_at: Validité 5 minutes
    │   │   ├── is_phone_verified: Statut de vérification
    │   │   ├── generate_otp(): Génère un code OTP
    │   │   └── verify_otp(code): Vérifie le code OTP
    │   │
    │   ├── 💰 Portefeuille
    │   │   ├── utilisateur: Lien 1-to-1 avec Utilisateur
    │   │   ├── solde: Montant en GNF
    │   │   ├── crediter(montant): Ajoute au solde
    │   │   └── debiter(montant): Retire du solde
    │   │
    │   ├── 💱 TauxDeChange
    │   │   ├── devise: USD / CNY / EUR
    │   │   ├── taux_gnf: Conversion vers GNF
    │   │   ├── date_application: Date du taux
    │   │   └── actif: Taux actuellement utilisé
    │   │
    │   ├── 📦 Conteneur
    │   │   ├── nom: Nom du conteneur
    │   │   ├── objectif: Montant cible
    │   │   ├── devise: GNF / USD / CNY
    │   │   ├── montant_actuel: Total collecté (GNF)
    │   │   ├── etape: collecte / mer / port
    │   │   ├── annule: Statut d'annulation
    │   │   ├── get_progression(): % de collecte
    │   │   ├── get_objectif_en_gnf(): Conversion avec taux
    │   │   ├── mettre_a_jour_montant(): MAJ du montant
    │   │   └── annuler_et_rembourser(): Remboursement auto
    │   │
    │   ├── 🤝 Participation
    │   │   ├── conteneur: Lien vers Conteneur
    │   │   ├── utilisateur: Lien vers Utilisateur
    │   │   ├── montant: Montant versé (GNF)
    │   │   ├── reference_paiement: Ref Orange Money
    │   │   ├── preuve_paiement: ImageField (capture d'écran)
    │   │   ├── valide: Paiement validé ou non
    │   │   └── date_participation: Date du versement
    │   │
    │   └── 📝 Transaction
    │       ├── portefeuille: Lien vers Portefeuille
    │       ├── type_transaction: depot / retrait / participation / remboursement
    │       ├── montant: Montant de la transaction
    │       ├── conteneur: Lien optionnel vers Conteneur
    │       ├── description: Détails de la transaction
    │       └── date_transaction: Date de l'opération
    │
    ├── 🎛️ admin.py (6 interfaces)
    │   ├── UtilisateurAdmin: Gestion des utilisateurs
    │   ├── PortefeuilleAdmin: Visualisation des soldes
    │   ├── TransactionAdmin: Historique des transactions
    │   ├── TauxDeChangeAdmin: Gestion des taux de change
    │   ├── ConteneurAdmin: 
    │   │   ├── Barre de progression colorée
    │   │   └── Action: Annuler et rembourser
    │   └── ParticipationAdmin:
    │       ├── Affichage des preuves de paiement
    │       └── Action: Valider les paiements sélectionnés
    │
    ├── 📦 serializers.py (8 serializers)
    │   ├── UtilisateurSerializer
    │   ├── OTPRequestSerializer
    │   ├── OTPVerifySerializer
    │   ├── PortefeuilleSerializer
    │   ├── TransactionSerializer
    │   ├── TauxDeChangeSerializer
    │   ├── ParticipationSerializer (avec URL preuve)
    │   └── ConteneurSerializer (avec progression)
    │
    ├── 🔌 views.py (7 ViewSets)
    │   ├── demander_otp(): Génère et envoie OTP
    │   ├── verifier_otp(): Vérifie OTP et retourne JWT
    │   ├── ConteneurViewSet: CRUD + action annuler + HTML rendering
    │   ├── ParticipationViewSet: CRUD (filtrée par user) + HTML
    │   ├── PortefeuilleViewSet: Lecture seule + HTML
    │   ├── TransactionViewSet: Historique + HTML
    │   └── TauxDeChangeViewSet: CRUD + action actifs + HTML
    │
    ├── 📊 dashboard.py ⭐ NOUVEAU
    │   ├── dashboard_view(): Vue principale avec stats et graphiques
    │   ├── export_conteneurs_csv()
    │   ├── export_participations_csv()
    │   ├── export_transactions_csv()
    │   └── export_all_excel(): Export complet (3 feuilles)
    │
    ├── 🔐 auth_views.py ⭐ NOUVEAU
    │   ├── login_view(): Page de connexion OTP
    │   └── admin_dashboard_view(): Panneau admin personnalisé
    │
    ├── 🗺️ urls.py (Routes API)
    │   ├── POST /api/auth/demander-otp/
    │   ├── POST /api/auth/verifier-otp/
    │   ├── GET/POST /api/conteneurs/
    │   ├── GET /api/conteneurs/{id}/
    │   ├── POST /api/conteneurs/{id}/annuler/
    │   ├── GET/POST /api/participations/
    │   ├── GET /api/portefeuilles/
    │   ├── GET /api/transactions/
    │   └── GET /api/taux-change/actifs/
    │
    ├── apps.py, tests.py, __init__.py
    │
    └── 📂 migrations/
        └── 0001_initial.py (6 tables créées)
```

---

## 🌐 URLs Disponibles (Mise à Jour)

### 🔐 Authentification (Sans JWT)
- **POST** `/api/auth/demander-otp/`
  ```json
  { "telephone": "+224620123456" }
  ```
  Retourne: `{ "otp_code": "123456" }` (en mode debug)

- **POST** `/api/auth/verifier-otp/`
  ```json
  { "telephone": "+224620123456", "otp_code": "123456" }
  ```
  Retourne: `{ "access": "token...", "refresh": "token..." }`

### 📱 API REST (Avec JWT Bearer Token)
- **Conteneurs**: `/api/conteneurs/`
- **Participations**: `/api/participations/`
- **Portefeuilles**: `/api/portefeuilles/`
- **Transactions**: `/api/transactions/`
- **Taux de change**: `/api/taux-change/`

### 🎛️ Admin Django
- **URL**: http://127.0.0.1:8000/admin/
- **Téléphone**: `+224620000000`
- **Username**: `admin`
- **Password**: `admin123`

---

## 🚀 Flux d'Utilisation

### 1️⃣ Connexion par OTP (Mobile)
```
1. Utilisateur entre son numéro → POST /api/auth/demander-otp/
2. Code OTP envoyé (SMS simulé)
3. Utilisateur entre le code → POST /api/auth/verifier-otp/
4. Reçoit token JWT + création auto du portefeuille
```

### 2️⃣ Participation à un Conteneur
```
1. GET /api/conteneurs/ → Liste des conteneurs actifs
2. POST /api/participations/
   - montant: 500000 (GNF)
   - reference_paiement: "OM123456789"
   - preuve_paiement: [fichier image]
3. Admin valide dans /admin/ → Portefeuille débité
4. Barre de progression du conteneur mise à jour
```

### 3️⃣ Annulation d'un Conteneur
```
1. Admin clique "Annuler et rembourser" dans /admin/
2. Système crédite automatiquement les portefeuilles
3. Transactions de remboursement créées
4. Utilisateurs peuvent voir l'historique dans /api/transactions/
```

---

## 🔧 Nouveautés Ajoutées

### ✅ 1. Authentification par Téléphone (OTP)
- Code à 6 chiffres généré automatiquement
- Validité de 5 minutes
- Connexion automatique après vérification
- Token JWT pour sécuriser l'API

### ✅ 2. Système de Portefeuille (Wallet)
- Créé automatiquement à la première connexion
- Solde en GNF (Franc Guinéen)
- Méthodes `crediter()` et `debiter()`
- Historique complet via Transaction

### ✅ 3. Gestion des Preuves (Media)
- `MEDIA_ROOT` et `MEDIA_URL` configurés
- Dossier `media/preuves_paiement/` créé
- ImageField dans Participation
- Affichage dans l'admin avec preview

### ✅ 4. Taux de Change (Devises)
- Support USD, CNY, EUR → GNF
- Conteneurs peuvent être en devises étrangères
- Conversion automatique pour la progression
- Admin peut activer/désactiver les taux

### ✅ 5. Système de Remboursement
- Méthode `annuler_et_rembourser()` sur Conteneur
- Crédite automatiquement les portefeuilles
- Crée des transactions de type "remboursement"
- Action admin en un clic

---

## 📊 Base de Données (db.sqlite3)

### Tables créées:
1. **core_utilisateur** (Custom User)
2. **core_portefeuille** (Wallets)
3. **core_transaction** (Historique)
4. **core_tauxdechange** (Devises)
5. **core_conteneur** (Projets)
6. **core_participation** (Versements)

---

## 🎯 Prêt pour Production

### Ce qui est implémenté:
- ✅ Authentification mobile-first (OTP)
- ✅ Gestion financière complète (Portefeuille + Transactions)
- ✅ Upload de fichiers (Preuves de paiement)
- ✅ Multi-devises avec taux de change
- ✅ Remboursement automatique
- ✅ API REST complète avec JWT
- ✅ Interface admin professionnelle

### Ce qui reste à faire:
- 🔄 Intégration SMS réelle (Twilio, Nexmo, etc.)
- 🔄 Frontend mobile (Flutter / React Native)
- 🔄 Paiement Orange Money API
- 🔄 Notifications push
- 🔄 Système de rôles avancés (Admin, Gérant, Commerçant)
