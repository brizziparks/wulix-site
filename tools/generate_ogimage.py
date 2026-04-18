"""WULIX - Generateur og-image.jpg pour SEO (1200x630px)"""
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT = r"C:\Users\USER\.claude\projects\projet jarvis\ui\og-image.jpg"
FONT_DIR = r"C:\Windows\Fonts"

def font(size, bold=False):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf" if bold else "arial.ttf"), size)
    except:
        return ImageFont.load_default()

img = Image.new("RGB", (1200, 630), (10, 0, 21))
draw = ImageDraw.Draw(img)

# Fond degrade
for i in range(630):
    v = int(i / 630 * 20)
    draw.line([(0, i), (1200, i)], fill=(10 + v, 0, 21 + v))

# Points decoratifs
import random
random.seed(99)
for _ in range(50):
    x, y = random.randint(0,1200), random.randint(0,630)
    r = random.randint(1,3)
    draw.ellipse([x-r,y-r,x+r,y+r], fill=(0,229,255))

# Bande gauche violette
draw.rectangle([0, 0, 8, 630], fill=(124, 58, 237))

# Logo WULIX
draw.text((50, 50), "WULIX", font=font(36, bold=True), fill=(255,255,255))
draw.line([(50, 95), (170, 95)], fill=(0,229,255), width=2)

# Titre principal
draw.text((50, 120), "Automatisation IA", font=font(72, bold=True), fill=(0,229,255))
draw.text((50, 205), "pour Freelances & PME", font=font(52, bold=True), fill=(255,255,255))

# Sous-titre
draw.text((50, 290), "Scripts Python  |  Agents IA  |  Workflows n8n", font=font(28), fill=(180,180,180))

# Separateur
draw.line([(50, 345), (700, 345)], fill=(124,58,237), width=1)

# Points forts
items = ["Livraison 48-72h", "Des 50 EUR", "100% sur mesure"]
x = 50
for item in items:
    draw.text((x, 365), "->  " + item, font=font(24), fill=(0,229,255))
    x += 340

# URL bas
draw.rectangle([0, 555, 1200, 630], fill=(20, 0, 40))
draw.text((50, 570), "wulix.fr  |  contact@wulix.fr", font=font(22), fill=(180,180,180))

# Badge "Solutions IA"
draw.rectangle([900, 130, 1150, 480], fill=(20, 0, 40))
draw.rectangle([900, 130, 1150, 131], fill=(0,229,255))
draw.text((920, 150), "Produits", font=font(18, bold=True), fill=(0,229,255))
products = [
    ("Pack Scripts", "Python  29EUR"),
    ("Pipeline", "LinkedIn  19EUR"),
    ("Guide", "Automatisation  9EUR"),
]
y = 195
for p1, p2 in products:
    draw.text((920, y), p1, font=font(16, bold=True), fill=(255,255,255))
    draw.text((920, y+20), p2, font=font(14), fill=(124,58,237))
    draw.line([(920, y+42), (1140, y+42)], fill=(30,0,50), width=1)
    y += 52

img.save(OUTPUT, "JPEG", quality=92)
print("[OK] og-image.jpg genere :", OUTPUT)
