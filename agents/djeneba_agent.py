"""
DJENEBA — Directrice Stratégie & Développement de WULIX
Plan stratégique, analyse concurrentielle, KPIs, nouvelles opportunités
Prénom bambara/dioula — Mali, Côte d'Ivoire, Burkina Faso
"""

import json
from datetime import datetime
from pathlib import Path
from .base_agent import BaseAgent

BASE_DIR     = Path(__file__).parent.parent
STRATEGY_DIR = BASE_DIR / "agents" / "strategy"
STRATEGY_DIR.mkdir(exist_ok=True)


class DjenebaAgent(BaseAgent):
    """Agent Stratégie — plan business, KPIs, analyse marché, nouvelles opportunités."""

    def __init__(self):
        super().__init__(
            name="Djeneba",
            role="Directrice Stratégie & Développement de WULIX",
            goal="Définir et piloter la stratégie de croissance de WULIX vers ses objectifs de revenus et de positionnement",
            backstory="""Tu es Djeneba, directrice stratégie de WULIX (WULIX.fr).
WULIX est une agence d'automatisation IA créée par Omar Sylla, freelance basé en France.
Objectifs actuels : 300-1000€/mois (SEO passif) + 500-3000€/mois (services).
Tu analyses le marché, identifies les opportunités, définis les KPIs et proposes des plans d'action.
Tu penses à long terme tout en restant pragmatique pour un freelance solo avec peu de budget.
Tu parles français, style stratégique mais accessible — pas de bullshit corporate."""
        )

    # ── Plan stratégique ──────────────────────────────────────────────────────
    def quarterly_plan(self, context: dict = None) -> str:
        """Génère le plan stratégique trimestriel."""
        trimestre = context.get("trimestre", "Q2 2025") if context else "Q2 2025"
        revenus_actuels = context.get("revenus_actuels", 0) if context else 0

        prompt = f"""En tant que directrice stratégie de WULIX, génère le plan stratégique pour {trimestre}.

Situation actuelle de WULIX :
- Revenus actuels : {revenus_actuels}€/mois
- Objectif court terme : 800-1000€/mois (SEO + freelance combinés)
- Objectif moyen terme : 3000€+/mois
- Ressources : 1 freelance (Omar Sylla), 10 agents IA, site WULIX.fr, blog SEO en cours
- Canaux actifs : Fiverr (@richardsylla), LinkedIn, Twitter/X, blog WULIX.fr
- Services : Agents IA, automatisation Python, développement web, contenu SEO

Plan stratégique à inclure :
1. Analyse SWOT rapide (Forces, Faiblesses, Opportunités, Menaces)
2. Objectifs SMART pour le trimestre (chiffrés, datés)
3. 3 axes stratégiques prioritaires
4. Plan d'action semaine par semaine (mois 1)
5. KPIs à suivre (revenus, trafic, leads, conversions)
6. Budget marketing estimé (faible, on mise sur le contenu organique)

Format markdown structuré, orienté action concrète."""

        return self.think(prompt, max_tokens=1200)

    # ── Analyse concurrentielle ───────────────────────────────────────────────
    def competitive_analysis(self, niche: str = "automatisation-ia-france") -> str:
        """Analyse concurrentielle sur la niche WULIX."""
        prompt = f"""Analyse concurrentielle pour WULIX dans la niche : {niche}

WULIX se positionne sur :
- Automatisation IA sur-mesure pour PME/freelances francophones
- Blog SEO sur l'IA et l'automatisation (WULIX.fr)
- Services freelance (Fiverr + direct)

Analyse :
1. Principaux concurrents (agences IA, freelances, outils no-code)
2. Leur positionnement et points forts
3. Faiblesses et angles non couverts (opportunités pour WULIX)
4. Différenciateurs uniques de WULIX à mettre en avant
5. Stratégie de différenciation recommandée
6. Niches sous-exploitées à cibler

Sois réaliste et pratique — WULIX est un freelance solo avec peu de budget.
Format markdown."""

        return self.think(prompt, max_tokens=1000)

    # ── KPIs & objectifs ──────────────────────────────────────────────────────
    def define_kpis(self) -> str:
        """Définit les KPIs stratégiques de WULIX."""
        prompt = """Définis les KPIs stratégiques pour piloter la croissance de WULIX.

Contexte : agence IA freelance, 2 tracks de revenus (services + SEO passif).
Objectif : atteindre 1500€/mois stable d'ici 6 mois.

Pour chaque KPI, indique :
- Nom et définition
- Fréquence de mesure
- Objectif cible (1 mois / 3 mois / 6 mois)
- Comment le mesurer concrètement
- Action corrective si KPI non atteint

Catégories de KPIs :
1. Revenus (CA mensuel, revenu moyen par client, MRR)
2. Acquisition (trafic blog, leads LinkedIn, conversion Fiverr)
3. SEO (articles publiés, mots-clés rankés, trafic organique)
4. Clients (NPS, taux de rétention, upsell)
5. Productivité agents (articles générés/semaine, posts publiés)

Format : tableau markdown clair."""

        return self.think(prompt, max_tokens=1000)

    # ── Nouvelles opportunités ────────────────────────────────────────────────
    def opportunity_scan(self) -> str:
        """Scanne les nouvelles opportunités de revenus pour WULIX."""
        prompt = """En tant que directrice stratégie, identifie les nouvelles opportunités de revenus pour WULIX.

Profil Omar Sylla / WULIX :
- Compétences : Python, IA, automatisation, agents, web, SEO
- Ressources : PC RTX 2070, agents IA opérationnels, site WULIX.fr
- Budget : minimal (pas d'investissement lourd)
- Temps disponible : partiel (freelance + construction du système)

Opportunités à explorer :
1. Produits digitaux (templates, scripts, mini-outils — Gumroad)
2. Formation / cours en ligne (IA pratique pour non-développeurs)
3. Affiliation (outils IA, hébergement, logiciels)
4. Partenariats agences (sous-traitance développement IA)
5. Newsletter payante / communauté
6. Nouveaux marchés (Afrique francophone, diasporas)

Pour chaque opportunité :
- Potentiel de revenus estimé
- Effort de mise en place (faible/moyen/fort)
- Délai avant premiers revenus
- Recommandation (oui/non/plus tard)

Format markdown avec tableau de priorisation."""

        return self.think(prompt, max_tokens=1000)

    # ── Rapport stratégique mensuel ───────────────────────────────────────────
    def monthly_strategy_report(self, context: dict = None) -> str:
        """Génère le rapport stratégique mensuel."""
        revenus = context.get("revenus", 0) if context else 0
        objectif = context.get("objectif", 800) if context else 800
        trafic = context.get("trafic_blog", 0) if context else 0
        articles = context.get("articles_publies", 0) if context else 0

        prompt = f"""Génère le rapport stratégique mensuel de WULIX.

Chiffres du mois :
- Revenus : {revenus}€ / Objectif : {objectif}€
- Trafic blog : {trafic} visiteurs
- Articles SEO publiés : {articles}
- Taux de réalisation objectif : {round(revenus/objectif*100, 1) if objectif > 0 else 0}%

Le rapport doit inclure :
1. Bilan exécutif (1 paragraphe)
2. Analyse des écarts (objectifs vs réalisé)
3. Ce qui a bien marché ce mois
4. Ce qui n'a pas marché et pourquoi
5. Ajustements stratégiques pour le mois prochain
6. Top 3 priorités absolues

Style : direct, honnête, constructif. Pas de langue de bois.
Format markdown."""

        return self.think(prompt, max_tokens=900)

    # ── Pitch WULIX ─────────────────────────────────────────────────────────
    def generate_pitch(self, audience: str = "pme") -> str:
        """Génère le pitch de WULIX adapté à l'audience."""
        audiences = {
            "pme":        "PME françaises (dirigeants, gérants)",
            "freelance":  "Freelances et indépendants",
            "startup":    "Startups tech",
            "afrique":    "Entrepreneurs africains et diaspora",
            "linkedin":   "Audience LinkedIn professionnelle",
        }
        cible = audiences.get(audience, audience)

        prompt = f"""Génère le pitch de WULIX adapté pour : {cible}

WULIX : agence d'automatisation IA, slogan "Automatise. Publie. Génère."
Services : agents IA sur-mesure, automatisation workflows, blog SEO, contenu LinkedIn/Twitter
Différenciateur : humain + IA, pragmatique, résultats concrets, prix accessibles

Le pitch doit exister en 3 versions :
1. Pitch 30 secondes (ascenseur)
2. Pitch 2 minutes (réunion)
3. Pitch écrit LinkedIn (200 mots)

Style : humain, direct, centré sur les bénéfices concrets pour l'audience cible.
Pas de jargon tech inutile pour les non-initiés."""

        return self.think(prompt, max_tokens=800)

    # ── Run ────────────────────────────────────────────────────────────────────
    def run(self, task: dict) -> dict:
        """
        task = {
            "mode": "quarterly_plan" | "competitive" | "kpis" | "opportunities" | "monthly_report" | "pitch",
            "context": {...},
            "niche": "...",
            "audience": "pme" | "freelance" | "startup" | "afrique" | "linkedin"
        }
        """
        mode     = task.get("mode", "quarterly_plan")
        context  = task.get("context", {})
        niche    = task.get("niche", "automatisation-ia-france")
        audience = task.get("audience", "pme")

        self.log(f"Démarrage — mode={mode}")

        try:
            if mode == "quarterly_plan":
                content  = self.quarterly_plan(context)
                filepath = STRATEGY_DIR / f"plan_Q_{datetime.now().strftime('%Y%m')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            elif mode == "competitive":
                content  = self.competitive_analysis(niche)
                filepath = STRATEGY_DIR / f"competitive_{datetime.now().strftime('%Y%m%d')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            elif mode == "kpis":
                content  = self.define_kpis()
                filepath = STRATEGY_DIR / f"kpis_{datetime.now().strftime('%Y%m%d')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            elif mode == "opportunities":
                content  = self.opportunity_scan()
                filepath = STRATEGY_DIR / f"opportunities_{datetime.now().strftime('%Y%m%d')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            elif mode == "monthly_report":
                content  = self.monthly_strategy_report(context)
                filepath = STRATEGY_DIR / f"strategy_{datetime.now().strftime('%Y%m')}.md"
                filepath.write_text(content, encoding="utf-8")
                return {"agent": self.name, "status": "success", "content": content, "file": str(filepath)}

            elif mode == "pitch":
                content = self.generate_pitch(audience)
                return {"agent": self.name, "status": "success", "content": content}

            else:
                return {"agent": self.name, "status": "error", "message": f"Mode inconnu: {mode}"}

        except Exception as e:
            self.log(f"Erreur: {e}", level="ERROR")
            return {"agent": self.name, "status": "error", "error": str(e)}
