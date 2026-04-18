# Guide Make.com — Automatisation Twitter/X WULIX
## Rédigé par MARIAMA (Comms) — WULIX

---

## MÉTHODE A — 8 scénarios individuels Make.com

### Étape 1 — Créer un compte / se connecter à Make.com
1. Va sur **make.com** → connecte-toi avec ton compte WULIX
2. Tableau de bord → **"Create a new scenario"**

### Étape 2 — Ajouter le module Twitter
1. Clique sur le **"+"** pour ajouter un module
2. Recherche **"Twitter"** ou **"X"**
3. Sélectionne **"Create a Tweet"**
4. Connecte ton compte Twitter WULIX via OAuth

### Étape 3 — Configurer le contenu
Dans le champ **"Text"**, colle le contenu du tweet correspondant (voir section Tweets ci-dessous)

### Étape 4 — Ajouter le déclencheur horaire
1. Clique sur l'horloge (trigger) en début de scénario
2. Sélectionne **"Schedule"** → **"At a specific time"**
3. Configure la date et l'heure selon le calendrier ci-dessous

### Étape 5 — Activer le scénario
1. Clique **"Save"**
2. Active le toggle **ON**
3. Teste avec **"Run once"** en mode test

---

## CALENDRIER DES 8 SCÉNARIOS

| # | Post | Semaine | Jour | Heure | Type |
|---|------|---------|------|-------|------|
| 1 | POST 7 | S2 | Lundi | 8h30 | Engagement |
| 2 | POST 1 | S2 | Mercredi | 8h30 | Éducatif |
| 3 | POST 3 | S2 | Vendredi | 18h00 | Social Proof |
| 4 | POST 2 | S3 | Mardi | 8h30 | Éducatif |
| 5 | POST 5 | S3 | Samedi | 10h00 | Produit 29€ |
| 6 | POST 4 | S4 | Jeudi | 18h00 | Social Proof |
| 7 | POST 6 | S4 | Samedi | 10h00 | Produit 19€ |
| 8 | POST 8 | S5 | Lundi | 8h30 | Backstory |

---

## TWEETS — CONTENU COMPLET À COPIER-COLLER

### POST 7 — Engagement (S2 Lundi 8h30)
```
Honnêtement —

Quelle tâche dans ton business tu DÉTESTES faire mais tu fais quand même à la main chaque semaine ?

(Spoiler : y'a sûrement un script Python ou un workflow n8n pour ça)

Dis-moi en commentaire 👇

#AutomatisationIA #Python #Freelance #PME #WULIX
```

### POST 1 — Éducatif (S2 Mercredi 8h30)
```
Tu veux automatiser tes tâches avec Python ?

Commence par ça :

1. requests → récupère des données de n'importe quel site
2. schedule → lance ton script tous les jours à 8h
3. smtplib → envoie un email automatiquement

3 lignes de code. Aucun outil payant.

On fait ça pour toi → wulix.fr

#Python #AutomatisationIA #TipDuJour #WULIX
```

### POST 3 — Social Proof (S2 Vendredi 18h00)
```
Client livré cette semaine ✅

Une consultante passait 2h/jour à copier des données entre Excel et son CRM.

Agent Python livré en 48h.
Résultat : 10 secondes au lieu de 2h.

C'est ça l'automatisation concrète.

→ wulix.fr | dès 50€

#AutomatisationIA #Python #PME #WULIX
```

### POST 2 — Éducatif (S3 Mardi 8h30)
```
n8n + IA = combo imbattable pour les freelances.

Exemple concret :
→ Un formulaire client arrive
→ n8n le lit, classe la demande
→ L'IA rédige une réponse personnalisée
→ L'email part tout seul

Zéro copier-coller. Zéro oubli.

Template clé en main dispo → wulix.fr

#n8n #WorkflowAutomation #IA #Freelance #WULIX
```

