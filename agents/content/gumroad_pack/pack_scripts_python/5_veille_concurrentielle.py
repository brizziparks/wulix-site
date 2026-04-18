# -*- coding: utf-8 -*-
"""
WULIX — Script 5 : Veille concurrentielle automatique
======================================================
Surveille des mots-cles sur le web et envoie un resume par email.
Sources : Google News RSS, pages web personnalisees.

Usage :
    pip install requests beautifulsoup4
    python 5_veille_concurrentielle.py

Le script genere un rapport HTML + envoi email facultatif.
"""

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import urllib.parse

# === CONFIG ===
MOTS_CLES = [
    "automatisation IA freelance",
    "agent Python automation",
    "n8n workflow automatisation",
    "no-code automation France",
]
FICHIER_RAPPORT = f"veille_{datetime.date.today()}.html"

# Email (optionnel — laisser vide pour desactiver)
ENVOYER_EMAIL  = False   # Mettre True pour activer
SMTP_HOST      = "smtp.gmail.com"
SMTP_PORT      = 587
MON_EMAIL      = "ton.email@gmail.com"
MOT_DE_PASSE   = "xxxx xxxx xxxx xxxx"
EMAIL_DEST     = "ton.email@gmail.com"
# ==============

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; WULIXBot/1.0)"}

def scrape_google_news(mot_cle):
    """Recupere les titres Google News pour un mot-cle via RSS."""
    q = urllib.parse.quote(mot_cle)
    url = f"https://news.google.com/rss/search?q={q}&hl=fr&gl=FR&ceid=FR:fr"
    resultats = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, "xml")
        items = soup.find_all("item")[:5]
        for item in items:
            titre = item.find("title").text if item.find("title") else "N/A"
            lien  = item.find("link").text if item.find("link") else "#"
            date  = item.find("pubDate").text[:16] if item.find("pubDate") else ""
            resultats.append({"titre": titre, "lien": lien, "date": date})
    except Exception as e:
        print(f"[ERR] {mot_cle} : {e}")
    return resultats

def generer_html(resultats_par_mot_cle):
    lignes_html = []
    lignes_html.append(f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">
<title>Veille WULIX — {datetime.date.today()}</title>
<style>
body{{font-family:Arial,sans-serif;background:#0a0015;color:#e0e0e0;padding:30px;}}
h1{{color:#00e5ff;}} h2{{color:#7c3aed;margin-top:30px;}}
a{{color:#00e5ff;}} li{{margin:8px 0;line-height:1.5;}}
.date{{color:#aaa;font-size:12px;margin-left:8px;}}
.footer{{color:#555;font-size:12px;margin-top:40px;}}
</style></head><body>
<h1>Veille Concurrentielle WULIX</h1>
<p style="color:#aaa">Rapport du {datetime.date.today()} — {sum(len(v) for v in resultats_par_mot_cle.values())} resultat(s)</p>
""")

    for mot_cle, resultats in resultats_par_mot_cle.items():
        lignes_html.append(f"<h2>{mot_cle}</h2><ul>")
        if not resultats:
            lignes_html.append("<li><i>Aucun resultat</i></li>")
        for r in resultats:
            lignes_html.append(
                f'<li><a href="{r["lien"]}" target="_blank">{r["titre"]}</a>'
                f'<span class="date">{r["date"]}</span></li>'
            )
        lignes_html.append("</ul>")

    lignes_html.append('<p class="footer">Genere par WULIX — wulix.fr</p></body></html>')
    return "\n".join(lignes_html)

def envoyer_email(corps_html):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Veille WULIX — {datetime.date.today()}"
    msg["From"]    = MON_EMAIL
    msg["To"]      = EMAIL_DEST
    msg.attach(MIMEText(corps_html, "html", "utf-8"))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(MON_EMAIL, MOT_DE_PASSE)
        server.sendmail(MON_EMAIL, EMAIL_DEST, msg.as_string())
    print(f"[OK] Email envoye a {EMAIL_DEST}")

def main():
    print(f"[INFO] Veille sur {len(MOTS_CLES)} mot(s)-cle(s)...")
    resultats = {}
    for mc in MOTS_CLES:
        print(f"  -> {mc}")
        resultats[mc] = scrape_google_news(mc)

    html = generer_html(resultats)
    with open(FICHIER_RAPPORT, "w", encoding="utf-8") as f:
        f.write(html)
    total = sum(len(v) for v in resultats.values())
    print(f"[OK] Rapport HTML genere : {FICHIER_RAPPORT} ({total} resultats)")

    if ENVOYER_EMAIL:
        envoyer_email(html)

if __name__ == "__main__":
    main()
