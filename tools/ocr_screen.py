"""
OCR écran — extrait du texte depuis une capture d'écran.
Utilise Gemini vision (priorité) ou pytesseract (fallback).

Aucune configuration requise si GEMINI_API_KEY est déjà dans .env.
pytesseract optionnel : pip install pytesseract + installer Tesseract-OCR.
"""

import os
import tempfile

try:
    import pyautogui
    PYAUTOGUI_OK = True
except ImportError:
    PYAUTOGUI_OK = False

try:
    from PIL import Image, ImageEnhance, ImageFilter
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    import pytesseract
    TESSERACT_OK = True
except ImportError:
    TESSERACT_OK = False


def _screenshot(region=None) -> str:
    """Capture l'écran (ou une région) et retourne le chemin du PNG temporaire."""
    if not PYAUTOGUI_OK or not PIL_OK:
        raise RuntimeError("pyautogui ou Pillow non installé")
    img = pyautogui.screenshot(region=region)
    tmp = os.path.join(tempfile.gettempdir(), "aisatou_ocr_temp.png")
    img.save(tmp)
    return tmp


def _gemini_ocr(img_path: str, instruction: str = "") -> str:
    """OCR via Gemini vision (meilleure qualité, multilangue)."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY manquant")
    try:
        from google import genai
        from PIL import Image as _Image
        client = genai.Client(api_key=api_key)
        img = _Image.open(img_path)
        prompt = instruction or (
            "Extrais TOUT le texte visible sur cette image. "
            "Conserve la mise en forme (colonnes, listes, tableaux). "
            "Réponds uniquement avec le texte extrait, rien d'autre."
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, img]
        )
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Gemini OCR erreur : {e}")


def _tesseract_ocr(img_path: str, lang: str = "fra+eng") -> str:
    """OCR via pytesseract (offline, nécessite Tesseract installé)."""
    img = Image.open(img_path)
    # Prétraitement pour améliorer la reconnaissance
    img = img.convert("L")  # Niveaux de gris
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = img.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(img, lang=lang).strip()


def extract_text_from_screen(instruction: str = "", region=None) -> str:
    """
    Capture l'écran et extrait le texte visible.

    Args:
        instruction: Instruction spécifique (ex: "extrait seulement les prix",
                     "liste les noms de fichiers"). Si vide, extrait tout.
        region:      Tuple (x, y, width, height) pour capturer une zone précise.

    Returns:
        Texte extrait de l'écran.
    """
    if not PYAUTOGUI_OK:
        return "pyautogui non installé — OCR écran impossible"
    try:
        path = _screenshot(region=region)
        try:
            result = _gemini_ocr(path, instruction)
        except Exception:
            if TESSERACT_OK:
                result = _tesseract_ocr(path)
            else:
                return "OCR écran : ni Gemini ni pytesseract disponibles."
        try:
            os.remove(path)
        except Exception:
            pass
        return result if result else "Aucun texte détecté sur l'écran."
    except Exception as e:
        return f"OCR écran erreur : {e}"


def extract_text_from_image(image_path: str, instruction: str = "") -> str:
    """
    Extrait le texte d'une image existante (fichier local).

    Args:
        image_path:  Chemin vers l'image.
        instruction: Instruction spécifique pour Gemini.
    """
    if not os.path.exists(image_path):
        return f"Image introuvable : {image_path}"
    try:
        return _gemini_ocr(image_path, instruction)
    except Exception:
        if TESSERACT_OK and PIL_OK:
            return _tesseract_ocr(image_path)
        return "OCR image : Gemini et pytesseract non disponibles."


def find_text_on_screen(search_text: str) -> str:
    """
    Vérifie si un texte spécifique est visible à l'écran.

    Args:
        search_text: Texte à rechercher.

    Returns:
        "Trouvé" / "Non trouvé" avec contexte.
    """
    full_text = extract_text_from_screen(f"Cherche le texte : '{search_text}'")
    if search_text.lower() in full_text.lower():
        return f"'{search_text}' trouvé à l'écran."
    return f"'{search_text}' non visible à l'écran."
