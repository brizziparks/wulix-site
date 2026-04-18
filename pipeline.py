#!/usr/bin/env python3
"""
WULIX — Pipeline Auto-Deploy
Génère un article SEO → Build HTML → Deploy sur Netlify

Usage :
  python pipeline.py              ← pipeline complet (seo + build + deploy)
  python pipeline.py build        ← build + deploy seulement
  python pipeline.py deploy       ← deploy seulement (site déjà buildé)
  python pipeline.py seo          ← génère article seulement

Variables .env requises :
  NETLIFY_TOKEN   — Personal access token (Netlify → User settings → Applications)
  NETLIFY_SITE_ID — Site ID (Netlify → ton site → Site configuration → Site ID)
"""

import os
import sys
import json
import zipfile
import io
import subprocess
from pathlib import Path
from datetime import datetime

# Fix encodage Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR     = Path(__file__).parent
SITE_DIR     = BASE_DIR.parent / "nexflow-site"
BUILD_SCRIPT = SITE_DIR / "build_site.py"
LOG_FILE     = BASE_DIR / "agents" / "pipeline_log.json"

# Charge le .env
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    # Lecture manuelle si dotenv pas dispo
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


# ── Étape 1 : Générer un article SEO ─────────────────────────────────────────
def step_seo(niche: str = "all") -> dict:
    print("\n📝 ÉTAPE 1 — Génération article SEO (Koumba)")
    print("-" * 45)
    sys.path.insert(0, str(BASE_DIR))
    from agents import SeoWriterAgent

    agent  = SeoWriterAgent()
    result = agent.run({"mode": "single", "niche": niche})
    arts   = result.get("results", [])

    for art in arts:
        if art.get("status") == "success":
            print(f"  ✅ [{art['niche']}] {art['title']}")
            print(f"     → {art['file']}")
        else:
            print(f"  ❌ Erreur : {art.get('error', '?')}")

    return result


# ── Étape 2 : Build HTML ──────────────────────────────────────────────────────
def step_build() -> bool:
    print("\n🏗️  ÉTAPE 2 — Build site HTML (build_site.py)")
    print("-" * 45)

    if not BUILD_SCRIPT.exists():
        print(f"  ❌ build_site.py introuvable : {BUILD_SCRIPT}")
        return False

    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
        cwd=str(SITE_DIR), env=env
    )

    for line in (result.stdout + result.stderr).splitlines():
        if line.strip():
            print(f"  {line}")

    success = result.returncode == 0
    if success:
        print("  ✅ Build terminé")
    else:
        print(f"  ❌ Build échoué (code {result.returncode})")
    return success


# ── Étape 3 : Deploy Netlify via API ─────────────────────────────────────────
def step_deploy() -> dict:
    print("\n🚀 ÉTAPE 3 — Déploiement Netlify")
    print("-" * 45)

    token   = os.environ.get("NETLIFY_TOKEN", "").strip()
    site_id = os.environ.get("NETLIFY_SITE_ID", "").strip()

    if not token:
        print("  ❌ NETLIFY_TOKEN manquant dans .env")
        print("     → Netlify → User settings → Applications → New access token")
        return {"status": "error", "reason": "missing NETLIFY_TOKEN"}

    if not site_id:
        print("  ❌ NETLIFY_SITE_ID manquant dans .env")
        print("     → Netlify → ton site → Site configuration → Site ID")
        return {"status": "error", "reason": "missing NETLIFY_SITE_ID"}

    if not SITE_DIR.exists():
        print(f"  ❌ Dossier site introuvable : {SITE_DIR}")
        return {"status": "error", "reason": "site_dir not found"}

    # Crée un ZIP en mémoire du dossier site
    print("  📦 Compression du site...")
    zip_buffer = io.BytesIO()
    files_count = 0

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in SITE_DIR.rglob("*"):
            if file_path.is_file():
                # Exclut les fichiers inutiles
                rel = file_path.relative_to(SITE_DIR)
                skip_patterns = [".git", "__pycache__", ".DS_Store", "*.py", "*.pyc"]
                should_skip = any(
                    part.startswith(".") or part == "__pycache__"
                    for part in rel.parts
                ) or file_path.suffix == ".py" or file_path.suffix == ".pyc"

                if not should_skip:
                    zf.write(file_path, rel)
                    files_count += 1

    zip_size_kb = len(zip_buffer.getvalue()) // 1024
    print(f"  📦 {files_count} fichiers — {zip_size_kb} KB")

    # Envoie à Netlify API
    print("  ⬆️  Upload vers Netlify...")
    try:
        import requests
        zip_buffer.seek(0)
        resp = requests.post(
            f"https://api.netlify.com/api/v1/sites/{site_id}/deploys",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/zip",
            },
            data=zip_buffer.read(),
            timeout=120,
        )

        if resp.status_code in (200, 201):
            data = resp.json()
            deploy_id  = data.get("id", "?")
            deploy_url = data.get("deploy_ssl_url") or data.get("ssl_url") or data.get("url", "")
            print(f"  ✅ Déploiement lancé !")
            print(f"     ID      : {deploy_id}")
            print(f"     URL     : {deploy_url}")
            return {"status": "success", "deploy_id": deploy_id, "url": deploy_url}
        else:
            print(f"  ❌ Erreur API Netlify : {resp.status_code}")
            print(f"     {resp.text[:300]}")
            return {"status": "error", "code": resp.status_code, "detail": resp.text[:300]}

    except ImportError:
        print("  ❌ Module 'requests' manquant — pip install requests")
        return {"status": "error", "reason": "requests not installed"}
    except Exception as e:
        print(f"  ❌ Erreur : {e}")
        return {"status": "error", "reason": str(e)}


# ── Log ───────────────────────────────────────────────────────────────────────
def save_log(run: dict):
    LOG_FILE.parent.mkdir(exist_ok=True)
    logs = []
    if LOG_FILE.exists():
        try:
            logs = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    logs.append(run)
    logs = logs[-50:]  # garde les 50 derniers runs
    LOG_FILE.write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Pipeline principal ────────────────────────────────────────────────────────
def run_pipeline(mode: str = "full", niche: str = "all") -> dict:
    start = datetime.now()
    print(f"\n{'='*50}")
    print(f"  🤖 WULIX PIPELINE — {mode.upper()}")
    print(f"  {start.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}")

    log = {
        "date": start.isoformat(),
        "mode": mode,
        "seo": None,
        "build": None,
        "deploy": None,
    }

    # Étape SEO
    if mode in ("full", "seo"):
        seo_result = step_seo(niche)
        log["seo"] = {
            "articles": seo_result.get("articles_generated", 0),
            "results":  [r.get("slug") for r in seo_result.get("results", []) if r.get("status") == "success"]
        }
        if mode == "seo":
            save_log(log)
            return log

    # Étape Build
    if mode in ("full", "build"):
        ok = step_build()
        log["build"] = "success" if ok else "failed"
        if not ok and mode == "full":
            print("\n  ⚠️  Build échoué — déploiement annulé")
            save_log(log)
            return log
        if mode == "build":
            # Pour le mode build seul, on déploie quand même
            pass

    # Étape Deploy
    if mode in ("full", "build", "deploy"):
        deploy_result = step_deploy()
        log["deploy"] = deploy_result

    duration = (datetime.now() - start).seconds
    print(f"\n{'='*50}")
    print(f"  ✅ Pipeline terminé en {duration}s")
    print(f"{'='*50}\n")

    save_log(log)
    return log


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]
    mode  = args[0] if args else "full"
    niche = args[1] if len(args) > 1 else "all"
    run_pipeline(mode, niche)
