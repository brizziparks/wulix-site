# =============================================================================
# WULIX — Pack Automatisation PME
# Script  : rapport_hebdo.py
# Version : 1.0.0
# Auteur  : WULIX (wulix.fr)
# Licence : Usage commercial autorisé — redistribution interdite
# =============================================================================
# DESCRIPTION :
#   Lit un fichier CSV de données hebdomadaires (ventes, tâches, KPIs),
#   calcule les totaux/moyennes, génère un rapport HTML stylisé et l'envoie
#   par email. Peut être planifié via cron (Linux) ou le Planificateur
#   de tâches Windows pour s'exécuter chaque lundi matin.
#
# UTILISATION :
#   1. Configure les variables ci-dessous
#   2. Prépare ton CSV : date,categorie,valeur,description
#   3. Lance : python rapport_hebdo.py
#   Planification Windows : Planificateur de tâches -> chaque lundi 8h00
#   Planification Linux   : crontab -e -> 0 8 * * 1 python /chemin/rapport_hebdo.py
#
# DÉPENDANCES :
#   Aucune bibliothèque externe requise
# =============================================================================

import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# =============================================================================
# CONFIGURATION
# =============================================================================

SMTP_SERVEUR        = "smtp.gmail.com"
SMTP_PORT           = 587
EMAIL_EXPEDITEUR    = "ton@email.com"
MOT_DE_PASSE        = "ton_mot_de_passe_app"
EMAIL_DESTINATAIRE  = "rapport@tonentreprise.com"
FICHIER_CSV         = "donnees_semaine.csv"
NOM_ENTREPRISE      = "Mon Entreprise"
MODE_TEST           = True   # True = génère le HTML sans envoyer


def charger_donnees(chemin_csv):
    """Charge les données depuis le CSV. Colonnes : date, categorie, valeur, description"""
    donnees = []
    if not Path(chemin_csv).exists():
        print(f"[ERREUR] Fichier introuvable : {chemin_csv}")
        return donnees
    with open(chemin_csv, newline='', encoding='utf-8') as f:
        for ligne in csv.DictReader(f):
            try:
                ligne['valeur'] = float(ligne['valeur'])
                donnees.append(ligne)
            except (ValueError, KeyError):
                print(f"[AVERTISSEMENT] Ligne ignorée : {ligne}")
    return donnees


def calculer_stats(donnees):
    """Calcule totaux et moyennes par catégorie."""
    par_categorie = defaultdict(list)
    for d in donnees:
        par_categorie[d.get('categorie', 'Autre')].append(d['valeur'])

    stats = {}
    for cat, valeurs in par_categorie.items():
        stats[cat] = {
            'total'  : sum(valeurs),
            'moyenne': sum(valeurs) / len(valeurs),
            'count'  : len(valeurs),
            'max'    : max(valeurs),
            'min'    : min(valeurs),
        }
    return stats


