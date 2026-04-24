"""
ROKHAYA — Agent CRM & Emails
Relances automatiques acheteurs Gumroad + follow-up prospects
"""
import os
import json
import datetime
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
CONTENT_DIR = BASE_DIR / "content"
CRM_FILE = BASE_DIR / "crm_contacts.json"
LOG_DIR.mkdir(exist_ok=True)
load_dotenv(BASE_DIR.parent / ".env")

# Mode sécurisé : DRY_RUN=true par défaut (aucun email envoyé sans activation explicite)
ROKHAYA_DRY_RUN = os.getenv("ROKHAYA_DRY_RUN", "true").lower() == "true"

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] ROKHAYA | {msg}"
    print(line)
    with open(LOG_DIR / "rokhaya.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

def load_crm() -> list:
    if CRM_FILE.exists():
        return json.loads(CRM_FILE.read_text(encoding="utf-8"))
    return []

def save_crm(contacts: list):
    with open(CRM_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

def add_buyer(email: str, prenom: str, produit: str):
    """Ajoute un acheteur Gumroad au CRM"""
    contacts = load_crm()
    now = datetime.datetime.now().isoformat()

    # Vérifie doublon
    if any(c["email"] == email and c["produit"] == produit for c in contacts):
        log(f"Acheteur déjà dans le CRM: {email} / {produit}")
        return

    contacts.append({
        "email": email,
        "prenom": prenom,
        "produit": produit,
        "date_achat": now,
        "email_welcome_sent": False,
        "email_followup_sent": False,
        "email_upsell_sent": False,
        "notes": ""
    })
    save_crm(contacts)
    log(f"Acheteur ajouté au CRM: {prenom} ({email}) — {produit}")

def send_email(to: str, subject: str, body_html: str) -> bool:
    """Envoie un email via Gmail SMTP"""
    try:
        gmail_user = os.getenv("GMAIL_USER")
        gmail_pass = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_pass:
            log(f"Crédentials Gmail manquants — email non envoyé à {to}")
            return False

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"WULIX Agency <{gmail_user}>"
        msg["To"] = to
        msg.attach(MIMEText(body_html, "html", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, to, msg.as_string())

        log(f"Email envoyé à {to} — Sujet: {subject}")
        return True
    except Exception as e:
        log(f"Erreur envoi email à {to}: {e}")
        return False

def process_welcome_emails():
    """Envoie les emails de bienvenue aux nouveaux acheteurs"""
    contacts = load_crm()
    sent = 0

    # Charge le template email
    template_file = CONTENT_DIR / "email_template_acheteur_gumroad.html"
    if not template_file.exists():
        log("Template email introuvable — skip")
        return

    template = template_file.read_text(encoding="utf-8")

    for c in contacts:
        if not c["email_welcome_sent"]:
            body = template.replace("{{prenom}}", c["prenom"])
            body = body.replace("{{nom_produit}}", c["produit"])
            body = body.replace("{{lien_telechargement}}", "https://app.gumroad.com/library")

            success = send_email(
                to=c["email"],
                subject=f"🎉 Votre accès WULIX est prêt, {c['prenom']} !",
                body_html=body
            )
            if success:
                c["email_welcome_sent"] = True
                sent += 1

    save_crm(contacts)
    log(f"Emails de bienvenue envoyés: {sent}")

def process_followup_emails():
    """Envoie des emails de suivi 3 jours après l'achat"""
    contacts = load_crm()
    sent = 0
    now = datetime.datetime.now()

    for c in contacts:
        if c["email_welcome_sent"] and not c["email_followup_sent"]:
            achat = datetime.datetime.fromisoformat(c["date_achat"])
            jours = (now - achat).days

            if jours >= 3:
                body = f"""
                <div style="font-family:Arial;max-width:600px;margin:0 auto;">
                <h2>Bonjour {c['prenom']}, comment ça se passe ? 👋</h2>
                <p>Ça fait {jours} jours que vous avez téléchargé <strong>{c['produit']}</strong>.</p>
                <p>Avez-vous pu l'utiliser ? Y a-t-il quelque chose qui bloque ?</p>
                <p>Répondez directement à cet email — je vous aide personnellement.</p>
                <br>
                <p>Omar Sylla<br><a href="https://wulix.fr">WULIX Agency</a></p>
                </div>
                """
                success = send_email(
                    to=c["email"],
                    subject=f"Comment ça se passe avec {c['produit']} ?",
                    body_html=body
                )
                if success:
                    c["email_followup_sent"] = True
                    sent += 1

    save_crm(contacts)
    log(f"Emails de suivi envoyés: {sent}")

def run(action="all"):
    log(f"Démarrage ROKHAYA — action: {action}")

    if action in ("all", "welcome"):
        process_welcome_emails()
    if action in ("all", "followup"):
        process_followup_emails()

    contacts = load_crm()
    log(f"CRM: {len(contacts)} contact(s) au total")
    log("ROKHAYA terminée")

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "all"
    run(action)
