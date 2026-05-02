# =============================================================================
# WULIX — GUMROAD Product Description Updater
# Script  : gumroad_updater.py
# Version : 1.0.0
# Description : Met à jour les descriptions des produits Gumroad via l'API
# Usage   : python gumroad_updater.py [--dry-run] [--list]
# =============================================================================

import requests
import json
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN", "2aSxUJz6nAfkjaAqqQcpe138NlaG6ENj9HoBPbFbKLg")
BASE_URL = "https://api.gumroad.com/v2"

# =============================================================================
# NOUVELLES DESCRIPTIONS — optimisées conversion
# =============================================================================

DESCRIPTIONS = {
    # Pack Scripts Python
    "scripts_python": {
        "match": ["script", "python"],
        "description": """<h2>5 scripts Python prets a l'emploi pour automatiser votre business</h2>

<p><strong>Economisez 5 a 10 heures par semaine</strong> avec ces scripts testes en conditions reelles sur l'activite freelance de WULIX.</p>

<h3>Ce que vous obtenez :</h3>
<ul>
<li><strong>Relanceur email automatique</strong> — Detecte les devis sans reponse dans Google Sheets et envoie des relances personnalisees par Gmail.</li>
<li><strong>Rapport hebdo automatique</strong> — Compile vos stats (Gumroad, Fiverr) et vous les envoie chaque lundi matin.</li>
<li><strong>Web scraper de leads</strong> — Identifie sur Reddit les personnes qui cherchent exactement vos services.</li>
<li><strong>Planificateur LinkedIn</strong> — Publie vos posts LinkedIn automatiquement selon un calendrier.</li>
<li><strong>Organisateur de fichiers</strong> — Trie automatiquement vos telechargements et projets par type et date.</li>
</ul>

<h3>Pourquoi ce pack ?</h3>
<p>Pas de SaaS, pas d'abonnement, pas de no-code fragile. Du Python pur que vous possedez, comprenez et modifiez comme vous voulez. Chaque script est documente ligne par ligne.</p>

<h3>Prerequis :</h3>
<p>Python 3.10+, librairies incluses dans requirements.txt. Niveau debutant suffisant.</p>

<h3>Support inclus :</h3>
<p>Une question ? Ecrivez a contact@wulix.fr — reponse sous 24h.</p>

<p><em>Ce pack est utilise par WULIX pour gerer son activite freelance au quotidien.</em></p>""",
    },
    # Guide PDF
    "guide_pdf": {
        "match": ["guide", "weekend", "sans coder", "tache"],
        "description": """<h2>Automatisez 5 taches repetitives ce weekend — sans ecrire une seule ligne de code</h2>

<p>Le guide pratique pour les entrepreneurs et freelances qui veulent recuperer du temps sans apprendre a programmer.</p>

<h3>Ce que vous apprenez :</h3>
<ul>
<li><strong>Identifier vos 5 taches les plus automatisables</strong> — methode rapide en 20 minutes</li>
<li><strong>Choisir le bon outil</strong> — n8n, Make.com, Zapier : lequel pour quel cas</li>
<li><strong>5 workflows concrets</strong> avec captures d'ecran pas a pas</li>
<li><strong>Integrer l'IA gratuitement</strong> — ChatGPT et Claude dans vos automatisations</li>
<li><strong>Deployer sans serveur</strong> — vos workflows tournent seuls, 24h/24</li>
</ul>

<h3>Resultats typiques :</h3>
<p>3 a 8 heures recuperees par semaine. ROI en moins d'une semaine.</p>

<h3>Format :</h3>
<p>PDF de 35 pages avec captures d'ecran et liens vers les outils. Applicable en 1 weekend.</p>

<p><strong>Garantie :</strong> Si le guide ne vous apporte pas au moins 1 automatisation applicable immediatement, remboursement integral — aucune question posee.</p>""",
    },
    # Pack Prompts IA
    "prompts": {
        "match": ["prompt", "chatgpt", "claude", "redige"],
        "description": """<h2>50 prompts IA testes pour automatiser, rediger et analyser — ChatGPT et Claude</h2>

<p>La collection de prompts que j'utilise chaque semaine pour aller 3x plus vite dans mon travail.</p>

<h3>Categories incluses :</h3>
<ul>
<li><strong>Automatisation</strong> — Generez du code Python/n8n a partir d'une description en francais</li>
<li><strong>Redaction</strong> — Emails clients, posts LinkedIn, articles de blog, propositions commerciales</li>
<li><strong>Analyse</strong> — Analyser une concurrence, un marche, un brief client en quelques secondes</li>
<li><strong>Productivite</strong> — Resumes, to-do lists, plans de projet, compte-rendus de reunion</li>
<li><strong>Commercial</strong> — Relances, devis, argumentaires, reponses aux objections</li>
</ul>

<h3>Format :</h3>
<p>Fichier PDF + Notion database. Chaque prompt inclut un exemple d'entree et de sortie.</p>

<p>Compatible ChatGPT (3.5, 4, 4o), Claude (Haiku, Sonnet, Opus) et Gemini.</p>

<p><em>Ces prompts sont actuellement utilises par l'equipe WULIX dans notre production quotidienne.</em></p>""",
    },
    # Template n8n Pack 3
    "n8n_pack": {
        "match": ["pack 3", "templates n8n", "pack.*n8n"],
        "description": """<h2>3 workflows n8n prets a deployer — Automatisation IA</h2>

<p>Des workflows n8n complets et documentes, testables en 5 minutes sur votre instance n8n (cloud ou self-hosted).</p>

<h3>Workflows inclus :</h3>
<ul>
<li><strong>Agent de veille IA</strong> — Scrape les dernieres news sur vos sujets, les resumes avec l'IA et vous les envoie par email chaque matin</li>
<li><strong>Pipeline de leads Reddit</strong> — Detecte automatiquement les posts ou les gens cherchent vos services, genere un message d'approche personnalise</li>
<li><strong>Relance email automatique</strong> — Surveille votre Google Sheets de devis et declenche des relances au bon moment</li>
</ul>

<h3>Ce que vous recevez :</h3>
<ul>
<li>3 fichiers JSON importables directement dans n8n</li>
<li>Guide d'installation pour chaque workflow (credentials, parametres)</li>
<li>Variables a configurer clairement identifiees</li>
</ul>

<h3>Prerequis :</h3>
<p>Instance n8n (gratuit en self-hosted ou plan Cloud). Comptes OpenAI ou Gemini (gratuit) pour les noeuds IA.</p>

<p>Support : contact@wulix.fr</p>""",
    },
    # Template n8n LinkedIn
    "n8n_linkedin": {
        "match": ["linkedin", "pipeline linkedin"],
        "description": """<h2>Template n8n — Pipeline LinkedIn automatise de A a Z</h2>

<p>Le workflow n8n complet pour publier sur LinkedIn sans y penser. Alimentez-le en contenu, il gere le reste.</p>

<h3>Ce que fait ce workflow :</h3>
<ul>
<li><strong>Planification</strong> — Publie automatiquement selon votre calendrier (1/jour, 3/semaine...)</li>
<li><strong>Generation IA</strong> — Transforme vos idees brutes en posts LinkedIn optimises (accroche, corps, hashtags)</li>
<li><strong>Posting automatique</strong> — Publie via l'API LinkedIn officielle</li>
<li><strong>Suivi</strong> — Log chaque publication dans Google Sheets avec date et statut</li>
</ul>

<h3>Ce que vous recevez :</h3>
<ul>
<li>Fichier JSON du workflow (import direct dans n8n)</li>
<li>Guide de configuration de l'API LinkedIn (OAuth2)</li>
<li>Template Google Sheets pour alimenter le pipeline</li>
<li>20 exemples de structures de posts LinkedIn qui fonctionnent</li>
</ul>

<h3>Prerequis :</h3>
<p>n8n (cloud ou self-hosted), compte LinkedIn, compte OpenAI ou Gemini.</p>

<p>Ce template est utilise par WULIX pour publier du contenu LinkedIn automatiquement chaque semaine.</p>

<p>Support : contact@wulix.fr</p>""",
    },
}

