# =============================================================================
# WULIX — Pack Automatisation PME
# Script  : email_relancer.py
# Version : 1.0.0
# Auteur  : WULIX (wulix.fr)
# Licence : Usage commercial autorisé — redistribution interdite
# =============================================================================
# DESCRIPTION :
#   Envoie automatiquement des emails de relance personnalisés à une liste de
#   prospects lus depuis un fichier CSV. Si le dernier contact date de plus de
#   X jours, un email est envoyé via SMTP (Gmail, Outlook, etc.).
#
# UTILISATION :
#   1. Remplis les variables de configuration ci-dessous
#   2. Prépare ton fichier CSV avec les colonnes : nom, email, derniere_contact
#      Exemple de ligne CSV : Jean Dupont,jean@exemple.fr,2024-03-01
#   3. Lance : python email_relancer.py
#
# DÉPENDANCES :
#   Aucune bibliothèque externe requise (modules Python standard uniquement)
# =============================================================================

import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# =============================================================================
# CONFIGURATION — Modifie ces valeurs avant de lancer le script
# =============================================================================

SMTP_SERVEUR        = "smtp.gmail.com"
SMTP_PORT           = 587
EMAIL_EXPEDITEUR    = "ton@email.com"
MOT_DE_PASSE        = "ton_mot_de_passe_app"
DELAI_RELANCE_JOURS = 7
FICHIER_CSV         = "prospects.csv"
SUJET_EMAIL         = "Retour sur notre échange — {nom}"
MODE_TEST           = True   # True = simulation, False = envoi réel

CORPS_EMAIL = """Bonjour {nom},

J'espère que vous allez bien.

Je me permets de revenir vers vous suite à notre dernier échange.
Avez-vous eu le temps de réfléchir à notre proposition ?

Je reste disponible pour répondre à vos questions.

Cordialement,
[Ton nom] — [Ton entreprise]
"""

# =============================================================================
# CODE PRINCIPAL
# =============================================================================

def charger_prospects(chemin_csv):
    prospects = []
    if not Path(chemin_csv).exists():
        print(f"[ERREUR] Fichier CSV introuvable : {chemin_csv}")
        return prospects
    try:
        with open(chemin_csv, newline='', encoding='utf-8') as f:
            for ligne in csv.DictReader(f):
                if all(col in ligne for col in ['nom', 'email', 'derniere_contact']):
                    prospects.append(ligne)
                else:
                    print(f"[AVERTISSEMENT] Ligne ignorée : {ligne}")
        print(f"[INFO] {len(prospects)} prospect(s) chargé(s)")
    except Exception as e:
        print(f"[ERREUR] Lecture CSV échouée : {e}")
    return prospects


def doit_relancer(date_str, delai_jours):
    try:
        date = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return (datetime.today() - date).days >= delai_jours
    except ValueError:
        print(f"[AVERTISSEMENT] Date invalide : '{date_str}'")
        return False


def envoyer_email(nom, email_dest):
    msg = MIMEMultipart()
    msg['From']    = EMAIL_EXPEDITEUR
    msg['To']      = email_dest
    msg['Subject'] = SUJET_EMAIL.format(nom=nom)
    msg.attach(MIMEText(CORPS_EMAIL.format(nom=nom), 'plain', 'utf-8'))
    try:
        with smtplib.SMTP(SMTP_SERVEUR, SMTP_PORT) as srv:
            srv.starttls()
            srv.login(EMAIL_EXPEDITEUR, MOT_DE_PASSE)
            srv.sendmail(EMAIL_EXPEDITEUR, email_dest, msg.as_string())
        return True
    except smtplib.SMTPAuthenticationError:
        print("[ERREUR] Authentification SMTP échouée.")
    except Exception as e:
        print(f"[ERREUR] Envoi échoué ({email_dest}) : {e}")
    return False


def main():
    print("=" * 55)
    print("  WULIX — Relance Email Automatique")
    print(f"  {datetime.today().strftime('%d/%m/%Y')} | Délai : {DELAI_RELANCE_JOURS}j | Test : {MODE_TEST}")
    print("=" * 55)

    envoyes = ignores = erreurs = 0

    for p in charger_prospects(FICHIER_CSV):
        nom, email, date = p['nom'].strip(), p['email'].strip(), p['derniere_contact'].strip()

        if not doit_relancer(date, DELAI_RELANCE_JOURS):
            print(f"[IGNORÉ]  {nom} — dernier contact < {DELAI_RELANCE_JOURS}j")
            ignores += 1
            continue

        if MODE_TEST:
            print(f"[TEST]    -> {nom} <{email}> (contact : {date})")
            envoyes += 1
        else:
            if envoyer_email(nom, email):
                print(f"[ENVOYÉ]  -> {nom} <{email}>")
                envoyes += 1
            else:
                erreurs += 1

    print(f"\n  Résumé : {envoyes} envoyé(s) | {ignores} ignoré(s) | {erreurs} erreur(s)")


if __name__ == "__main__":
    main()
