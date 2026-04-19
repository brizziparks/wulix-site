"""
LAMINE — Agent Support Client
Lit les emails entrants, répond aux questions basiques, trie les demandes
"""
import os
import json
import datetime
import imaplib
import email
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] LAMINE | {msg}"
    print(line)
    with open(LOG_DIR / "lamine.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

# Base de connaissance pour réponses automatiques
FAQ = {
    "remboursement": {
        "keywords": ["remboursement", "rembourser", "refund", "annuler"],
        "response": """Bonjour,

Merci de nous avoir contactés. Concernant votre demande de remboursement :

Notre politique : remboursement complet sous 7 jours après l'achat si le produit n'a pas été téléchargé.

Pour traiter votre demande, j'ai besoin de :
- Votre email Gumroad
- La date d'achat
- La raison de votre demande

Je reviens vers vous sous 24h.

Cordialement,
Omar — WULIX Agency"""
    },
    "aide_technique": {
        "keywords": ["erreur", "bug", "marche pas", "fonctionne pas", "problème", "aide", "help"],
        "response": """Bonjour,

Merci de nous avoir contactés. Je vois que vous rencontrez une difficulté technique.

Pour vous aider efficacement, pourriez-vous me préciser :
1. Quel produit vous utilisez
2. Le message d'erreur exact (capture d'écran si possible)
3. Votre système d'exploitation (Windows/Mac/Linux)
4. La version de Python installée (si applicable)

Je vous réponds personnellement sous 4h ouvrées.

Cordialement,
Omar — WULIX Agency"""
    },
    "devis": {
        "keywords": ["devis", "tarif", "prix", "combien", "quote", "mission"],
        "response": """Bonjour,

Merci de votre intérêt pour WULIX Agency !

Pour vous préparer un devis personnalisé, j'ai besoin de quelques infos :
- Quelle tâche souhaitez-vous automatiser ?
- Quels outils utilisez-vous actuellement ?
- Quel est votre délai ?

En attendant, vous pouvez consulter nos tarifs indicatifs sur wulix.fr/services.html

Je vous réponds sous 48h.

Cordialement,
Omar — WULIX Agency"""
    }
}

def get_email_text(msg) -> str:
    """Extrait le texte d'un email"""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode("utf-8", errors="ignore")
    else:
        return msg.get_payload(decode=True).decode("utf-8", errors="ignore")
    return ""

def classify_email(text: str) -> str:
    """Classifie l'email selon les mots-clés"""
    text_lower = text.lower()
    for category, data in FAQ.items():
        for keyword in data["keywords"]:
            if keyword in text_lower:
                return category
    return "autre"

def send_auto_reply(to: str, subject: str, body: str) -> bool:
    """Envoie une réponse automatique"""
    try:
        from dotenv import load_dotenv
        load_dotenv(BASE_DIR.parent / ".env")

        gmail_user = os.getenv("GMAIL_USER")
        gmail_pass = os.getenv("GMAIL_APP_PASSWORD")
        if not gmail_user or not gmail_pass:
            log("Crédentials Gmail manquants")
            return False

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Re: {subject}"
        msg["From"] = f"Omar — WULIX Agency <{gmail_user}>"
        msg["To"] = to
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, to, msg.as_string())

        log(f"Réponse auto envoyée à {to}")
        return True
    except Exception as e:
        log(f"Erreur envoi: {e}")
        return False

def process_inbox():
    """Lit les emails non lus et répond aux questions basiques"""
    try:
        from dotenv import load_dotenv
        load_dotenv(BASE_DIR.parent / ".env")

        gmail_user = os.getenv("GMAIL_USER")
        gmail_pass = os.getenv("GMAIL_APP_PASSWORD")
        if not gmail_user or not gmail_pass:
            log("Crédentials Gmail manquants — skip lecture inbox")
            return

        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(gmail_user, gmail_pass)
        imap.select("INBOX")

        _, msgs = imap.search(None, "UNSEEN")
        email_ids = msgs[0].split()

        log(f"{len(email_ids)} email(s) non lu(s) trouvé(s)")

        tickets = []
        for eid in email_ids[-10:]:  # Max 10 emails à la fois
            _, data = imap.fetch(eid, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode("utf-8", errors="ignore")

            sender = msg["From"]
            body = get_email_text(msg)
            category = classify_email(body)

            ticket = {
                "id": eid.decode(),
                "from": sender,
                "subject": subject,
                "category": category,
                "date": msg["Date"]
            }
            tickets.append(ticket)
            log(f"Email [{category}] de {sender}: {subject[:50]}")

            # Réponse auto si catégorie connue
            if category in FAQ:
                # Extrait l'adresse email
                email_addr = sender.split("<")[-1].strip(">") if "<" in sender else sender
                send_auto_reply(email_addr, subject, FAQ[category]["response"])
            else:
                log(f"Email non classifié — nécessite réponse manuelle: {subject[:50]}")

        # Sauvegarde les tickets
        tickets_file = LOG_DIR / f"lamine_tickets_{datetime.date.today().strftime('%Y%m%d')}.json"
        with open(tickets_file, "w", encoding="utf-8") as f:
            json.dump(tickets, f, indent=2, ensure_ascii=False)

        imap.logout()
        log(f"Traitement terminé: {len(tickets)} ticket(s)")

    except Exception as e:
        log(f"Erreur lecture inbox: {e}")

def run():
    log("Démarrage LAMINE — support client")
    process_inbox()
    log("LAMINE terminé")

if __name__ == "__main__":
    run()
