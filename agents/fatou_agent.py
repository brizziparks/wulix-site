"""
FATOU — Directrice Financière & Comptable de WULIX
Gère les revenus, factures, dépenses et rapports financiers
Prénom soninké — Sénégal, Guinée, Mali
"""

import json
from datetime import datetime
from pathlib import Path
from .base_agent import BaseAgent

BASE_DIR      = Path(__file__).parent.parent
FINANCE_DIR   = BASE_DIR / "agents" / "finance"
INVOICES_FILE = BASE_DIR / "agents" / "invoices.json"
REVENUE_FILE  = BASE_DIR / "agents" / "revenue_tracker.json"
FINANCE_DIR.mkdir(exist_ok=True)


def _load_json(path: Path) -> list:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []


def _save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class FatouAgent(BaseAgent):
    """Agent Financier — factures, suivi revenus, rapports, objectifs."""

    def __init__(self):
        super().__init__(
            name="Fatou",
            role="Directrice Financière & Comptable de WULIX",
            goal="Gérer les finances de WULIX : facturation, suivi des revenus, objectifs mensuels et rapports financiers",
            backstory="""Tu es Fatou, directrice financière de WULIX (WULIX.fr).
WULIX est une agence freelance d'automatisation IA créée par Omar Sylla en France.
Tu gères la comptabilité, la facturation, le suivi des paiements et les objectifs de revenus.
Objectifs actuels : 300-1000€/mois (SEO passif) + 500-3000€/mois (freelance services).
Tu es rigoureuse, précise, et tu alertes proactivement sur les risques financiers.
Tu parles français, style professionnel et chiffré."""
        )

    # ── Factures ───────────────────────────────────────────────────────────────
    def generate_invoice(self, context: dict) -> dict:
        """Génère une facture formatée."""
        invoices  = _load_json(INVOICES_FILE)
        invoice_n = len(invoices) + 1
        invoice_id = f"WULIX-{datetime.now().year}-{invoice_n:03d}"

        client   = context.get("client", "Client")
        mission  = context.get("mission", "Prestation développement IA")
        montant  = context.get("montant", 0)
        tva      = context.get("tva", False)  # Auto-entrepreneur = pas de TVA par défaut
        date_str = datetime.now().strftime("%d/%m/%Y")

        # Génère le contenu markdown de la facture
        prompt = f"""Génère une facture professionnelle complète en markdown pour :

Émetteur : WULIX — Omar Sylla, auto-entrepreneur
           Email : contact@WULIX.fr | Site : WULIX.fr
Client : {client}
Mission : {mission}
Montant HT : {montant}€
TVA : {'Non applicable (auto-entrepreneur, art. 293B CGI)' if not tva else '20%'}
Date : {date_str}
Numéro : {invoice_id}
Conditions de paiement : 30 jours net

La facture doit être claire, professionnelle, avec toutes les mentions légales obligatoires françaises.
Format : tableau des prestations, sous-total, total, conditions de paiement, RIB [PLACEHOLDER]."""

        content = self.think(prompt, max_tokens=1000)

        invoice = {
            "id":         invoice_id,
            "client":     client,
            "mission":    mission,
            "montant":    montant,
            "date":       datetime.now().isoformat(),
            "status":     "generated",
            "content":    content,
        }

        invoices.append(invoice)
        _save_json(INVOICES_FILE, invoices)

        # Sauvegarde en fichier MD
        filepath = FINANCE_DIR / f"{invoice_id}.md"
        filepath.write_text(content, encoding="utf-8")
        invoice["file"] = str(filepath)

        self.log(f"Facture générée : {invoice_id} — {montant}€")
        return invoice

    # ── Suivi revenus ──────────────────────────────────────────────────────────
    def add_revenue(self, source: str, montant: float, type_revenu: str = "freelance", note: str = "") -> dict:
        """Enregistre une entrée de revenus."""
        revenues = _load_json(REVENUE_FILE)
        entry = {
            "date":    datetime.now().isoformat(),
            "source":  source,
            "montant": montant,
            "type":    type_revenu,  # freelance | seo | affiliation | autre
            "note":    note,
        }
        revenues.append(entry)
        _save_json(REVENUE_FILE, revenues)
        self.log(f"Revenu enregistré : {montant}€ ({source})")
        return entry

    def monthly_report(self) -> dict:
        """Génère le rapport financier du mois courant."""
        revenues = _load_json(REVENUE_FILE)
        invoices = _load_json(INVOICES_FILE)

        now   = datetime.now()
        month = now.strftime("%Y-%m")

        # Filtre ce mois
        month_revenues = [r for r in revenues if r["date"].startswith(month)]
        month_invoices = [i for i in invoices if i["date"].startswith(month)]

        total          = sum(r["montant"] for r in month_revenues)
        total_freelance = sum(r["montant"] for r in month_revenues if r["type"] == "freelance")
        total_seo      = sum(r["montant"] for r in month_revenues if r["type"] in ("seo", "affiliation"))

        # Objectifs
        obj_seo        = 300
        obj_freelance  = 500
        obj_total      = obj_seo + obj_freelance

        data_str = json.dumps({
            "mois": month,
            "revenus": month_revenues,
            "total": total,
            "freelance": total_freelance,
            "seo_passif": total_seo,
            "factures": len(month_invoices),
            "objectif_seo": obj_seo,
            "objectif_freelance": obj_freelance,
        }, ensure_ascii=False)

        prompt = f"""En tant que directrice financière de WULIX, génère un rapport financier mensuel.

Données du mois {month} :
{data_str}

Le rapport doit inclure :
1. Résumé exécutif (1 paragraphe)
2. Tableau revenus vs objectifs (avec % de réalisation)
3. Analyse par source (freelance vs SEO passif)
4. Points d'alerte si objectifs non atteints
5. 3 recommandations concrètes pour le mois prochain

Style : concis, chiffré, orienté action. Format markdown."""

        report_text = self.think(prompt, max_tokens=1000)

        report = {
            "mois":              month,
            "total":             total,
            "freelance":         total_freelance,
            "seo":               total_seo,
            "objectif_total":    obj_total,
            "taux_realisation":  round(total / obj_total * 100, 1) if obj_total > 0 else 0,
            "nb_factures":       len(month_invoices),
            "rapport":           report_text,
            "generated_at":      now.isoformat(),
        }

        # Sauvegarde
        filepath = FINANCE_DIR / f"rapport_{month}.md"
        filepath.write_text(report_text, encoding="utf-8")
        report["file"] = str(filepath)

        self.log(f"Rapport mensuel généré : {month} — {total}€ / objectif {obj_total}€")
        return report

    def cashflow_forecast(self) -> str:
        """Prévision de trésorerie sur 3 mois."""
        revenues = _load_json(REVENUE_FILE)

        prompt = f"""En tant que directrice financière de WULIX (agence IA freelance), génère une prévision de trésorerie sur 3 mois.

Historique des revenus disponible : {len(revenues)} entrées.
Modèle de revenus :
- Track 1 : Services freelance (agents IA, automatisation, web) — objectif 500-3000€/mois
- Track 2 : SEO passif (blog WULIX.fr, AdSense, affiliation) — objectif 300-1000€/mois à 6-12 mois

Génère :
1. Prévision réaliste mois M+1, M+2, M+3
2. Scénario pessimiste / optimiste
3. Seuil de rentabilité (charges fixes estimées auto-entrepreneur)
4. Actions prioritaires pour atteindre les objectifs

Format markdown, orienté décision."""

        return self.think(prompt, max_tokens=800)

    # ── Run ────────────────────────────────────────────────────────────────────
    def run(self, task: dict) -> dict:
        """
        task = {
            "mode": "invoice" | "add_revenue" | "monthly_report" | "forecast",
            "context": {...}
        }
        """
        mode    = task.get("mode", "monthly_report")
        context = task.get("context", {})

        self.log(f"Démarrage — mode={mode}")

        try:
            if mode == "invoice":
                result = self.generate_invoice(context)
                return {"agent": self.name, "status": "success", "invoice": result}

            elif mode == "add_revenue":
                entry = self.add_revenue(
                    source     = context.get("source", "Client"),
                    montant    = context.get("montant", 0),
                    type_revenu = context.get("type", "freelance"),
                    note       = context.get("note", ""),
                )
                return {"agent": self.name, "status": "success", "entry": entry}

            elif mode == "monthly_report":
                report = self.monthly_report()
                return {"agent": self.name, "status": "success", "report": report}

            elif mode == "forecast":
                forecast = self.cashflow_forecast()
                return {"agent": self.name, "status": "success", "forecast": forecast}

            else:
                return {"agent": self.name, "status": "error", "message": f"Mode inconnu: {mode}"}

        except Exception as e:
            self.log(f"Erreur: {e}", level="ERROR")
            return {"agent": self.name, "status": "error", "error": str(e)}
