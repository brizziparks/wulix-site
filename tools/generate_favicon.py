"""WULIX - Generateur favicon"""
from PIL import Image, ImageDraw, ImageFont
import os

FONT_DIR = r"C:\Windows\Fonts"
UI = r"C:\Users\USER\.claude\projects\projet jarvis\ui"

def font(size, bold=True):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf" if bold else "arial.ttf"), size)
    except:
        return ImageFont.load_default()

def make_icon(size):
    img = Image.new("RGBA", (size, size), (124, 58, 237, 255))
    draw = ImageDraw.Draw(img)
    # Lettre W centree
    f = font(int(size * 0.65))
    bbox = draw.textbbox((0, 0), "W", font=f)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - w) // 2 - bbox[0]
    y = (size - h) // 2 - bbox[1]
    draw.text((x, y), "W", font=f, fill=(255, 255, 255, 255))
    return img

# ICO multi-taille (16 + 32)
icon32 = make_icon(32)
icon16 = make_icon(16)
ico_path = os.path.join(UI, "favicon.ico")
icon32.save(ico_path, format="ICO", sizes=[(16,16),(32,32)])
print(f"[OK] favicon.ico : {ico_path}")

# PNG 192 pour PWA
icon192 = make_icon(192)
png_path = os.path.join(UI, "favicon-192.png")
icon192.save(png_path, "PNG")
print(f"[OK] favicon-192.png : {png_path}")