DEFAULT_DESCRIPTION = """<h2>🚀 Automatisez votre business avec WULIX</h2>

<p>Scripts Python, agents IA et workflows n8n pour les freelances et entrepreneurs qui veulent récupérer du temps.</p>

<p><strong>Garantie satisfaction :</strong> remboursement sous 7 jours si vous n'êtes pas satisfait.</p>
<p><strong>Support :</strong> contact@wulix.fr — réponse sous 24h.</p>"""

# =============================================================================
# FONCTIONS API
# =============================================================================

def get_headers():
    return {"Authorization": f"Bearer {TOKEN}"}


def list_products():
    """Récupère tous les produits Gumroad."""
    r = requests.get(f"{BASE_URL}/products", headers=get_headers(), timeout=15)
    r.raise_for_status()
    return r.json().get("products", [])


def update_product(product_id: str, payload: dict):
    """Met à jour un produit Gumroad."""
    r = requests.put(
        f"{BASE_URL}/products/{product_id}",
        headers=get_headers(),
        data=payload,
        timeout=15
    )
    r.raise_for_status()
    return r.json()


def match_description(product):
    """Trouve la description appropriee pour un produit."""
    name = (product.get("name") or "").lower()
    url = (product.get("short_url") or product.get("url") or "").lower()
    combined = name + " " + url

    # Matching par URL slug en priorite (plus fiable)
    if "scripts-python" in url or ("script" in combined and "python" in combined):
        return DESCRIPTIONS["scripts_python"]["description"]
    if "guide-automatisation" in url or "weekend" in combined or "sans coder" in combined:
        return DESCRIPTIONS["guide_pdf"]["description"]
    if "iozlxv" in url or "prompt" in combined:
        return DESCRIPTIONS["prompts"]["description"]
    if "n8n-linkedin" in url or "linkedin" in combined:
        return DESCRIPTIONS["n8n_linkedin"]["description"]
    if "n8n-templates" in url or ("n8n" in combined and "template" in combined):
        return DESCRIPTIONS["n8n_pack"]["description"]

    # Fallback par mots-cles dans le nom
    for key, cfg in DESCRIPTIONS.items():
        if any(kw in combined for kw in cfg["match"]):
            return cfg["description"]

    return DEFAULT_DESCRIPTION


