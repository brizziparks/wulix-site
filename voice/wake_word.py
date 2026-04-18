"""
Wake word detector — écoute en continu "Aisatou"
Utilise speech_recognition, 100% gratuit, aucune clé requise.
"""

import threading
import time

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

# Variantes acceptées du wake word (orthographes approximatives que Google retourne)
WAKE_WORDS = {
    "aisatou", "aïsatou", "aisatu", "isatou", "aissatou",
    "issa tou", "aisa tou", "hey aisatou", "aisatou,",
}

def _normalize(text: str) -> str:
    return text.lower().strip().rstrip(".,!?")


class WakeWordDetector:
    """
    Écoute le micro en arrière-plan.
    Quand le wake word est détecté, appelle le callback `on_wake`.
    """

    def __init__(self, on_wake, language: str = "fr-FR"):
        self.on_wake   = on_wake
        self.language  = language
        self._running  = False
        self._thread   = None
        self._paused   = False   # Pause pendant qu'AISATOU parle

    def start(self):
        if not SR_AVAILABLE:
            print("[Wake word] speech_recognition non installé.")
            return
        self._running = True
        self._thread  = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print("[Wake word] En écoute — dis 'Aisatou' pour l'activer.")

    def stop(self):
        self._running = False

    def pause(self):
        """Pause pendant que l'assistante parle (évite l'auto-détection)."""
        self._paused = True

    def resume(self):
        self._paused = False

    def _loop(self):
        r = sr.Recognizer()
        r.energy_threshold    = 250
        r.dynamic_energy_threshold = True
        r.pause_threshold     = 0.6
        r.phrase_threshold    = 0.3

        while self._running:
            if self._paused:
                time.sleep(0.2)
                continue
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.2)
                    try:
                        audio = r.listen(source, timeout=3, phrase_time_limit=4)
                    except sr.WaitTimeoutError:
                        continue

                if self._paused:
                    continue

                try:
                    text = r.recognize_google(audio, language=self.language)
                    normalized = _normalize(text)
                    print(f"[Wake word] Entendu : '{text}'")

                    # Vérifie si le wake word est dans la phrase
                    if any(w in normalized for w in WAKE_WORDS):
                        print("[Wake word] Activé !")
                        # Extraire la commande après le wake word (si dite en même temps)
                        command = self._extract_command(normalized)
                        self.on_wake(command)

                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    time.sleep(2)

            except OSError:
                time.sleep(1)
            except Exception as e:
                print(f"[Wake word] Erreur : {e}")
                time.sleep(1)

    def _extract_command(self, text: str) -> str:
        """Retire le wake word et retourne la commande qui suit."""
        for w in sorted(WAKE_WORDS, key=len, reverse=True):
            if text.startswith(w):
                return text[len(w):].strip().lstrip(",").strip()
        return ""
