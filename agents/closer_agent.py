"""
Agent Closer — Rédige des messages d'approche clients et réponses Fiverr
"""

import json
from datetime import datetime
from pathlib import Path
from .base_agent import BaseAgent

BASE_DIR  = Path(__file__).parent.parent
OUTREACH_FILE = BASE_DIR / "agents" / "outreach_queue.json"


class CloserAgent(BaseAgent):
    """Agent qui rédige des messages d'approche personnalisés et gère les prospects."""

    def __init__(self):
        super().__init__(
            name="Closer",
            role="Rédacteur de messages d'approche et de propositions commerciales",
            goal="Convertir les prospects en clients pour WULIX",
            backstory="""Tu rédiges des messages commerciaux pour WULIX (WULIX.fr).
Services : assistant IA (50-180€), automatisation n8n/Python (30-120€), dashboard HUD (20-80€).
Fiverr : fiverr.com/richardsylla | Demo : aisatou.rosmedia.fr

STRATÉGIE LINKEDIN ACTUELLE :
- Le profil PERSONNEL d'Omar est en PAUSE — aucun post ni prospection depuis ce compte
- Tous les messages d'approche partent depuis la PAGE WULIX (linkedin.com/company/WULIX)
- Style : chaleureux, direct, professionnel. Pas de spam. Messages courts et personnalisés."""
        )

    def generate_linkedin_outreach(self, prospect_info: dict) -> str:
        """Génère un message LinkedIn d'approche personnalisé."""
        prompt = f"""Rédige un message LinkedIn court et personnalisé pour approcher ce prospect.

Prospect :
- Secteur : {prospect_info.get('secteur', 'tech')}
- Problème identifié : {prospect_info.get('probleme', 'automatisation de tâches')}
- Contexte : {prospect_info.get('contexte', '')}

Contraintes :
- Maximum 3 phrases
- Commence par montrer qu'on a lu leur profil/contenu
- Propose une solution concrète sans être vendeur
- Termine par une question ouverte
- Pas de "je vous contacte car..." ni de liste de services
- Ton humain, pas template

Écris UNIQUEMENT le message."""
        return self.think(prompt, max_tokens=200)

    def generate_fiverr_response(self, client_message: str) -> str:
        """Génère une réponse professionnelle à un message Fiverr."""
        prompt = f"""Un client potentiel sur Fiverr a envoyé ce message :
"{client_message}"

Rédige une réponse professionnelle de la part d'Omar Sylla qui :
- Répond précisément à sa demande
- Montre de l'expertise sans jargon
- Propose un appel de 15 min pour mieux comprendre le projet
- Reste entre 100-150 mots
- Ton chaleureux et professionnel

Écris UNIQUEMENT la réponse."""
        return self.think(prompt, max_tokens=300)

    def generate_proposal(self, project_brief: str) -> str:
        """Génère une proposition commerciale complète."""
        prompt = f"""Rédige une proposition commerciale courte pour Omar Sylla.

Brief client : {project_brief}

Format :
1. Compréhension du besoin (2 phrases)
2. Solution proposée (3-4 points)
3. Délai et prix (1-2 lignes)
4. Prochaine étape

Total : max 250 mots. Ton professionnel mais accessible.
Écris UNIQUEMENT la proposition."""
        return self.think(prompt, max_tokens=500)

    def generate_follow_up(self, initial_context: str, days_since: int) -> str:
        """Génère un message de relance pour un prospect."""
        prompt = f"""Rédige un message de relance pour un prospect qui n'a pas répondu.

Contexte initial : {initial_context}
Jours depuis le premier contact : {days_since}

Le message doit :
- Être court (max 2 phrases)
- Apporter une valeur ajoutée (partager une ressource, une info utile)
- Ne pas être insistant
- Donner une porte de sortie naturelle

Écris UNIQUEMENT le message de relance."""
        return self.think(prompt, max_tokens=150)

    def save_outreach(self, items: list[dict]):
        existing = []
        if OUTREACH_FILE.exists():
            with open(OUTREACH_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing.extend(items)
        with open(OUTREACH_FILE, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

    def run(self, task: dict) -> dict:
        """
        task = {
            "mode": "linkedin" | "fiverr" | "proposal" | "followup",
            "data": {...}
        }
        """
        mode = task.get("mode", "linkedin")
        data = task.get("data", {})

        self.log(f"Démarrage — mode={mode}")

        if mode == "linkedin":
            message = self.generate_linkedin_outreach(data)
            result = {
                "agent": self.name,
                "mode": mode,
                "prospect": data,
                "message": message,
                "status": "ready",
                "created_at": datetime.now().isoformat(),
            }
            self.save_outreach([result])
            self.log("✓ Message LinkedIn généré")
            return {"agent": self.name, "status": "success", "message": message}

        elif mode == "fiverr":
            client_msg = data.get("client_message", "")
            response   = self.generate_fiverr_response(client_msg)
            result = {
                "agent": self.name,
                "mode": mode,
                "client_message": client_msg,
                "response": response,
                "status": "ready",
                "created_at": datetime.now().isoformat(),
            }
            self.save_outreach([result])
            self.log("✓ Réponse Fiverr générée")
            return {"agent": self.name, "status": "success", "response": response}

        elif mode == "proposal":
            brief    = data.get("brief", "")
            proposal = self.generate_proposal(brief)
            result = {
                "agent": self.name,
                "mode": mode,
                "brief": brief,
                "proposal": proposal,
                "status": "ready",
                "created_at": datetime.now().isoformat(),
            }
            self.save_outreach([result])
            self.log("✓ Proposition commerciale générée")
            return {"agent": self.name, "status": "success", "proposal": proposal}

        elif mode == "followup":
            context   = data.get("context", "")
            days      = data.get("days_since", 3)
            follow_up = self.generate_follow_up(context, days)
            self.log("✓ Message de relance généré")
            return {"agent": self.name, "status": "success", "followup": follow_up}

        return {"agent": self.name, "status": "error", "message": f"Mode inconnu: {mode}"}
