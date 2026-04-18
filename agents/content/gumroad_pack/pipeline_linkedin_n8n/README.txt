WULIX — Pipeline LinkedIn Automatise
=====================================
Template n8n v1.0 | wulix.fr | contact@wulix.fr

CONTENU DU PACK :
  WULIX_Pipeline_LinkedIn.json   -> Workflow n8n a importer
  README.txt                     -> Ce fichier (guide d'installation)

PREREQUIS :
  - n8n installe (cloud : app.n8n.cloud / self-hosted : n8n.io)
  - Compte LinkedIn avec acces Developer
  - Google Sheets avec les colonnes : ligne_id | statut | texte | hashtags | date_publication

INSTALLATION EN 5 ETAPES :

1. IMPORTER LE WORKFLOW
   - Ouvrir n8n > Workflows > Import from file
   - Selectionner WULIX_Pipeline_LinkedIn.json

2. CONFIGURER GOOGLE SHEETS
   - Creer un Google Sheet avec l'onglet "Posts"
   - Colonnes : ligne_id | statut | texte | hashtags | date_publication
   - Dans n8n : ajouter des credentials Google Sheets (OAuth2)
   - Remplacer TON_GOOGLE_SHEET_ID par l'ID de ton fichier (dans l'URL)

3. CONFIGURER LINKEDIN
   - Aller sur : https://www.linkedin.com/developers/apps
   - Creer une app > Activer "Share on LinkedIn" + "Sign In with LinkedIn"
   - Dans n8n : Credentials > LinkedIn OAuth2 > Autoriser

4. AJOUTER TES POSTS dans Google Sheets :
   - statut : a_publier
   - texte  : Le contenu de ton post
   - hashtags : #automatisation #IA #freelance

5. ACTIVER LE WORKFLOW
   - Cliquer sur le toggle "Active" dans n8n
   - Le workflow se declenchera chaque lundi a 9h00

PERSONNALISATION :
  - Changer la frequence : modifier le noeud "Planification hebdomadaire"
  - Publier plusieurs fois par semaine : dupliquer le workflow
  - Ajouter une image : modifier le noeud "Publier sur LinkedIn" (champ mediaUrn)

SUPPORT : contact@wulix.fr | wulix.fr
LICENCE  : Usage personnel uniquement. Redistribution interdite.
(c) 2026 WULIX — Art. L.335-2 CPI
