"""
Génère la cover Gumroad Produit 3 — "Automatise 5 tâches en 1 weekend"
1280 x 720 px
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUTPUT = Path("C:/Users/USER/.claude/projects/projet jarvis/agents/content/gumroad_pack/cover_guide_automatisation.png")

W, H = 1280, 720

img = Image.new("RGB", (W, H), "#0a0015")
draw = ImageDraw.Draw(img)

# Dégradé fond
for y in range(H):
    ratio = y / H
    r = int(10 + ratio * 15)
    g = int(0)
    b = int(21 + ratio * 20)
    for x in range(W):
        xr = x / W
        r2 = int(r + xr * 20)
        draw.point((x, y), fill=(min(r2,60), g, min(b,60)))

# Particules déco
import random
random.seed(42)
for _ in range(120):
    x = random.randint(0, W)
    y = random.randint(0, H)
    size = random.randint(1, 3)
    alpha = random.randint(40, 140)
    draw.ellipse([x, y, x+size, y+size], fill=(alpha, 0, alpha*2))

# Bande violette gauche
draw.rectangle([0, 0, 6, H], fill="#7c3aed")

# Bande violette basse
draw.rectangle([0, H-6, W, H], fill="#7c3aed")

# Logo WULIX haut gauche
try:
    font_logo = ImageFont.truetype("arialbd.ttf", 28)
except:
    font_logo = ImageFont.load_default()
draw.text((40, 36), "WULIX", fill="#7c3aed", font=font_logo)

# Badge "GUIDE PDF"
draw.rounded_rectangle([38, 80, 175, 110], radius=6, fill="#1a0030")
try:
    font_badge = ImageFont.truetype("arial.ttf", 16)
except:
    font_badge = ImageFont.load_default()
draw.text((55, 88), "GUIDE PDF", fill="#c4b5fd", font=font_badge)

# Titre ligne 1
try:
    font_title = ImageFont.truetype("arialbd.ttf", 72)
except:
    font_title = ImageFont.load_default()

draw.text((40, 145), "Automatise 5 tâches", fill="#00dcff", font=font_title)
draw.text((40, 230), "en 1 weekend", fill="#00dcff", font=font_title)

# Sous-titre
try:
    font_sub = ImageFont.truetype("arial.ttf", 38)
except:
    font_sub = ImageFont.load_default()
draw.text((40, 330), "Sans écrire une seule ligne de code", fill="#e2e8f0", font=font_sub)

# Séparateur
draw.rectangle([40, 400, 300, 403], fill="#7c3aed")

# 5 points
try:
    font_pts = ImageFont.truetype("arial.ttf", 22)
except:
    font_pts = ImageFont.load_default()

points = [
    "Relances email automatiques",
    "Tableau de bord en temps réel",
    "Posts réseaux planifiés",
    "Alertes intelligentes",
    "Fichiers organisés auto",
]
y_pt = 425
for pt in points:
    draw.text((40, y_pt), "✓", fill="#7c3aed", font=font_pts)
    draw.text((68, y_pt), pt, fill="#94a3b8", font=font_pts)
    y_pt += 34

# Badge prix (droite)
draw.rounded_rectangle([980, 260, 1200, 380], radius=20, fill="#7c3aed")
try:
    font_prix = ImageFont.truetype("arialbd.ttf", 90)
except:
    font_prix = ImageFont.load_default()
draw.text((1010, 265), "9€", fill="white", font=font_prix)

try:
    font_prix2 = ImageFont.truetype("arial.ttf", 20)
except:
    font_prix2 = ImageFont.load_default()
draw.text((993, 390), "Téléchargement immédiat", fill="#94a3b8", font=font_prix2)

# URL bas droite
try:
    font_url = ImageFont.truetype("arial.ttf", 22)
except:
    font_url = ImageFont.load_default()
draw.text((980, 660), "wulix.fr", fill="#7c3aed", font=font_url)

img.save(str(OUTPUT), "PNG", quality=95)
print(f"Cover générée : {OUTPUT}")
