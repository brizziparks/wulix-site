"""System control tools — open apps and URLs."""

import os
import subprocess
import webbrowser
import sys

# Common Windows app aliases
APP_ALIASES = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "task manager": "taskmgr.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "edge": "msedge.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "spotify": r"%APPDATA%\Spotify\Spotify.exe",
    "discord": r"%LOCALAPPDATA%\Discord\Update.exe",
    "vscode": "code",
    "vs code": "code",
}


def open_application(name: str) -> str:
    """Open an application by name."""
    name_lower = name.lower().strip()
    cmd = APP_ALIASES.get(name_lower, name)

    try:
        if sys.platform == "win32":
            os.startfile(os.path.expandvars(cmd))
        else:
            subprocess.Popen([cmd])
        return f"Opened: {name}"
    except FileNotFoundError:
        # Try subprocess as fallback
        try:
            subprocess.Popen(cmd, shell=True)
            return f"Opened: {name}"
        except Exception as e:
            return f"Could not open {name}: {str(e)}"
    except Exception as e:
        return f"Could not open {name}: {str(e)}"


def open_url(url: str) -> str:
    """Open a URL in the default browser."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opened in browser: {url}"
