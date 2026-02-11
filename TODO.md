# 📝 TODO - PROCHAINES ÉTAPES

**Dernière mise à jour** : 11 Février 2026  
**État actuel** : ✅ Prêt pour production  

---

## 🚀 URGENT (À faire MAINTENANT)

### 1. Déployer sur Railway ou Render
- [ ] Créer compte Railway/Render
- [ ] Pousser code sur GitHub
- [ ] Connecter repo à Railway/Render
- [ ] Ajouter PostgreSQL
- [ ] Configurer variables d'environnement
- [ ] Tester en production

**Temps estimé** : 30 minutes  
**Guide** : `DEPLOIEMENT.md`

---

### 2. Créer les Données Initiales en Production
- [ ] Exécuter migrations (`python manage.py migrate`)
- [ ] Créer superutilisateur admin
- [ ] Ajouter taux de change (USD, EUR, CNY)
- [ ] Créer 2-3 conteneurs actifs
- [ ] Tester avec 5 commerçants réels

**Temps estimé** : 1 heure

---

## 🔴 HAUTE PRIORITÉ (Cette semaine)

### 3. Tests Utilisateurs Réels
- [ ] Inviter 5-10 commerçants de confiance
- [ ] Les faire tester le processus complet :
  - Connexion OTP
  - Participer à un conteneur
  - Upload preuve de paiement
  - Voir leur historique
- [ ] Collecter feedback (UX, bugs, suggestions)

**Temps estimé** : 2-3 heures (+ temps utilisateurs)

---

### 4. Corriger les Bugs Identifiés
- [ ] Problèmes de navigation (si détectés)
- [ ] Erreurs de calcul (si détectées)
- [ ] Problèmes d'upload (si détectés)
- [ ] Redirection incorrecte (si détectée)

**Temps estimé** : Variable selon bugs

---

### 5. Configurer le Stockage Media Externe
**Problème** : Railway/Render effacent les fichiers uploadés à chaque redéploiement.

**Solution** : Utiliser Cloudinary ou AWS S3

- [ ] Créer compte Cloudinary (gratuit 25GB)
- [ ] Installer `django-cloudinary-storage`
- [ ] Configurer `MEDIA_URL` et `DEFAULT_FILE_STORAGE`
- [ ] Tester upload de preuve en production

**Temps estimé** : 1 heure  
**Guide** : À créer ou voir doc Django Cloudinary

---

## 🟡 MOYENNE PRIORITÉ (2 semaines)

### 6. Intégration SMS Réel
**Actuellement** : OTP en mode debug (affiché dans la réponse)

