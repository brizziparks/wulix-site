# =============================================================================
# WULIX — Gumroad Covers Upload
# Script  : gumroad_covers_upload.py
# Version : 1.0.0
# Description : Upload les covers et active shown_on_profile pour chaque produit
# Usage   : python agents/gumroad_covers_upload.py [--dry-run]
# =============================================================================

import requests
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

TOKEN    = os.getenv("GUMROAD_ACCESS_TOKEN", "2aSxUJz6nAfkjaAqqQcpe138NlaG6ENj9HoBPbFbKLg")
BASE_URL = "https://api.gumroad.com/v2"
BASE_DIR = Path(__file__).parent.parent

# =============================================================================
# MAPPING : produit → fichier cover
# =============================================================================
# Clé = sous-chaîne présente dans l'URL du produit (slug)
COVER_MAP = {
    "scripts-python"   : BASE_DIR / "ui/covers/cover_pack_scripts_python.png",
    "guide-automatisation": BASE_DIR / "ui/covers/cover_guide_automatisation.png",
    "pipeline-linkedin": BASE_DIR / "ui/covers/cover_pipeline_linkedin.png",
    "n8n-linkedin"     : BASE_DIR / "ui/covers/cover_pipeline_linkedin.png",
    "prompts"          : BASE_DIR / "agents/content/gumroad_pack/cover_prompts_ia.png",
    "bundle"           : BASE_DIR / "agents/content/gumroad_pack/cover_bundle_complet.png",
    "n8n-templates"    : BASE_DIR / "agents/content/gumroad_pack/cover_n8n_templates.png",
    "iozlxv"           : BASE_DIR / "agents/content/gumroad_pack/cover_prompts_ia.png",
}


def get_headers():
    return {"Authorization": f"Bearer {TOKEN}"}


def list_products():
    r = requests.get(f"{BASE_URL}/products", headers=get_headers(), timeout=15)
    r.raise_for_status()
    return r.json().get("products", [])


def find_cover(product):
    """Trouve le fichier cover associé au produit."""
    url = (product.get("short_url") or product.get("url") or "").lower()
    name = (product.get("name") or "").lower()
    combined = url + " " + name
    for slug, path in COVER_MAP.items():
        if slug in combined:
            return path
    return None


def upload_cover(product_id: str, cover_path: Path):
    """Upload une cover image via multipart/form-data."""
    with open(cover_path, "rb") as f:
        files = {"cover": (cover_path.name, f, "image/png")}
        r = requests.put(
            f"{BASE_URL}/products/{product_id}",
            headers=get_headers(),
            files=files,
            timeout=30,
        )
    return r


def activate_profile(product_id: str):
    """Active shown_on_profile pour que le produit apparaisse sur wulix.gumroad.com."""
    r = requests.put(
        f"{BASE_URL}/products/{product_id}",
        headers=get_headers(),
        data={"shown_on_profile": "true", "published": "true"},
        timeout=15,
    )
    return r


def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print("  WULIX — Gumroad Covers Upload")
    print("=" * 60)
    if dry_run:
        print("  [DRY-RUN] Simulation — aucun changement\n")

    try:
        products = list_products()
    except Exception as e:
        print(f"[ERREUR] API Gumroad : {e}")
        sys.exit(1)

    print(f"[INFO] {len(products)} produit(s) trouves\n")

    for p in products:
        pid  = p.get("id", "?")
        name = p.get("name", "?")
        url  = p.get("short_url") or p.get("url", "")
        shown = p.get("shown_on_profile", False)
        has_cover = bool(p.get("cover_url") or p.get("preview_url"))

        print(f"  [PRODUIT] {name}")
        print(f"     ID      : {pid}")
        print(f"     URL     : {url}")
        print(f"     Profile : {'oui' if shown else 'NON'}")
        print(f"     Cover   : {'oui' if has_cover else 'NON'}")

        cover_path = find_cover(p)

        if cover_path:
            if not cover_path.exists():
                print(f"     [WARN] Fichier cover introuvable : {cover_path}")
                cover_path = None
            else:
                print(f"     Cover trouvee : {cover_path.name}")

        if not cover_path:
            print(f"     [SKIP] Aucune cover mappee pour ce produit")

        if dry_run:
            if cover_path:
                print(f"     [DRY] Uploaderait : {cover_path.name}")
            if not shown:
                print(f"     [DRY] Activerait shown_on_profile")
            print()
            continue

        # Upload cover si disponible
        if cover_path:
            try:
                r = upload_cover(pid, cover_path)
                if r.ok:
                    print(f"     [OK] Cover uploadee ({cover_path.name})")
                elif r.status_code == 422:
                    print(f"     [WARN] Cover rejetee (format?) — essai sans cover")
                    print(f"     Reponse : {r.text[:120]}")
                else:
                    print(f"     [ERREUR] Cover : {r.status_code} — {r.text[:120]}")
            except Exception as e:
                print(f"     [ERREUR] Upload : {e}")

        # Activer shown_on_profile
        try:
            r = activate_profile(pid)
            if r.ok:
                data = r.json().get("product", {})
                if data.get("shown_on_profile"):
                    print(f"     [OK] shown_on_profile actif")
                else:
                    print(f"     [OK] Produit mis a jour")
            else:
                print(f"     [ERREUR] Profile : {r.status_code} — {r.text[:80]}")
        except Exception as e:
            print(f"     [ERREUR] Profile : {e}")

        print()

    if not dry_run:
        print("[OK] Traitement termine !")
        print("     Verifie sur : https://wulix.gumroad.com/")


if __name__ == "__main__":
    main()
