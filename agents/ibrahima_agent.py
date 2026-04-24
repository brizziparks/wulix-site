"""
IBRAHIMA — Agent Design IA
Génère visuels Pillow : covers, OG images, miniatures, avatar Malt
"""
import os
import datetime
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

BASE_DIR = Path(__file__).parent
UI_DIR = BASE_DIR.parent / "ui"
LOG_DIR = BASE_DIR / "logs"
VISUALS_DIR = BASE_DIR / "visuals"
LOG_DIR.mkdir(exist_ok=True)
VISUALS_DIR.mkdir(exist_ok=True)

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] IBRAHIMA | {msg}"
    print(line)
    with open(LOG_DIR / "ibrahima.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

def create_malt_avatar(output_path: Path = None) -> Path:
    """
    Crée un avatar professionnel illustré pour Malt
    Style : silhouette abstraite + initiales, sans visage identifiable
    """
    if not PIL_AVAILABLE:
        log("Pillow non disponible — pip install Pillow")
        return None

    if output_path is None:
        output_path = VISUALS_DIR / "malt_avatar.png"

    size = 400
    img = Image.new("RGB", (size, size), "#0f0f0f")
    draw = ImageDraw.Draw(img)

    # Fond dégradé simulé avec cercles
    for i in range(20, 0, -1):
        alpha = int(255 * (i / 20) * 0.3)
        r = int(124 + (i * 3))
        g = int(58 - (i * 2))
        b = int(237 - (i * 5))
        color = (min(r,255), max(g,0), max(b,0))
        draw.ellipse([
            size//2 - i*12, size//2 - i*12,
            size//2 + i*12, size//2 + i*12
        ], fill=color)

    # Cercle principal violet
    margin = 40
    draw.ellipse([margin, margin, size-margin, size-margin],
                 fill="#7c3aed", outline="#9d5bf5", width=4)

    # Silhouette abstraite (tête + épaules stylisées)
    cx, cy = size // 2, size // 2

    # Tête (cercle)
    head_r = 55
    draw.ellipse([cx-head_r, cy-85-head_r, cx+head_r, cy-85+head_r],
                 fill="#1a0a3d")

    # Corps/épaules (arc)
    draw.chord([cx-90, cy-20, cx+90, cy+80],
               start=0, end=180, fill="#1a0a3d")

    # Initiales "OS" au centre
    try:
        font_large = ImageFont.truetype("arial.ttf", 52)
    except:
        font_large = ImageFont.load_default()

    text = "OS"
    bbox = draw.textbbox((0, 0), text, font=font_large)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw//2, cy + 30 - th//2), text, fill="white", font=font_large)

    # Badge "WULIX" en bas
    badge_y = size - margin - 30
    draw.rounded_rectangle([cx-50, badge_y-15, cx+50, badge_y+15],
                           radius=8, fill="#5b21b6")
    try:
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_small = ImageFont.load_default()

    draw.text((cx-22, badge_y-8), "WULIX", fill="white", font=font_small)

    img.save(output_path, "PNG", quality=95)
    log(f"Avatar Malt créé: {output_path}")
    return output_path

def create_blog_thumbnail(title: str, output_path: Path = None) -> Path:
    """Crée une miniature pour un article de blog"""
    if not PIL_AVAILABLE:
        return None

    if output_path is None:
        slug = title[:20].lower().replace(" ", "_")
        output_path = VISUALS_DIR / f"thumb_{slug}.png"

    img = Image.new("RGB", (1200, 630), "#0f0f0f")
    draw = ImageDraw.Draw(img)

    # Bande colorée gauche
    draw.rectangle([0, 0, 8, 630], fill="#7c3aed")

    # Fond décoratif
    for i in range(5):
        x = 900 + i * 60
        draw.ellipse([x-100, -100, x+100, 100], fill="#1a0a3d")

    # Logo WULIX
    try:
        font_logo = ImageFont.truetype("arialbd.ttf", 32)
    except:
        font_logo = ImageFont.load_default()
    draw.text((60, 50), "WULIX", fill="#7c3aed", font=font_logo)

    # Titre
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 52)
    except:
        font_title = ImageFont.load_default()

    # Wrap du titre
    words = title.split()
    lines = []
    current = []
    for word in words:
        current.append(word)
        if len(" ".join(current)) > 30:
            lines.append(" ".join(current[:-1]))
            current = [word]
    lines.append(" ".join(current))

    y = 160
    for line in lines[:3]:
        draw.text((60, y), line, fill="white", font=font_title)
        y += 65

    # Tag
    draw.rounded_rectangle([60, y+20, 220, y+50], radius=6, fill="#7c3aed")
    try:
        font_tag = ImageFont.truetype("arial.ttf", 18)
    except:
        font_tag = ImageFont.load_default()
    draw.text((75, y+28), "WULIX Blog", fill="white", font=font_tag)

    img.save(output_path, "PNG")
    log(f"Miniature créée: {output_path}")
    return output_path

def create_social_visual(text: str, platform: str = "linkedin") -> Path:
    """Crée un visuel carré pour post social"""
    if not PIL_AVAILABLE:
        return None

    sizes = {"linkedin": (1200, 627), "twitter": (1200, 675), "instagram": (1080, 1080)}
    w, h = sizes.get(platform, (1200, 627))

    output_path = VISUALS_DIR / f"social_{platform}_{datetime.date.today().strftime('%Y%m%d')}.png"

    img = Image.new("RGB", (w, h), "#0f0f0f")
    draw = ImageDraw.Draw(img)

    # Dégradé violet diagonal
    for i in range(w):
        ratio = i / w
        r = int(15 + ratio * 50)
        g = int(15)
        b = int(15 + ratio * 30)
        draw.line([(i, 0), (i, h)], fill=(r, g, b))

    # Accent
    draw.rectangle([0, 0, 6, h], fill="#7c3aed")
    draw.rectangle([0, h-6, w, h], fill="#7c3aed")

    # Logo
    draw.text((40, 40), "WULIX", fill="#7c3aed")

    # Texte principal
    draw.text((40, h//2 - 40), text[:60], fill="white")

    img.save(output_path, "PNG")
    log(f"Visuel {platform} créé: {output_path}")
    return output_path

def run(action="avatar"):
    log(f"Démarrage IBRAHIMA — action: {action}")

    if action == "avatar":
        path = create_malt_avatar()
        if path:
            log(f"Avatar disponible: {path}")
            import shutil
            UI_DIR.mkdir(exist_ok=True)
            shutil.copy(path, UI_DIR / "malt_avatar.png")

    elif action == "thumbnail":
        create_blog_thumbnail("Comment automatiser votre business")

    elif action == "social":
        create_social_visual("L'automatisation, c'est du temps retrouvé.", "linkedin")

    log("IBRAHIMA terminé")

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "avatar"
    run(action)
