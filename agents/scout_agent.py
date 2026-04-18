"""
Agent Scout — Cherche des clients potentiels et opportunités de missions
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from .base_agent import BaseAgent

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))
PROSPECTS_FILE = BASE_DIR / "agents" / "prospects.json"


class ScoutAgent(BaseAgent):
    """Agent qui identifie des opportunités clients et missions freelance."""

    def __init__(self):
        super().__init__(
            name="Scout",
            role="Chasseur d'opportunités freelance et de prospects clients",
            goal="Trouver des clients potentiels pour des missions Python/IA/Automatisation",
            backstory="""Tu cherches des opportunités de missions pour Omar Sylla (@richardsylla).
Ses services : assistant IA personnalisé (50-180€), automatisation n8n/Python (30-120€), dashboard HUD (20-80€).
Cible : PME françaises, startups, indépendants qui ont besoin d'automatisation ou d'IA.
Plateformes cibles : Fiverr, Malt, LinkedIn, Codeur.fr, communautés Slack/Discord tech."""
        )

    def generate_search_queries(self) -> list[str]:
        """Génère des requêtes de recherche pour trouver des clients."""
        prompt = """Génère 10 requêtes de recherche pour trouver des clients qui ont besoin de :
- Automatisation Python/n8n
- Chatbot IA personnalisé
- Dashboard web
- Scripts de productivité

Pour les plateformes : LinkedIn, Twitter/X, forums français, Reddit r/france.
Format : une requête par ligne, sans numérotation.
Exemple : "cherche développeur Python automatisation Slack"
Écris UNIQUEMENT les requêtes."""
        raw = self.think(prompt, max_tokens=400)
        return [q.strip() for q in raw.strip().split("\n") if q.strip()]

    def generate_prospect_profile(self, context: str) -> dict:
        """Génère un profil de prospect cible idéal."""
        prompt = f"""Crée un profil détaillé d'un prospect idéal pour Omar Sylla (développeur Python/IA).
Contexte : {context}

Inclus :
- Secteur d'activité
- Taille de l'entreprise
- Problème qu'ils ont (que Omar peut résoudre)
- Budget estimé
- Où les trouver
- Message d'approche en 2 phrases

Réponds en JSON avec les clés : secteur, taille, probleme, budget, ou_trouver, message_approche"""
        raw = self.think(prompt, max_tokens=500)
        try:
            start = raw.find("{")
            end   = raw.rfind("}") + 1
            return json.loads(raw[start:end])
        except Exception:
            return {"raw": raw}

    def generate_opportunities_report(self) -> dict:
        """Génère un rapport d'opportunités hebdomadaire."""
        prompt = """Génère un rapport d'opportunités freelance pour la semaine pour un développeur Python/IA en France.

Inclus :
1. 5 types de clients à cibler cette semaine (avec secteur et besoin précis)
2. 3 plateformes où chercher (avec stratégie précise pour chacune)
3. 2 idées de contenu qui attirent ces clients
4. 1 action prioritaire pour cette semaine

Sois très concret et actionnable. Réponds en JSON avec les clés :
clients_cibles, plateformes, idees_contenu, action_prioritaire"""
        raw = self.think(prompt, max_tokens=800)
        try:
            start = raw.find("{")
            end   = raw.rfind("}") + 1
            return json.loads(raw[start:end])
        except Exception:
            return {"rapport": raw}

    def save_prospects(self, prospects: list[dict]):
        existing = []
        if PROSPECTS_FILE.exists():
            with open(PROSPECTS_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing.extend(prospects)
        with open(PROSPECTS_FILE, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

    def run(self, task: dict) -> dict:
        """
        task = {"mode": "opportunities" | "queries" | "profile", "context": "..."}
        """
        mode    = task.get("mode", "opportunities")
        context = task.get("context", "PME française cherchant automatisation")

        self.log(f"Démarrage — mode={mode}")

        if mode == "opportunities":
            report = self.generate_opportunities_report()
            result = {
                "agent": self.name,
                "status": "success",
                "mode": mode,
                "report": report,
                "created_at": datetime.now().isoformat(),
            }
            self.save_prospects([result])
            self.log("✓ Rapport d'opportunités généré")
            return result

        elif mode == "queries":
            queries = self.generate_search_queries()
            result = {
                "agent": self.name,
                "status": "success",
                "mode": mode,
                "queries": queries,
                "created_at": datetime.now().isoformat(),
            }
            self.log(f"✓ {len(queries)} requêtes générées")
            return result

        elif mode == "profile":
            profile = self.generate_prospect_profile(context)
            result = {
                "agent": self.name,
                "status": "success",
                "mode": mode,
                "profile": profile,
                "created_at": datetime.now().isoformat(),
            }
            self.save_prospects([result])
            self.log("✓ Profil prospect généré")
            return result

        return {"agent": self.name, "status": "error", "message": f"Mode inconnu: {mode}"}