**À faire** :
- [ ] Choisir provider SMS (ex: Twilio, Africa's Talking)
- [ ] Créer compte et obtenir API keys
- [ ] Configurer `SMS_PROVIDER`, `SMS_API_KEY`, `SMS_API_SECRET`
- [ ] Tester envoi SMS réel en Guinée
- [ ] Désactiver mode debug (`SMS_PROVIDER=twilio`)

**Coût estimé** : 0.05-0.10 USD par SMS  
**Temps estimé** : 2 heures

---

### 7. Notifications Email
- [ ] Configurer SendGrid ou Mailgun
- [ ] Email de bienvenue à l'inscription
- [ ] Email quand participation validée
- [ ] Email quand conteneur plein (expédition)
- [ ] Email quand conteneur arrive au port

**Temps estimé** : 3 heures

---

### 8. Export PDF des Reçus
- [ ] Installer `reportlab` ou `weasyprint`
- [ ] Créer template PDF pour reçu de participation
- [ ] Bouton "Télécharger reçu PDF" dans historique commerçant
- [ ] Admin peut exporter facture complète du conteneur

**Temps estimé** : 4 heures

---

### 9. Graphiques & Dashboard Améliorés
- [ ] Intégrer Chart.js ou ApexCharts
- [ ] Graphique d'évolution du conteneur (temps réel)
- [ ] Graphique participations par jour
- [ ] Graphique répartition par catégorie
- [ ] Graphique marge plateforme (admin only)

**Temps estimé** : 3 heures

---

## 🟢 BASSE PRIORITÉ (1 mois)

### 10. Application Mobile (Flutter)
- [ ] Setup projet Flutter
- [ ] Design UI/UX (Figma)
- [ ] Écrans :
  - Login OTP
  - Dashboard commerçant
  - Liste conteneurs
  - Participer (avec photo)
  - Historique
  - Profil
- [ ] Intégration API Django
- [ ] Notifications push (Firebase)
- [ ] Tests iOS & Android
- [ ] Publication Play Store / App Store

**Temps estimé** : 40-60 heures (2-3 semaines)

---

### 11. Intégration Orange Money API
**Actuellement** : Upload manuel de preuve de paiement

**À faire** :
- [ ] Obtenir accès Orange Money API (Guinée)
- [ ] Implémenter paiement direct depuis l'app
- [ ] Validation automatique des paiements
- [ ] Plus besoin d'upload manuel

**Temps estimé** : 1 semaine (dépend de Orange)  
**Coût** : Frais Orange Money (~2-3%)

---

### 12. Suivi GPS des Conteneurs
- [ ] Intégrer API de suivi (ex: Marine Traffic)
- [ ] Afficher position du conteneur en temps réel
- [ ] Notifications :
  - Départ de Chine
  - Arrivée au port de Conakry
  - Dédouanement terminé
- [ ] Photos à chaque étape

**Temps estimé** : 1 semaine

---

### 13. Système de Rating Fournisseurs
- [ ] Commerçants peuvent noter leurs fournisseurs (1-5 étoiles)
- [ ] Commentaires (optionnel)
- [ ] Note moyenne affichée dans le catalogue
- [ ] Anti-manipulation (1 note par commande validée)

**Temps estimé** : 2 jours

---

### 14. Programme de Fidélité
- [ ] Points de fidélité (1 point = 1000 GNF investi)
- [ ] Récompenses :
  - 10 000 points = 100 000 GNF de réduction
  - 50 000 points = Livraison gratuite
  - 100 000 points = 1 CBM offert
- [ ] Dashboard points de fidélité

**Temps estimé** : 3 jours

---

### 15. Assurance Marchandise Intégrée
- [ ] Partenariat avec compagnie d'assurance
- [ ] Option assurance à 2-3% du total
- [ ] Indemnisation automatique si perte/dommage
- [ ] Processus de déclaration en ligne

**Temps estimé** : Dépend des négociations

---

### 16. Expansion Géographique
- [ ] Sénégal (Dakar)
- [ ] Mali (Bamako)
- [ ] Côte d'Ivoire (Abidjan)
- [ ] Adapter les tarifs par pays
- [ ] Trouver partenaires transitaires locaux

**Temps estimé** : Variable par pays

---

## 🛠️ AMÉLIORATIONS TECHNIQUES

### 17. Performance & Optimisation
- [ ] Ajouter cache Redis (sessions, API)
- [ ] Optimiser queries DB (select_related, prefetch_related)
- [ ] Compresser images uploadées automatiquement
- [ ] Lazy loading des images
- [ ] Minifier CSS/JS

**Temps estimé** : 2 jours

---

### 18. Monitoring & Alertes
- [ ] Configurer Sentry (suivi des erreurs)
- [ ] Alertes Slack/Email si erreur critique
- [ ] Dashboard métriques (New Relic ou similaire)
- [ ] Logs centralisés (Papertrail)

**Temps estimé** : 1 jour

---

### 19. Tests Automatisés
- [ ] Tests unitaires (modèles, calculs)
- [ ] Tests d'intégration (API)
- [ ] Tests end-to-end (Selenium)
- [ ] CI/CD avec GitHub Actions
- [ ] Coverage > 80%

**Temps estimé** : 1 semaine

---

### 20. Documentation API
- [ ] Swagger/OpenAPI documentation
- [ ] Exemples de requêtes (curl, Python, JS)
- [ ] Guide d'intégration pour développeurs tiers
- [ ] Postman collection

**Temps estimé** : 2 jours

---

## 💼 BUSINESS & MARKETING

### 21. Site Web Vitrine
- [ ] Landing page professionnelle
- [ ] Présentation du service
- [ ] Témoignages clients
- [ ] FAQ
- [ ] Formulaire de contact
- [ ] SEO optimisé

**Temps estimé** : 1 semaine

---

### 22. Marketing Digital
- [ ] Campagne Facebook Ads (ciblage Madina)
- [ ] WhatsApp Business (support client)
- [ ] Groupe WhatsApp commerçants VIP
- [ ] Vidéos explicatives (TikTok, YouTube)
- [ ] Partenariats influenceurs locaux

**Temps estimé** : Continu

---

### 23. Programme de Parrainage
- [ ] "Parraine un ami, gagne 10 000 GNF"
- [ ] Code promo personnalisé
- [ ] Tracking des parrainages
- [ ] Paiement automatique des bonus

**Temps estimé** : 2 jours

---

## 📊 PRIORISATION RECOMMANDÉE

### Semaine 1
1. ✅ Déploiement production (URGENT)
2. ✅ Données initiales (URGENT)
3. ✅ Tests utilisateurs réels (HAUTE)

### Semaine 2
4. ✅ Stockage media externe (HAUTE)
5. ✅ Corrections bugs identifiés (HAUTE)
6. ⏳ Intégration SMS réel (MOYENNE)

### Semaine 3-4
7. ⏳ Notifications email (MOYENNE)
8. ⏳ Export PDF reçus (MOYENNE)
9. ⏳ Graphiques dashboard (MOYENNE)

### Mois 2
10. ⏳ Application mobile (BASSE)
11. ⏳ Orange Money API (BASSE)

### Mois 3+
12. ⏳ Suivi GPS (BASSE)
13. ⏳ Rating fournisseurs (BASSE)
14. ⏳ Programme fidélité (BASSE)
15. ⏳ Expansion géographique (BASSE)

---

## 📝 NOTES

### Critères de Priorisation

**URGENT** : Bloquant pour le lancement  
**HAUTE** : Nécessaire pour une bonne expérience utilisateur  
**MOYENNE** : Améliore significativement la plateforme  
**BASSE** : Nice to have, peut attendre

---

### Estimation Temps Total

- **Urgent + Haute** : 10-15 heures
- **Moyenne** : 15-20 heures
- **Basse** : 100+ heures

**Recommandation** : Focus sur Urgent + Haute les 2 premières semaines, puis itérer selon feedback utilisateurs.

---

**Date** : 11 Février 2026  
**Statut actuel** : ✅ Prêt pour déploiement  
**Prochaine action** : Déployer sur Railway/Render
