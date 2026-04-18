# =============================================================================
# WULIX — Pack Automatisation PME
# Script  : web_scraper.py
# Version : 1.0.0
# Auteur  : WULIX (wulix.fr)
# Licence : Usage commercial autorisé — redistribution interdite
# =============================================================================
# DESCRIPTION :
#   Scraper générique pour sites e-commerce. Extrait titres, prix et
#   descriptions depuis une ou plusieurs pages. Sauvegarde les résultats
#   en CSV. Inclut rotation d'user-agents et gestion des erreurs robuste.
#
# UTILISATION :
#   1. Configure les variables ci-dessous (URL, sélecteurs CSS)
#   2. Installe les dépendances : pip install requests beautifulsoup4
#   3. Lance : python web_scraper.py
#
# DÉPENDANCES :
#   pip install requests beautifulsoup4
# =============================================================================

import csv
import time
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

URLS_A_SCRAPER = [
    "https://books.toscrape.com/",  # Site de démo gratuit pour tests
    # "https://ton-site-ecommerce.fr/produits",
]

# Sélecteurs CSS — adapte selon le site cible (F12 dans le navigateur)
SELECTEUR_PRODUIT     = "article.product_pod"
SELECTEUR_TITRE       = "h3 a"
SELECTEUR_PRIX        = "p.price_color"
SELECTEUR_DESCRIPTION = "p.instock"

DELAI_MIN_SECONDES = 1
DELAI_MAX_SECONDES = 3
NB_TENTATIVES_MAX  = 3
TIMEOUT_REQUETE    = 10

FICHIER_SORTIE = f"produits_scrapes_{datetime.today().strftime('%Y%m%d_%H%M')}.csv"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
]


def get_headers():
    return {
        "User-Agent"      : random.choice(USER_AGENTS),
        "Accept-Language" : "fr-FR,fr;q=0.9,en;q=0.8",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept"          : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection"      : "keep-alive",
    }


def telecharger_page(url, tentative=1):
    if tentative > NB_TENTATIVES_MAX:
        print(f"[ÉCHEC] {url} — abandon après {NB_TENTATIVES_MAX} tentatives")
        return None
    try:
        if tentative > 1:
            delai = random.uniform(DELAI_MIN_SECONDES * tentative, DELAI_MAX_SECONDES * tentative)
            print(f"[ATTENTE] Tentative {tentative} — pause {delai:.1f}s...")
            time.sleep(delai)
        response = requests.get(url, headers=get_headers(), timeout=TIMEOUT_REQUETE)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.exceptions.HTTPError as e:
        print(f"[ERREUR HTTP] {url} : {e}")
        return telecharger_page(url, tentative + 1)
    except requests.exceptions.ConnectionError:
        print(f"[ERREUR RÉSEAU] Impossible de se connecter à {url}")
        return telecharger_page(url, tentative + 1)
    except requests.exceptions.Timeout:
        print(f"[TIMEOUT] {url} — délai dépassé ({TIMEOUT_REQUETE}s)")
        return telecharger_page(url, tentative + 1)
    except Exception as e:
        print(f"[ERREUR] {url} : {e}")
        return None


def extraire_produits(html, url_source):
    produits = []
    soup = BeautifulSoup(html, 'html.parser')
    conteneurs = soup.select(SELECTEUR_PRODUIT)

    if not conteneurs:
        print(f"[AVERTISSEMENT] Aucun produit trouvé sur {url_source}")
        print(f"  Vérifie le sélecteur CSS : '{SELECTEUR_PRODUIT}'")
        return produits

    for conteneur in conteneurs:
        try:
            el_titre = conteneur.select_one(SELECTEUR_TITRE)
            titre = el_titre.get('title') or el_titre.get_text(strip=True) if el_titre else "N/A"

            el_prix = conteneur.select_one(SELECTEUR_PRIX)
            prix = el_prix.get_text(strip=True) if el_prix else "N/A"

            el_desc = conteneur.select_one(SELECTEUR_DESCRIPTION)
            description = el_desc.get_text(strip=True) if el_desc else "N/A"

            produits.append({
                'titre'      : titre,
                'prix'       : prix,
                'description': description,
                'url_source' : url_source,
                'date_scrape': datetime.today().strftime('%Y-%m-%d %H:%M'),
            })
        except Exception as e:
            print(f"[AVERTISSEMENT] Extraction d'un produit échouée : {e}")
            continue
    return produits


def sauvegarder_csv(produits, chemin_sortie):
    if not produits:
        print("[INFO] Aucun produit à sauvegarder.")
        return
    colonnes = ['titre', 'prix', 'description', 'url_source', 'date_scrape']
    try:
        with open(chemin_sortie, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=colonnes)
            writer.writeheader()
            writer.writerows(produits)
        print(f"[SAUVEGARDÉ] {len(produits)} produit(s) -> {chemin_sortie}")
    except Exception as e:
        print(f"[ERREUR] Sauvegarde CSV échouée : {e}")


def main():
    print("=" * 55)
    print("  WULIX — Web Scraper E-commerce")
    print(f"  {datetime.today().strftime('%d/%m/%Y %H:%M')} | {len(URLS_A_SCRAPER)} URL(s)")
    print("=" * 55)

    tous_les_produits = []

    for i, url in enumerate(URLS_A_SCRAPER, 1):
        print(f"\n[{i}/{len(URLS_A_SCRAPER)}] Scraping : {url}")
        html = telecharger_page(url)
        if not html:
            continue
        produits = extraire_produits(html, url)
        tous_les_produits.extend(produits)
        print(f"  -> {len(produits)} produit(s) extrait(s)")

        if i < len(URLS_A_SCRAPER):
            pause = random.uniform(DELAI_MIN_SECONDES, DELAI_MAX_SECONDES)
            print(f"  Pause {pause:.1f}s avant la prochaine URL...")
            time.sleep(pause)

    sauvegarder_csv(tous_les_produits, FICHIER_SORTIE)
    print(f"\n  Total : {len(tous_les_produits)} produit(s) scrapé(s)")


if __name__ == "__main__":
    main()
