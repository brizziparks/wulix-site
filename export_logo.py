#!/usr/bin/env python3
"""
WULIX — Export Logo
Génère les logos PNG dans toutes les tailles nécessaires
depuis le SVG source.

Requires: pip install cairosvg pillow
"""

import sys
from pathlib import Path

BASE_DIR  = Path(__file__).parent
SVG_FILE  = BASE_DIR / "ui" / "WULIX_logo.svg"
OUT_DIR   = BASE_DIR / "ui" / "brand"
OUT_DIR.mkdir(exist_ok=True)

# Tailles par plateforme
SIZES = {
    "logo_400x400.png":          400,   # Standard
    "twitter_profile_400x400.png": 400, # Twitter profil
    "linkedin_logo_300x300.png": 300,   # LinkedIn page logo
    "fiverr_profile_250x250.png":  250, # Fiverr profil
    "favicon_32x32.png":           32,  # Favicon site
    "favicon_64x64.png":           64,  # Favicon HD
    "og_image_logo_200x200.png":  200,  # Open Graph
}

def export_with_cairosvg():
    try:
        import cairosvg
        svg_data = SVG_FILE.read_bytes()
        for filename, size in SIZES.items():
            out = OUT_DIR / filename
            cairosvg.svg2png(bytestring=svg_data, write_to=str(out),
                           output_width=size, output_height=size)
            print(f"  ✅ {filename} ({size}x{size}px)")
        return True
    except ImportError:
        return False

def export_with_pillow_fallback():
    """Fallback : ouvre le SVG dans le navigateur pour export manuel."""
    import webbrowser
    print("  ⚠️  cairosvg non installé — ouverture du SVG dans le navigateur")
    print("  → Fais clic droit > Enregistrer sous pour chaque taille")
    webbrowser.open(str(SVG_FILE))

if __name__ == "__main__":
    print("\n🎨 WULIX — Export Logo")
    print("=" * 40)
    print(f"Source : {SVG_FILE.name}")
    print(f"Output : {OUT_DIR}")
    print()

    if not SVG_FILE.exists():
        print("❌ SVG introuvable !")
        sys.exit(1)

    print("Tentative export cairosvg...")
    if not export_with_cairosvg():
        # Essaie pip install
        import subprocess
        print("  Installation cairosvg...")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "cairosvg", "-q"],
                          capture_output=True)
        if r.returncode == 0:
            if not export_with_cairosvg():
                export_with_pillow_fallback()
        else:
            export_with_pillow_fallback()

    print()
    print(f"✅ Logos dans : {OUT_DIR}")
    print("=" * 40)
