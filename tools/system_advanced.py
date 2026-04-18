"""Outils système avancés : clipboard, screenshot, volume."""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ── Clipboard ────────────────────────────────────────────────────────────────

try:
    import pyperclip
    PYPERCLIP = True
except ImportError:
    PYPERCLIP = False


def get_clipboard() -> str:
    """Lire le contenu du presse-papiers."""
    if PYPERCLIP:
        try:
            content = pyperclip.paste()
            return content if content else "(presse-papiers vide)"
        except Exception as e:
            return f"Erreur presse-papiers : {e}"
    # Fallback PowerShell
    try:
        r = subprocess.run(
            ["powershell", "-command", "Get-Clipboard"],
            capture_output=True, text=True, timeout=5
        )
        return r.stdout.strip() or "(presse-papiers vide)"
    except Exception as e:
        return f"Erreur : {e}"


def set_clipboard(text: str) -> str:
    """Copier du texte dans le presse-papiers."""
    if PYPERCLIP:
        try:
            pyperclip.copy(text)
            return f"Copie dans le presse-papiers : {text[:60]}{'...' if len(text)>60 else ''}"
        except Exception as e:
            return f"Erreur : {e}"
    try:
        subprocess.run(
            ["powershell", "-command", f"Set-Clipboard -Value '{text}'"],
            capture_output=True, timeout=5
        )
        return "Copie dans le presse-papiers."
    except Exception as e:
        return f"Erreur : {e}"


# ── Screenshot ────────────────────────────────────────────────────────────────

try:
    import pyautogui
    PYAUTOGUI = True
except ImportError:
    PYAUTOGUI = False

SCREENSHOTS_DIR = Path.home() / "Pictures" / "AISATOU"


def take_screenshot(filename: str = "") -> str:
    """Prendre une capture d'écran et la sauvegarder."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    if not filename:
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = SCREENSHOTS_DIR / filename

    if PYAUTOGUI:
        try:
            img = pyautogui.screenshot()
            img.save(str(path))
            return f"Screenshot sauvegarde : {path}"
        except Exception as e:
            return f"Erreur screenshot : {e}"

    # Fallback PowerShell
    try:
        script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "Add-Type -AssemblyName System.Drawing; "
            "$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; "
            "$bmp = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height); "
            "$g = [System.Drawing.Graphics]::FromImage($bmp); "
            "$g.CopyFromScreen($screen.Location, "
            "[System.Drawing.Point]::Empty, $screen.Size); "
            f"$bmp.Save('{str(path).replace(chr(92), '/')}');"
        )
        subprocess.run(["powershell", "-command", script], capture_output=True, timeout=10)
        return f"Screenshot sauvegarde : {path}"
    except Exception as e:
        return f"Erreur screenshot : {e}"


# ── Volume ────────────────────────────────────────────────────────────────────

def get_volume() -> str:
    """Obtenir le volume système actuel."""
    try:
        r = subprocess.run(
            ["powershell", "-command",
             "(Get-WmiObject -Class Win32_SoundDevice | Select-Object -First 1).Name; "
             "$vol = [math]::Round((Get-WmiObject -Namespace root/cimv2 "
             "-Class Win32_SoundDevice).count); "
             "Add-Type -TypeDefinition 'using System.Runtime.InteropServices; "
             "[Guid(\"5CDF2C82-841E-4546-9722-0CF74078229A\")] "
             "public interface IMMDevice {}'; "
             "echo 'Volume OK'"],
            capture_output=True, text=True, timeout=5
        )
        # Approche plus simple via nircmd si dispo, sinon PowerShell audio
        r2 = subprocess.run(
            ["powershell", "-command",
             "Add-Type -AssemblyName presentationCore; "
             "[int]([Windows.Media.Volume.GetVolume()]*100)"],
            capture_output=True, text=True, timeout=5
        )
        return f"Volume actuel : {r2.stdout.strip()}%"
    except Exception:
        return "Impossible de lire le volume (utilise set_volume pour le changer)."


def set_volume(level: int) -> str:
    """
    Régler le volume système (0-100).
    """
    level = max(0, min(100, int(level)))
    try:
        # nircmd est le plus fiable sur Windows
        nircmd = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "nircmd" / "nircmd.exe"
        if nircmd.exists():
            subprocess.run([str(nircmd), "setsysvolume", str(int(level * 655.35))],
                          capture_output=True, timeout=5)
        else:
            # PowerShell via WScript
            script = (
                "$wsh = New-Object -ComObject WScript.Shell; "
                f"$steps = [math]::Round(({level}/100) * 50); "
                "$wsh.SendKeys([char]174 * 50); "  # Mute all
                "$wsh.SendKeys([char]175 * $steps)"  # Vol up
            )
            subprocess.run(["powershell", "-command", script],
                          capture_output=True, timeout=5)
        return f"Volume regle a {level}%"
    except Exception as e:
        return f"Erreur volume : {e}"


def mute() -> str:
    """Couper/rétablir le son."""
    try:
        script = (
            "$wsh = New-Object -ComObject WScript.Shell; "
            "$wsh.SendKeys([char]173)"
        )
        subprocess.run(["powershell", "-command", script],
                      capture_output=True, timeout=5)
        return "Son coupé / rétabli"
    except Exception as e:
        return f"Erreur mute : {e}"
