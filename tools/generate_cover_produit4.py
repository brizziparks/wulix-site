"""
Génère la cover Gumroad Produit 4 — "Pack 50 Prompts IA"
1280 x 720 px
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random

OUTPUT = Path("C:/Users/USER/.claude/projects/projet jarvis/agents/content/gumroad_pack/cover_prompts_ia.png")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 1280, 720

img = Image.new("RGB", (W, H), "#00100a")
draw = ImageDraw.Draw(img)

# Dégradé fond vert sombre -> noir
for y in range(H):
    ratio = y / H
    r = int(0 + ratio * 5)
    g = int(20 - ratio * 10)
    b = int(10 + ratio * 5)
    for x in range(W):
        xr = x / W
        g2 = int(g + xr * 15)
        draw.point((x, y), fill=(r, min(g2, 40), b))

# Particules déco
random.seed(99)
for _ in range(100):
    x = random.randint(0, W)
    y = random.randint(0, H)
    size = random.randint(1, 3)
    alpha = random.randint(30, 120)
    draw.ellipse([x, y, x+size, y+size], fill=(0, alpha, alpha//2))

# Bande verte gauche
draw.rectangle([0, 0, 6, H], fill="#00dc82")
# Bande verte basse
draw.rectangle([0, H-6, W, H], fill="#00dc82")

# Logo WULIX
try:
    font_logo = ImageFont.truetype("arialbd.ttf", 28)
except:
    font_logo = ImageFont.load_default()
draw.text((40, 36), "WULIX", fill="#00dc82", font=font_logo)

# Badge
draw.rounded_rectangle([38, 80, 155, 110], radius=6, fill="#001a0d")
try:
    font_badge = ImageFont.truetype("arial.ttf", 16)
except:
    font_badge = ImageFont.load_default()
draw.text((52, 88), "PACK PDF", fill="#00dc82", font=font_badge)

# Titre
try:
    font_title = ImageFont.truetype("arialbd.ttf", 78)
except:
    font_title = ImageFont.load_default()
draw.text((40, 145), "50 Prompts IA", fill="#00dc82", font=font_title)

# Sous-titre
try:
    font_sub = ImageFont.truetype("arialbd.ttf", 38)
except:
    font_sub = ImageFont.load_default()
draw.text((40, 255), "Prets a l'emploi", fill="#ffffff", font=font_sub)

# Desc
try:
    font_desc = ImageFont.truetype("arial.ttf", 26)
except:
    font_desc = ImageFont.load_default()
draw.text((40, 320), "ChatGPT  /  Claude  /  Gemini", fill="#94a3b8", font=font_desc)

# Separateur
draw.rectangle([40, 375, 280, 378], fill="#00dc82")

# 5 catégories
try:
    font_pts = ImageFont.truetype("arial.ttf", 21)
except:
    font_pts = ImageFont.load_default()

cats = ["Redaction", "Automatisation", "Analyse", "Business", "Productivite"]
y_pt = 398
for cat in cats:
    draw.text((40, y_pt), "✓", fill="#00dc82", font=font_pts)
    draw.text((65, y_pt), cat, fill="#94a3b8", font=font_pts)
    y_pt += 32

# Badge prix droite
draw.rounded_rectangle([980, 260, 1200, 370], radius=20, fill="#00dc82")
try:
    font_prix = ImageFont.truetype("arialbd.ttf", 95)
except:
    font_prix = ImageFont.load_default()
draw.text((1020, 263), "5EUR", fill="#001a0d", font=font_prix)

try:
    font_prix2 = ImageFont.truetype("arial.ttf", 20)
except:
    font_prix2 = ImageFont.load_default()
draw.text((993, 385), "Telechargement immediat", fill="#94a3b8", font=font_prix2)

# URL bas droite
try:
    font_url = ImageFont.truetype("arial.ttf", 22)
except:
    font_url = ImageFont.load_default()
draw.text((980, 660), "wulix.fr", fill="#00dc82", font=font_url)

img.save(str(OUTPUT), "PNG", quality=95)
print(f"Cover generee : {OUTPUT}")
