"""
NDEYE — Agent Analytics & Reporting
Scrape les stats Fiverr/Gumroad chaque matin + rapport quotidien
"""
import os
import json
import datetime
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
FINANCE_DIR = BASE_DIR / "finance"
LOG_DIR.mkdir(exist_ok=True)
FINANCE_DIR.mkdir(exist_ok=True)

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] NDEYE | {msg}"
    print(line)
    with open(LOG_DIR / "ndeye.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

def get_gumroad_stats() -> dict:
    """Récupère les ventes Gumroad via API"""
    try:
        import requests
        from dotenv import load_dotenv
        load_dotenv(BASE_DIR.parent / ".env")

        token = os.getenv("GUMROAD_ACCESS_TOKEN")
        if not token:
            return {"error": "GUMROAD_ACCESS_TOKEN manquant dans .env"}

        today = datetime.date.today().isoformat()
        r = requests.get(
            "https://api.gumroad.com/v2/sales",
            params={"access_token": token, "after": today},
            timeout=10
        )
        data = r.json()

        if data.get("success"):
            sales = data.get("sales", [])
            total = sum(float(s.get("price", 0)) for s in sales) / 100
            return {
                "platform": "gumroad",
                "sales_count": len(sales),
                "revenue_eur": round(total, 2),
                "date": today
            }
        return {"platform": "gumroad", "error": data.get("message", "Erreur API")}
    except Exception as e:
        return {"platform": "gumroad", "error": str(e)}

def get_fiverr_stats() -> dict:
    """Fiverr n'a pas d'API publique — lecture du fichier de suivi manuel"""
    suivi_file = FINANCE_DIR / "suivi_manuel.json"
    if suivi_file.exists():
        data = json.loads(suivi_file.read_text(encoding="utf-8"))
        return data.get("fiverr", {"platform": "fiverr", "note": "Suivi manuel — mettre à jour suivi_manuel.json"})
    return {
        "platform": "fiverr",
        "sales_count": 0,
        "revenue_eur": 0,
        "note": "Pas de données — créer finance/suivi_manuel.json"
    }

def generate_daily_report(stats: list) -> str:
    """Génère le rapport quotidien en Markdown"""
    today = datetime.date.today().strftime("%d/%m/%Y")
    total_revenue = sum(s.get("revenue_eur", 0) for s in stats if "revenue_eur" in s)
    total_sales = sum(s.get("sales_count", 0) for s in stats if "sales_count" in s)

    lines = [
        f"# 📊 Rapport Quotidien WULIX — {today}",
        f"\n**Total du jour : {total_revenue:.2f}€ | {total_sales} vente(s)**\n",
        "---\n",
    ]

    for s in stats:
        platform = s.get("platform", "?").upper()
        if "error" in s:
            lines.append(f"## {platform}\n⚠️ {s['error']}\n")
        else:
            revenue = s.get("revenue_eur", 0)
            sales = s.get("sales_count", 0)
            lines.append(f"## {platform}\n- Ventes : {sales}\n- Revenus : {revenue:.2f}€\n")

    lines.append("---")
    lines.append(f"*Rapport généré automatiquement par NDEYE — {datetime.datetime.now().strftime('%H:%M')}*")
    return "\n".join(lines)

def send_report_email(report_text: str):
    """Envoie le rapport par email à omarichard284@gmail.com"""
    try:
        from dotenv import load_dotenv
        load_dotenv(BASE_DIR.parent / ".env")

        gmail_user = os.getenv("GMAIL_USER")
        gmail_pass = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_pass:
            log("GMAIL_USER / GMAIL_APP_PASSWORD manquants dans .env — email non envoyé")
            return False

        today = datetime.date.today().strftime("%d/%m/%Y")
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📊 WULIX — Rapport du {today}"
        msg["From"] = gmail_user
        msg["To"] = "omarichard284@gmail.com"

        msg.attach(MIMEText(report_text, "plain", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, "omarichard284@gmail.com", msg.as_string())

        log("Rapport envoyé par email ✓")
        return True
    except Exception as e:
        log(f"Erreur envoi email: {e}")
        return False

def run():
    log("Démarrage NDEYE — rapport quotidien")

    stats = [
        get_gumroad_stats(),
        get_fiverr_stats(),
    ]

    log(f"Stats collectées: {json.dumps(stats, ensure_ascii=False)}")

    report = generate_daily_report(stats)

    # Sauvegarde
    today_str = datetime.date.today().strftime("%Y%m%d")
    report_file = FINANCE_DIR / f"rapport_{today_str}.md"
    report_file.write_text(report, encoding="utf-8")
    log(f"Rapport sauvegardé: {report_file}")

    print("\n" + report)

    # Envoi email
    send_report_email(report)

    log("NDEYE terminé")

if __name__ == "__main__":
    run()