def generer_html(donnees, stats):
    """Génère le rapport HTML complet."""
    aujourd_hui   = datetime.today()
    semaine_debut = aujourd_hui - timedelta(days=aujourd_hui.weekday() + 7)
    semaine_fin   = semaine_debut + timedelta(days=6)

    lignes_tableau = ""
    for d in donnees:
        lignes_tableau += f"""
        <tr>
            <td>{d.get('date','')}</td>
            <td><span class="badge">{d.get('categorie','')}</span></td>
            <td><strong>{d['valeur']:,.2f}</strong></td>
            <td>{d.get('description','')}</td>
        </tr>"""

    blocs_stats = ""
    for cat, s in stats.items():
        blocs_stats += f"""
        <div class="stat-card">
            <h3>{cat}</h3>
            <p class="stat-total">{s['total']:,.2f}</p>
            <p class="stat-label">Total</p>
            <hr>
            <p>Moyenne : <strong>{s['moyenne']:,.2f}</strong></p>
            <p>Entrées : <strong>{s['count']}</strong></p>
            <p>Max : {s['max']:,.2f} | Min : {s['min']:,.2f}</p>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rapport Hebdomadaire — {NOM_ENTREPRISE}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f4f6f9; color: #333; margin: 0; padding: 20px; }}
        .container {{ max-width: 900px; margin: auto; background: white; border-radius: 8px;
                      box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: white;
                   padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 26px; }}
        .header p {{ margin: 5px 0 0; opacity: 0.8; }}
        .section {{ padding: 25px; }}
        .section h2 {{ color: #1a1a2e; border-bottom: 2px solid #e8e8e8; padding-bottom: 8px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .stat-card {{ background: #f8f9ff; border: 1px solid #e0e4f0; border-radius: 8px;
                      padding: 15px; text-align: center; }}
        .stat-card h3 {{ margin: 0 0 8px; color: #444; font-size: 14px; text-transform: uppercase; }}
        .stat-total {{ font-size: 28px; font-weight: bold; color: #1a1a2e; margin: 5px 0; }}
        .stat-label {{ color: #888; font-size: 12px; margin: 0; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        th {{ background: #1a1a2e; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 9px 10px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f8f9ff; }}
        .badge {{ background: #e8f0fe; color: #1a73e8; padding: 2px 8px;
                  border-radius: 12px; font-size: 12px; }}
        .footer {{ background: #f4f6f9; text-align: center; padding: 15px;
                   font-size: 12px; color: #888; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Rapport Hebdomadaire</h1>
        <p>{NOM_ENTREPRISE} · Semaine du {semaine_debut.strftime('%d/%m')} au {semaine_fin.strftime('%d/%m/%Y')}</p>
    </div>
    <div class="section">
        <h2>Résumé par catégorie</h2>
        <div class="stats-grid">{blocs_stats}</div>
    </div>
    <div class="section">
        <h2>Détail des entrées</h2>
        <table>
            <thead><tr><th>Date</th><th>Catégorie</th><th>Valeur</th><th>Description</th></tr></thead>
            <tbody>{lignes_tableau}</tbody>
        </table>
    </div>
    <div class="footer">
        Généré le {aujourd_hui.strftime('%d/%m/%Y à %H:%M')} · WULIX Automatisation
    </div>
</div>
</body>
</html>"""
    return html


def envoyer_rapport(html):
    msg = MIMEMultipart('alternative')
    msg['From']    = EMAIL_EXPEDITEUR
    msg['To']      = EMAIL_DESTINATAIRE
    msg['Subject'] = f"Rapport Hebdomadaire — {NOM_ENTREPRISE} — {datetime.today().strftime('%d/%m/%Y')}"
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    try:
        with smtplib.SMTP(SMTP_SERVEUR, SMTP_PORT) as srv:
            srv.starttls()
            srv.login(EMAIL_EXPEDITEUR, MOT_DE_PASSE)
            srv.sendmail(EMAIL_EXPEDITEUR, EMAIL_DESTINATAIRE, msg.as_string())
        print(f"[ENVOYÉ] Rapport envoyé à {EMAIL_DESTINATAIRE}")
    except Exception as e:
        print(f"[ERREUR] Envoi échoué : {e}")


def main():
    print("=" * 55)
    print("  WULIX — Rapport Hebdomadaire")
    print(f"  {datetime.today().strftime('%d/%m/%Y %H:%M')} | Test : {MODE_TEST}")
    print("=" * 55)

    donnees = charger_donnees(FICHIER_CSV)
    if not donnees:
        print("[FIN] Aucune donnée à traiter.")
        return

    stats = calculer_stats(donnees)
    html  = generer_html(donnees, stats)

    fichier_sortie = f"rapport_{datetime.today().strftime('%Y_%m_%d')}.html"
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[SAUVEGARDÉ] Rapport HTML -> {fichier_sortie}")

    if not MODE_TEST:
        envoyer_rapport(html)
    else:
        print(f"[TEST] Email non envoyé (MODE_TEST=True). Ouvre {fichier_sortie} pour prévisualiser.")


if __name__ == "__main__":
    main()
