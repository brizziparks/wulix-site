"""
BACKUP — Agent de sauvegarde automatique
Copie tous les fichiers JSON importants dans agents/backups/YYYYMMDD/
Conserve les 7 derniers backups.
Recommandation ADAMA audit #1 : système de sauvegarde automatique.
"""
import json
import shutil
import datetime
from pathlib import Path

BASE_DIR   = Path(__file__).parent
BACKUP_DIR = BASE_DIR / "backups"
LOG_DIR    = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

# Fichiers et dossiers à sauvegarder
TARGETS = [
    BASE_DIR / "tasks_config.json",
    BASE_DIR / "tasks_log.json",
    BASE_DIR / "content_queue.json",
    BASE_DIR / "prospects.json",
    BASE_DIR / "outreach_queue.json",
    BASE_DIR / "daily_report.json",
    BASE_DIR / "blog_queue.json",
    BASE_DIR / "pipeline_log.json",
    BASE_DIR / "email_templates.json",
    BASE_DIR.parent / "memory" / "facts.md",
    BASE_DIR.parent / "memory" / "activity_log.md",
]


def log(msg: str):
    ts   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] BACKUP | {msg}"
    print(line)
    with open(LOG_DIR / "backup.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run_backup() -> dict:
    today     = datetime.date.today().strftime("%Y%m%d")
    dest_dir  = BACKUP_DIR / today
    dest_dir.mkdir(exist_ok=True)

    copied  = []
    skipped = []

    for src in TARGETS:
        if not src.exists():
            skipped.append(str(src.name))
            continue
        dest = dest_dir / src.name
        try:
            shutil.copy2(src, dest)
            copied.append(src.name)
        except Exception as e:
            log(f"Erreur copie {src.name}: {e}")
            skipped.append(src.name)

    # Sauvegarde du dossier finance complet
    finance_src = BASE_DIR / "finance"
    if finance_src.exists():
        finance_dest = dest_dir / "finance"
        try:
            if finance_dest.exists():
                shutil.rmtree(finance_dest)
            shutil.copytree(finance_src, finance_dest)
            copied.append("finance/")
        except Exception as e:
            log(f"Erreur copie finance/: {e}")

    log(f"Backup {today} : {len(copied)} fichiers copiés, {len(skipped)} manquants")

    # Nettoyage : garde les 7 derniers backups
    all_backups = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir()])
    if len(all_backups) > 7:
        to_delete = all_backups[:-7]
        for old in to_delete:
            try:
                shutil.rmtree(old)
                log(f"Backup supprimé (rotation) : {old.name}")
            except Exception as e:
                log(f"Erreur suppression {old.name}: {e}")

    # Écrit un fichier manifeste
    manifest = {
        "date":    today,
        "ts":      datetime.datetime.now().isoformat(),
        "copied":  copied,
        "skipped": skipped,
        "backups_kept": [d.name for d in sorted(BACKUP_DIR.iterdir()) if d.is_dir()]
    }
    (dest_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return manifest


def run():
    log("Démarrage BACKUP")
    result = run_backup()
    print(f"\n✅ Backup terminé : {len(result['copied'])} fichiers")
    print(f"   Fichiers : {', '.join(result['copied'])}")
    if result['skipped']:
        print(f"   Non trouvés : {', '.join(result['skipped'])}")
    print(f"   Backups conservés : {', '.join(result['backups_kept'])}")
    log("BACKUP terminé")


if __name__ == "__main__":
    run()
