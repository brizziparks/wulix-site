"""
ADAMA — DSI (Directeur des Systèmes d'Information) de WULIX
Veille technologique, audit technique, documentation, roadmap produit
Prénom bambara — Mali, Sénégal, Guinée
"""

import json
from datetime import datetime
from pathlib import Path
from .base_agent import BaseAgent

BASE_DIR  = Path(__file__).parent.parent
TECH_DIR  = BASE_DIR / "agents" / "tech"
TECH_DIR.mkdir(exist_ok=True)


class AdamaAgent(BaseAgent):
    """Agent DSI — veille tech, audits, documentation, roadmap produit."""

    def __init__(self):
        super().__init__(
            name="Adama",
            role="DSI — Directeur des Systèmes d'Information de WULIX",
            goal="Maintenir l'excellence technique de WULIX : veille IA, audits, documentation, sécurité, roadmap",
            backstory="""Tu es Adama, DSI de WULIX (WULIX.fr).
WULIX est une agence d'automatisation IA créée par Omar Sylla (développeur Python, France).
Stack actuel : Python, FastAPI, Gemini API, Ollama (Llama3/Mistral), HTML/CSS/JS, Netlify.
Tu surveilles les nouvelles technos IA, audites les systèmes, documentes les projets
et proposes des améliorations techniques concrètes.
Tu parles le langage des développeurs : précis, pragmatique, orienté implémentation."""
        )

    # ── Veille technologique ──────────────────────────────────────────────────
    def tech_watch(self, domaine: str = "ia-automatisation") -> str:
        """Génère un rapport de veille technologique."""
        domaines = {
            "ia-automatisation": "IA générative, LLMs, agents IA, automatisation Python",
            "seo-ia": "SEO technique, IA pour le contenu, Google SGE, outils SEO 2025",
            "monetisation": "Monétisation blog, AdSense, affiliation, produits digitaux",
            "outils-dev": "Nouveaux frameworks Python, FastAPI updates, outils développement",
        }
        focus = domaines.get(domaine, domaine)

        prompt = f"""En tant que DSI de WULIX, génère un rapport de veille technologique.

Domaine : {focus}
Stack actuel WULIX : Python 3.11, FastAPI, Gemini 2.0, Ollama, HTML/CSS/JS, Netlify

Le rapport doit inclure :
1. Top 5 tendances / nouveautés importantes cette semaine
2. Outils/librairies à surveiller ou tester
3. Opportunités concrètes pour WULIX (nouveaux services potentiels)
4. Risques/menaces technologiques (concurrence, obsolescence)
5. Recommandations d'actions immédiates (max 3)

Format markdown, concis, orienté décision. Chaque point = 2-3 phrases max."""

        return self.think(prompt, max_tokens=1000)

    # ── Audit technique ───────────────────────────────────────────────────────
    def audit_system(self, context: dict = None) -> str:
        """Audit de l'infrastructure technique actuelle de WULIX."""
        prompt = """En tant que DSI, réalise un audit technique du système WULIX.

Infrastructure actuelle :
- Backend IA : Python 3.11 + FastAPI (port 7777)
- LLMs : Gemini 2.0 Flash Lite (API) + Ollama local (llama3.2:3b, gemma3:12b, mistral)
- Agents : Aisatou(DG), Mariama(Communication), Bintou(Scout), Seydou(Commercial),
           Koumba(SEO), Fatou(Finance), Aminata(RH), Modibo(Juridique), Adama(DSI), Djeneba(Stratégie)
- Interface : HUD web (HTML/CSS/JS + WebSocket)
- Site : WULIX.fr (HTML statique, Netlify)
- Automatisation : Windows Scheduled Task (8h30 daily)
- Stockage : JSON files locaux
- OS : Windows 11, RTX 2070 8Go, 16Go RAM

L'audit doit couvrir :
1. Points forts de l'architecture
2. Points faibles et risques techniques
3. Sécurité (API keys, données, accès)
4. Performance et scalabilité
5. 5 améliorations prioritaires avec effort estimé (S/M/L)
6. Roadmap technique suggérée (3 mois)

Format markdown structuré."""

        return self.think(prompt, max_tokens=1200)

    # ── Documentation ─────────────────────────────────────────────────────────
    def generate_doc(self, context: dict) -> str:
        """Génère la documentation technique d'un composant ou agent."""
        composant = context.get("composant", "Agent IA WULIX")
        code      = context.get("code", "")
        objectif  = context.get("objectif", "Documentation technique complète")

        prompt = f"""Génère la documentation technique pour : {composant}

Objectif : {objectif}
{'Code source : ' + code[:500] + '...' if code else ''}

La documentation doit inclure :
1. Description et rôle dans WULIX
2. Prérequis et dépendances
3. Installation / configuration
4. API / méthodes disponibles (avec exemples)
5. Exemples d'utilisation concrets
6. Gestion des erreurs courantes
7. Maintenance et évolution

Format markdown technique, exemples de code Python inclus."""

        return self.think(prompt, max_tokens=1200)

    # ── Roadmap produit ───────────────────────────────────────────────────────
    def generate_roadmap(self, horizon: str = "3 mois") -> str:
        """Génère la roadmap produit et technique de WULIX."""
        prompt = f"""En tant que DSI de WULIX, génère la roadmap technique et produit sur {horizon}.

État actuel :
- ✅ 10 agents IA opérationnels (DG, Communication, Scout, Commercial, SEO, Finance, RH, Juridique, DSI, Stratégie)
- ✅ HUD web de monitoring
- ✅ Site WULIX.fr déployé sur Netlify
- ✅ Tâche planifiée quotidienne (8h30)
- 🔄 Blog SEO en cours de génération
- ❌ Base de données (JSON seulement)
- ❌ Authentification HUD
- ❌ API publique
- ❌ Auto-publish sur LinkedIn/Twitter
- ❌ Dashboard analytics revenus

Objectifs business :
- Track 1 : 500-3000€/mois services freelance
- Track 2 : 300-1000€/mois SEO passif

Génère une roadmap priorisée :
1. Quick wins (cette semaine)
2. Sprint 1 (mois 1)
3. Sprint 2 (mois 2)
4. Sprint 3 (mois 3)
5. Backlog (plus tard)

Pour chaque item : effort (XS/S/M/L), impact business (faible/moyen/fort), priorité."""

        return self.think(prompt, max_tokens=1200)

    # ── Rapport de sécurité ───────────────────────────────────────────────────
    def security_check(self) -> str:
        """Audit de sécurité des systèmes WULIX."""
        prompt = """En tant que DSI, réalise un audit de sécurité rapide pour WULIX.

Points à vérifier :
1. Protection des clés API (GEMINI_API_KEY, ANTHROPIC_API_KEY dans .env)
2. Sécurité du HUD web (pas d'authentification actuellement)
3. Exposition des endpoints FastAPI
4. Sécurité des fichiers JSON (données clients, finances)
5. Sécurité du site Netlify (headers, HTTPS)

Pour chaque point : niveau de risque (faible/moyen/critique) + action recommandée.
Termine par les 3 actions de sécurité prioritaires à faire immédiatement.

Format markdown avec tableau des risques."""

        return self.think(prompt, max_tokens=800)

    # ── Run ────────────────────────────────────────────────────────────────────
    def run(self, task: dict) -> dict:
        """
        task = {
            "mode": "veille" | "audit" | "doc" | "roadmap" | "security",
            "context": {...},
            "domaine": "ia-automatisation" | "seo-ia" | "monetisation" | "outils-dev"
        }
        """
        mode    = task.get("mode", "veille")
        context = task.get("context", {})
        domaine = task.get("domaine", "ia-automatisation")

        self.log(f"Démarrage — mode={mode}")

        try:
            if mode == "veille":
                content  = self.tech_watch(domaine)
                filepath = TECH_DIR / f"veille_{datetime.now().strftime('%Y%m%d')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            elif mode == "audit":
                content  = self.audit_system(context)
                filepath = TECH_DIR / f"audit_{datetime.now().strftime('%Y%m%d')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            elif mode == "doc":
                content  = self.generate_doc(context)
                nom      = context.get("composant", "doc").lower().replace(" ", "_")
                filepath = TECH_DIR / f"doc_{nom}_{datetime.now().strftime('%Y%m%d')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            elif mode == "roadmap":
                horizon  = context.get("horizon", "3 mois")
                content  = self.generate_roadmap(horizon)
                filepath = TECH_DIR / f"roadmap_{datetime.now().strftime('%Y%m%d')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            elif mode == "security":
                content  = self.security_check()
                filepath = TECH_DIR / f"security_{datetime.now().strftime('%Y%m%d')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            else:
                return {"agent": self.name, "status": "error", "message": f"Mode inconnu: {mode}"}

        except Exception as e:
            self.log(f"Erreur: {e}", level="ERROR")
            return {"agent": self.name, "status": "error", "error": str(e)}
