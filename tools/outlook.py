"""
Intégration Outlook via exchangelib (Exchange/Office 365)
ou win32com (Outlook desktop installé sur Windows).
"""

import subprocess
import sys
from datetime import datetime, timedelta

# ── Méthode 1 : win32com (Outlook desktop) ───────────────────────────────────
try:
    import win32com.client
    WIN32 = True
except ImportError:
    WIN32 = False

# ── Méthode 2 : exchangelib (Exchange/Office 365 via credentials) ─────────────
try:
    from exchangelib import (
        Account, Credentials, Configuration,
        DELEGATE, EWSDateTime, EWSTimeZone,
        CalendarItem, Message, Mailbox,
    )
    EXCHANGELIB = True
except ImportError:
    EXCHANGELIB = False


# ─────────────────────────────────────────────────────────────────────────────
# Interface unifiée — détecte automatiquement ce qui est disponible
# ─────────────────────────────────────────────────────────────────────────────

def _get_outlook_app():
    """Retourne l'objet COM Outlook si disponible."""
    if not WIN32:
        return None
    try:
        return win32com.client.Dispatch("Outlook.Application")
    except Exception:
        return None


# ── Emails ────────────────────────────────────────────────────────────────────

def get_unread_emails(count: int = 10) -> str:
    """Lire les emails non lus."""
    app = _get_outlook_app()
    if app:
        return _outlook_unread(app, count)
    return "Outlook desktop non disponible. Configure les credentials Exchange dans .env"


def _outlook_unread(app, count: int) -> str:
    try:
        ns      = app.GetNamespace("MAPI")
        inbox   = ns.GetDefaultFolder(6)  # 6 = Inbox
        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        results = []
        unread_count = 0
        for i, msg in enumerate(messages):
            if unread_count >= count:
                break
            try:
                if msg.UnRead:
                    results.append(
                        f"{unread_count+1}. De : {msg.SenderName} <{msg.SenderEmailAddress}>\n"
                        f"   Objet : {msg.Subject}\n"
                        f"   Reçu  : {msg.ReceivedTime.strftime('%d/%m/%Y %H:%M')}\n"
                        f"   Aperçu: {str(msg.Body)[:150].strip()}...\n"
                    )
                    unread_count += 1
            except Exception:
                continue

        if not results:
            return "Aucun email non lu."
        return f"{unread_count} email(s) non lu(s) :\n\n" + "\n".join(results)
    except Exception as e:
        return f"Erreur lecture Outlook : {e}"


def search_emails(query: str, count: int = 5) -> str:
    """Rechercher des emails par mot-clé."""
    app = _get_outlook_app()
    if not app:
        return "Outlook non disponible."
    try:
        ns    = app.GetNamespace("MAPI")
        inbox = ns.GetDefaultFolder(6)
        items = inbox.Items
        items.Sort("[ReceivedTime]", True)

        results = []
        q = query.lower()
        for msg in items:
            if len(results) >= count:
                break
            try:
                if q in str(msg.Subject).lower() or q in str(msg.SenderName).lower():
                    results.append(
                        f"• {msg.Subject} — {msg.SenderName} ({msg.ReceivedTime.strftime('%d/%m/%Y')})"
                    )
            except Exception:
                continue

        return "\n".join(results) if results else f"Aucun email trouvé pour : {query}"
    except Exception as e:
        return f"Erreur : {e}"


def send_email(to: str, subject: str, body: str) -> str:
    """Rédiger et envoyer un email via Outlook."""
    app = _get_outlook_app()
    if not app:
        return "Outlook non disponible."
    try:
        mail = app.CreateItem(0)  # 0 = MailItem
        mail.To      = to
        mail.Subject = subject
        mail.Body    = body
        mail.Send()
        return f"Email envoyé à {to} : {subject}"
    except Exception as e:
        return f"Erreur envoi email : {e}"


def draft_email(to: str, subject: str, body: str) -> str:
    """Créer un brouillon (sans envoyer) — ouvre la fenêtre Outlook."""
    app = _get_outlook_app()
    if not app:
        return "Outlook non disponible."
    try:
        mail = app.CreateItem(0)
        mail.To      = to
        mail.Subject = subject
        mail.Body    = body
        mail.Display()  # Ouvre la fenêtre de composition
        return f"Brouillon ouvert dans Outlook pour : {to}"
    except Exception as e:
        return f"Erreur brouillon : {e}"


# ── Calendrier Outlook ────────────────────────────────────────────────────────

def get_calendar_today() -> str:
    """Voir les rendez-vous du jour."""
    return get_calendar_range(days=1)


def get_calendar_range(days: int = 7) -> str:
    """Voir les rendez-vous des N prochains jours."""
    app = _get_outlook_app()
    if not app:
        return "Outlook non disponible."
    try:
        ns  = app.GetNamespace("MAPI")
        cal = ns.GetDefaultFolder(9)  # 9 = Calendar
        items = cal.Items
        items.IncludeRecurrences = True
        items.Sort("[Start]")

        now   = datetime.now()
        end   = now + timedelta(days=days)
        start_str = now.strftime("%m/%d/%Y %H:%M %p")
        end_str   = end.strftime("%m/%d/%Y %H:%M %p")

        restriction = (
            f"[Start] >= '{start_str}' AND [Start] <= '{end_str}'"
        )
        restricted = items.Restrict(restriction)

        results = []
        for item in restricted:
            try:
                start = item.Start.strftime("%d/%m/%Y %H:%M")
                results.append(f"• {start} — {item.Subject} ({item.Location or 'Sans lieu'})")
            except Exception:
                continue

        label = "aujourd'hui" if days == 1 else f"{days} prochains jours"
        if not results:
            return f"Aucun rendez-vous {label}."
        return f"Agenda {label} :\n" + "\n".join(results)
    except Exception as e:
        return f"Erreur calendrier : {e}"


def create_meeting(subject: str, start: str, duration_min: int = 60,
                   location: str = "", body: str = "") -> str:
    """
    Créer un rendez-vous dans le calendrier Outlook.
    start : format 'DD/MM/YYYY HH:MM'
    """
    app = _get_outlook_app()
    if not app:
        return "Outlook non disponible."
    try:
        appt = app.CreateItem(1)  # 1 = AppointmentItem
        appt.Subject  = subject
        appt.Location = location
        appt.Body     = body

        dt = datetime.strptime(start, "%d/%m/%Y %H:%M")
        appt.Start    = dt.strftime("%m/%d/%Y %H:%M")
        appt.Duration = duration_min

        appt.Save()
        return f"Rendez-vous créé : '{subject}' le {start} ({duration_min} min)"
    except ValueError:
        return "Format de date invalide. Utilise : JJ/MM/AAAA HH:MM"
    except Exception as e:
        return f"Erreur création RDV : {e}"
