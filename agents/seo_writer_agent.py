"""
Agent SEO Writer — Génère des articles de blog optimisés SEO pour WULIX
Sauvegarde les articles en markdown dans agents/blog_queue.json + blog/content/
"""

import json
import re
import random
from datetime import datetime
from pathlib import Path
from .base_agent import BaseAgent

BASE_DIR   = Path(__file__).parent.parent
BLOG_QUEUE = BASE_DIR / "agents" / "blog_queue.json"
BLOG_DIR   = BASE_DIR / "blog" / "content"

# ── Sujets SEO rotatifs ────────────────────────────────────────────────────────
SEO_TOPICS = [
    # NICHE 1 — Tutos outils IA gratuits
    {
        "slug": "ollama-installer-ia-gratuit-pc",
        "title": "Ollama : comment installer une IA gratuite sur son PC en 5 minutes",
        "keyword": "ollama installer",
        "secondary": ["ia locale", "llm gratuit", "ollama tuto français"],
        "niche": "tutos-ia",
        "angle": "Guide pas-à-pas pour installer Ollama et faire tourner Llama 3 ou Mistral localement, sans internet ni abonnement"
    },
    {
        "slug": "meilleurs-outils-ia-gratuits-2025",
        "title": "Les 5 meilleurs outils IA gratuits pour PME en 2025",
        "keyword": "outils ia gratuits",
        "secondary": ["ia pour entreprise", "chatgpt gratuit", "gemini gratuit"],
        "niche": "tutos-ia",
        "angle": "Comparatif concret des outils IA gratuits les plus utiles : ChatGPT, Gemini, Claude, Ollama, Perplexity — avec cas d'usage réels"
    },
    {
        "slug": "gemini-api-gratuit-guide-complet",
        "title": "Gemini API gratuit : guide complet pour l'utiliser dans vos projets",
        "keyword": "gemini api gratuit",
        "secondary": ["google gemini api", "gemini flash gratuit", "ia api gratuite"],
        "niche": "tutos-ia",
        "angle": "Comment obtenir et utiliser l'API Gemini gratuitement pour automatiser du contenu ou créer des apps IA"
    },
    {
        "slug": "chatgpt-vs-gemini-vs-claude-comparatif",
        "title": "ChatGPT vs Gemini vs Claude : quel LLM choisir en 2025 ?",
        "keyword": "chatgpt vs gemini vs claude",
        "secondary": ["meilleur llm", "comparatif ia", "quel chatbot ia choisir"],
        "niche": "tutos-ia",
        "angle": "Comparaison honnête des 3 grands LLMs : prix, qualité, cas d'usage — pour choisir sans se tromper"
    },
    # NICHE 2 — Automatisation pour freelances / entrepreneurs
    {
        "slug": "automatiser-emails-python-ia",
        "title": "Comment automatiser ses emails avec Python et l'IA (guide 2025)",
        "keyword": "automatiser emails python",
        "secondary": ["automatisation email ia", "python gmail automatisation", "gain de temps email"],
        "niche": "automatisation",
        "angle": "Tutoriel complet pour trier, répondre et classer ses emails automatiquement avec Python + un LLM gratuit"
    },
    {
        "slug": "creer-agent-ia-python-debutant",
        "title": "Créer son premier agent IA en Python : guide débutant pas-à-pas",
        "keyword": "créer agent ia python",
        "secondary": ["agent ia débutant", "python ia tuto", "llm agent python"],
        "niche": "automatisation",
        "angle": "Guide accessible pour créer un agent IA fonctionnel en Python, même sans expérience — avec code source"
    },
    {
        "slug": "freelance-ia-doubler-productivite",
        "title": "Freelance + IA : comment doubler sa productivité sans travailler plus",
        "keyword": "freelance ia productivité",
        "secondary": ["ia freelance", "gagner du temps freelance", "automatisation freelance"],
        "niche": "automatisation",
        "angle": "Stratégie concrète pour intégrer l'IA dans son workflow freelance : rédaction, prospection, admin, facturation"
    },
    {
        "slug": "n8n-make-automatisation-comparatif",
        "title": "n8n vs Make : quelle solution d'automatisation choisir en 2025 ?",
        "keyword": "n8n vs make",
        "secondary": ["zapier alternative", "automatisation no-code", "workflow automatisation"],
        "niche": "automatisation",
        "angle": "Comparatif détaillé n8n vs Make (ex-Integromat) : prix, facilité, intégrations — avec notre recommandation"
    },
    # NICHE 3 — IA pour PME francophones
    {
        "slug": "intelligence-artificielle-pme-par-ou-commencer",
        "title": "Intelligence artificielle pour PME : par où commencer en 2025 ?",
        "keyword": "intelligence artificielle pme",
        "secondary": ["ia pour pme", "transformation digitale pme", "ia petite entreprise"],
        "niche": "ressources-pme",
        "angle": "Guide pratique pour les PME qui veulent adopter l'IA sans budget énorme ni équipe technique"
    },
    {
        "slug": "automatisation-marketing-pme-ia",
        "title": "Automatisation marketing pour PME : gagner 10h/semaine avec l'IA",
        "keyword": "automatisation marketing pme",
        "secondary": ["marketing ia pme", "contenu automatique ia", "réseaux sociaux automatisation"],
        "niche": "ressources-pme",
        "angle": "Cas concrets d'automatisation marketing avec l'IA pour les PME : réseaux sociaux, emails, blog — chiffres à l'appui"
    },
    {
        "slug": "generer-contenu-linkedin-ia",
        "title": "Comment générer du contenu LinkedIn avec l'IA (méthode WULIX)",
        "keyword": "générer contenu linkedin ia",
        "secondary": ["linkedin ia automatisation", "posts linkedin automatiques", "ia contenu réseaux sociaux"],
        "niche": "ressources-pme",
        "angle": "Méthode étape par étape pour générer des posts LinkedIn professionnels avec l'IA, en restant authentique"
    },
    {
        "slug": "roi-ia-pme-chiffres-concrets",
        "title": "ROI de l'IA pour les PME : chiffres concrets et retours d'expérience",
        "keyword": "roi ia pme",
        "secondary": ["rentabilité ia entreprise", "investissement ia pme", "ia résultats concrets"],
        "niche": "ressources-pme",
        "angle": "Analyse du retour sur investissement réel de l'IA pour les PME françaises — avec exemples et calculs"
    },
]


