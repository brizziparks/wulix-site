"""
Hermes Agent integration — délègue des tâches techniques lourdes à Hermes (NousResearch)
qui tourne dans WSL2 Ubuntu.

AISATOU appelle Hermes pour :
- Refactor/écriture de code longue
- Browser automation (Playwright)
- Tâches qui demandent un environnement Linux isolé
- Skills Hermes spécifiques (89 skills built-in : architecture-diagram, design-md, manim-video, opencode, etc.)
"""

import subprocess
import shlex
import os
from pathlib import Path

WSL_EXE     = r"C:\Windows\System32\wsl.exe"
HERMES_BIN  = "/usr/local/bin/hermes"
DISTRO      = "Ubuntu"
DEFAULT_TIMEOUT = 180  # 3 minutes max par défaut


def _check_wsl_available() -> bool:
    """Vérifie que WSL Ubuntu + Hermes sont installés."""
    if not Path(WSL_EXE).exists():
        return False
    try:
        r = subprocess.run(
            [WSL_EXE, "-d", DISTRO, "--", "test", "-x", HERMES_BIN],
            capture_output=True, timeout=5
        )
        return r.returncode == 0
    except Exception:
        return False


def hermes_run(task: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    Délègue une tâche à Hermes Agent. Hermes répond en mode non-interactif (-q).

    Args:
        task: la tâche en langage naturel (FR ou EN)
        timeout: timeout en secondes (défaut 180s = 3 min)

    Returns:
        La réponse de Hermes (string), ou un message d'erreur préfixé [HERMES ERROR].

    Exemple :
        hermes_run("Liste les 5 premiers fichiers Python du projet")
        hermes_run("Génère un diagramme d'architecture pour mon FastAPI")
    """
    if not _check_wsl_available():
        return "[HERMES ERROR] WSL2 Ubuntu ou Hermes Agent non disponible. Lance d'abord l'installation."

    if not task or not task.strip():
        return "[HERMES ERROR] Tâche vide."

    # Échappement basique : on encode la tâche en base64 pour éviter les soucis de quoting
    import base64
    task_b64 = base64.b64encode(task.encode("utf-8")).decode("ascii")

    cmd = [
        WSL_EXE, "-d", DISTRO, "--",
        "bash", "-c",
        f'TASK=$(echo {task_b64} | base64 -d) && timeout {timeout - 5} {HERMES_BIN} chat -q "$TASK" -Q --max-turns 5 2>&1'
    ]

    try:
        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace"
        )
        out = (r.stdout or "").strip()
        # Nettoie les codes ANSI et lignes vides excessives
        import re
        out = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', out)
        out = re.sub(r'\n{3,}', '\n\n', out).strip()

        if r.returncode != 0 and not out:
            return f"[HERMES ERROR] Exit code {r.returncode} : {(r.stderr or '').strip()[:200]}"

        # Limite la taille de la réponse pour ne pas saturer le contexte AISATOU
        if len(out) > 4000:
            out = out[:4000] + "\n\n[... tronqué — réponse Hermes trop longue]"

        return out or "[HERMES] Aucune réponse."

    except subprocess.TimeoutExpired:
        return f"[HERMES TIMEOUT] La tâche a dépassé {timeout}s. Reformule en plus simple ou augmente le timeout."
    except Exception as e:
        return f"[HERMES ERROR] {type(e).__name__}: {str(e)[:200]}"


def hermes_status() -> str:
    """Vérifie l'état de Hermes Agent et renvoie un résumé."""
    if not _check_wsl_available():
        return "Hermes : [X] non installe (WSL2 Ubuntu ou Hermes manquant)"
    try:
        r = subprocess.run(
            [WSL_EXE, "-d", DISTRO, "--", HERMES_BIN, "--version"],
            capture_output=True, text=True, timeout=10
        )
        version = (r.stdout or "").strip().split("\n")[0]
        return f"Hermes : [OK] {version}"
    except Exception as e:
        return f"Hermes : [WARN] {type(e).__name__}: {e}"


def hermes_skills() -> str:
    """Liste les skills disponibles dans Hermes."""
    if not _check_wsl_available():
        return "[HERMES ERROR] non disponible"
    try:
        r = subprocess.run(
            [WSL_EXE, "-d", DISTRO, "--", HERMES_BIN, "skills", "list"],
            capture_output=True, text=True, timeout=15
        )
        out = (r.stdout or "").strip()
        if len(out) > 2000:
            out = out[:2000] + "\n[... tronqué]"
        return out or "Aucun skill listé"
    except Exception as e:
        return f"[HERMES ERROR] {e}"


if __name__ == "__main__":
    # Test rapide
    print("=== Hermes Status ===")
    print(hermes_status())
    print("\n=== Test simple ===")
    print(hermes_run("Réponds en 1 ligne : Hermes OK ?"))
