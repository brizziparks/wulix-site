"""
File watcher — surveille un dossier et notifie AISATOU des nouveaux fichiers.
Tourne en arrière-plan, callback configurable.

Usage :
    from tools.file_watcher import FileWatcher, watch_downloads
    watch_downloads(callback=lambda f: print(f"Nouveau : {f}"))
"""

import os
import threading
import time
from datetime import datetime
from pathlib import Path
from collections import deque


class FileWatcher:
    """
    Surveille un dossier pour les nouveaux fichiers.
    Appelle `on_new_file(path)` à chaque détection.
    """

    def __init__(
        self,
        folder: str,
        on_new_file=None,
        extensions: list = None,
        poll_interval: float = 2.0,
        recursive: bool = False,
    ):
        self.folder        = Path(folder).expanduser()
        self.on_new_file   = on_new_file or (lambda p: None)
        self.extensions    = {e.lower() for e in (extensions or [])}
        self.poll_interval = poll_interval
        self.recursive     = recursive
        self._running      = False
        self._thread       = None
        self._seen: set    = set()
        self.events: deque = deque(maxlen=50)   # log des derniers événements

    def start(self):
        """Démarre la surveillance en arrière-plan."""
        if not self.folder.exists():
            raise FileNotFoundError(f"Dossier introuvable : {self.folder}")
        # Initialiser avec les fichiers existants (pas d'alerte au démarrage)
        self._seen = self._scan()
        self._running = True
        self._thread  = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        return self

    def stop(self):
        self._running = False

    def _scan(self) -> set:
        """Retourne l'ensemble des fichiers actuels."""
        if self.recursive:
            files = self.folder.rglob("*")
        else:
            files = self.folder.glob("*")
        result = set()
        for f in files:
            if f.is_file():
                if not self.extensions or f.suffix.lower() in self.extensions:
                    result.add(str(f))
        return result

    def _loop(self):
        while self._running:
            try:
                current = self._scan()
                new_files = current - self._seen
                for path in sorted(new_files):
                    event = {
                        "path":      path,
                        "name":      Path(path).name,
                        "size":      os.path.getsize(path),
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                    }
                    self.events.appendleft(event)
                    try:
                        self.on_new_file(path)
                    except Exception:
                        pass
                self._seen = current
            except Exception:
                pass
            time.sleep(self.poll_interval)


# ── Instances globales ────────────────────────────────────────────────────────
_watchers: dict = {}   # {name: FileWatcher}


def start_watching(
    folder: str,
    name: str = "default",
    extensions: list = None,
    on_new_file=None,
) -> str:
    """
    Démarre la surveillance d'un dossier.

    Args:
        folder:      Chemin du dossier (ex: "downloads", "bureau", ou chemin complet)
        name:        Nom de la surveillance (pour la référencer)
        extensions:  Liste d'extensions à surveiller (ex: [".pdf", ".xlsx"]). None = tout.
        on_new_file: Callback(path) appelé pour chaque nouveau fichier.

    Returns:
        Message de confirmation.
    """
    # Raccourcis
    shortcuts = {
        "downloads":       os.path.join(os.environ.get("USERPROFILE", ""), "Downloads"),
        "telechargements": os.path.join(os.environ.get("USERPROFILE", ""), "Downloads"),
        "bureau":          os.path.join(os.environ.get("USERPROFILE", ""), "Desktop"),
        "desktop":         os.path.join(os.environ.get("USERPROFILE", ""), "Desktop"),
        "documents":       os.path.join(os.environ.get("USERPROFILE", ""), "Documents"),
    }
    resolved = shortcuts.get(folder.lower(), folder)

    if name in _watchers:
        _watchers[name].stop()

    try:
        watcher = FileWatcher(resolved, on_new_file=on_new_file, extensions=extensions)
        watcher.start()
        _watchers[name] = watcher
        ext_info = f" (extensions : {', '.join(extensions)})" if extensions else ""
        return f"Surveillance démarrée sur '{resolved}'{ext_info} — nom : '{name}'"
    except FileNotFoundError as e:
        return f"Erreur : {e}"


def stop_watching(name: str = "default") -> str:
    """Arrête une surveillance."""
    if name in _watchers:
        _watchers[name].stop()
        del _watchers[name]
        return f"Surveillance '{name}' arrêtée."
    return f"Surveillance '{name}' introuvable."


def get_recent_files(name: str = "default", count: int = 10) -> str:
    """
    Liste les fichiers récemment détectés par la surveillance.

    Args:
        name:  Nom de la surveillance.
        count: Nombre de fichiers à afficher.
    """
    if name not in _watchers:
        return f"Surveillance '{name}' non démarrée. Lance start_watching() d'abord."
    watcher = _watchers[name]
    events  = list(watcher.events)[:count]
    if not events:
        return "Aucun nouveau fichier détecté depuis le démarrage."
    lines = [f"Nouveaux fichiers détectés ({len(events)}) :"]
    for ev in events:
        size_kb = ev["size"] // 1024
        lines.append(f"  [{ev['timestamp']}] {ev['name']} ({size_kb} Ko)")
    return "\n".join(lines)


def list_watchers() -> str:
    """Liste les surveillances actives."""
    if not _watchers:
        return "Aucune surveillance active."
    lines = ["Surveillances actives :"]
    for name, watcher in _watchers.items():
        lines.append(f"  [{name}] → {watcher.folder} ({'actif' if watcher._running else 'arrêté'})")
    return "\n".join(lines)
