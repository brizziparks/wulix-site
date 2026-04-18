"""
Agent Publisher — Génère du contenu LinkedIn/Twitter pour WULIX
Marque : WULIX — Automatisation IA pour PME & Entrepreneurs
"""

import json
import random
from datetime import datetime
from pathlib import Path
from .base_agent import BaseAgent

BASE_DIR = Path(__file__).parent.parent
QUEUE_FILE = BASE_DIR / "agents" / "content_queue.json"

# ── Thèmes de contenu rotatifs ─────────────────────────────────────────────────
BRAND = {
    "name": "WULIX",
    "slogan": "Automatise. Publie. Génère.",
    "url": "WULIX.fr",
    "email": "contact@WULIX.fr",
    "fiverr": "fiverr.com/richardsylla",
    "linkedin": "linkedin.com/company/WULIX",
    "twitter": "@WULIXIA",
    "description": "Automatisation IA pour PME, freelances & entrepreneurs",
}

CONTENT_THEMES = [
    {
        "type": "education",
        "topic": "Tutoriel IA locale avec Ollama",
        "angle": "Explique comment faire tourner une IA gratuitement sur son PC sans envoyer ses données au cloud"
    },
    {
        "type": "value",
        "topic": "Automatiser les tâches répétitives avec Python",
        "angle": "Montre combien de temps on peut gagner avec l'automatisation — chiffres concrets"
    },
    {
        "type": "education",
        "topic": "Gemini API gratuit vs ChatGPT payant",
        "angle": "Comparaison honnête, comment utiliser Gemini gratuitement dans ses projets"
    },
    {
        "type": "offer",
        "topic": "Service WULIX : agent IA sur-mesure pour PME",
        "angle": "Présente WULIX de manière naturelle — ce qu'on fait, pour qui, résultats concrets"
    },
    {
        "type": "story",
        "topic": "Comment on a automatisé une tâche qui prenait 3h/semaine",
        "angle": "Histoire concrète d'un cas d'usage automatisation — avant/après"
    },
    {
        "type": "education",
        "topic": "Les 5 meilleurs outils IA gratuits en 2025",
        "angle": "Liste pratique d'outils que toute PME peut utiliser sans budget"
    },
    {
        "type": "value",
        "topic": "Créer son premier agent IA en 10 minutes",
        "angle": "Mini-tuto accessible, donne envie de démarrer avec l'IA"
    },
    {
        "type": "showcase",
        "topic": "WULIX en action : automatisation d'un workflow client",
        "angle": "Démo concrète d'un projet WULIX — avant manuel, après automatisé"
    },
    {
        "type": "education",
        "topic": "SEO + IA : générer du contenu qui ranke sur Google",
        "angle": "Comment combiner IA et SEO pour attirer du trafic organique gratuit"
    },
    {
        "type": "value",
        "topic": "Pourquoi les freelances qui utilisent l'IA gagnent 2x plus",
        "angle": "Données + raisonnement sur la productivité IA vs sans IA"
    },
]


