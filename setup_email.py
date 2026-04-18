#!/usr/bin/env python3
"""
Setup guidé pour connecter Outlook et Gmail à AISATOU.
Lance : python setup_email.py
"""

import sys
import os
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent
GOOGLE_DIR = BASE_DIR / "memory" / "google"

def header():
    print("\n" + "="*55)
    print("  AISATOU — Configuration Email & Agenda")
    print("="*55 + "\n")

def setup_outlook():
    print("\n── OUTLOOK ──────────────────────────────────────────")
    try:
        import win32com.client
        app = win32com.client.Dispatch("Outlook.Application")
        ns  = app.GetNamespace("MAPI")
        inbox = ns.GetDefaultFolder(6)
        count = inbox.Items.Count
        print(f"  Outlook detecte ! ({count} emails dans la boite de reception)")
        print("  Aucune configuration supplementaire necessaire.")
        print("  AISATOU peut lire tes emails et ton calendrier Outlook.")
        return True
    except ImportError:
        print("  pywin32 non installe. Lance : pip install pywin32")
        return False
    except Exception as e:
        print(f"  Outlook non detecte : {e}")
        print("  Assure-toi qu'Outlook est installe et ouvert.")
        return False

def setup_gmail():
    print("\n── GMAIL & GOOGLE CALENDAR ──────────────────────────")
    GOOGLE_DIR.mkdir(parents=True, exist_ok=True)
    creds_file = GOOGLE_DIR / "gmail_credentials.json"

    if not creds_file.exists():
        print("""
  Etapes pour connecter Gmail :

  1. Va sur : https://console.cloud.google.com/
  2. Cree un projet (ex: "AISATOU")
  3. Active ces deux APIs :
     • Gmail API
     • Google Calendar API
  4. Cree des identifiants OAuth2 :
     APIs & Services > Identifiants > + Creer des identifiants
     > ID client OAuth 2.0 > Type : Application de bureau
  5. Telecharge le fichier JSON
  6. Renomme-le "gmail_credentials.json"
  7. Deplace-le dans :
     """ + str(creds_file) + """

  Appuie sur Entree quand c'est fait...
        """)
        input()

    if not creds_file.exists():
        print("  Fichier non trouve. Gmail non configure.")
        return False

    print("  Fichier credentials.json trouve. Connexion en cours...")
    try:
        from tools.gmail import _get_service
        _get_service("gmail", "v1")
        print("  Gmail connecte avec succes !")
        _get_service("calendar", "v3")
        print("  Google Calendar connecte avec succes !")
        return True
    except Exception as e:
        print(f"  Erreur : {e}")
        return False

def test_all():
    print("\n── TEST FINAL ───────────────────────────────────────")

    # Test Outlook
    try:
        from tools.outlook import get_unread_emails
        result = get_unread_emails(3)
        print("  Outlook :", result[:80] + "..." if len(result) > 80 else result)
    except Exception as e:
        print(f"  Outlook : {e}")

    # Test Gmail
    try:
        from tools.gmail import gmail_unread
        result = gmail_unread(3)
        print("  Gmail   :", result[:80] + "..." if len(result) > 80 else result)
    except Exception as e:
        print(f"  Gmail   : {e}")

    # Test Calendar
    try:
        from tools.outlook import get_calendar_today
        result = get_calendar_today()
        print("  Agenda  :", result[:80] + "..." if len(result) > 80 else result)
    except Exception as e:
        print(f"  Agenda  : {e}")


if __name__ == "__main__":
    header()
    print("Ce script configure la connexion d'AISATOU")
    print("a Outlook, Gmail et Google Calendar.\n")

    ok_outlook = setup_outlook()
    ok_gmail   = setup_gmail()

    print("\n── RESUME ───────────────────────────────────────────")
    print(f"  Outlook          : {'OK' if ok_outlook else 'Non configure'}")
    print(f"  Gmail / GCal     : {'OK' if ok_gmail   else 'Non configure'}")

    if ok_outlook or ok_gmail:
        print("\n  Test de connexion...")
        test_all()

    print("\n" + "="*55)
    print("  Configuration terminee !")
    print("  Lance AISATOU : python aisatou.py")
    print("="*55 + "\n")
