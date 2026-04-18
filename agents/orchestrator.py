"""
Orchestrateur AISATOU — Boss des agents IA
Coordonne Publisher, Scout et Closer pour générer des revenus.
"""

import json
from datetime import datetime
from pathlib import Path
from .base_agent import BaseAgent
from .publisher_agent import PublisherAgent
from .scout_agent import ScoutAgent
from .closer_agent import CloserAgent

BASE_DIR    = Path(__file__).parent.parent
REPORT_FILE = BASE_DIR / "agents" / "daily_report.json"


class Orchestrator(BaseAgent):
    """Boss agent qui coordonne les agents spécialisés."""

    def __init__(self):
        super().__init__(
            name="AISATOU-Boss",
            role="Orchestrateur de l'équipe d'agents IA",
            goal="Maximiser les revenus freelance d'Omar via une stratégie coordonnée",
            backstory="""Tu es le cerveau de l'équipe. Tu décides quelles tâches donner à quel agent.
Tu analyses les résultats et adaptes la stratégie. Tu es pragmatique et orienté résultats."""
        )
        self.publisher = PublisherAgent()
        self.scout     = ScoutAgent()
        self.closer    = CloserAgent()

    def plan_week(self) -> dict:
        """Planifie les actions de la semaine."""
        prompt = """Planifie la semaine d'un développeur freelance Python/IA qui veut générer ses premières missions.
Il a : Fiverr actif, LinkedIn, pas encore de Malt.
Durée disponible : 1-2h par jour.

Génère un plan en JSON avec :
{
  "objectif_semaine": "...",
  "lundi": {"publisher": true/false, "scout": true/false, "closer": true/false, "priorite": "..."},
  "mardi": {...},
  "mercredi": {...},
  "jeudi": {...},
  "vendredi": {...},
  "action_critique": "la chose la plus importante à faire cette semaine"
}"""
        raw = self.think(prompt, max_tokens=600)
        try:
            start = raw.find("{")
            end   = raw.rfind("}") + 1
            return json.loads(raw[start:end])
        except Exception:
            return {"plan": raw}

    def daily_briefing(self) -> str:
        """Génère le briefing quotidien pour Omar."""
        # Lire la file de contenu
        content_count  = 0
        prospects_count = 0
        outreach_count  = 0

        queue_file = BASE_DIR / "agents" / "content_queue.json"
        if queue_file.exists():
            with open(queue_file, "r", encoding="utf-8") as f:
                content_count = len(json.load(f))

        prospects_file = BASE_DIR / "agents" / "prospects.json"
        if prospects_file.exists():
            with open(prospects_file, "r", encoding="utf-8") as f:
                prospects_count = len(json.load(f))

        outreach_file = BASE_DIR / "agents" / "outreach_queue.json"
        if outreach_file.exists():
            with open(outreach_file, "r", encoding="utf-8") as f:
                outreach_count = len(json.load(f))

        prompt = f"""Génère un briefing matinal court et motivant pour Omar Sylla, développeur freelance.

Contexte :
- {content_count} posts en attente de publication
- {prospects_count} opportunités identifiées
- {outreach_count} messages d'approche prêts
- Date : {datetime.now().strftime('%A %d %B %Y')}

Le briefing doit :
- Commencer par "Bonjour Omar !"
- Donner 3 actions prioritaires du jour (très concrètes)
- Finir par une phrase motivante
- Max 150 mots"""
        return self.think(prompt, max_tokens=300)

    def run_daily_routine(self) -> dict:
        """Lance la routine quotidienne complète."""
        self.log("=== ROUTINE QUOTIDIENNE DÉMARRÉE ===")
        results = {}

        # 1. Scout : opportunités du jour
        self.log("Scout → analyse des opportunités...")
        results["scout"] = self.scout.run({"mode": "opportunities"})

        # 2. Publisher : 1 post LinkedIn
        self.log("Publisher → génération d'un post LinkedIn...")
        results["publisher"] = self.publisher.run({
            "mode": "single",
            "platform": "linkedin"
        })

        # 3. Closer : message d'approche basé sur opportunités
        scout_data = results["scout"].get("report", {})
        if isinstance(scout_data, dict) and scout_data.get("clients_cibles"):
            cible = scout_data["clients_cibles"][0] if scout_data["clients_cibles"] else {}
            self.log("Closer → message d'approche...")
            results["closer"] = self.closer.run({
                "mode": "linkedin",
                "data": {
                    "secteur": cible.get("secteur", "tech"),
                    "probleme": cible.get("besoin", "automatisation"),
                    "contexte": str(cible),
                }
            })

        # 4. Briefing Omar
        results["briefing"] = self.daily_briefing()

        # Sauvegarder le rapport
        report = {
            "date": datetime.now().isoformat(),
            "results": results,
        }
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        self.log("=== ROUTINE QUOTIDIENNE TERMINÉE ===")
        return report

    def run(self, task: dict) -> dict:
        mode = task.get("mode", "daily")

        if mode == "daily":
            return self.run_daily_routine()
        elif mode == "plan":
            plan = self.plan_week()
            return {"agent": self.name, "status": "success", "plan": plan}
        elif mode == "briefing":
            briefing = self.daily_briefing()
            return {"agent": self.name, "status": "success", "briefing": briefing}
        elif mode == "publisher":
            return self.publisher.run(task.get("publisher_task", {"mode": "single", "platform": "linkedin"}))
        elif mode == "scout":
            return self.scout.run(task.get("scout_task", {"mode": "opportunities"}))
        elif mode == "closer":
            return self.closer.run(task.get("closer_task", {"mode": "linkedin", "data": {}}))

        return {"agent": self.name, "status": "error", "message": f"Mode inconnu: {mode}"}
