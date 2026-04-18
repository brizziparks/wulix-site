# -*- coding: utf-8 -*-
"""
WULIX — Script 2 : Relance email automatique
=============================================
Envoie des emails de relance personnalises depuis une liste CSV.
Utilise Gmail SMTP (ou tout autre SMTP).

Usage :
    python 2_relance_email.py

Prerequis :
    - Activer "Mots de passe d'application" dans Gmail
      (Compte Google > Securite > Validation en 2 etapes > Mots de passe d'app)
    - Creer contacts.csv avec colonnes : prenom, email, statut
"""

import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# === CONFIG — modifie ces valeurs ===
SMTP_HOST     = "smtp.gmail.com"
SMTP_PORT     = 587
MON_EMAIL     = "ton.email@gmail.com"
MOT_DE_PASSE  = "xxxx xxxx xxxx xxxx"   # Mot de passe d'application Gmail
FICHIER_CSV   = "contacts.csv"
SUJET         = "On fait le point ?"
# =====================================

TEMPLATE_CORPS = """\
Bonjour {prenom},

Je voulais prendre quelques minutes pour faire le point avec toi.

Suite a notre dernier echange, je voulais m'assurer que tout se passait bien
et voir si tu avais des questions ou des besoins specifiques.

N'hesite pas a me repondre directement a cet email — je reponds sous 24h.

A bientot,
Omar
WULIX | wulix.fr
"""

def charger_contacts(fichier):
    contacts = []
    try:
        with open(fichier, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("statut", "").lower() == "a_relancer":
                    contacts.append(row)
    except FileNotFoundError:
        print(f"[ERREUR] Fichier {fichier} introuvable.")
        print("[INFO] Creez contacts.csv avec colonnes : prenom,email,statut")
        print("[INFO] Valeurs 'statut' : a_relancer | envoye | ignore")
    return contacts

def envoyer_email(smtp, destinataire, prenom):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUJET
    msg["From"]    = MON_EMAIL
    msg["To"]      = destinataire

    corps = TEMPLATE_CORPS.format(prenom=prenom)
    msg.attach(MIMEText(corps, "plain", "utf-8"))

    smtp.sendmail(MON_EMAIL, destinataire, msg.as_string())

def main():
    contacts = charger_contacts(FICHIER_CSV)
    if not contacts:
        print("[INFO] Aucun contact a relancer.")
        return

    print(f"[INFO] {len(contacts)} contact(s) a relancer...")
    print(f"[INFO] Connexion SMTP {SMTP_HOST}:{SMTP_PORT}...")

    envoyes = 0
    erreurs = 0

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(MON_EMAIL, MOT_DE_PASSE)

            for contact in contacts:
                prenom = contact.get("prenom", "")
                email  = contact.get("email", "")
                if not email:
                    continue
                try:
                    envoyer_email(server, email, prenom)
                    print(f"[OK]  Email envoye a {prenom} <{email}>")
                    envoyes += 1
                except Exception as e:
                    print(f"[ERR] Echec pour {email} : {e}")
                    erreurs += 1

    except smtplib.SMTPAuthenticationError:
        print("[ERREUR] Authentification SMTP echouee. Verifiez MON_EMAIL et MOT_DE_PASSE.")
        return

    print(f"\n[DONE] {envoyes} email(s) envoye(s), {erreurs} erreur(s)")
    print(f"       Log : {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()
