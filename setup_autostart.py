"""
Autostart AISATOU — enregistre une tâche planifiée Windows au démarrage.
Lance automatiquement le HUD AISATOU quand Windows démarre.

Usage : python setup_autostart.py [--remove]
"""

import os
import sys
import subprocess
from pathlib import Path

BASE_DIR    = Path(__file__).parent
TASK_NAME   = "AISATOU_HUD_Autostart"
PYTHON_EXE  = sys.executable
SCRIPT_PATH = BASE_DIR / "aisatou_hud.py"

# Script batch intermédiaire pour lancement propre (fenêtre minimisée)
BAT_PATH = BASE_DIR / "start_aisatou.bat"


def create_launcher_bat():
    """Crée un fichier .bat pour lancer le HUD en arrière-plan."""
    content = f"""@echo off
TITLE AISATOU HUD
cd /d "{BASE_DIR}"
"{PYTHON_EXE}" "{SCRIPT_PATH}"
"""
    BAT_PATH.write_text(content, encoding="utf-8")
    return str(BAT_PATH)


def register_autostart():
    """Enregistre la tâche planifiée Windows au démarrage de session."""
    bat = create_launcher_bat()

    cmd = [
        "schtasks", "/Create",
        "/TN", TASK_NAME,
        "/TR", f'"{bat}"',
        "/SC", "ONLOGON",
        "/RL", "HIGHEST",
        "/F",        # Écraser si existe déjà
        "/DELAY", "0001:00",   # Délai 1 minute après logon
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            print(f"✅ Tâche '{TASK_NAME}' créée.")
            print(f"   AISATOU démarrera automatiquement à chaque connexion Windows.")
            print(f"   Délai : 1 minute après connexion (pour laisser le réseau démarrer).")
            return True
        else:
            print(f"❌ Erreur schtasks : {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False


def remove_autostart():
    """Supprime la tâche planifiée."""
    cmd = ["schtasks", "/Delete", "/TN", TASK_NAME, "/F"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            print(f"✅ Tâche '{TASK_NAME}' supprimée — AISATOU ne démarrera plus automatiquement.")
        else:
            print(f"❌ Erreur : {result.stderr}")
    except Exception as e:
        print(f"❌ Erreur : {e}")


def check_autostart() -> bool:
    """Vérifie si la tâche existe."""
    cmd = ["schtasks", "/Query", "/TN", TASK_NAME]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except Exception:
        return False


if __name__ == "__main__":
    if "--remove" in sys.argv:
        remove_autostart()
    elif "--check" in sys.argv:
        exists = check_autostart()
        print(f"Autostart AISATOU : {'✅ actif' if exists else '❌ non configuré'}")
    else:
        print(f"Configuration autostart AISATOU HUD...")
        print(f"  Script  : {SCRIPT_PATH}")
        print(f"  Python  : {PYTHON_EXE}")
        print()
        register_autostart()
        print()
        print("Pour désactiver : python setup_autostart.py --remove")
