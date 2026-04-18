"""Notifications Windows toast + sons système."""

import subprocess
import sys
from pathlib import Path

try:
    from winotify import Notification, audio
    WINOTIFY = True
except ImportError:
    WINOTIFY = False

ICON_PATH = str(Path(__file__).parent.parent / "ui" / "icon.png")


def notify(title: str, message: str, duration: str = "short", sound: bool = True) -> str:
    """
    Envoie une notification toast Windows.
    duration : "short" (5s) ou "long" (25s)
    """
    if WINOTIFY:
        try:
            toast = Notification(
                app_id="AISATOU",
                title=title,
                msg=message,
                duration=duration,
                icon=ICON_PATH if Path(ICON_PATH).exists() else "",
            )
            if sound:
                toast.set_audio(audio.Default, loop=False)
            toast.show()
            return f"Notification envoyee : {title}"
        except Exception as e:
            return _fallback_notify(title, message)
    return _fallback_notify(title, message)


def _fallback_notify(title: str, message: str) -> str:
    """Fallback PowerShell si winotify indisponible."""
    try:
        script = (
            f"Add-Type -AssemblyName System.Windows.Forms; "
            f"$n = New-Object System.Windows.Forms.NotifyIcon; "
            f"$n.Icon = [System.Drawing.SystemIcons]::Information; "
            f"$n.Visible = $true; "
            f"$n.ShowBalloonTip(5000, '{title}', '{message}', "
            f"[System.Windows.Forms.ToolTipIcon]::Info); "
            f"Start-Sleep -s 6; $n.Visible = $false"
        )
        subprocess.Popen(
            ["powershell", "-WindowStyle", "Hidden", "-Command", script],
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        return f"Notification envoyee : {title}"
    except Exception as e:
        return f"Impossible d'envoyer la notification : {e}"


def remind(message: str, minutes: int = 0, seconds: int = 30) -> str:
    """Planifie un rappel dans X minutes/secondes (thread séparé)."""
    import threading
    delay = minutes * 60 + seconds

    def _fire():
        import time
        time.sleep(delay)
        notify("Rappel AISATOU", message, duration="long", sound=True)

    t = threading.Thread(target=_fire, daemon=True)
    t.start()
    delay_str = f"{minutes}min {seconds}s" if minutes else f"{seconds}s"
    return f"Rappel programme dans {delay_str} : {message}"