class SeoWriterAgent(BaseAgent):
    """Agent qui génère des articles de blog SEO pour WULIX."""

    def __init__(self):
        super().__init__(
            name="SeoWriter",
            role="Rédacteur SEO spécialisé IA et automatisation",
            goal="Générer des articles de blog optimisés SEO pour WULIX.fr — attirer du trafic organique et monétiser via AdSense + affiliation",
            backstory="""Tu es rédacteur SEO pour WULIX (WULIX.fr).
WULIX est une agence d'automatisation IA qui aide PME, freelances et entrepreneurs.
Slogan : "Automatise. Publie. Génère."
Tes articles ciblent les francophones (France, Belgique, Suisse, Afrique francophone).
Tu écris des articles utiles, pratiques, bien structurés — pas du contenu vide.
Tu intègres naturellement les mots-clés sans sur-optimiser.
Chaque article doit apporter une vraie valeur au lecteur."""
        )

    # ── Génération d'article ───────────────────────────────────────────────────
    def generate_article(self, topic: dict) -> dict:
        """Génère un article SEO complet en markdown."""

        prompt = f"""Rédige un article de blog SEO complet en français pour WULIX (WULIX.fr).

SUJET : {topic['title']}
MOT-CLÉ PRINCIPAL : {topic['keyword']}
MOTS-CLÉS SECONDAIRES : {', '.join(topic['secondary'])}
ANGLE ÉDITORIAL : {topic['angle']}

STRUCTURE REQUISE (en markdown) :
# {topic['title']}

[Introduction : 2-3 phrases accroche + problème du lecteur + promesse de l'article]

## [Section 1 — contexte / pourquoi c'est important]
[contenu]

## [Section 2 — guide pratique / étapes concrètes]
[contenu avec exemples]

## [Section 3 — conseils avancés ou comparatif]
[contenu]

## [Section 4 — erreurs à éviter / FAQ courte]
[contenu]

## Conclusion
[résumé + appel à l'action vers WULIX.fr]

CONTRAINTES :
- Entre 800 et 1200 mots
- Ton : humain, direct, pédagogique — pas corporate
- Intègre le mot-clé principal dans le titre, intro, 2-3 sous-titres et conclusion
- Intègre naturellement 2-3 mots-clés secondaires dans le corps
- Termine par : "Besoin d'aide pour automatiser votre business ? [Découvrez WULIX](https://WULIX.fr)"
- Écris UNIQUEMENT l'article en markdown, sans commentaire autour"""

        content = self.think(prompt, max_tokens=2000)
        return {
            "slug":       topic["slug"],
            "title":      topic["title"],
            "keyword":    topic["keyword"],
            "secondary":  topic["secondary"],
            "niche":      topic["niche"],
            "content":    content,
            "word_count": len(content.split()),
            "status":     "draft",
            "created_at": datetime.now().isoformat(),
        }

    def generate_meta(self, topic: dict, article_content: str) -> dict:
        """Génère la meta description SEO."""
        prompt = f"""Génère une meta description SEO pour cet article :
Titre : {topic['title']}
Mot-clé : {topic['keyword']}

Règles :
- Entre 140 et 160 caractères exactement
- Inclut le mot-clé principal
- Donne envie de cliquer
- Pas de guillemets
- Écris UNIQUEMENT la meta description, rien d'autre"""

        meta = self.think(prompt, max_tokens=100)
        return meta.strip().strip('"').strip("'")

    # ── Sauvegarde ─────────────────────────────────────────────────────────────
    def save_to_queue(self, article: dict):
        """Ajoute l'article à blog_queue.json."""
        existing = []
        if BLOG_QUEUE.exists():
            try:
                with open(BLOG_QUEUE, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                pass

        # Évite les doublons par slug
        existing = [a for a in existing if a.get("slug") != article["slug"]]
        existing.append(article)

        with open(BLOG_QUEUE, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

        self.log(f"Article ajouté à la queue : {article['slug']}")

    def save_markdown(self, article: dict):
        """Sauvegarde l'article en fichier .md dans blog/content/."""
        BLOG_DIR.mkdir(parents=True, exist_ok=True)
        niche_dir = BLOG_DIR / article["niche"]
        niche_dir.mkdir(exist_ok=True)

        filepath = niche_dir / f"{article['slug']}.md"

        frontmatter = f"""---
title: "{article['title']}"
slug: "{article['slug']}"
keyword: "{article['keyword']}"
niche: "{article['niche']}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
status: "{article['status']}"
---

"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter + article["content"])

        self.log(f"Markdown sauvegardé : {filepath}")
        return str(filepath)

    # ── Run principal ──────────────────────────────────────────────────────────
    def run(self, task: dict) -> dict:
        """
        Génère des articles SEO.
        task = {
            "mode": "single" | "batch",
            "count": 3,          # pour batch
            "niche": "tutos-ia" | "automatisation" | "ressources-pme" | "all",
            "slug": "..."        # pour cibler un topic précis
        }
        """
        mode  = task.get("mode", "single")
        niche = task.get("niche", "all")
        count = task.get("count", 3)
        slug  = task.get("slug")

        self.log(f"Démarrage — mode={mode}, niche={niche}, count={count}")

        # Filtre les topics par niche
        if slug:
            topics = [t for t in SEO_TOPICS if t["slug"] == slug]
        elif niche == "all":
            topics = SEO_TOPICS.copy()
        else:
            topics = [t for t in SEO_TOPICS if t["niche"] == niche]

        if not topics:
            return {"agent": self.name, "status": "error", "message": "Aucun topic trouvé"}

        # Sélection des topics à traiter
        if mode == "single":
            selected = [random.choice(topics)]
        else:
            selected = random.sample(topics, min(count, len(topics)))

        results = []
        for i, topic in enumerate(selected):
            self.log(f"Génération article {i+1}/{len(selected)} — {topic['title']}")

            try:
                article = self.generate_article(topic)
                meta    = self.generate_meta(topic, article["content"])
                article["meta_description"] = meta

                # Sauvegarde
                md_path = self.save_markdown(article)
                self.save_to_queue(article)
                article["file_path"] = md_path

                results.append({
                    "slug":        article["slug"],
                    "title":       article["title"],
                    "niche":       article["niche"],
                    "word_count":  article["word_count"],
                    "file":        md_path,
                    "status":      "success",
                })
                self.log(f"✓ Article généré : {article['slug']} ({article['word_count']} mots)")

            except Exception as e:
                self.log(f"Erreur sur {topic['slug']}: {e}", level="ERROR")
                results.append({"slug": topic["slug"], "status": "error", "error": str(e)})

        success = sum(1 for r in results if r["status"] == "success")
        self.log(f"✓ {success}/{len(selected)} articles générés avec succès")

        return {
            "agent":            self.name,
            "status":           "success",
            "articles_generated": success,
            "results":          results,
        }
