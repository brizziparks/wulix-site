"""
Historique presse-papiers — mémorise les N dernières valeurs copiées.
Tourne en arrière-plan et se met à jour automatiquement.

Démarrage : ClipboardHistory.start()  (thread daemon)
Utilisation : get_clipboard_history(), get_last_clipboard(n)
"""

import threading
import time
from collections import deque
from datetime import datetime

try:
    import pyperclip
    PYPERCLIP_OK = True
except ImportError:
    PYPERCLIP_OK = False


class ClipboardHistory:
    """Surveille le presse-papiers et conserve les N dernières entrées."""

    MAX_ENTRIES  = 20
    POLL_INTERVAL = 0.8   # secondes entre chaque vérification

    _history: deque = deque(maxlen=MAX_ENTRIES)
    _last_value: str = ""
    _running: bool   = False
    _thread: threading.Thread = None
    _lock: threading.Lock = threading.Lock()

    @classmethod
    def start(cls):
        """Démarre la surveillance en arrière-plan (thread daemon)."""
        if not PYPERCLIP_OK:
            return
        if cls._running:
            return
        cls._running = True
        cls._thread  = threading.Thread(target=cls._loop, daemon=True)
        cls._thread.start()

    @classmethod
    def stop(cls):
        cls._running = False

    @classmethod
    def _loop(cls):
        while cls._running:
            try:
                current = pyperclip.paste()
                if current and current != cls._last_value:
                    cls._last_value = current
                    with cls._lock:
                        cls._history.appendleft({
                            "text":      current,
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "preview":   current[:80].replace("\n", " "),
                        })
            except Exception:
                pass
            time.sleep(cls.POLL_INTERVAL)

    @classmethod
    def get_history(cls, n: int = 10) -> list:
        """Retourne les n dernières entrées."""
        with cls._lock:
            return list(cls._history)[:n]

    @classmethod
    def clear(cls):
        """Efface l'historique."""
        with cls._lock:
            cls._history.clear()
        cls._last_value = ""


# ── API publique ──────────────────────────────────────────────────────────────

def start_clipboard_watcher():
    """Démarre la surveillance du presse-papiers en arrière-plan."""
    ClipboardHistory.start()
    return "Surveillance presse-papiers démarrée."


def get_clipboard_history(count: int = 10) -> str:
    """
    Retourne les dernières valeurs copiées dans le presse-papiers.

    Args:
        count: Nombre d'entrées à retourner (max 20).
    """
    if not PYPERCLIP_OK:
        return "pyperclip non installé."

    history = ClipboardHistory.get_history(min(count, 20))
    if not history:
        return "Historique presse-papiers vide (rien copié depuis le démarrage)."

    lines = [f"Dernières {len(history)} copies :"]
    for i, entry in enumerate(history, 1):
        preview = entry["preview"][:60] + ("…" if len(entry["preview"]) > 60 else "")
        lines.append(f"  {i}. [{entry['timestamp']}] {preview}")
    return "\n".join(lines)


def get_last_clipboard(position: int = 1) -> str:
    """
    Retourne une entrée spécifique de l'historique.

    Args:
        position: 1 = la plus récente, 2 = avant-dernière, etc.
    """
    if not PYPERCLIP_OK:
        return "pyperclip non installé."

    history = ClipboardHistory.get_history(position)
    if not history or position > len(history):
        return f"Entrée {position} non disponible dans l'historique."

    entry = history[position - 1]
    return f"Copie #{position} [{entry['timestamp']}] :\n{entry['text']}"


def restore_clipboard(position: int = 1) -> str:
    """
    Remet une ancienne copie dans le presse-papiers actuel.

    Args:
        position: Position dans l'historique (1 = plus récente).
    """
    if not PYPERCLIP_OK:
        return "pyperclip non installé."

    history = ClipboardHistory.get_history(position)
    if not history or position > len(history):
        return f"Entrée {position} non disponible."

    text = history[position - 1]["text"]
    pyperclip.copy(text)
    preview = text[:60] + ("…" if len(text) > 60 else "")
    return f"Presse-papiers restauré : {preview}"


def clear_clipboard_history() -> str:
    """Efface tout l'historique du presse-papiers."""
    ClipboardHistory.clear()
    return "Historique presse-papiers effacé."
