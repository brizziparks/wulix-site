"""Text-to-Speech using edge-tts (Microsoft Neural voices, free, Windows-friendly)."""

import asyncio
import os
import tempfile

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

# Voix féminine française — naturelle et chaleureuse pour AISATOU
AISATOU_VOICE = os.getenv("AISATOU_VOICE", "fr-FR-DeniseNeural")
AISATOU_RATE  = os.getenv("AISATOU_RATE", "+0%")
AISATOU_PITCH = os.getenv("AISATOU_PITCH", "-3Hz")


async def _speak_edge_tts(text: str):
    """Génère et lit un fichier audio avec edge-tts + pygame."""
    communicate = edge_tts.Communicate(text, AISATOU_VOICE, rate=AISATOU_RATE, pitch=AISATOU_PITCH)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        tmp_path = f.name

    try:
        await communicate.save(tmp_path)

        if PYGAME_AVAILABLE:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            pygame.mixer.music.unload()
        else:
            import subprocess
            subprocess.run(
                ["powershell", "-c",
                 f'$wmp = New-Object -ComObject WMPlayer.OCX; '
                 f'$wmp.openPlayer("{tmp_path}"); Start-Sleep -s 5'],
                capture_output=True, timeout=30
            )
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def _speak_pyttsx3(text: str):
    """TTS de secours avec pyttsx3 (hors-ligne, qualité moindre)."""
    engine = pyttsx3.init()
    for voice in engine.getProperty("voices"):
        if "french" in voice.name.lower() or "hortense" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
    engine.setProperty("rate", 160)
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()


async def speak(text: str):
    """Lit le texte à voix haute avec le meilleur moteur TTS disponible."""
    if not text or not text.strip():
        return

    if EDGE_TTS_AVAILABLE:
        try:
            await _speak_edge_tts(text)
            return
        except Exception as e:
            print(f"[TTS] edge-tts error: {e} — bascule sur pyttsx3")

    if PYTTSX3_AVAILABLE:
        try:
            _speak_pyttsx3(text)
            return
        except Exception as e:
            print(f"[TTS] pyttsx3 error: {e}")
            return

    print("[TTS non disponible — installe edge-tts et pygame]")


async def list_voices() -> list[str]:
    """Liste les voix edge-tts françaises et anglophones disponibles."""
    if not EDGE_TTS_AVAILABLE:
        return ["edge-tts non installé"]
    voices = await edge_tts.list_voices()
    return [v["ShortName"] for v in voices if "fr" in v["ShortName"].lower() or "en" in v["ShortName"].lower()]