class PublisherAgent(BaseAgent):
    """Agent qui génère du contenu social media pour attirer des clients freelance."""

    def __init__(self):
        super().__init__(
            name="Publisher",
            role="Créateur de contenu LinkedIn et Twitter/X pour WULIX",
            goal="Attirer des clients PME, freelances et entrepreneurs avec du contenu utile sur l'IA et l'automatisation",
            backstory="""Tu travailles pour WULIX (WULIX.fr), une agence d'automatisation IA créée par Omar Sylla.
WULIX aide les PME, freelances et entrepreneurs à automatiser leurs workflows avec l'IA.
Slogan : "Automatise. Publie. Génère."
Services : agents IA sur-mesure, automatisation Python, workflows intelligents.
Fiverr : fiverr.com/richardsylla
Ton rôle : créer du contenu authentique, éducatif et engageant sous la marque WULIX.
Ton style : humain, direct, concret — pas corporate, pas de jargon inutile."""
        )

    def generate_linkedin_post(self, theme: dict) -> str:
        """Génère un post LinkedIn optimisé."""
        prompt = f"""Génère un post LinkedIn pour WULIX (WULIX.fr), agence d'automatisation IA.

Thème : {theme['topic']}
Angle : {theme['angle']}
Type de contenu : {theme['type']}

Contraintes :
- Entre 150 et 300 mots
- Commence par une accroche forte (question, fait surprenant, ou déclaration audacieuse)
- Ton authentique, pas corporate
- 3-5 emojis maximum, bien placés
- Termine par un appel à l'action léger (question à la communauté, ou lien discret)
- Mention naturelle de WULIX.fr si pertinent
- 5 hashtags pertinents à la fin (#WULIX #IA #Automatisation #Python #PME)
- NE PAS mentionner Fiverr directement sauf si le type est 'offer'

Écris UNIQUEMENT le post, sans introduction ni commentaire."""

        return self.think(prompt, max_tokens=600)

    def generate_twitter_thread(self, theme: dict) -> list[str]:
        """Génère un thread Twitter/X (5-7 tweets)."""
        prompt = f"""Génère un thread Twitter/X pour WULIX (WULIX.fr), agence d'automatisation IA.

Thème : {theme['topic']}
Angle : {theme['angle']}

Format :
- 5 tweets numérotés (1/5, 2/5, etc.)
- Chaque tweet max 280 caractères
- Premier tweet = accroche forte qui donne envie de lire la suite
- Dernier tweet = conclusion + appel à l'action
- Ton décontracté et direct
- Quelques emojis stratégiques

Écris UNIQUEMENT les tweets séparés par "---", sans introduction."""

        raw = self.think(prompt, max_tokens=800)
        tweets = [t.strip() for t in raw.split("---") if t.strip()]
        return tweets

    def generate_short_post(self) -> str:
        """Génère un post court et percutant pour une publication rapide."""
        ideas = [
            "Une stat choc sur le temps perdu en tâches manuelles + solution WULIX",
            "Un fait surprenant sur l'IA locale vs cloud en 2025",
            "Une vérité que les PME ignorent sur l'automatisation",
            "Une citation percutante sur la productivité + IA",
            "Un micro-tuto IA en 3 étapes",
        ]
        idea = random.choice(ideas)
        prompt = f"""Génère un post court percutant pour LinkedIn/Twitter.
Idée : {idea}
Max 100 mots. Ton direct, authentique. 2-3 hashtags.
Écris UNIQUEMENT le post."""
        return self.think(prompt, max_tokens=200)

    def generate_twitter_profile(self) -> dict:
        """Génère le contenu complet du profil Twitter/X WULIX."""
        bio = self.think("""Génère une bio Twitter/X pour le compte @WULIXIA (agence automatisation IA).
Contraintes STRICTES :
- Maximum 160 caractères (compte les espaces et emojis)
- Accroche immédiate, ton humain et direct
- Mentionne : automatisation IA, PME/freelances, résultats concrets
- 2-3 emojis max bien placés
- Finir par WULIX.fr
Écris UNIQUEMENT la bio, rien d'autre.""", max_tokens=100)

        pinned = self.think("""Génère un tweet d'épinglage pour lancer le compte @WULIXIA.
C'est le premier tweet — il doit présenter WULIX et donner envie de suivre.
- Max 280 caractères
- Présente ce que fait WULIX (automatisation IA pour PME & freelances)
- Appel à l'action clair
- 3 hashtags : #IA #Automatisation #WULIX
Écris UNIQUEMENT le tweet.""", max_tokens=150)

        header = self.think("""Génère un texte pour le header/bannière Twitter de WULIX.
Court, percutant, max 60 caractères. Slogan ou accroche visuelle.
Écris UNIQUEMENT le texte.""", max_tokens=50)

        return {
            "nom": "WULIX",
            "username": "@WULIXIA",
            "bio": bio.strip()[:160],
            "header_texte": header.strip(),
            "tweet_epingle": pinned.strip(),
            "site_web": "WULIX.fr",
            "localisation": "France 🇫🇷",
        }

    def generate_linkedin_profile(self) -> dict:
        """Génère le contenu complet de la page LinkedIn WULIX."""
        tagline = self.think("""Génère le tagline LinkedIn pour la page entreprise WULIX.
Max 120 caractères. Court, percutant, mémorable.
WULIX = agence automatisation IA pour PME & freelances.
Écris UNIQUEMENT le tagline.""", max_tokens=60)

        about = self.think("""Génère la section "À propos" de la page LinkedIn WULIX.
Entre 200 et 400 mots. Structuré, professionnel mais humain.
Inclure :
- Ce que fait WULIX (automatisation IA, agents Python, workflows)
- Pour qui (PME, freelances, entrepreneurs)
- Comment on travaille (simple, rapide, résultats concrets)
- Services principaux
- Appel à l'action (WULIX.fr, Fiverr : fiverr.com/richardsylla)
Ton : professionnel mais accessible, pas corporate.
Écris UNIQUEMENT le texte "À propos".""", max_tokens=600)

        post_fondateur = self.think("""Génère un post LinkedIn de lancement pour WULIX (premier post de la page).
Annonce le lancement de WULIX, agence IA automatisation.
- 150-250 mots
- Ton authentique, histoire personnelle possible
- Explique la vision : l'IA accessible à tous
- Finir par un appel à l'action (suivre la page, visiter WULIX.fr)
- 5 hashtags
Écris UNIQUEMENT le post.""", max_tokens=500)

        return {
            "nom_page": "WULIX",
            "tagline": tagline.strip()[:120],
            "secteur": "Technologie de l'information",
            "taille": "1-10 employés",
            "type": "Travailleur indépendant",
            "site_web": "https://WULIX.fr",
            "specialites": ["Automatisation IA", "Agents Python", "Workflows", "PME", "Freelance", "ChatGPT", "Gemini API"],
            "about": about.strip(),
            "premier_post": post_fondateur.strip(),
        }

    def generate_fiverr_profile(self) -> dict:
        """Génère le contenu optimisé pour le profil Fiverr @richardsylla."""
        bio = self.think("""Génère une description de profil Fiverr pour Omar Sylla (@richardsylla).
Omar propose des services d'automatisation IA via WULIX.
Services : agents IA Python, automatisation workflows, bots, scripts, intégration API IA.
Contraintes :
- Max 600 caractères (bio courte Fiverr)
- Ton professionnel et vendeur
- Mentionne les technos : Python, Gemini API, Ollama, FastAPI, n8n
- Mentionne les résultats : gain de temps, économies, ROI
- Finir par une phrase d'engagement
Écris UNIQUEMENT la bio.""", max_tokens=200)

        gig1_title = self.think("""Génère un titre de Gig Fiverr pour ce service :
"Créer un agent IA Python personnalisé pour automatiser vos tâches"
Max 80 caractères, optimisé SEO Fiverr, accrocheur.
Écris UNIQUEMENT le titre.""", max_tokens=50)

        gig1_desc = self.think("""Génère une description complète de Gig Fiverr pour :
Service : création d'agent IA Python sur-mesure
Vendeur : Omar Sylla, développeur IA via WULIX
Inclure :
- Ce que tu livres exactement
- Technologies utilisées (Python, Gemini/Ollama, FastAPI)
- 3 packages (Basic 50€ / Standard 150€ / Premium 400€)
- FAQ 3 questions
- Garanties (révisions, délais)
Max 1200 caractères.
Écris UNIQUEMENT la description.""", max_tokens=600)

        gig2_title = self.think("""Génère un titre de Gig Fiverr pour :
"Automatiser un workflow répétitif avec Python ou n8n/Make"
Max 80 caractères, SEO Fiverr.
Écris UNIQUEMENT le titre.""", max_tokens=50)

        skills = ["Python", "Automatisation", "Intelligence Artificielle", "API Integration", "Chatbot", "Web Scraping", "FastAPI", "n8n"]

        return {
            "username": "richardsylla",
            "bio": bio.strip()[:600],
            "langue": "Français (natif), Anglais (courant)",
            "competences": skills,
            "gig_1": {
                "titre": gig1_title.strip()[:80],
                "description": gig1_desc.strip(),
                "categorie": "Programming & Tech > AI Development",
                "tags": ["python agent", "ai automation", "chatbot", "gemini api", "workflow automation"],
            },
            "gig_2": {
                "titre": gig2_title.strip()[:80],
                "categorie": "Programming & Tech > Automation",
                "tags": ["automation", "python script", "n8n", "workflow", "make integromat"],
            },
        }

    def setup_profiles(self) -> dict:
        """Génère tout le contenu des profils Twitter, LinkedIn et Fiverr."""
        self.log("Génération profils Twitter, LinkedIn, Fiverr...")

        twitter  = self.generate_twitter_profile()
        self.log("✓ Profil Twitter généré")

        linkedin = self.generate_linkedin_profile()
        self.log("✓ Profil LinkedIn généré")

        fiverr   = self.generate_fiverr_profile()
        self.log("✓ Profil Fiverr généré")

        result = {
            "generated_at": datetime.now().isoformat(),
            "twitter":  twitter,
            "linkedin": linkedin,
            "fiverr":   fiverr,
        }

        # Sauvegarde
        out = Path(__file__).parent.parent / "agents" / "profiles_setup.json"
        out.write_text(
            __import__("json").dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        self.log(f"✓ Profils sauvegardés → {out}")
        return result

    def save_to_queue(self, content_items: list[dict]):
        """Sauvegarde le contenu généré dans la file d'attente."""
        existing = []
        if QUEUE_FILE.exists():
            with open(QUEUE_FILE, "r", encoding="utf-8-sig") as f:
                existing = json.load(f)

        existing.extend(content_items)
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

        self.log(f"{len(content_items)} éléments ajoutés à la file d'attente")

    def run(self, task: dict) -> dict:
        """
        Tâche principale : génère du contenu pour la semaine.
        task = {"mode": "weekly" | "single", "platform": "linkedin" | "twitter" | "both"}
        """
        mode     = task.get("mode", "single")
        platform = task.get("platform", "linkedin")
        results  = []

        self.log(f"Démarrage — mode={mode}, platform={platform}")

        if mode == "weekly":
            # Génère 5 posts LinkedIn + 2 threads Twitter pour la semaine
            themes = random.sample(CONTENT_THEMES, min(5, len(CONTENT_THEMES)))
            for i, theme in enumerate(themes):
                self.log(f"Génération post {i+1}/5 — {theme['topic']}")
                if platform in ("linkedin", "both"):
                    post = self.generate_linkedin_post(theme)
                    results.append({
                        "id": f"li_{datetime.now().strftime('%Y%m%d')}_{i}",
                        "platform": "linkedin",
                        "type": theme["type"],
                        "topic": theme["topic"],
                        "content": post,
                        "status": "ready",
                        "created_at": datetime.now().isoformat(),
                    })

                if platform in ("twitter", "both"):
                    tweets = self.generate_twitter_thread(theme)
                    results.append({
                        "id": f"tw_{datetime.now().strftime('%Y%m%d')}_{i}",
                        "platform": "twitter",
                        "type": theme["type"],
                        "topic": theme["topic"],
                        "content": tweets,
                        "status": "ready",
                        "created_at": datetime.now().isoformat(),
                    })

        else:
            # Génère un seul post
            theme = random.choice(CONTENT_THEMES)
            self.log(f"Génération d'un post — {theme['topic']}")
            if platform == "linkedin":
                post = self.generate_linkedin_post(theme)
                results.append({
                    "id": f"li_{datetime.now().strftime('%Y%m%d%H%M')}",
                    "platform": "linkedin",
                    "type": theme["type"],
                    "topic": theme["topic"],
                    "content": post,
                    "status": "ready",
                    "created_at": datetime.now().isoformat(),
                })
            elif platform == "twitter":
                tweets = self.generate_twitter_thread(theme)
                results.append({
                    "id": f"tw_{datetime.now().strftime('%Y%m%d%H%M')}",
                    "platform": "twitter",
                    "type": theme["type"],
                    "topic": theme["topic"],
                    "content": tweets,
                    "status": "ready",
                    "created_at": datetime.now().isoformat(),
                })

        self.save_to_queue(results)
        self.log(f"✓ {len(results)} contenus générés et sauvegardés")

        return {
            "agent": self.name,
            "status": "success",
            "items_generated": len(results),
            "results": results,
        }
