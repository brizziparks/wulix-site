"""
Génère la cover Gumroad Bundle — "Pack Complet WULIX"
1280 x 720 px
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random

OUTPUT = Path("C:/Users/USER/.claude/projects/projet jarvis/agents/content/gumroad_pack/cover_bundle_complet.png")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 1280, 720

img = Image.new("RGB", (W, H), "#00100a")
draw = ImageDraw.Draw(img)

# Fond dégradé
for y in range(H):
    ratio = y / H
    r = int(0 + ratio * 5)
    g = int(20 - ratio * 10)
    b = int(10 + ratio * 5)
    for x in range(W):
        xr = x / W
        g2 = int(g + xr * 15)
        draw.point((x, y), fill=(r, min(g2, 40), b))

# Particules
random.seed(42)
for _ in range(80):
    x = random.randint(0, W)
    y = random.randint(0, H)
    size = random.randint(1, 3)
    alpha = random.randint(20, 100)
    draw.ellipse([x, y, x+size, y+size], fill=(0, alpha, alpha//2))

# Bordures vertes
draw.rectangle([0, 0, 6, H], fill="#00dc82")
draw.rectangle([0, H-6, W, H], fill="#00dc82")

# Logo
try:
    font_logo = ImageFont.truetype("arialbd.ttf", 28)
except:
    font_logo = ImageFont.load_default()
draw.text((40, 36), "WULIX", fill="#00dc82", font=font_logo)

# Badge BUNDLE
draw.rounded_rectangle([38, 80, 175, 112], radius=6, fill="#00dc82")
try:
    font_badge = ImageFont.truetype("arialbd.ttf", 16)
except:
    font_badge = ImageFont.load_default()
draw.text((52, 89), "PACK COMPLET", fill="#001a0d", font=font_badge)

# Titre principal
try:
    font_title = ImageFont.truetype("arialbd.ttf", 68)
except:
    font_title = ImageFont.load_default()
draw.text((40, 140), "Automatise ton", fill="#00dc82", font=font_title)
draw.text((40, 220), "Business", fill="#00dc82", font=font_title)

# Sous-titre
try:
    font_sub = ImageFont.truetype("arialbd.ttf", 30)
except:
    font_sub = ImageFont.load_default()
draw.text((40, 305), "4 produits. 1 achat. Tout de suite.", fill="#ffffff", font=font_sub)

# Séparateur
draw.rectangle([40, 352, 320, 355], fill="#00dc82")

# 4 produits listés
try:
    font_pts = ImageFont.truetype("arial.ttf", 19)
except:
    font_pts = ImageFont.load_default()

produits = [
    "Scripts Python (29EUR)",
    "Pipeline LinkedIn n8n (19EUR)",
    "Guide PDF 5 taches (9EUR)",
    "50 Prompts IA (5EUR)",
]
y_pt = 372
for p in produits:
    draw.text((40, y_pt), "->", fill="#00dc82", font=font_pts)
    draw.text((72, y_pt), p, fill="#94a3b8", font=font_pts)
    y_pt += 30

# Badge prix
draw.rounded_rectangle([960, 240, 1210, 380], radius=20, fill="#00dc82")
try:
    font_prix = ImageFont.truetype("arialbd.ttf", 80)
except:
    font_prix = ImageFont.load_default()
draw.text((985, 243), "45EUR", fill="#001a0d", font=font_prix)

try:
    font_old = ImageFont.truetype("arial.ttf", 22)
except:
    font_old = ImageFont.load_default()
draw.text((975, 395), "Au lieu de 62EUR  (-27%)", fill="#94a3b8", font=font_old)
draw.text((1010, 425), "Telechargement immediat", fill="#94a3b8", font=font_old)

# URL bas droite
try:
    font_url = ImageFont.truetype("arial.ttf", 22)
except:
    font_url = ImageFont.load_default()
draw.text((980, 660), "wulix.fr", fill="#00dc82", font=font_url)

img.save(str(OUTPUT), "PNG", quality=95)
print(f"Cover bundle generee : {OUTPUT}")
