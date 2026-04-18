"""
AMINATA — DRH & Responsable des Missions de WULIX
Gère les offres de mission, onboarding clients, satisfaction, sous-traitants
Prénom soninké/bambara — Sénégal, Mali, Guinée
"""

import json
from datetime import datetime
from pathlib import Path
from .base_agent import BaseAgent

BASE_DIR   = Path(__file__).parent.parent
RH_DIR     = BASE_DIR / "agents" / "rh"
CLIENTS_FILE = BASE_DIR / "agents" / "clients.json"
MISSIONS_FILE = BASE_DIR / "agents" / "missions.json"
RH_DIR.mkdir(exist_ok=True)


def _load_json(path: Path) -> list:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []


def _save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class AminataAgent(BaseAgent):
    """Agent RH — gestion missions, onboarding clients, satisfaction, sous-traitants."""

    def __init__(self):
        super().__init__(
            name="Aminata",
            role="DRH & Responsable des Missions de WULIX",
            goal="Gérer les relations clients et missions de WULIX : onboarding, suivi, satisfaction, offres de mission",
            backstory="""Tu es Aminata, DRH et responsable des missions de WULIX (WULIX.fr).
WULIX est une agence d'automatisation IA freelance créée par Omar Sylla en France.
Tu gères l'onboarding des nouveaux clients, le suivi des missions en cours, la satisfaction client,
et les offres de collaboration pour les sous-traitants éventuels.
Tu es organisée, empathique et orientée résultats client.
Tu parles français, style professionnel et chaleureux."""
        )

    # ── Onboarding client ─────────────────────────────────────────────────────
    def generate_onboarding(self, context: dict) -> str:
        """Génère un kit d'onboarding pour un nouveau client."""
        client  = context.get("client", "Client")
        mission = context.get("mission", "Projet IA/Automatisation")
        montant = context.get("montant", "À définir")
        duree   = context.get("duree", "4 semaines")

        prompt = f"""Génère un email d'onboarding complet pour accueillir un nouveau client chez WULIX.

Client : {client}
Mission : {mission}
Budget : {montant}
Durée estimée : {duree}

L'email doit inclure :
1. Message de bienvenue chaleureux (ton humain, pas corporate)
2. Présentation de l'équipe WULIX (Omar Sylla + agents IA spécialisés)
3. Processus de travail détaillé (étapes, livrables, jalons)
4. Canaux de communication préférés
5. Ce dont on a besoin du client pour démarrer (accès, infos, briefing)
6. Planning prévisionnel
7. CTA : appel de démarrage à planifier

Style : professionnel mais chaleureux, rassurant, orienté résultats."""

        return self.think(prompt, max_tokens=800)

    # ── Suivi satisfaction ────────────────────────────────────────────────────
    def generate_satisfaction_survey(self, context: dict) -> str:
        """Génère une enquête de satisfaction post-mission."""
        client  = context.get("client", "Client")
        mission = context.get("mission", "La mission")

        prompt = f"""Génère un email d'enquête de satisfaction post-mission pour WULIX.

Client : {client}
Mission réalisée : {mission}

L'email doit :
1. Remercier chaleureusement pour la collaboration
2. Demander un retour honnête (5 questions max, rating 1-5 + commentaire)
3. Proposer de continuer la collaboration (upsell naturel)
4. Demander un témoignage/avis si satisfait
5. CTA pour planifier la suite

Questions de satisfaction à inclure :
- Qualité des livrables (1-5)
- Respect des délais (1-5)
- Communication pendant la mission (1-5)
- Recommanderiez-vous WULIX ? (1-5)
- Ce qu'on peut améliorer (champ libre)

Style : chaleureux, sincère, court. Pas trop long."""

        return self.think(prompt, max_tokens=700)

    # ── Offre de mission ──────────────────────────────────────────────────────
    def generate_mission_offer(self, context: dict) -> str:
        """Génère une offre de collaboration / sous-traitance."""
        profil  = context.get("profil", "Développeur Python")
        mission = context.get("mission", "Développement agent IA")
        tjm     = context.get("tjm", "200-300€/jour")
        duree   = context.get("duree", "2 semaines")

        prompt = f"""Génère une offre de mission/collaboration pour WULIX.

Profil recherché : {profil}
Mission : {mission}
TJM indicatif : {tjm}
Durée : {duree}

L'offre doit inclure :
1. Présentation de WULIX (1 paragraphe)
2. Description de la mission (contexte, livrables, stack)
3. Profil recherché (compétences, expérience)
4. Conditions (TJM, durée, remote)
5. Processus de sélection simple
6. Contact pour postuler

Style : direct, attractif, sans jargon RH inutile. On cherche quelqu'un de compétent et autonome."""

        return self.think(prompt, max_tokens=700)

    # ── Rapport hebdo équipe ──────────────────────────────────────────────────
    def weekly_team_report(self) -> str:
        """Génère un rapport hebdomadaire sur l'état de l'équipe et des missions."""
        missions  = _load_json(MISSIONS_FILE)
        clients   = _load_json(CLIENTS_FILE)
        actives   = [m for m in missions if m.get("status") == "active"]
        en_attente = [m for m in missions if m.get("status") == "pending"]

        prompt = f"""En tant que DRH de WULIX, génère le rapport hebdomadaire RH/missions.

Contexte WULIX :
- Missions actives : {len(actives)}
- Missions en attente : {len(en_attente)}
- Clients total : {len(clients)}
- Équipe : agents IA (Aisatou DG, Mariama Communication, Bintou Scout, Seydou Commercial, Koumba SEO, Fatou Finance, Modibo Juridique, Adama DSI, Djeneba Stratégie, Aminata RH)

Rapport à inclure :
1. État des missions en cours
2. Points d'attention RH (délais, risques)
3. Actions prioritaires cette semaine
4. Indicateurs clés (taux de conversion prospects, satisfaction client)
5. Message de motivation pour l'équipe 😄

Format markdown, concis, orienté action."""

        return self.think(prompt, max_tokens=800)

    # ── Gestion clients ────────────────────────────────────────────────────────
    def add_client(self, context: dict) -> dict:
        """Ajoute un nouveau client dans le CRM."""
        clients = _load_json(CLIENTS_FILE)
        client  = {
            "id":       f"CLT-{len(clients)+1:03d}",
            "nom":      context.get("nom", ""),
            "email":    context.get("email", ""),
            "company":  context.get("company", ""),
            "source":   context.get("source", ""),  # fiverr, linkedin, blog...
            "status":   "active",
            "created":  datetime.now().isoformat(),
            "notes":    context.get("notes", ""),
        }
        clients.append(client)
        _save_json(CLIENTS_FILE, clients)
        self.log(f"Nouveau client ajouté : {client['id']} — {client['nom']}")
        return client

    # ── Run ────────────────────────────────────────────────────────────────────
    def run(self, task: dict) -> dict:
        """
        task = {
            "mode": "onboarding" | "satisfaction" | "mission_offer" | "weekly_report" | "add_client",
            "context": {...}
        }
        """
        mode    = task.get("mode", "weekly_report")
        context = task.get("context", {})

        self.log(f"Démarrage — mode={mode}")

        try:
            if mode == "onboarding":
                content = self.generate_onboarding(context)
                filepath = RH_DIR / f"onboarding_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            elif mode == "satisfaction":
                content = self.generate_satisfaction_survey(context)
                return {"agent": self.name, "status": "success", "content": content}

            elif mode == "mission_offer":
                content = self.generate_mission_offer(context)
                filepath = RH_DIR / f"offre_mission_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            elif mode == "weekly_report":
                report = self.weekly_team_report()
                return {"agent": self.name, "status": "success", "report": report}

            elif mode == "add_client":
                client = self.add_client(context)
                return {"agent": self.name, "status": "success", "client": client}

            else:
                return {"agent": self.name, "status": "error", "message": f"Mode inconnu: {mode}"}

        except Exception as e:
            self.log(f"Erreur: {e}", level="ERROR")
            return {"agent": self.name, "status": "error", "error": str(e)}
