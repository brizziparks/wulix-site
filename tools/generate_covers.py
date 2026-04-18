"""
WULIX — Générateur de covers Gumroad
Génère les 3 covers produits en PNG (1280x720px)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# === CONFIG ===
OUTPUT_DIR = r"C:\Users\USER\.claude\projects\projet jarvis\ui\covers"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Couleurs WULIX
BG_COLOR      = (10, 0, 21)       # #0a0015
CYAN          = (0, 229, 255)     # #00e5ff
WHITE         = (255, 255, 255)
PURPLE        = (124, 58, 237)    # #7c3aed
PURPLE_DARK   = (26, 0, 48)       # #1a0030
GRAY          = (180, 180, 180)

# Polices
FONT_DIR = r"C:\Windows\Fonts"
def font(size, bold=False):
    try:
        path = os.path.join(FONT_DIR, "arialbd.ttf" if bold else "arial.ttf")
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill)
    draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill)
    draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill)
    draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill)

def centered_text(draw, text, y, font_obj, color, width=1280):
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    w = bbox[2] - bbox[0]
    x = (width - w) // 2
    draw.text((x, y), text, font=font_obj, fill=color)
    return bbox[3] - bbox[1]

def add_decorative_dots(draw, count=30):
    import random
    random.seed(42)
    for _ in range(count):
        x = random.randint(0, 1280)
        y = random.randint(0, 720)
        r = random.randint(1, 3)
        alpha = random.randint(40, 120)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(0, 229, 255, alpha))

def make_cover(filename, title_lines, subtitle, price, badge_label=None, checkmarks=None):
    img = Image.new("RGB", (1280, 720), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Fond dégradé simulé (bandes)
    for i in range(720):
        alpha = int(i / 720 * 15)
        draw.line([(0, i), (1280, i)], fill=(20, 0, 40 + alpha))

    # Points décoratifs
    import random
    random.seed(42)
    for _ in range(40):
        x = random.randint(0, 1280)
        y = random.randint(0, 720)
        r = random.randint(1, 3)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(0, 229, 255))

    # Logo WULIX (haut gauche)
    wulix_font = font(28, bold=True)
    draw.text((60, 45), "WULIX", font=wulix_font, fill=WHITE)
    # Ligne déco sous WULIX
    draw.line([(60, 82), (160, 82)], fill=CYAN, width=2)

    # Titre principal (lignes multiples)
    title_font = font(82, bold=True)
    title_small_font = font(68, bold=True)

    total_lines = len(title_lines)
    start_y = 140 if total_lines <= 2 else 120

    for i, line in enumerate(title_lines):
        f = title_font if len(line) < 20 else title_small_font
        bbox = draw.textbbox((0, 0), line, font=f)
        w = bbox[2] - bbox[0]
        x = (1280 - w) // 2
        draw.text((x, start_y + i * 95), line, font=f, fill=CYAN)

    # Sous-titre
    if subtitle:
        sub_font = font(34)
        sub_y = start_y + total_lines * 95 + 20
        bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        w = bbox[2] - bbox[0]
        x = (1280 - w) // 2
        draw.text((x, sub_y), subtitle, font=sub_font, fill=WHITE)

    # Checkmarks (liste de features)
    if checkmarks:
        check_font = font(26)
        check_y = start_y + total_lines * 95 + 80
        for item in checkmarks:
            bbox = draw.textbbox((0, 0), f"✓  {item}", font=check_font)
            w = bbox[2] - bbox[0]
            x = (1280 - w) // 2
            draw.text((x, check_y), f"->  {item}", font=check_font, fill=(180, 255, 180))
            check_y += 38

    # Badge prix (bas droite)
    price_font = font(52, bold=True)
    price_bbox = draw.textbbox((0, 0), price, font=price_font)
    pw = price_bbox[2] - price_bbox[0]

    badge_x2 = 1280 - 60
    badge_x1 = badge_x2 - pw - 40
    badge_y1 = 720 - 105
    badge_y2 = 720 - 35

    draw_rounded_rect(draw, [badge_x1, badge_y1, badge_x2, badge_y2], 15, PURPLE)
    draw.text((badge_x1 + 20, badge_y1 + 8), price, font=price_font, fill=WHITE)

    # Label badge (optionnel)
    if badge_label:
        label_font = font(20)
        lb = draw.textbbox((0,0), badge_label, font=label_font)
        lw = lb[2] - lb[0]
        lx = badge_x2 - lw
        draw.text((lx, badge_y1 - 30), badge_label, font=label_font, fill=GRAY)

    # Ligne déco bas
    draw.line([(60, 690), (500, 690)], fill=PURPLE, width=1)
    small_font = font(20)
    draw.text((60, 695), "wulix.fr", font=small_font, fill=GRAY)

    # Sauvegarde
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path, "PNG", quality=95)
    print(f"[OK] Cree : {path}")
    return path


# === PRODUIT 1 — Pack Scripts Python 29€ ===
make_cover(
    filename="cover_pack_scripts_python.png",
    title_lines=["Pack Scripts Python"],
    subtitle="5 automatisations prêtes à l'emploi",
    price="29€",
    badge_label="Téléchargement immédiat",
    checkmarks=[
        "Scraper de donnees",
        "Relance email automatique",
        "Générateur de rapports PDF",
        "Auto-poster LinkedIn",
        "Veille concurrentielle"
    ]
)

# === PRODUIT 2 — Pipeline LinkedIn 19€ ===
make_cover(
    filename="cover_pipeline_linkedin.png",
    title_lines=["Pipeline LinkedIn", "Automatisé"],
    subtitle="Workflow n8n prêt à importer",
    price="19€",
    badge_label="Template n8n — Aucun code requis",
    checkmarks=[
        "Publie automatiquement chaque semaine",
        "API LinkedIn officielle",
        "Import en 2 clics"
    ]
)

# === PRODUIT 3 — Guide PDF 9€ ===
make_cover(
    filename="cover_guide_automatisation.png",
    title_lines=["Automatise 5 tâches", "en 1 weekend"],
    subtitle="Sans coder — Guide PDF 20 pages",
    price="9€",
    badge_label="Outils 100% gratuits",
    checkmarks=[
        "Relances email automatiques",
        "Tableau de bord auto (Sheets)",
        "Posts réseaux programmés",
        "Alertes intelligentes",
        "Tri de fichiers automatique"
    ]
)

print("\n[DONE] 3 covers generees dans :", OUTPUT_DIR)
