"""
Intégration Gmail via Google API (OAuth2).
Setup guidé : python -m tools.gmail --setup
"""

import json
import os
import pickle
from datetime import datetime
from pathlib import Path

CREDENTIALS_DIR = Path(__file__).parent.parent / "memory" / "google"
TOKEN_FILE      = CREDENTIALS_DIR / "gmail_token.pickle"
CREDS_FILE      = CREDENTIALS_DIR / "gmail_credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/calendar",
]

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


def _get_service(api: str, version: str):
    """Retourne un service Google authentifié."""
    if not GOOGLE_AVAILABLE:
        raise RuntimeError(
            "google-api-python-client non installé. "
            "Lance : pip install google-auth google-auth-oauthlib google-api-python-client"
        )

    if not CREDS_FILE.exists():
        raise RuntimeError(
            f"Fichier credentials.json manquant.\n"
            f"1. Va sur https://console.cloud.google.com/\n"
            f"2. Crée un projet → Active Gmail API + Calendar API\n"
            f"3. Crée des identifiants OAuth2 Desktop\n"
            f"4. Télécharge credentials.json → place-le dans {CREDS_FILE}\n"
            f"5. Lance : python -m tools.gmail --setup"
        )

    creds = None
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build(api, version, credentials=creds)


# ── Gmail ─────────────────────────────────────────────────────────────────────

def gmail_unread(count: int = 10) -> str:
    """Lire les emails non lus Gmail."""
    try:
        svc = _get_service("gmail", "v1")
        results = svc.users().messages().list(
            userId="me", labelIds=["UNREAD", "INBOX"], maxResults=count
        ).execute()

        messages = results.get("messages", [])
        if not messages:
            return "Aucun email non lu."

        emails = []
        for m in messages:
            msg = svc.users().messages().get(
                userId="me", id=m["id"], format="metadata",
                metadataHeaders=["From", "Subject", "Date"]
            ).execute()

            headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
            snippet = msg.get("snippet", "")[:120]
            emails.append(
                f"• De : {headers.get('From','?')}\n"
                f"  Objet : {headers.get('Subject','?')}\n"
                f"  Aperçu : {snippet}..."
            )

        return f"{len(emails)} email(s) non lu(s) :\n\n" + "\n\n".join(emails)
    except RuntimeError as e:
        return str(e)
    except Exception as e:
        return f"Erreur Gmail : {e}"


def gmail_search(query: str, count: int = 5) -> str:
    """Rechercher des emails Gmail."""
    try:
        svc = _get_service("gmail", "v1")
        results = svc.users().messages().list(
            userId="me", q=query, maxResults=count
        ).execute()

        messages = results.get("messages", [])
        if not messages:
            return f"Aucun email trouvé pour : {query}"

        emails = []
        for m in messages:
            msg = svc.users().messages().get(
                userId="me", id=m["id"], format="metadata",
                metadataHeaders=["From", "Subject", "Date"]
            ).execute()
            headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
            emails.append(f"• {headers.get('Subject','?')} — {headers.get('From','?')}")

        return "\n".join(emails)
    except RuntimeError as e:
        return str(e)
    except Exception as e:
        return f"Erreur : {e}"


def gmail_send(to: str, subject: str, body: str) -> str:
    """Envoyer un email via Gmail."""
    import base64
    from email.mime.text import MIMEText
    try:
        svc = _get_service("gmail", "v1")
        msg = MIMEText(body)
        msg["to"]      = to
        msg["subject"] = subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        svc.users().messages().send(userId="me", body={"raw": raw}).execute()
        return f"Email envoyé à {to} : {subject}"
    except RuntimeError as e:
        return str(e)
    except Exception as e:
        return f"Erreur envoi Gmail : {e}"


# ── Google Calendar ───────────────────────────────────────────────────────────

def gcal_today() -> str:
    """Voir les événements Google Calendar du jour."""
    return gcal_range(days=1)


def gcal_range(days: int = 7) -> str:
    """Voir les événements des N prochains jours."""
    from datetime import timezone
    try:
        svc = _get_service("calendar", "v3")
        now  = datetime.utcnow().isoformat() + "Z"
        end  = (datetime.utcnow().replace(hour=23, minute=59) +
                __import__("datetime").timedelta(days=days-1)).isoformat() + "Z"

        events_result = svc.events().list(
            calendarId="primary",
            timeMin=now, timeMax=end,
            maxResults=20, singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])
        if not events:
            return f"Aucun événement dans les {days} prochains jours."

        lines = []
        for e in events:
            start = e["start"].get("dateTime", e["start"].get("date", ""))
            if "T" in start:
                dt = datetime.fromisoformat(start.replace("Z",""))
                start = dt.strftime("%d/%m %H:%M")
            lines.append(f"• {start} — {e.get('summary','Sans titre')}")

        label = "aujourd'hui" if days == 1 else f"{days} prochains jours"
        return f"Agenda Google ({label}) :\n" + "\n".join(lines)
    except RuntimeError as e:
        return str(e)
    except Exception as e:
        return f"Erreur Google Calendar : {e}"


def gcal_create(summary: str, start: str, duration_min: int = 60,
                description: str = "") -> str:
    """
    Créer un événement Google Calendar.
    start : format 'DD/MM/YYYY HH:MM'
    """
    try:
        svc = _get_service("calendar", "v3")
        dt_start = datetime.strptime(start, "%d/%m/%Y %H:%M")
        dt_end   = dt_start + __import__("datetime").timedelta(minutes=duration_min)

        event = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": dt_start.isoformat(), "timeZone": "Europe/Paris"},
            "end":   {"dateTime": dt_end.isoformat(),   "timeZone": "Europe/Paris"},
        }
        result = svc.events().insert(calendarId="primary", body=event).execute()
        return f"Événement créé : '{summary}' le {start}"
    except ValueError:
        return "Format date invalide. Utilise : JJ/MM/AAAA HH:MM"
    except RuntimeError as e:
        return str(e)
    except Exception as e:
        return f"Erreur création événement : {e}"


# ── Setup guide ───────────────────────────────────────────────────────────────

def setup_guide() -> str:
    return """
CONFIGURATION GMAIL & GOOGLE CALENDAR
======================================

1. Va sur : https://console.cloud.google.com/

2. Crée un nouveau projet (ex: "AISATOU")

3. Active les APIs :
   - Gmail API
   - Google Calendar API

4. Crée des identifiants :
   Menu : APIs > Identifiants > Créer des identifiants > ID client OAuth 2.0
   Type : Application de bureau
   Télécharge le fichier JSON

5. Place le fichier téléchargé ici :
   memory/google/gmail_credentials.json

6. Lance la connexion :
   python -m tools.gmail_setup

AISATOU s'occupera du reste !
"""


if __name__ == "__main__":
    import sys
    if "--setup" in sys.argv:
        print(setup_guide())
        # Déclenche le flux OAuth
        try:
            _get_service("gmail", "v1")
            print("Connexion Gmail reussie !")
        except Exception as e:
            print(f"Erreur : {e}")
