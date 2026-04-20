"""
SAMBA — Agent SEO Continu
Publie 1 article/semaine auto dans blog.html, surveille les positions
"""
import os
import json
import datetime
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
UI_DIR = BASE_DIR.parent / "ui"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] SAMBA | {msg}"
    print(line)
    with open(LOG_DIR / "samba.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

ARTICLE_TOPICS = [
    {
        "title": "Comment automatiser ses relances clients avec Python en 30 minutes",
        "keyword": "automatiser relances clients python",
        "intro": "Vous perdez du temps à relancer manuellement vos clients ? Voici comment Python peut le faire pour vous en 30 minutes de setup.",
        "sections": [
            ("Le problème : les relances manuelles coûtent cher", "Chaque email de relance envoyé manuellement représente 3 à 5 minutes de travail. Multiplié par 20 clients actifs, c'est 1h30 par semaine minimum."),
            ("La solution Python en 3 étapes", "1. Lire votre liste clients depuis un CSV\\n2. Vérifier qui n'a pas payé ou répondu\\n3. Envoyer l'email personnalisé automatiquement"),
            ("Le code complet", "Notre script email_relancer.py du Pack Scripts Python fait exactement ça. Configurez-le une fois, il tourne tout seul."),
            ("Résultat attendu", "Nos clients réduisent leur temps de relance de 90%. Un consultant a récupéré 6h par mois.")
        ]
    },
    {
        "title": "n8n vs Make.com : lequel choisir pour automatiser votre business ?",
        "keyword": "n8n vs make.com automatisation",
        "intro": "Deux outils d'automatisation no-code dominent le marché. Voici une comparaison honnête pour choisir celui qui vous convient.",
        "sections": [
            ("n8n : open-source et puissant", "n8n s'installe sur votre propre serveur. Zéro coût récurrent, données chez vous, personnalisation totale."),
            ("Make.com : simple et rapide", "Make.com est cloud, plus intuitif pour les débutants. Idéal pour démarrer sans serveur."),
            ("Notre recommandation", "TPE avec budget limité et données sensibles → n8n. Indépendant qui veut aller vite → Make.com."),
            ("Et WULIX dans tout ça ?", "On maîtrise les deux. On vous aide à choisir et configurer selon votre situation réelle.")
        ]
    },
    {
        "title": "5 tâches que vous pouvez automatiser ce week-end (sans coder)",
        "keyword": "automatisation sans code débutant",
        "intro": "Vous pensez que l'automatisation c'est réservé aux développeurs ? Ces 5 exemples prouvent le contraire.",
        "sections": [
            ("1. Sauvegarder vos fichiers automatiquement", "Google Drive + Make.com : chaque nouveau fichier dans un dossier est automatiquement sauvegardé. Setup : 10 min."),
            ("2. Répondre aux formulaires de contact", "Un formulaire reçu → email de confirmation envoyé → notification Slack. Zéro code, 15 min."),
            ("3. Planifier vos posts LinkedIn", "Google Sheets + n8n → LinkedIn. Remplissez la feuille le dimanche, les posts partent toute la semaine."),
            ("4. Facturer automatiquement", "Stripe + n8n → PDF facture généré et envoyé dès qu'un paiement arrive."),
            ("5. Veille concurrentielle", "Notre script surveille les prix de vos concurrents et vous envoie un email si ça change.")
        ]
    },
    {
        "title": "Comment générer un rapport PDF automatiquement avec Python",
        "keyword": "générer rapport PDF python automatique",
        "intro": "Chaque semaine vous passez du temps à créer le même rapport ? Un script Python peut le générer en 10 secondes chrono.",
        "sections": [
            ("Pourquoi automatiser vos rapports ?", "Un rapport hebdo prend en moyenne 45 minutes à préparer. Avec Python + fpdf2, ce même rapport est généré automatiquement et envoyé par email chaque lundi matin."),
            ("Les outils nécessaires", "fpdf2 pour la génération PDF, smtplib pour l'envoi email, pandas pour lire vos données CSV ou Excel. Tout est gratuit et open-source."),
            ("Structure en 3 étapes", "1. Lire les données source (CSV, Google Sheets, base de données)\\n2. Générer le PDF avec mise en page professionnelle\\n3. Envoyer automatiquement par email à votre liste"),
            ("Ce que ça change concrètement", "Un de nos clients freelance a automatisé son rapport mensuel client. Résultat : 6h récupérées par mois, zéro oubli, image plus professionnelle.")
        ]
    },
    {
        "title": "Automatiser sa veille concurrentielle avec Python en 2026",
        "keyword": "veille concurrentielle automatique python",
        "intro": "Surveiller les prix, les offres et les actualités de vos concurrents manuellement est chronophage. Voici comment l'automatiser.",
        "sections": [
            ("Le coût réel de la veille manuelle", "Vérifier 5 concurrents 3 fois par semaine = 2h perdues. Sur un an, c'est plus de 100h de travail non facturable."),
            ("La solution : un agent Python de veille", "Un script scrape les pages cibles, détecte les changements de prix ou de contenu, et vous envoie une alerte email instantanément."),
            ("Ce qu'on peut surveiller automatiquement", "Prix produits, nouvelles offres de services, changements de pages web, nouvelles publications LinkedIn ou blog, avis clients."),
            ("Notre offre", "Le Pack Scripts Python WULIX inclut un script de veille concurrentielle configurable en 15 minutes. Disponible sur wulix.gumroad.com.")
        ]
    },
    {
        "title": "Créer un agent IA de support client avec Python et Gmail",
        "keyword": "agent IA support client python gmail",
        "intro": "Répondre aux mêmes questions clients encore et encore ? Un agent Python connecté à Gmail peut traiter 80% de vos demandes automatiquement.",
        "sections": [
            ("Le problème du support répétitif", "Dans la plupart des petites entreprises, 80% des emails reçus concernent les mêmes 5-10 questions. Remboursement, délais, accès produit, aide technique..."),
            ("Architecture de l'agent", "1. Connexion IMAP Gmail pour lire les emails entrants\\n2. Classification par mots-clés\\n3. Réponse automatique personnalisée\\n4. Escalade vers vous si non reconnu"),
            ("Ce que ça change", "Réponse en moins de 5 minutes 24h/24, satisfaction client améliorée, votre temps libéré pour les vraies missions."),
            ("Disponible chez WULIX", "C'est exactement ce que fait notre agent LAMINE, disponible à la configuration dans nos missions sur mesure. Contactez-nous sur wulix.fr.")
        ]
    },
    {
        "title": "Comment automatiser sa facturation avec Python et Stripe",
        "keyword": "automatiser facturation python stripe",
        "intro": "Générer et envoyer vos factures manuellement chaque mois ? Un script Python connecté à Stripe peut le faire en 10 secondes à chaque paiement.",
        "sections": [
            ("Le coût caché de la facturation manuelle", "Un freelance passe en moyenne 2h par mois sur sa facturation. Sur un an : 24h perdues, soit 3 jours de travail non facturé."),
            ("Le setup en 3 étapes", "1. Stripe webhook déclenche le script à chaque paiement\\n2. Python génère le PDF facture avec fpdf2\\n3. smtplib envoie la facture au client automatiquement"),
            ("Ce que ça change", "Facturation instantanée, zéro oubli, image professionnelle. Votre comptable reçoit aussi une copie automatiquement."),
            ("Notre solution clé en main", "Le Pack Scripts Python WULIX inclut ce script de facturation automatique. Configurable en 20 minutes. Disponible sur wulix.gumroad.com.")
        ]
    },
    {
        "title": "Publier automatiquement sur LinkedIn avec n8n : le guide complet",
        "keyword": "publier automatiquement linkedin n8n",
        "intro": "Publier sur LinkedIn chaque semaine prend du temps. Avec n8n et l'API LinkedIn, vous programmez vos posts une fois et ils partent tout seuls.",
        "sections": [
            ("Pourquoi automatiser LinkedIn ?", "La régularité est la clé sur LinkedIn. Les comptes qui publient 3x/semaine ont 5x plus de visibilité. Mais rédiger et publier manuellement prend 1h+ par semaine."),
            ("Le workflow n8n en 4 noeuds", "1. Schedule Trigger (lundi 9h)\\n2. Read Binary File (lit posts.txt)\\n3. HTTP Request (API LinkedIn ugcPosts)\\n4. Slack/email notification de confirmation"),
            ("Les pré-requis", "Compte LinkedIn, token OAuth valide (90 jours), fichier de posts prêts, n8n self-hosted ou cloud. Setup complet : 45 minutes."),
            ("Notre pipeline prêt à l'emploi", "Le Pipeline LinkedIn Automatisé WULIX inclut le workflow n8n JSON + guide de configuration. 19€ sur wulix.gumroad.com/l/n8n-linkedin.")
        ]
    },
    {
        "title": "Scraping web avec Python en 2026 : les meilleures pratiques",
        "keyword": "scraping web python 2026",
        "intro": "Collecter des données web manuellement est chronophage. Python + requests + BeautifulSoup permettent d'automatiser cette collecte en quelques lignes.",
        "sections": [
            ("Pourquoi scraper en 2026 ?", "Veille tarifaire, collecte de leads, surveillance de concurrents, agrégation de données marché — le scraping est devenu indispensable pour les PME qui veulent des données fraîches sans abonnement coûteux."),
            ("Les outils recommandés", "requests + BeautifulSoup pour les sites statiques. Playwright pour les sites JavaScript. pandas pour traiter les données. schedule pour automatiser les runs."),
            ("Bonnes pratiques légales", "Respectez le fichier robots.txt, ajoutez des délais entre requêtes, ne scrapez pas de données personnelles sans consentement, vérifiez les CGU du site cible."),
            ("Notre script de veille", "Le Pack Scripts Python WULIX inclut web_scraper.py : surveillance de prix + alertes email configurables. Disponible sur wulix.gumroad.com.")
        ]
    },
    {
        "title": "Automatiser son onboarding client avec des emails Python",
        "keyword": "automatiser onboarding client email python",
        "intro": "Un bon onboarding client augmente la satisfaction et réduit les demandes de support. Voici comment l'automatiser entièrement avec Python.",
        "sections": [
            ("Pourquoi l'onboarding est crucial", "70% des clients qui churent le font dans les 90 premiers jours. Un onboarding structuré et automatisé réduit ce chiffre de moitié selon les études SaaS."),
            ("La séquence en 5 emails", "J+0 : email de bienvenue + accès\\nJ+3 : premiers pas + ressources\\nJ+7 : check-in satisfaction\\nJ+14 : upsell doux\\nJ+30 : témoignage ou renouvellement"),
            ("Le code Python", "smtplib + schedule + CSV clients. Le script lit votre liste, calcule les jours depuis l'inscription, et envoie l'email correspondant. 50 lignes de code maximum."),
            ("Résultat attendu", "Nos clients qui ont mis en place cette séquence ont réduit leurs demandes de support de 40% et augmenté leur taux de renouvellement de 25%.")
        ]
    },
    {
        "title": "ChatGPT vs Claude vs Gemini : lequel pour automatiser votre business ?",
        "keyword": "chatgpt vs claude vs gemini automatisation business",
        "intro": "Trois IA dominent le marché en 2026. Laquelle choisir pour automatiser vos tâches business ? Comparaison honnête basée sur nos tests.",
        "sections": [
            ("ChatGPT (GPT-4o) : le plus polyvalent", "Meilleur pour : rédaction, analyse, code. API bien documentée. Prix : 0,005$/1k tokens. Idéal pour les automatisations générales et le traitement de texte en volume."),
            ("Claude (Anthropic) : le plus précis", "Meilleur pour : analyse de documents longs, code complexe, instructions précises. Fenêtre de contexte 200k tokens. Idéal pour les tâches qui demandent nuance et rigueur."),
            ("Gemini (Google) : le plus intégré", "Meilleur pour : intégration Google Workspace, analyse d'images, recherche web en temps réel. Idéal si votre stack est déjà Google (Sheets, Drive, Gmail)."),
            ("Notre recommandation WULIX", "Pour 90% des cas business : commencez avec l'API Gemini (gratuit jusqu'à 60 req/min) pour tester, puis migrez vers Claude ou GPT-4o selon vos besoins spécifiques.")
        ]
    },
    {
        "title": "Créer un tableau de bord business automatique avec Python",
        "keyword": "tableau de bord business automatique python",
        "intro": "Avoir une vision en temps réel de votre business sans ouvrir 5 onglets différents — c'est possible avec Python et quelques APIs.",
        "sections": [
            ("Les données à centraliser", "Ventes Gumroad/Stripe, trafic site (Google Analytics), engagement LinkedIn, emails entrants, revenus vs objectifs. Tout ça dans un seul email quotidien ou dashboard web."),
            ("Le stack technique", "Python + requests pour collecter les APIs, pandas pour agréger, matplotlib pour les graphiques, fpdf2 pour le rapport PDF, smtplib pour l'envoi automatique chaque matin."),
            ("Setup en 1 weekend", "Jour 1 : connecter les APIs et collecter les données. Jour 2 : mettre en forme le rapport et planifier l'envoi automatique avec schedule ou Windows Task Scheduler."),
            ("Ce que nos clients en disent", "Un consultant indépendant reçoit maintenant son rapport business chaque matin à 8h. Il a arrêté de checker manuellement ses stats — ça lui économise 30 min par jour.")
        ]
    },
    {
        "title": "Automatiser sa prospection LinkedIn avec n8n et Sales Navigator",
        "keyword": "automatiser prospection linkedin n8n",
        "intro": "La prospection LinkedIn manuelle prend des heures pour peu de résultats. Voici comment créer un pipeline de prospection semi-automatique avec n8n.",
        "sections": [
            ("Le problème de la prospection manuelle", "Chercher des prospects, visiter les profils, envoyer des messages personnalisés — en faisant ça manuellement, vous pouvez contacter 10-15 personnes par jour maximum."),
            ("Le pipeline n8n en 5 étapes", "1. Google Sheets avec liste de prospects\\n2. n8n lit les prospects non contactés\\n3. Génère un message personnalisé via API IA\\n4. Simule une visite de profil\\n5. Log le statut dans Sheets"),
            ("Les limites à respecter", "LinkedIn détecte et bannit l'automatisation agressive. Notre approche : max 20 actions/jour, délais aléatoires, messages vraiment personnalisés. Semi-automatique, pas bot."),
            ("Notre offre", "On configure ce pipeline pour vous en 2h de mission. Résultat : 20 prospects contactés/jour, messages personnalisés, suivi automatique. Contactez-nous sur wulix.fr.")
        ]
    },
    {
        "title": "Python pour freelances : 5 scripts qui font gagner 10h par semaine",
        "keyword": "python freelance gagner du temps scripts",
        "intro": "Vous n'avez pas besoin d'être développeur pour utiliser Python. Ces 5 scripts sont conçus pour les freelances qui veulent récupérer leur temps.",
        "sections": [
            ("Script 1 : Relances clients automatiques", "Lit votre CRM CSV, détecte les clients sans réponse depuis X jours, envoie un email personnalisé. Setup : 15 min. Gain : 1h/semaine."),
            ("Script 2 : Génération de devis PDF", "Vous remplissez un fichier Excel, le script génère un PDF professionnel et l'envoie par email. Plus jamais de mise en page Word. Gain : 30 min/devis."),
            ("Script 3 : Rapport hebdo automatique", "Collecte vos KPIs (ventes, heures, clients), génère un PDF, vous l'envoie le vendredi soir. Gain : 45 min/semaine."),
            ("Script 4 : Tri des emails entrants", "Classe automatiquement vos emails par catégorie (prospects, clients, factures, spam) et vous envoie un résumé quotidien. Gain : 20 min/jour."),
            ("Où les trouver", "Ces 5 scripts + documentation sont dans le Pack Scripts Python WULIX. 29€ sur wulix.gumroad.com/l/scripts-python — téléchargement immédiat.")
        ]
    },
    {
        "title": "Automatiser sa facturation avec Python et Stripe",
        "keyword": "automatiser facturation python stripe",
        "intro": "Vous générez vos factures manuellement chaque mois ? Un script Python connecté à Stripe peut le faire en 10 secondes automatiquement à chaque paiement.",
        "sections": [
            ("Le problème des factures manuelles", "Chaque facture : 10-15 min de mise en page, envoi manuel, archivage. Sur 20 clients/mois, c'est 4-5h perdues. Et le risque d'erreur ou d'oubli."),
            ("Python + Stripe : la solution en 3 étapes", "1. Stripe envoie un webhook à chaque paiement. 2. Python reçoit l'événement et génère la facture PDF (fpdf2). 3. La facture est envoyée automatiquement par email au client."),
            ("Le code en 50 lignes", "Avec les libs stripe, fpdf2 et smtplib, le script tient en moins de 100 lignes. Configurez une fois, il tourne pour toujours. Compatible auto-entrepreneur (sans TVA) et société."),
            ("Aller plus loin", "Ce script fait partie du Pack Scripts Python WULIX (29€). Il inclut aussi : relances impayés, rapport mensuel automatique, archivage GDrive. Disponible sur wulix.gumroad.com/l/scripts-python.")
        ]
    },
    {
        "title": "Créer un chatbot WhatsApp avec n8n en 2026",
        "keyword": "chatbot whatsapp n8n automatisation",
        "intro": "Répondre aux messages WhatsApp Business manuellement vous prend du temps. Avec n8n et l'API WhatsApp Business, automatisez 80% de vos réponses sans coder.",
        "sections": [
            ("Pourquoi WhatsApp en 2026", "2,7 milliards d'utilisateurs, taux d'ouverture 98% contre 22% pour l'email. Pour les PME et freelances français, c'est devenu un canal client incontournable."),
            ("Le setup n8n en 4 étapes", "1. Créer un compte Meta Business et activer l'API WhatsApp. 2. Configurer le webhook dans n8n. 3. Brancher un modèle IA (Gemini/GPT) pour les réponses. 4. Tester avec des cas concrets."),
            ("Ce que vous pouvez automatiser", "Réponses aux FAQ, prise de RDV, envoi de devis PDF, confirmation de commande, relances de paiement. Le bot répond 24h/24, vous intervenez seulement sur les cas complexes."),
            ("Notre offre", "On configure ce chatbot WhatsApp pour vous en une journée. Vous fournissez vos FAQ, on livre un bot opérationnel. Contactez-nous sur wulix.fr ou Fiverr : fiverr.com/richardsylla.")
        ]
    },
    {
        "title": "Remplacer Zapier par Make.com : économisez 80% sur vos automatisations",
        "keyword": "remplacer zapier make.com moins cher",
        "intro": "Zapier peut coûter 50-100€/mois dès que vous avez quelques automatisations actives. Make.com offre la même puissance à 10€/mois. Voici comment migrer sans stress.",
        "sections": [
            ("Pourquoi Zapier devient vite cher", "Zapier facture par 'task' : chaque action exécutée dans un Zap compte. Avec 5 automatisations qui tournent quotidiennement, vous consommez 5000+ tasks/mois. Le plan 750 tasks/mois coûte déjà 20$/mois."),
            ("Make.com : la même chose pour moins", "Make.com facture par 'opération' mais de façon plus généreuse. Le plan gratuit : 1000 ops/mois. Le plan Core à 9€/mois : 10 000 ops. Gain moyen constaté chez nos clients : 60-80% sur la facture d'automatisation."),
            ("Migrer sans tout refaire", "Make.com a un outil d'import Zapier qui convertit vos Zaps automatiquement. 80% des workflows migrent en 1 clic. Les 20% restants nécessitent un reconfiguration manuelle (30-60 min maximum)."),
            ("Notre aide à la migration", "On propose une migration Zapier → Make.com en moins d'une journée. Audit de vos Zaps actuels, migration, test, formation. Contactez contact@wulix.fr pour un devis.")
        ]
    },
    {
        "title": "Pipeline de prospection LinkedIn automatisé avec Make.com",
        "keyword": "pipeline prospection linkedin automatise make.com",
        "intro": "Trouver des clients sur LinkedIn prend des heures. Un pipeline semi-automatisé avec Make.com vous permet de contacter 20 prospects qualifiés par jour en 15 minutes de travail.",
        "sections": [
            ("Le workflow en 5 étapes", "1. Google Sheets avec vos critères (secteur, taille, poste). 2. Make.com scrape LinkedIn Sales Navigator. 3. IA génère un message personnalisé pour chaque prospect. 4. Vous validez en 1 clic. 5. Make.com envoie et logue les réponses."),
            ("La personnalisation qui fait la différence", "Un message générique obtient 2-3% de réponse. Un message qui mentionne le dernier post LinkedIn du prospect, son secteur précis et son problème spécifique : 8-12%. L'IA rend ça scalable."),
            ("Les règles pour rester sous le radar", "Max 20 actions/jour. Délais aléatoires entre les actions (30-120 secondes). Pas de messages identiques. Profil LinkedIn Premium recommandé. Ces règles évitent la restriction de compte."),
            ("Résultat attendu", "Avec ce pipeline, nos clients obtiennent 2-4 rendez-vous qualifiés par semaine sans démarchage manuel. On configure ce workflow pour vous : voir wulix.fr/services.")
        ]
    },
    {
        "title": "Générer des rapports Excel automatiquement avec Python",
        "keyword": "générer rapport excel automatique python",
        "intro": "Vous passez du temps chaque semaine à compiler des données dans Excel ? Python peut générer vos rapports automatiquement avec mise en forme, graphiques et envoi par email.",
        "sections": [
            ("Les libs Python pour Excel", "openpyxl pour créer/modifier des fichiers .xlsx. xlsxwriter pour les graphiques avancés. pandas pour la manipulation de données. xlrd pour lire les fichiers existants. Toutes gratuites et faciles à installer."),
            ("Exemple concret : rapport de ventes", "Chaque lundi matin, le script lit votre base clients (CSV ou Google Sheets), calcule les KPIs de la semaine, génère un Excel coloré avec graphiques et vous l'envoie par email. Zéro intervention manuelle."),
            ("Connecter vos sources de données", "Votre CRM via API. Google Sheets via gspread. Base de données SQL avec pandas.read_sql. Fichiers CSV dans un dossier. Le script agrège tout et génère le rapport unifié."),
            ("Ce qu'on livre", "Script Python opérationnel + documentation + planification automatique (Windows Task Scheduler ou cron Linux). Inclus dans le Pack Scripts Python sur wulix.gumroad.com/l/scripts-python.")
        ]
    },
    {
        "title": "Automatiser sa veille Google Alerts avec n8n",
        "keyword": "automatiser veille google alerts n8n",
        "intro": "Google Alerts envoie des emails en vrac difficiles à trier. Avec n8n, transformez votre veille en un digest quotidien intelligent, priorisé par IA.",
        "sections": [
            ("Le problème des Google Alerts classiques", "20-30 emails par jour pour 5 alertes actives. Impossible de tout lire. Résultat : vous finissez par ignorer vos alertes et rater les informations importantes."),
            ("Le workflow n8n qui résout ça", "1. Google Alerts → RSS feed (option peu connue). 2. n8n lit le RSS chaque matin. 3. IA (Gemini) évalue la pertinence de chaque alerte (1-5). 4. Seules les alertes 4-5 sont gardées. 5. Digest email quotidien à 8h avec les 3-5 infos clés."),
            ("Aller plus loin : veille concurrentielle", "Suivre les nouveaux articles de vos concurrents, leurs offres d'emploi (signal de croissance), leurs mentions presse, leurs avis clients. Tout ça automatiquement dans un rapport hebdomadaire."),
            ("Notre configuration", "Ce workflow n8n est livré clé en main avec le Pack Workflows WULIX. Voir wulix.gumroad.com ou contactez contact@wulix.fr pour une configuration sur mesure.")
        ]
    },
    {
        "title": "Créer une API REST avec FastAPI en 1 heure",
        "keyword": "créer api rest fastapi python tutoriel",
        "intro": "Vous avez un script Python utile mais personne ne peut l'utiliser facilement ? FastAPI vous permet de créer une API REST propre et documentée en moins d'une heure.",
        "sections": [
            ("Pourquoi FastAPI en 2026", "FastAPI est devenu le standard Python pour les APIs. Validation automatique des données, documentation Swagger générée automatiquement, async natif, typage Python. 3x plus rapide que Flask sur les benchmarks."),
            ("Votre première API en 20 lignes", "from fastapi import FastAPI\\napp = FastAPI()\\n@app.post('/automatiser')\\ndef run_task(data: TaskInput):\\n    result = votre_script(data)\\n    return {'result': result}\\nuvicorn app:app --reload"),
            ("Les cas d'usage concrets", "Exposer votre script de génération PDF comme API. Créer un endpoint webhook pour n8n ou Make.com. Construire un mini-SaaS. Connecter votre script à une interface web ou un chatbot."),
            ("Déploiement en 5 minutes", "Railway.app ou Render.com permettent de déployer votre FastAPI gratuitement depuis GitHub. HTTPS automatique, domaine gratuit, scaling auto. Votre API est en ligne en moins de 10 minutes.")
        ]
    },
    {
        "title": "Automatiser les posts Instagram avec Make.com",
        "keyword": "automatiser posts instagram make.com",
        "intro": "Poster régulièrement sur Instagram est chronophage. Make.com peut automatiser la publication à partir d'un simple Google Sheets — sans application tierce payante.",
        "sections": [
            ("Ce qui est possible légalement", "L'API Instagram Business (via Meta) autorise la publication automatique de photos, carousels et Reels pour les comptes Business. Pas de compte personnel — uniquement Business ou Creator."),
            ("Le workflow Make.com pas à pas", "1. Préparez vos visuels et captions dans Google Sheets (colonne image URL, caption, hashtags, date). 2. Make.com lit le sheet chaque matin. 3. Si la date = aujourd'hui, il publie via l'API Instagram Graph. 4. Log dans Sheets."),
            ("Générer les captions avec l'IA", "Branchez un module OpenAI ou Gemini dans Make.com pour générer automatiquement les captions à partir d'un brief court. Vous fournissez le thème, l'IA écrit 3 variantes, vous choisissez."),
            ("Résultat concret", "Nos clients publient 5x/semaine sur Instagram en 30 min de travail par semaine (au lieu de 3-4h). Contactez-nous pour configurer ça pour vous : wulix.fr/services.")
        ]
    },
    {
        "title": "Connecter Notion à son site web automatiquement avec n8n",
        "keyword": "connecter notion site web automatique n8n",
        "intro": "Vous gérez votre contenu dans Notion mais votre site reste statique ? n8n peut synchroniser automatiquement vos pages Notion avec votre site web sans intervention manuelle.",
        "sections": [
            ("Notion comme CMS headless", "Notion a une API officielle puissante. Vous créez et modifiez votre contenu dans Notion (articles, offres, portfolio), n8n détecte les modifications et met à jour votre site automatiquement."),
            ("Le workflow de synchronisation", "1. n8n vérifie toutes les heures les pages Notion modifiées. 2. Si modification détectée : extrait le contenu via l'API Notion. 3. Convertit en HTML ou JSON. 4. Met à jour votre site via son API ou un fichier JSON statique. 5. Déclenche un rebuild si nécessaire."),
            ("Pour quel type de site", "Sites statiques (Netlify, Cloudflare Pages) : n8n génère les fichiers et commit sur GitHub. Sites WordPress : utilise l'API REST WP. Sites custom FastAPI : endpoint webhook. La solution s'adapte à votre stack."),
            ("Notre réalisation", "WULIX utilise ce système pour son propre blog : l'agent SAMBA écrit les articles, ils sont automatiquement publiés sur wulix.fr via Cloudflare Pages. On peut reproduire ça pour votre site.")
        ]
    },
    {
        "title": "Créer un assistant IA qui répond à vos emails clients",
        "keyword": "assistant ia repondre emails clients automatique",
        "intro": "Répondre à tous les emails clients prend 1-2h par jour. Un assistant IA peut traiter 70-80% des demandes courantes automatiquement, en moins de 5 minutes.",
        "sections": [
            ("Comment ça fonctionne", "Python + Gmail API surveille votre boîte. Pour chaque email entrant, l'IA analyse la demande (Gemini ou Claude). Si c'est une question courante (prix, délais, support), l'IA rédige et envoie la réponse. Sinon, elle vous alerte."),
            ("Les types de demandes automatisables", "Questions sur les prix et délais (70% des emails). Accusés de réception et confirmations. Demandes de devis simples (IA génère le devis PDF). Suivi de commande. FAQ récurrentes."),
            ("Contrôle et sécurité", "L'IA ne répond jamais sans votre validation pour les cas sensibles. Vous pouvez configurer des seuils de confiance. Tous les emails traités sont loggés. Vous pouvez corriger et entraîner l'IA sur vos retours."),
            ("Ce qu'on a construit pour nos clients", "Notre agent LAMINE fait exactement ça pour WULIX. Il tourne sur Gmail 24h/24. On peut le configurer pour votre entreprise en 2-3 jours. Contactez contact@wulix.fr.")
        ]
    },
    {
        "title": "Automatiser la gestion des commandes Gumroad",
        "keyword": "automatiser gestion commandes gumroad python",
        "intro": "Chaque vente Gumroad peut déclencher automatiquement une série d'actions : email de bienvenue, accès produit, facturation, CRM. Voici comment tout automatiser.",
        "sections": [
            ("L'API Gumroad : ce qu'elle permet", "Récupérer les ventes en temps réel via webhook. Accéder aux infos acheteur (email, pays, produit). Gérer les licences. Envoyer des emails personnalisés. Tout ça sans plugin ou outil externe."),
            ("Le workflow post-achat idéal", "1. Gumroad webhook → n8n/Python. 2. Ajouter l'acheteur dans votre CRM (Notion, Airtable, Google Sheets). 3. Envoyer un email de bienvenue personnalisé. 4. Créer une facture PDF. 5. Planifier les emails de suivi J+3 et J+7."),
            ("Automatiser les relances de satisfaction", "J+3 : 'Avez-vous pu l'utiliser ?'. J+7 : 'Vos résultats ? Témoignage ?'. J+30 : proposition d'upsell ou de mission sur mesure. Ces séquences tournent seules et multiplient les avis positifs."),
            ("Résultat concret", "Un créateur de contenu a automatisé toute sa gestion post-vente. Il ne touche plus à ses commandes Gumroad manuellement. 5h/semaine récupérées. On configure ça pour vous sur wulix.fr.")
        ]
    },
    {
        "title": "Déployer un site web automatiquement avec GitHub Actions",
        "keyword": "déployer site web automatique github actions",
        "intro": "Modifier votre site et devoir se connecter en FTP ou lancer un script manuellement, c'est fini. GitHub Actions déploie automatiquement dès que vous poussez du code.",
        "sections": [
            ("GitHub Actions : c'est quoi concrètement", "C'est un système de CI/CD gratuit intégré à GitHub. Chaque fois que vous faites git push, un workflow se déclenche automatiquement : build, tests, déploiement. Pour un site statique, c'est prêt en 10 minutes."),
            ("Configuration pour Cloudflare Pages", "Créez un fichier .github/workflows/deploy.yml. Définissez le trigger (push sur main). Ajoutez les secrets Cloudflare dans GitHub. En 2-3 lignes YAML, votre site se déploie en 30 secondes après chaque commit."),
            ("Aller plus loin : déploiement conditionnel", "Déployer uniquement si les tests passent. Déployer sur un environnement de staging d'abord. Notifier par email ou Slack après déploiement réussi. Rollback automatique si le déploiement échoue."),
            ("Notre pipeline WULIX", "WULIX utilise exactement ce système : les articles SAMBA sont générés, committés et déployés sur Cloudflare Pages automatiquement chaque lundi. Le site se met à jour sans aucune intervention manuelle.")
        ]
    },
    {
        "title": "Héberger n8n gratuitement sur un VPS : guide complet 2026",
        "keyword": "héberger n8n vps gratuit 2026",
        "intro": "n8n en cloud coûte 20€/mois. En self-hosted sur un VPS à 4€/mois, vous avez la même puissance sans limite d'opérations. Voici comment faire.",
        "sections": [
            ("Pourquoi self-héberger n8n ?", "La version cloud n8n est limitée à 5000 opérations/mois sur le plan de base. En self-hosted : illimité. Vos données restent sur votre serveur. Coût : 4-6€/mois avec Hostinger VPS."),
            ("Le setup en 30 minutes", "1. Commander un VPS Ubuntu (Hostinger 4€/mois recommandé)\\n2. Se connecter en SSH\\n3. Installer Docker (apt install docker.io)\\n4. Lancer n8n : docker run -d -p 5678:5678 n8nio/n8n\\n5. Configurer le reverse proxy nginx"),
            ("Sécuriser votre instance", "Activer HTTPS avec Let's Encrypt (certbot), configurer l'authentification n8n, ouvrir uniquement les ports 80/443, sauvegarder le volume Docker quotidiennement."),
            ("Notre guide détaillé", "On propose une mission de setup n8n self-hosted en 2h : VPS configuré, n8n sécurisé, premier workflow opérationnel. Voir wulix.fr/services ou contactez contact@wulix.fr.")
        ]
    }
]

def generate_article_html(topic: dict) -> str:
    """Génère le HTML d'un article SEO"""
    today = datetime.date.today().strftime("%d %B %Y")
    sections_html = ""
    for title, content in topic["sections"]:
        sections_html += f"""
            <h2>{title}</h2>
            <p>{content.replace(chr(10), '</p><p>')}</p>
        """

    return f"""
    <article data-id="samba_{datetime.date.today().strftime('%Y%m%d')}" style="display:none;">
        <button onclick="showListe()" style="background:none;border:none;color:#7c3aed;cursor:pointer;font-size:14px;margin-bottom:24px;">← Retour au blog</button>
        <h1 style="font-size:clamp(1.5rem,4vw,2.2rem);font-weight:800;line-height:1.2;margin-bottom:16px;">{topic['title']}</h1>
        <div style="color:#9ca3af;font-size:14px;margin-bottom:32px;">
            Par <strong>Omar Sylla</strong> · WULIX Agency · {today}
        </div>
        <p style="font-size:18px;color:#d1d5db;margin-bottom:32px;font-style:italic;">{topic['intro']}</p>
        {sections_html}
        <div style="background:#1a1a2e;border-left:4px solid #7c3aed;padding:24px;border-radius:8px;margin-top:40px;">
            <p style="margin:0;font-weight:600;">Besoin d'aide pour automatiser ?</p>
            <p style="margin:8px 0 0;color:#9ca3af;">WULIX Agency configure tout pour vous. <a href="/" style="color:#7c3aed;">Contactez-nous →</a></p>
        </div>
        <div style="background:#0d0020;border:1px solid #1a0030;border-radius:8px;padding:24px;margin-top:24px;">
            <p style="margin:0 0 12px;font-weight:600;color:#c4b5fd;">Nos ressources pour aller plus loin</p>
            <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px;">
                <li><a href="https://wulix.gumroad.com/l/scripts-python" style="color:#00dcff;text-decoration:none;">→ Pack Scripts Python WULIX — 29€ (5 automatisations clé en main)</a></li>
                <li><a href="https://wulix.gumroad.com/l/n8n-linkedin" style="color:#00dcff;text-decoration:none;">→ Pipeline LinkedIn Automatisé n8n — 19€</a></li>
                <li><a href="https://wulix.gumroad.com" style="color:#00dcff;text-decoration:none;">→ Guide PDF "Automatise 5 tâches en 1 weekend" — 9€</a></li>
            </ul>
            <p style="margin:16px 0 8px;font-weight:600;color:#c4b5fd;">Outils recommandés</p>
            <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px;">
                <li><a href="https://n8n.io/?utm_source=wulix" style="color:#94a3b8;text-decoration:none;">→ n8n — Automatisation open-source (self-hosted gratuit)</a></li>
                <li><a href="https://www.make.com/en/register?pc=wulix" style="color:#94a3b8;text-decoration:none;">→ Make.com — 1000 opérations/mois gratuites</a></li>
                <li><a href="https://www.hostinger.com/fr?REFERRALCODE=HDACONTAC7BT" style="color:#94a3b8;text-decoration:none;">→ Hostinger VPS — Héberger n8n pour 4€/mois</a></li>
            </ul>
        </div>
    </article>
    """

def get_unused_topic() -> dict:
    """Retourne un topic non encore publié"""
    posted_file = BASE_DIR / "content" / "samba_posted.json"
    posted = json.loads(posted_file.read_text()) if posted_file.exists() else []

    for i, topic in enumerate(ARTICLE_TOPICS):
        if i not in posted:
            return i, topic

    log("Tous les articles de base publiés — génération nécessaire")
    return 0, ARTICLE_TOPICS[0]  # Cycle

def add_article_to_blog(topic: dict, topic_index: int):
    """Injecte le nouvel article dans blog.html"""
    blog_file = UI_DIR / "blog.html"
    if not blog_file.exists():
        log(f"ERREUR: blog.html introuvable dans {UI_DIR}")
        return False

    content = blog_file.read_text(encoding="utf-8")

    # Ajoute la carte dans la liste
    today = datetime.date.today().strftime("%d/%m/%Y")
    article_id = f"samba_{datetime.date.today().strftime('%Y%m%d')}"

    card_html = f"""
            <div class="card" onclick="showArticle('{article_id}')">
                <span class="badge">Automatisation</span>
                <h2>{topic['title']}</h2>
                <p>{topic['intro'][:120]}...</p>
                <div class="meta">{today} · 4 min de lecture</div>
            </div>"""

    # Insère avant la fermeture du grid
    content = content.replace(
        "<!-- SAMBA_INSERT_POINT -->",
        card_html + "\n            <!-- SAMBA_INSERT_POINT -->"
    )

    # Ajoute l'article complet
    article_html = generate_article_html(topic)
    content = content.replace(
        "<!-- SAMBA_ARTICLES_POINT -->",
        article_html + "\n    <!-- SAMBA_ARTICLES_POINT -->"
    )

    blog_file.write_text(content, encoding="utf-8")

    # Marque comme publié
    posted_file = BASE_DIR / "content" / "samba_posted.json"
    posted = json.loads(posted_file.read_text()) if posted_file.exists() else []
    posted.append(topic_index)
    with open(posted_file, "w") as f:
        json.dump(posted, f)

    log(f"Article ajouté au blog: {topic['title']}")
    return True

def check_sitemap(topic: dict):
    """Met à jour sitemap.xml avec le nouvel article"""
    sitemap_file = UI_DIR / "sitemap.xml"
    if not sitemap_file.exists():
        return

    content = sitemap_file.read_text(encoding="utf-8")
    today = datetime.date.today().isoformat()

    # Blog URL déjà dans le sitemap, on met juste à jour lastmod
    content = re.sub(
        r'(<loc>https://wulix\.fr/blog\.html</loc>\s*<lastmod>)[^<]*(</lastmod>)',
        f'\\g<1>{today}\\g<2>',
        content
    )
    sitemap_file.write_text(content, encoding="utf-8")
    log(f"Sitemap mis à jour — blog lastmod: {today}")

def run():
    log("Démarrage SAMBA — publication hebdomadaire")

    topic_index, topic = get_unused_topic()
    log(f"Article sélectionné: {topic['title']}")

    success = add_article_to_blog(topic, topic_index)
    if success:
        check_sitemap(topic)
        log("Publication réussie")

    log("SAMBA terminé")

if __name__ == "__main__":
    run()
