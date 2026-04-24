"""
KOFI — Agent Veille IA & Automatisation
Surveille les tendances IA chaque matin, genere un digest et l'envoie par email
"""
import os
import json
import datetime
import smtplib
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

GMAIL_USER     = os.getenv("GMAIL_USER", "omarichard284@gmail.com")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
DEST_EMAIL     = os.getenv("GMAIL_USER", "omarichard284@gmail.com")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Flux RSS a surveiller
RSS_FEEDS = [
    ("The Verge — AI",      "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("VentureBeat AI",      "https://venturebeat.com/category/ai/feed/"),
    ("MIT Tech Review AI",  "https://www.technologyreview.com/feed/"),
    ("HuggingFace Blog",    "https://huggingface.co/blog/feed.xml"),
    ("n8n Blog",            "https://blog.n8n.io/rss/"),
    ("Make Blog",           "https://www.make.com/en/blog/feed"),
]

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] KOFI | {msg}"
    print(line)
    with open(LOG_DIR / "kofi.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def fetch_rss(url: str, max_items: int = 5) -> list[dict]:
    """Recupere les derniers articles d'un flux RSS."""
    items = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
        root = ET.fromstring(raw)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        # Format RSS 2.0
        for item in root.findall(".//item")[:max_items]:
            title = item.findtext("title", "").strip()
            link  = item.findtext("link", "").strip()
            desc  = item.findtext("description", "").strip()[:200]
            items.append({"title": title, "link": link, "desc": desc})

        # Format Atom
        if not items:
            for entry in root.findall(".//atom:entry", ns)[:max_items]:
                title = entry.findtext("atom:title", "", ns).strip()
                link_el = entry.find("atom:link", ns)
                link = link_el.get("href", "") if link_el is not None else ""
                items.append({"title": title, "link": link, "desc": ""})

    except Exception as e:
        log(f"Erreur RSS {url[:50]} : {e}")
    return items


def collect_news() -> list[dict]:
    """Collecte les articles de tous les flux RSS."""
    all_items = []
    for source, url in RSS_FEEDS:
        log(f"Fetch {source}...")
        items = fetch_rss(url, max_items=4)
        for item in items:
            item["source"] = source
        all_items.extend(items)
        log(f"  {len(items)} articles")
    return all_items


def generate_digest_gemini(articles: list[dict]) -> str:
    """Genere le digest avec Gemini."""
    if not GEMINI_API_KEY:
        return generate_digest_simple(articles)

    # Construit le contexte
    ctx_lines = []
    for a in articles[:20]:
        ctx_lines.append(f"- [{a['source']}] {a['title']}")
        if a.get("desc"):
            ctx_lines.append(f"  {a['desc'][:120]}")

    ctx = "\n".join(ctx_lines)
    today = datetime.date.today().strftime("%d/%m/%Y")

    prompt = f"""Tu es KOFI, agent de veille IA pour WULIX.
Voici les actualites IA et automatisation du {today} :

{ctx}

Redige un digest email professionnel et concis pour Omar Sylla, fondateur de WULIX (agence IA/automatisation).
Le digest doit :
1. Commencer par un titre accrocheur
2. Selectionner les 5 infos les plus pertinentes pour un freelance IA/automatisation
3. Pour chaque info : 2-3 lignes max + pourquoi c'est important pour WULIX
4. Terminer par 1 opportunite business concrete (gig Fiverr, contenu LinkedIn, produit Gumroad)
5. Ton : professionnel mais direct, pas de blabla

Format HTML simple (h2, p, ul, li, strong). Pas de CSS inline. En francais."""

    try:
        import urllib.request
        import json as _json

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={GEMINI_API_KEY}"
        payload = _json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 1500, "temperature": 0.7}
        }).encode("utf-8")

        req = urllib.request.Request(url, data=payload,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = _json.loads(resp.read())

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        log(f"Gemini error: {e} — fallback simple")
        return generate_digest_simple(articles)


def generate_digest_simple(articles: list[dict]) -> str:
    """Fallback : digest HTML sans IA."""
    today = datetime.date.today().strftime("%d/%m/%Y")
    NL = "\n"
    lines = [
        "<h2>Veille IA WULIX — " + today + "</h2>",
        "<p>Voici les dernieres actus IA et automatisation :</p>",
        "<ul>",
    ]
    for a in articles[:10]:
        link = a.get("link", "#")
        title = a.get("title", "")
        source = a.get("source", "")
        lines.append(f'<li><strong>[{source}]</strong> <a href="{link}">{title}</a></li>')
    lines.append("</ul>")
    lines.append("<p><em>— Agent KOFI, WULIX</em></p>")
    return NL.join(lines)


def send_email(subject: str, html_body: str) -> bool:
    """Envoie le digest par email Gmail."""
    if not GMAIL_PASSWORD:
        log("GMAIL_APP_PASSWORD manquant — email non envoye")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["From"]    = GMAIL_USER
        msg["To"]      = DEST_EMAIL
        msg["Subject"] = subject

        today = datetime.date.today().strftime("%d/%m/%Y")
        full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8">
<style>
  body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #1a1a2e; }}
  h2 {{ color: #7c3aed; border-bottom: 2px solid #7c3aed; padding-bottom: 8px; }}
  a {{ color: #7c3aed; }}
  li {{ margin-bottom: 12px; line-height: 1.5; }}
  .footer {{ margin-top: 30px; padding: 12px; background: #f0f2f8;
             border-radius: 6px; font-size: 12px; color: #7070a0; }}
</style>
</head>
<body>
{html_body}
<div class="footer">
  <strong>KOFI</strong> — Agent Veille IA WULIX | {today}<br>
  <a href="https://wulix.fr">wulix.fr</a> | <a href="https://aisatou.rosmedia.fr">AISATOU</a>
</div>
</body>
</html>"""

        msg.attach(MIMEText(full_html, "html", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, DEST_EMAIL, msg.as_string())

        log(f"Email envoye a {DEST_EMAIL}")
        return True

    except Exception as e:
        log(f"Erreur envoi email : {e}")
        return False


def save_digest(html: str, articles: list[dict]):
    """Sauvegarde le digest en JSON pour archivage."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    out_dir = Path(__file__).parent / "content" / "veille"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"digest_{today}.json"
    data = {
        "date": today,
        "articles_count": len(articles),
        "sources": list({a["source"] for a in articles}),
        "html": html,
    }
    out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Digest sauvegarde : {out_file.name}")


def run():
    """Point d'entree principal de l'agent KOFI."""
    today = datetime.date.today().strftime("%d/%m/%Y")
    log(f"=== KOFI Veille IA — {today} ===")

    # Collecte
    articles = collect_news()
    log(f"Total : {len(articles)} articles collectes")

    if not articles:
        log("Aucun article — arret")
        return

    # Generation digest
    log("Generation du digest avec Gemini...")
    digest_html = generate_digest_gemini(articles)
    log(f"Digest genere ({len(digest_html)} caracteres)")

    # Sauvegarde
    save_digest(digest_html, articles)

    # Envoi email
    subject = f"[WULIX Veille] IA & Automatisation — {today}"
    ok = send_email(subject, digest_html)

    if ok:
        log("=== KOFI termine avec succes ===")
    else:
        log("=== KOFI termine (email non envoye) ===")

    return {"status": "ok", "articles": len(articles), "email_sent": ok}


if __name__ == "__main__":
    run()
