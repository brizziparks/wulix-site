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
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
FINANCE_DIR = BASE_DIR / "finance"
LOG_DIR.mkdir(exist_ok=True)
FINANCE_DIR.mkdir(exist_ok=True)
load_dotenv(BASE_DIR.parent / ".env")

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

def load_yesterday_report() -> dict:
    """Charge le rapport d'hier pour la comparaison"""
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    report_file = FINANCE_DIR / f"rapport_{yesterday}.json"
    if report_file.exists():
        try:
            return json.loads(report_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def get_trend(today_val: float, yesterday_val: float) -> str:
    """Retourne une flèche de tendance avec le delta"""
    if yesterday_val == 0:
        return "🆕 nouveau"
    delta = today_val - yesterday_val
    pct = (delta / yesterday_val) * 100 if yesterday_val else 0
    if delta > 0:
        return f"▲ +{delta:.2f}€ (+{pct:.0f}%)"
    elif delta < 0:
        return f"▼ {delta:.2f}€ ({pct:.0f}%)"
    return "→ stable"

def generate_daily_report(stats: list) -> str:
    """Génère le rapport quotidien enrichi en Markdown"""
    today = datetime.date.today().strftime("%d/%m/%Y")
    now   = datetime.datetime.now().strftime("%H:%M")
    total_revenue  = sum(s.get("revenue_eur", 0)   for s in stats if "revenue_eur"  in s)
    total_sales    = sum(s.get("sales_count", 0)   for s in stats if "sales_count"  in s)
    has_error      = any("error" in s for s in stats)

    yesterday = load_yesterday_report()
    y_revenue  = yesterday.get("total_revenue", 0)
    y_sales    = yesterday.get("total_sales",   0)
    trend_rev  = get_trend(total_revenue, y_revenue)
    trend_sal  = get_trend(float(total_sales), float(y_sales))

    # Objectifs mensuels
    obj_mensuel = 500.0
    jour_du_mois = datetime.date.today().day
    jours_dans_mois = 30
    revenu_projete = (total_revenue / jour_du_mois * jours_dans_mois) if jour_du_mois else 0
    progression_obj = (total_revenue / obj_mensuel * 100) if obj_mensuel else 0

    lines = [
        f"# 📊 Rapport WULIX — {today} ({now})",
        "",
        "## 🎯 Résumé exécutif",
        f"- Revenus du jour : **{total_revenue:.2f}€** {trend_rev}",
        f"- Ventes du jour : **{total_sales}** {trend_sal}",
        f"- Projection mensuelle : **{revenu_projete:.0f}€** / objectif {obj_mensuel:.0f}€ ({progression_obj:.0f}%)",
        "",
        "## 📈 Détail par plateforme",
    ]

    for s in stats:
        platform = s.get("platform", "?").upper()
        if "error" in s:
            lines.append(f"\n### {platform} ⚠️")
            lines.append(f"Erreur : {s['error']}")
        else:
            revenue = s.get("revenue_eur", 0)
            sales   = s.get("sales_count", 0)
            lines.append(f"\n### {platform}")
            lines.append(f"- Ventes : {sales}")
            lines.append(f"- Revenus : {revenue:.2f}€")

    lines.append("")
    lines.append("## 🚀 Actions recommandées")
    actions = []
    if total_sales == 0:
        actions.append("⚠️ Aucune vente aujourd'hui → vérifier que les pages Gumroad sont actives")
        actions.append("💡 Publier un post LinkedIn ou envoyer une newsletter pour relancer le trafic")
    elif total_revenue < 20:
        actions.append("📢 Ventes faibles → programmer un post MARIAMA sur LinkedIn aujourd'hui")
    else:
        actions.append("✅ Bonne journée → maintenir le rythme de publication SAMBA/MARIAMA")

    if has_error:
        actions.append("🔧 Des APIs sont en erreur → vérifier les tokens dans .env")
    if not actions:
        actions.append("✅ Tout roule — continuer le plan hebdo")

    for a in actions[:3]:
        lines.append(f"- {a}")

    if has_error or total_sales == 0:
        lines.append("")
        lines.append("## 🚨 Alertes")
        if has_error:
            lines.append("- Token API manquant — rapport incomplet")
        if total_sales == 0:
            lines.append("- Aucune vente détectée — vérifier les plateformes manuellement")

    lines.append("")
    lines.append("---")
    lines.append(f"*Rapport NDEYE · {now} · wulix.fr*")

    # Sauvegarde aussi en JSON pour comparaison demain
    json_data = {"total_revenue": total_revenue, "total_sales": total_sales, "date": today, "stats": stats}
    today_str = datetime.date.today().strftime("%Y%m%d")
    (FINANCE_DIR / f"rapport_{today_str}.json").write_text(
        json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

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
        msg["Subject"] = f"[WULIX] Rapport du {today}"
        msg["From"] = gmail_user
        msg["To"] = "omarichard284@gmail.com"

        msg.attach(MIMEText(report_text, "plain", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.send_message(msg)

        log("Rapport envoye par email OK")
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

    print("\n" + report.encode("cp1252", errors="replace").decode("cp1252"))

    # Envoi email
    send_report_email(report)

    log("NDEYE terminé")

if __name__ == "__main__":
    run()
