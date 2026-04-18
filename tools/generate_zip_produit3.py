# -*- coding: utf-8 -*-
"""WULIX - Cree le ZIP de livraison du Produit 3 (Guide PDF 9EUR)"""

import zipfile
import os

PACK_DIR = r"C:\Users\USER\.claude\projects\projet jarvis\agents\content\gumroad_pack"
COVERS_DIR = r"C:\Users\USER\.claude\projects\projet jarvis\ui\covers"
OUTPUT_ZIP = os.path.join(PACK_DIR, "WULIX_Guide_Automatisation_v1.0.zip")

# Fichiers a inclure
files = [
    (os.path.join(PACK_DIR, "guide_automatisation_wulix.pdf"), "guide_automatisation_wulix.pdf"),
    (os.path.join(COVERS_DIR, "cover_guide_automatisation.png"), "cover_guide_automatisation.png"),
]

# README bonus dans le ZIP
readme_content = """WULIX - Automatise 5 taches en 1 weekend
=========================================

Merci pour votre achat !

CONTENU DU PACK :
- guide_automatisation_wulix.pdf  : Guide complet 20 pages
- cover_guide_automatisation.png  : Image de couverture

SUPPORT :
Email : contact@wulix.fr
Site  : https://wulix.fr

LICENCE :
Usage personnel uniquement. Redistribution interdite.
(c) 2026 WULIX - Art. L.335-2 CPI
"""

with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
    for filepath, arcname in files:
        if os.path.exists(filepath):
            zf.write(filepath, arcname)
            print(f"[OK] Ajoute : {arcname}")
        else:
            print(f"[SKIP] Fichier manquant : {filepath}")
    # Ajouter le README
    zf.writestr("README.txt", readme_content)
    print("[OK] Ajoute : README.txt")

size_kb = os.path.getsize(OUTPUT_ZIP) // 1024
print(f"\n[DONE] ZIP cree : {OUTPUT_ZIP}")
print(f"       Taille   : {size_kb} Ko")
