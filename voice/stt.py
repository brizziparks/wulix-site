"""Speech-to-Text using speech_recognition (Google Web Speech API)."""

import os

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False


def listen(timeout: int = 5, phrase_limit: int = 15, language: str = None) -> str | None:
    """
    Écoute le microphone et transcrit la parole.

    Retourne :
        Le texte transcrit, ou None si rien n'a été entendu / en cas d'erreur.
    """
    if not SR_AVAILABLE:
        print("[STT] speech_recognition non installé — mode clavier uniquement")
        return None

    lang = language or os.getenv("AISATOU_LANG", "fr-FR")
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8

    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            except sr.WaitTimeoutError:
                return None

        try:
            text = r.recognize_google(audio, language=lang)
            return text.strip()
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"[STT] Erreur API Google Speech : {e}")
            try:
                text = r.recognize_sphinx(audio)
                return text.strip()
            except Exception:
                return None

    except OSError as e:
        print(f"[STT] Erreur microphone : {e}")
        return None
    except Exception as e:
        print(f"[STT] Erreur : {e}")
        return None


def list_microphones() -> list[str]:
    """Liste les microphones disponibles."""
    if not SR_AVAILABLE:
        return []
    return list(sr.Microphone.list_microphone_names())