# =============================================================================
# MAIN
# =============================================================================

def main():
    dry_run = "--dry-run" in sys.argv
    list_only = "--list" in sys.argv

    print("=" * 60)
    print("  WULIX — Gumroad Product Updater")
    print("=" * 60)

    try:
        products = list_products()
    except Exception as e:
        print(f"[ERREUR] Impossible de récupérer les produits : {e}")
        sys.exit(1)

    if not products:
        print("[INFO] Aucun produit trouvé sur Gumroad.")
        return

    print(f"[INFO] {len(products)} produit(s) trouvé(s)\n")

    for p in products:
        pid = p.get("id", "?")
        name = p.get("name", "Sans nom")
        price = p.get("price", 0)
        sales = p.get("sales_count", 0)
        url = p.get("short_url") or p.get("url", "")

        print(f"  [PRODUIT] {name}")
        print(f"     ID    : {pid}")
        print(f"     Prix  : {price/100:.2f}EUR")
        print(f"     Ventes: {sales}")
        print(f"     URL   : {url}")

        if list_only:
            print()
            continue

        new_desc = match_description(p)

        if dry_run:
            print(f"     [DRY-RUN] Description serait mise à jour ({len(new_desc)} chars)")
        else:
            try:
                update_product(pid, {"description": new_desc})
                print(f"     [OK] Description mise a jour ({len(new_desc)} chars)")
            except Exception as e:
                print(f"     [ERREUR] : {e}")

        print()

    if dry_run:
        print("[INFO] Mode dry-run — relancez sans --dry-run pour appliquer les changements.")
    elif not list_only:
        print("[OK] Toutes les descriptions ont été mises à jour !")
        print("     Vérifiez sur : https://app.gumroad.com/products")


if __name__ == "__main__":
    main()