### POST 5 — Produit 29€ (S3 Samedi 10h00)
```
🛒 NOUVEAU sur Gumroad

Pack "Automatise ton business" — 29€

5 scripts Python prêts à l'emploi :
✅ Scraper de données
✅ Auto-poster LinkedIn
✅ Relance email automatique
✅ Générateur de rapports PDF
✅ Veille concurrentielle

Plug & play. Commenté en français.

👉 wulix.gumroad.com/l/scripts-python

#Python #Gumroad #AutomatisationIA #Freelance
```

### POST 4 — Social Proof (S4 Jeudi 18h00)
```
Ce qu'un client nous a dit après livraison :

"Je savais pas que c'était possible en si peu de temps."

Un script Python.
72h de délai.
5h/semaine récupérées.

Si t'as une tâche répétitive qui t'énerve — on la règle.

DM ou wulix.fr 👇

#AgentIA #Python #Résultats #WULIX
```

### POST 6 — Produit 19€ (S4 Samedi 10h00)
```
Tu utilises n8n ?

Notre template "Pipeline LinkedIn automatisé" — 19€

→ Lit tes posts depuis un fichier txt
→ Publie automatiquement chaque semaine
→ API LinkedIn officielle
→ Import en 2 clics

Aucun code requis.

👉 wulix.gumroad.com/l/n8n-linkedin

#n8n #NoCode #AutomatisationIA #Gumroad #WULIX
```

### POST 8 — Backstory (S5 Lundi 8h30)
```
WULIX vient du mot mandé "Wuli" — s'éveiller, se lever.

On a choisi ce nom parce que l'IA ne remplace pas les humains.

Elle les réveille.

Elle libère du temps pour ce qui compte vraiment : créer, vendre, grandir.

Solutions IA accessibles dès 50€.

→ wulix.fr

#IA #Automatisation #WULIX #AgenceIA #France
```

---

## MÉTHODE B — Alternative Google Sheets (1 scénario unique)

### Setup Google Sheets
Crée un Google Sheet avec ces colonnes :
| Date | Heure | Statut | Contenu |
|------|-------|--------|---------|
| 2026-04-27 | 08:30 | pending | [tweet POST 7] |
| 2026-04-29 | 08:30 | pending | [tweet POST 1] |
| ... | ... | ... | ... |

### Scénario Make.com
1. **Trigger** : Schedule → toutes les heures
2. **Module 1** : Google Sheets → Search Rows (filtre : Date = today, Heure = now, Statut = pending)
3. **Module 2** : Twitter → Create a Tweet (Text = colonne Contenu)
4. **Module 3** : Google Sheets → Update Row (Statut = posted)

**Avantage** : 1 seul scénario pour tous les posts, facile à modifier

---

## CHECKLIST DE VÉRIFICATION

### Avant activation
- [ ] Compte Twitter WULIX connecté à Make.com via OAuth
- [ ] Accès API Twitter vérifié (compte Developer si nécessaire)
- [ ] Contenu de chaque tweet vérifié (280 caractères max)
- [ ] Dates et heures configurées correctement

### Test
- [ ] Lancer "Run once" sur un scénario test
- [ ] Vérifier que le tweet apparaît sur le profil Twitter WULIX
- [ ] Supprimer le tweet test

### Après activation
- [ ] Tous les scénarios activés (toggle ON)
- [ ] Notifications d'erreur Make.com activées
- [ ] Vérifier le crédit Make.com disponible (1000 opérations/mois sur plan gratuit)

### Gestion erreurs API Twitter
- Si erreur 403 : vérifier les permissions de l'app Twitter (Read + Write)
- Si erreur 429 : limite de taux atteinte, espacer les posts de 15 min minimum
- Si erreur 401 : reconnecter le compte OAuth dans Make.com

---

## COMPARATIF LINKEDIN vs TWITTER sur Make.com

| | LinkedIn | Twitter/X |
|--|---------|-----------|
| Module | "Create a Company Text Post" | "Create a Tweet" |
| Auth | OAuth via WULIX LinkedIn | OAuth via @WULIX |
| Cible | Page entreprise | Compte personnel/marque |
| Scénario actif | ✅ Lundi 9h | ⏳ À configurer |
| Fréquence | 1x/semaine | 2-3x/semaine |

---

*MARIAMA — Agent Communications WULIX | 18 avril 2026 | contact@wulix.fr*
