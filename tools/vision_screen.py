"""
Vision écran — screenshot + Gemini vision → click / type n'importe où sur l'écran.
Inspiré de JARVIS (techenclair.fr) jarvis_vision_cliquer / jarvis_vision_ecrire.

Nécessite : pyautogui, Pillow, google-genai, GEMINI_API_KEY dans .env
"""

import json
import os
import re
import time
import tempfile

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def _get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except Exception:
        return None


def _screenshot() -> str:
    """Prend une capture d'écran, retourne le chemin du fichier temporaire."""
    if not PYAUTOGUI_AVAILABLE or not PIL_AVAILABLE:
        raise RuntimeError("pyautogui ou Pillow non installé")
    tmp = os.path.join(tempfile.gettempdir(), "aisatou_vision_temp.png")
    pyautogui.screenshot().save(tmp)
    return tmp


def _ask_gemini_for_box(img_path: str, prompt: str) -> list:
    """
    Envoie screenshot + prompt à Gemini, récupère la bounding box [ymin, xmin, ymax, xmax]
    normalisée sur 0-1000.
    """
    client = _get_gemini_client()
    if not client:
        raise RuntimeError("GEMINI_API_KEY non configuré — vision écran impossible")

    img = Image.open(img_path)
    try:
        from google.genai import types
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, img]
        )
    except Exception as e:
        raise RuntimeError(f"Erreur Gemini vision : {e}")

    rep = response.text.strip()
    # Extraire le JSON
    m = re.search(r'\{[^}]+\}', rep, re.DOTALL)
    if not m:
        raise ValueError(f"Gemini n'a pas retourné de JSON : {rep[:200]}")
    data = json.loads(m.group())
    box = data.get("box", [500, 500, 500, 500])
    return box


def _box_to_screen_coords(box: list) -> tuple[int, int]:
    """Convertit une bounding box [ymin, xmin, ymax, xmax] (0-1000) en pixels."""
    ymin, xmin, ymax, xmax = box
    center_y = (ymin + ymax) / 2
    center_x = (xmin + xmax) / 2
    screen_w, screen_h = pyautogui.size()
    x = int((center_x / 1000) * screen_w)
    y = int((center_y / 1000) * screen_h)
    return x, y


def vision_click(instruction: str) -> str:
    """
    Prend une capture d'écran, demande à Gemini où cliquer selon `instruction`,
    puis effectue le clic.

    Args:
        instruction: Description de l'élément à cliquer (ex: "bouton Publier en haut à droite")

    Returns:
        Message de confirmation ou d'erreur.
    """
    if not PYAUTOGUI_AVAILABLE:
        return "pyautogui non installé — vision_click non disponible"

    try:
        path = _screenshot()
        prompt = (
            f"Tu es la vision d'AISATOU. Voici une capture d'écran.\n"
            f"Instruction : {instruction}\n"
            "Trouve EXACTEMENT la position de cet élément sur l'écran.\n"
            "Réponds UNIQUEMENT avec ce JSON (bounding box normalisée 0-1000) :\n"
            '{"box": [ymin, xmin, ymax, xmax]}\n'
            "Exemple : {\"box\": [250, 480, 290, 520]}"
        )
        box = _ask_gemini_for_box(path, prompt)
        x, y = _box_to_screen_coords(box)
        pyautogui.moveTo(x, y, duration=0.4)
        pyautogui.click()
        try:
            os.remove(path)
        except Exception:
            pass
        return f"Clic effectué sur : {instruction} (position {x},{y})"
    except Exception as e:
        return f"Vision écran — erreur : {e}"


def vision_type(instruction: str, text: str) -> str:
    """
    Prend une capture d'écran, clique sur le champ décrit par `instruction`,
    puis tape `text`.

    Args:
        instruction: Champ de saisie à cibler (ex: "champ de recherche en haut")
        text:        Texte à taper

    Returns:
        Message de confirmation ou d'erreur.
    """
    if not PYAUTOGUI_AVAILABLE:
        return "pyautogui non installé — vision_type non disponible"

    try:
        path = _screenshot()
        prompt = (
            f"Tu es la vision d'AISATOU. Voici une capture d'écran.\n"
            f"Je veux écrire dans : {instruction}\n"
            "Trouve EXACTEMENT la position de ce champ de saisie.\n"
            "Réponds UNIQUEMENT avec ce JSON :\n"
            '{"box": [ymin, xmin, ymax, xmax]}'
        )
        box = _ask_gemini_for_box(path, prompt)
        x, y = _box_to_screen_coords(box)
        pyautogui.moveTo(x, y, duration=0.4)
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.write(text, interval=0.04)
        try:
            os.remove(path)
        except Exception:
            pass
        return f"Texte '{text}' saisi dans : {instruction}"
    except Exception as e:
        return f"Vision écran — erreur : {e}"


def vision_screenshot_describe(question: str = "") -> str:
    """
    Capture l'écran et demande à Gemini de le décrire / répondre à une question dessus.

    Args:
        question: Question optionnelle (ex: "Qu'est-ce qui est affiché ?")
    """
    try:
        path = _screenshot()
        client = _get_gemini_client()
        if not client:
            return "GEMINI_API_KEY non configuré"
        img = Image.open(path)
        q = question or "Décris brièvement ce que tu vois sur cet écran."
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[q, img]
        )
        try:
            os.remove(path)
        except Exception:
            pass
        return response.text.strip()
    except Exception as e:
        return f"Vision écran — erreur : {e}"
