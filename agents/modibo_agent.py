"""
MODIBO — Directeur Juridique de WULIX
Génère CGV, contrats freelance, mentions légales, conseils RGPD
Prénom bambara — Mali
"""

import json
from datetime import datetime
from pathlib import Path
from .base_agent import BaseAgent

BASE_DIR    = Path(__file__).parent.parent
LEGAL_DIR   = BASE_DIR / "agents" / "legal"
LEGAL_DIR.mkdir(exist_ok=True)


class ModiboAgent(BaseAgent):
    """Agent Juridique — génère documents légaux et conseils conformité."""

    def __init__(self):
        super().__init__(
            name="Modibo",
            role="Directeur Juridique de WULIX",
            goal="Sécuriser juridiquement l'activité freelance : contrats, CGV, RGPD, mentions légales",
            backstory="""Tu es Modibo, directeur juridique de WULIX (WULIX.fr).
WULIX est une agence d'automatisation IA fondée par Omar Sylla, développeur freelance basé en France.
Tu as une expertise en droit du numérique français, droit des contrats, RGPD et propriété intellectuelle.
Tu rédiges des documents juridiques clairs, protecteurs et conformes au droit français.
Tu conseilles sur les risques légaux et proposes des solutions pragmatiques.
Tu parles français, style professionnel mais accessible."""
        )

    # ── Documents ─────────────────────────────────────────────────────────────
    def generate_cgv(self, context: dict) -> str:
        """Génère des CGV pour WULIX."""
        activite = context.get("activite", "développement web, agents IA et automatisation")
        tarif_horaire = context.get("tarif_horaire", "50-80€/h")
        delai_paiement = context.get("delai_paiement", "30 jours")

        prompt = f"""Rédige des Conditions Générales de Vente (CGV) complètes pour WULIX.

Activité : {activite}
Tarif indicatif : {tarif_horaire}
Délai de paiement : {delai_paiement}
Statut : Auto-entrepreneur / Freelance basé en France
Client type : PME, startups, entrepreneurs

Les CGV doivent couvrir :
1. Objet et champ d'application
2. Commandes et devis
3. Tarifs et modalités de paiement
4. Délais de livraison
5. Propriété intellectuelle (cession des droits à la livraison et paiement complet)
6. Confidentialité
7. Garantie et responsabilité limitée
8. Résiliation
9. Litiges et droit applicable (droit français)

Style : professionnel, clair, protecteur pour WULIX. Format markdown structuré."""

        return self.think(prompt, max_tokens=2000)

    def generate_contract(self, context: dict) -> str:
        """Génère un contrat de prestation freelance."""
        client = context.get("client", "Le Client")
        mission = context.get("mission", "Développement d'un agent IA sur-mesure")
        montant = context.get("montant", "À définir")
        duree = context.get("duree", "30 jours")

        prompt = f"""Rédige un contrat de prestation de services freelance entre WULIX et un client.

Prestataire : WULIX (Omar Sylla) — WULIX.fr
Client : {client}
Mission : {mission}
Montant : {montant}
Durée : {duree}

Le contrat doit inclure :
1. Identification des parties
2. Objet de la mission (description détaillée)
3. Livrables attendus
4. Planning et jalons
5. Rémunération et modalités de paiement (acompte 30% à la commande)
6. Propriété intellectuelle
7. Confidentialité (NDA intégré)
8. Obligations de chaque partie
9. Résiliation
10. Signature et date

Style : contrat professionnel français. Format markdown avec sections numérotées."""

        return self.think(prompt, max_tokens=2000)

    def generate_mentions_legales(self) -> str:
        """Génère les mentions légales pour WULIX.fr."""
        prompt = """Rédige les mentions légales complètes pour le site web WULIX.fr.

Éditeur : WULIX — Omar Sylla, auto-entrepreneur, France
Site : WULIX.fr
Activité : Conseil en systèmes d'information, développement IA et automatisation

Les mentions doivent inclure :
1. Éditeur du site (identité, SIRET, adresse, email)
2. Hébergeur
3. Propriété intellectuelle
4. Données personnelles (RGPD)
5. Cookies
6. Limitation de responsabilité
7. Droit applicable

Laisse des [PLACEHOLDER] pour les infos à compléter (SIRET, adresse exacte, etc.)
Format markdown structuré."""

        return self.think(prompt, max_tokens=1500)

    def generate_rgpd_policy(self) -> str:
        """Génère la politique de confidentialité RGPD."""
        prompt = """Rédige une politique de confidentialité RGPD complète pour WULIX.fr.

Contexte : site vitrine + formulaire de contact + blog
Données collectées : nom, email, message via formulaire de contact
Pas d'e-commerce, pas de compte utilisateur

La politique doit couvrir :
1. Responsable du traitement
2. Données collectées et finalités
3. Base légale du traitement
4. Durée de conservation
5. Droits des utilisateurs (accès, rectification, effacement, portabilité)
6. Cookies (analytics uniquement)
7. Sous-traitants (Formspree pour le formulaire, Netlify pour l'hébergement)
8. Contact DPO

Laisse [PLACEHOLDER] pour les infos à compléter.
Style : clair, accessible, conforme RGPD. Format markdown."""

        return self.think(prompt, max_tokens=1500)

    def legal_advice(self, question: str) -> str:
        """Répond à une question juridique liée à l'activité freelance."""
        prompt = f"""En tant que conseiller juridique spécialisé en droit du numérique français :

Question : {question}

Contexte : Omar Sylla est freelance (auto-entrepreneur) en France, activité développement IA et automatisation.

Réponds de manière pratique et claire. Indique les risques, les protections recommandées et les actions concrètes.
Précise si une consultation d'un vrai avocat est conseillée pour ce sujet.
Réponse en français, max 400 mots."""

        return self.think(prompt, max_tokens=600)

    # ── Sauvegarde ─────────────────────────────────────────────────────────────
    def save_document(self, doc_type: str, content: str, context: dict = None) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename  = f"{doc_type}_{timestamp}.md"
        filepath  = LEGAL_DIR / filename

        header = f"""---
type: {doc_type}
generated: {datetime.now().isoformat()}
agent: Modibo (Juridique)
---

"""
        filepath.write_text(header + content, encoding="utf-8")
        self.log(f"Document sauvegardé : {filepath}")
        return str(filepath)

    # ── Run ────────────────────────────────────────────────────────────────────
    def run(self, task: dict) -> dict:
        """
        task = {
            "mode": "cgv" | "contrat" | "mentions" | "rgpd" | "conseil",
            "context": {...},   # pour cgv et contrat
            "question": "..."   # pour conseil
        }
        """
        mode     = task.get("mode", "cgv")
        context  = task.get("context", {})
        question = task.get("question", "")

        self.log(f"Démarrage — mode={mode}")

        try:
            if mode == "cgv":
                content  = self.generate_cgv(context)
                filepath = self.save_document("cgv", content, context)
                result   = {"type": "cgv", "content": content, "file": filepath}

            elif mode == "contrat":
                content  = self.generate_contract(context)
                filepath = self.save_document("contrat", content, context)
                result   = {"type": "contrat", "content": content, "file": filepath}

            elif mode == "mentions":
                content  = self.generate_mentions_legales()
                filepath = self.save_document("mentions_legales", content)
                result   = {"type": "mentions", "content": content, "file": filepath}

            elif mode == "rgpd":
                content  = self.generate_rgpd_policy()
                filepath = self.save_document("rgpd_policy", content)
                result   = {"type": "rgpd", "content": content, "file": filepath}

            elif mode == "conseil":
                content = self.legal_advice(question)
                result  = {"type": "conseil", "question": question, "reponse": content}

            else:
                return {"agent": self.name, "status": "error", "message": f"Mode inconnu: {mode}"}

            self.log(f"✓ Document juridique généré : {mode}")
            return {"agent": self.name, "status": "success", **result}

        except Exception as e:
            self.log(f"Erreur: {e}", level="ERROR")
            return {"agent": self.name, "status": "error", "error": str(e)}
