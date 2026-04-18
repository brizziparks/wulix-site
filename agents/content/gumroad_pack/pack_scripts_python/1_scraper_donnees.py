# -*- coding: utf-8 -*-
"""
WULIX — Script 1 : Scraper de donnees web
==========================================
Scrape les titres, prix et descriptions d'une page e-commerce ou blog.
Exporte les resultats dans un fichier CSV.

Usage :
    pip install requests beautifulsoup4
    python 1_scraper_donnees.py
"""

import requests
from bs4 import BeautifulSoup
import csv
import datetime

# === CONFIG — modifie ces valeurs ===
URL_CIBLE = "https://books.toscrape.com/"   # Remplace par ton URL
FICHIER_SORTIE = f"donnees_{datetime.date.today()}.csv"
# =====================================

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; WULIXBot/1.0)"}

def scraper(url):
    print(f"[INFO] Scraping : {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERREUR] Impossible de joindre {url} : {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    resultats = []

    # --- Adapte ce bloc selon la structure de ta page ---
    for article in soup.select("article.product_pod"):
        titre = article.select_one("h3 a")
        prix  = article.select_one("p.price_color")
        dispo = article.select_one("p.availability")

        resultats.append({
            "titre": titre["title"] if titre else "N/A",
            "prix":  prix.text.strip() if prix else "N/A",
            "dispo": dispo.text.strip() if dispo else "N/A",
            "url":   url
        })
    # ----------------------------------------------------

    return resultats

def sauvegarder_csv(donnees, fichier):
    if not donnees:
        print("[INFO] Aucune donnee a sauvegarder.")
        return
    champs = list(donnees[0].keys())
    with open(fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(donnees)
    print(f"[OK] {len(donnees)} ligne(s) exportee(s) dans : {fichier}")

if __name__ == "__main__":
    donnees = scraper(URL_CIBLE)
    sauvegarder_csv(donnees, FICHIER_SORTIE)
    if donnees:
        print(f"\n--- Apercu ({min(3, len(donnees))} premiers resultats) ---")
        for d in donnees[:3]:
            print(d)
