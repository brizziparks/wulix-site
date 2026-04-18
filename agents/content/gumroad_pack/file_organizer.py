# =============================================================================
# WULIX — Pack Automatisation PME
# Script  : file_organizer.py
# Version : 1.0.0
# Auteur  : WULIX (wulix.fr)
# Licence : Usage commercial autorisé — redistribution interdite
# =============================================================================
# DESCRIPTION :
#   Organise automatiquement un dossier en sous-dossiers.
#   3 modes :
#     - PAR TYPE    : images/, docs/, videos/, audio/, archives/, autres/
#     - PAR DATE    : 2024-01/, 2024-02/, etc.
#     - PAR MOT-CLE : sous-dossiers selon mots-clés dans le nom du fichier
#   Mode dry-run intégré pour prévisualiser sans rien déplacer.
#
# UTILISATION :
#   1. Configure les variables ci-dessous
#   2. Mets MODE_DRY_RUN = True pour prévisualiser
#   3. Lance : python file_organizer.py
#   4. Vérifie le résultat, puis mets MODE_DRY_RUN = False pour exécuter
#
# DÉPENDANCES :
#   Aucune bibliothèque externe requise
# =============================================================================

import os
import shutil
from pathlib import Path
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================

DOSSIER_SOURCE    = r"C:\Users\USER\Downloads"   # Windows
# DOSSIER_SOURCE  = "/home/user/Downloads"        # Linux/Mac

MODE_ORGANISATION = "type"    # "type" | "date" | "mot-cle"
MODE_DRY_RUN      = True      # True = aperçu | False = déplace réellement
RECURSIF          = False     # False = seulement les fichiers du niveau racine

# =============================================================================
# CLASSIFICATION PAR TYPE (extensions)
# =============================================================================

CATEGORIES_PAR_EXTENSION = {
    "images"   : [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff", ".raw"],
    "videos"   : [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpeg"],
    "audio"    : [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".opus"],
    "docs"     : [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".pages"],
    "tableurs" : [".xls", ".xlsx", ".csv", ".ods", ".numbers"],
    "slides"   : [".ppt", ".pptx", ".odp", ".key"],
    "code"     : [".py", ".js", ".ts", ".html", ".css", ".php", ".java", ".cpp", ".c", ".go", ".rb", ".sql"],
    "archives" : [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "exe"      : [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
    "ebooks"   : [".epub", ".mobi", ".azw", ".cbr", ".cbz"],
}
DOSSIER_AUTRES = "autres"

# =============================================================================
# CLASSIFICATION PAR MOT-CLE
# =============================================================================

REGLES_MOTS_CLES = {
    "facture"   : "Factures",
    "invoice"   : "Factures",
    "contrat"   : "Contrats",
    "contract"  : "Contrats",
    "cv"        : "CV_Recrutement",
    "resume"    : "CV_Recrutement",
    "rapport"   : "Rapports",
    "report"    : "Rapports",
    "photo"     : "Photos",
    "screenshot": "Captures_Ecran",
    "capture"   : "Captures_Ecran",
}
DOSSIER_SANS_MOT_CLE = "Non_classés"


def trouver_categorie_par_type(extension):
    ext_lower = extension.lower()
    for categorie, extensions in CATEGORIES_PAR_EXTENSION.items():
        if ext_lower in extensions:
            return categorie
    return DOSSIER_AUTRES


def trouver_categorie_par_date(chemin_fichier):
    timestamp = chemin_fichier.stat().st_mtime
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m")


def trouver_categorie_par_mot_cle(nom_fichier):
    nom_lower = nom_fichier.lower()
    for mot_cle, dossier in REGLES_MOTS_CLES.items():
        if mot_cle in nom_lower:
            return dossier
    return DOSSIER_SANS_MOT_CLE


def obtenir_chemin_destination(fichier, mode):
    if mode == "type":
        categorie = trouver_categorie_par_type(fichier.suffix)
    elif mode == "date":
        categorie = trouver_categorie_par_date(fichier)
    elif mode == "mot-cle":
        categorie = trouver_categorie_par_mot_cle(fichier.name)
    else:
        print(f"[ERREUR] Mode inconnu : '{mode}'")
        return None
    return Path(DOSSIER_SOURCE) / categorie / fichier.name


def resoudre_conflit_nom(chemin_destination):
    if not chemin_destination.exists():
        return chemin_destination
    stem = chemin_destination.stem
    suffix = chemin_destination.suffix
    parent = chemin_destination.parent
    compteur = 1
    while True:
        nouveau_nom = parent / f"{stem}({compteur}){suffix}"
        if not nouveau_nom.exists():
            return nouveau_nom
        compteur += 1


def lister_fichiers(dossier, recursif):
    dossier_path = Path(dossier)
    if recursif:
        return [f for f in dossier_path.rglob('*') if f.is_file()]
    else:
        return [f for f in dossier_path.iterdir() if f.is_file()]


def main():
    print("=" * 60)
    print("  WULIX — Organisateur de Fichiers")
    print(f"  Mode : {MODE_ORGANISATION.upper()} | Dry-run : {MODE_DRY_RUN}")
    print(f"  Dossier : {DOSSIER_SOURCE}")
    print("=" * 60)

    if not Path(DOSSIER_SOURCE).exists():
        print(f"[ERREUR] Dossier introuvable : {DOSSIER_SOURCE}")
        return

    if MODE_DRY_RUN:
        print("\n  [DRY-RUN] Simulation — aucun fichier ne sera déplacé.\n")

    fichiers = lister_fichiers(DOSSIER_SOURCE, RECURSIF)
    print(f"[INFO] {len(fichiers)} fichier(s) trouvé(s)\n")

    if not fichiers:
        print("[FIN] Aucun fichier à organiser.")
        return

    deplacements = {}
    nb_ok = nb_err = 0

    for fichier in fichiers:
        destination = obtenir_chemin_destination(fichier, MODE_ORGANISATION)
        if not destination:
            continue
        destination = resoudre_conflit_nom(destination)
        dossier_dest = destination.parent.name
        deplacements[dossier_dest] = deplacements.get(dossier_dest, 0) + 1

        print(f"  {'[DRY-RUN]' if MODE_DRY_RUN else '[DÉPLACER]'} {fichier.name}")
        print(f"            -> {dossier_dest}/{destination.name}")

        if not MODE_DRY_RUN:
            try:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(fichier), str(destination))
                nb_ok += 1
            except PermissionError:
                print(f"  [ERREUR] Permission refusée : {fichier.name}")
                nb_err += 1
            except Exception as e:
                print(f"  [ERREUR] {fichier.name} : {e}")
                nb_err += 1
        else:
            nb_ok += 1

    print("\n" + "=" * 60)
    print("  Résumé des destinations :")
    for dossier, count in sorted(deplacements.items(), key=lambda x: -x[1]):
        print(f"    {dossier:25s} : {count} fichier(s)")
    print(f"\n  Total : {nb_ok} traité(s) | {nb_err} erreur(s)")
    if MODE_DRY_RUN:
        print("\n  Pour exécuter, mets MODE_DRY_RUN = False")
    print("=" * 60)


if __name__ == "__main__":
    main()
