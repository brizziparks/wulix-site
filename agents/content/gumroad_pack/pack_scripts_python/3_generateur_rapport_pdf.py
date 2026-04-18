# -*- coding: utf-8 -*-
"""
WULIX — Script 3 : Generateur de rapports PDF automatique
==========================================================
Genere un rapport PDF professionnel depuis un fichier CSV de donnees.
Ideal pour : rapports de ventes, suivi de projet, bilan mensuel.

Usage :
    pip install fpdf2
    python 3_generateur_rapport_pdf.py

Prerequis :
    - donnees_rapport.csv avec colonnes : date, description, montant
"""

from fpdf import FPDF
import csv
import datetime
import os

# === CONFIG ===
FICHIER_CSV    = "donnees_rapport.csv"
FICHIER_SORTIE = f"rapport_{datetime.date.today()}.pdf"
TITRE_RAPPORT  = "Rapport Mensuel"
NOM_ENTREPRISE = "WULIX"
AUTEUR         = "Omar Sylla"
# ==============

class RapportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 11)
        self.set_fill_color(124, 58, 237)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {NOM_ENTREPRISE}  |  {TITRE_RAPPORT}", fill=True, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}  |  Genere le {datetime.date.today()}  |  {NOM_ENTREPRISE}", align="C")

def charger_donnees(fichier):
    lignes = []
    try:
        with open(fichier, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lignes.append(row)
    except FileNotFoundError:
        # Donnees de demo si pas de CSV
        print(f"[INFO] {fichier} introuvable — utilisation de donnees demo")
        lignes = [
            {"date": "2026-04-01", "description": "Mission automatisation client A", "montant": "350"},
            {"date": "2026-04-05", "description": "Vente Pack Scripts Python Gumroad", "montant": "29"},
            {"date": "2026-04-10", "description": "Mission automatisation client B", "montant": "700"},
            {"date": "2026-04-12", "description": "Vente Guide PDF Gumroad", "montant": "9"},
            {"date": "2026-04-15", "description": "Mission n8n client C", "montant": "1050"},
            {"date": "2026-04-18", "description": "Vente Pipeline LinkedIn Gumroad", "montant": "19"},
        ]
    return lignes

def generer_pdf(donnees):
    pdf = RapportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "", 11)

    # Titre
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 14, TITRE_RAPPORT, align="C", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, f"Genere le {datetime.date.today()} par {AUTEUR}", align="C", ln=True)
    pdf.ln(8)

    # En-tete tableau
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(26, 0, 48)
    pdf.set_text_color(0, 229, 255)
    pdf.cell(35, 9, "Date", fill=True)
    pdf.cell(120, 9, "Description", fill=True)
    pdf.cell(35, 9, "Montant (EUR)", fill=True, align="R", ln=True)

    # Lignes
    total = 0.0
    pdf.set_font("Helvetica", "", 10)
    for i, ligne in enumerate(donnees):
        fill = i % 2 == 0
        pdf.set_fill_color(245, 240, 255) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(40, 40, 40)

        date  = ligne.get("date", "")
        desc  = ligne.get("description", "")
        mont  = ligne.get("montant", "0")

        try:
            montant = float(mont.replace(",", ".").replace(" ", "").replace("EUR", ""))
            total += montant
            mont_affiche = f"{montant:,.2f}"
        except ValueError:
            mont_affiche = mont

        pdf.cell(35, 8, date, fill=fill)
        pdf.cell(120, 8, desc[:60], fill=fill)
        pdf.cell(35, 8, mont_affiche, fill=fill, align="R", ln=True)

    # Total
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(124, 58, 237)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(155, 11, "  TOTAL", fill=True)
    pdf.cell(35, 11, f"{total:,.2f} EUR", fill=True, align="R", ln=True)

    # Resume
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 8, "Resume", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 7, f"Nombre de lignes : {len(donnees)}", ln=True)
    pdf.cell(0, 7, f"Total            : {total:,.2f} EUR", ln=True)
    pdf.cell(0, 7, f"Auteur           : {AUTEUR}  |  {NOM_ENTREPRISE}", ln=True)

    pdf.output(FICHIER_SORTIE)
    print(f"[OK] Rapport genere : {FICHIER_SORTIE}  ({len(donnees)} lignes, total {total:.2f} EUR)")

if __name__ == "__main__":
    donnees = charger_donnees(FICHIER_CSV)
    generer_pdf(donnees)
