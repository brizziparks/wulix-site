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
GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")

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


def collect_news_ddg() -> list[dict]:
    """Cherche les vraies actus IA du jour via DuckDuckGo."""
    items = []
    queries = [
        "AI automation news today 2026",
        "n8n make.com update 2026",
        "python AI agent news",
    ]
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            for query in queries:
                for r in ddgs.news(query, max_results=4):
                    items.append({
                        "title": r.get("title", ""),
                        "link": r.get("url", ""),
                        "desc": r.get("body", "")[:200],
                        "source": f"Web — {r.get('source', query)}"
                    })
        log(f"DuckDuckGo: {len(items)} actus trouvées")
    except Exception as e:
        log(f"DuckDuckGo error: {e}")
    return items


def collect_news() -> list[dict]:
    """Collecte les articles de tous les flux RSS + DuckDuckGo."""
    all_items = []
    for source, url in RSS_FEEDS:
        log(f"Fetch {source}...")
        items = fetch_rss(url, max_items=4)
        for item in items:
            item["source"] = source
        all_items.extend(items)
        log(f"  {len(items)} articles")
    # Enrichir avec recherche web directe
    ddg_items = collect_news_ddg()
    all_items.extend(ddg_items)
    return all_items


def generate_digest_gemini(articles: list[dict]) -> str:
    """Genere le digest avec Groq (priorité) ou Gemini (fallback)."""
    if not GEMINI_API_KEY and not GROQ_API_KEY:
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

    # Groq en priorité (pas de limite de quota journalier)
    if GROQ_API_KEY:
        try:
            import httpx, json as _json
            ctx_lines = [f"- [{a['source']}] {a['title']}" for a in articles[:20]]
            ctx = "\n".join(ctx_lines)
            today = datetime.date.today().strftime("%d/%m/%Y")
            prompt_groq = f"""Tu es KOFI, agent de veille IA pour WULIX.\nVoici les actualites IA et automatisation du {today} :\n\n{ctx}\n\nRedige un digest email HTML (h2, p, ul, li, strong) en français. 5 actus max, chacune en 2-3 lignes + impact WULIX. Termine par 1 opportunité business concrète pour WULIX."""
            r = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt_groq}], "max_tokens": 1200, "temperature": 0.7},
                timeout=25
            )
            return r.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            log(f"Groq error: {e} — fallback Gemini")

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


# ═══════════════════════════════════════════════════════════════════════════
# MODE "IDEES D'APPS VALIDEES" — scrape Reddit + HN pour detecter les pain points
# Lance : python agents/veille_agent.py --ideas
# ═══════════════════════════════════════════════════════════════════════════

REDDIT_FEEDS = [
    ("r/SaaS",                  "https://old.reddit.com/r/SaaS/.rss"),
    ("r/EntrepreneurRideAlong", "https://old.reddit.com/r/EntrepreneurRideAlong/.rss"),
    ("r/SideProject",           "https://old.reddit.com/r/SideProject/.rss"),
    ("r/automate",              "https://old.reddit.com/r/automate/.rss"),
    ("r/freelance",             "https://old.reddit.com/r/freelance/.rss"),
]

HN_FEED = ("Hacker News",       "https://news.ycombinator.com/rss")
REDDIT_UA = "WULIX-Veille/1.0 (by /u/wulixfr; contact:contact@wulix.fr)"


def fetch_reddit_rss(url: str, max_items: int = 15) -> list[dict]:
    """Reddit-specific fetcher avec UA approprie pour eviter le 403."""
    items = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": REDDIT_UA})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
        root = ET.fromstring(raw)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall(".//atom:entry", ns)[:max_items]:
            title = entry.findtext("atom:title", "", ns).strip()
            link_el = entry.find("atom:link", ns)
            link = link_el.get("href", "") if link_el is not None else ""
            content = entry.findtext("atom:content", "", ns).strip()
            # Strip HTML tags pour le matching de keywords
            import re as _re
            desc = _re.sub(r'<[^>]+>', ' ', content)[:300]
            items.append({"title": title, "link": link, "desc": desc})
    except Exception as e:
        log(f"Erreur Reddit {url[:50]} : {e}")
    return items

# Mots-cles signalant un pain point / besoin d'outil
PAIN_KEYWORDS = [
    "looking for", "is there a tool", "need a tool", "best way to", "how do you",
    "any recommendations", "tired of", "annoying", "wish there was", "frustrating",
    "anyone built", "how to automate", "is there any way",
    "cherche un outil", "comment automatiser", "y a-t-il", "besoin d'un",
    "quel outil", "marre de", "frustrant",
]


def collect_pain_points() -> list[dict]:
    """Collecte les posts Reddit + HN qui ressemblent a des pain points."""
    candidates = []
    feeds = REDDIT_FEEDS + [HN_FEED]

    for source, url in feeds:
        log(f"Scan {source}...")
        # Reddit utilise un fetcher dedie (UA specifique anti-403)
        if "reddit.com" in url:
            items = fetch_reddit_rss(url, max_items=15)
        else:
            items = fetch_rss(url, max_items=15)
        for item in items:
            text = (item.get("title", "") + " " + item.get("desc", "")).lower()
            score = sum(1 for kw in PAIN_KEYWORDS if kw in text)
            if score > 0:
                item["source"] = source
                item["pain_score"] = score
                candidates.append(item)
        log(f"  {len([c for c in candidates if c['source']==source])} pain points")

    # Trie par score decroissant
    candidates.sort(key=lambda x: x.get("pain_score", 0), reverse=True)
    return candidates


def generate_app_ideas_report(pain_points: list[dict]) -> str:
    """Genere un rapport d'idees d'apps via Gemini/Groq a partir des pain points."""
    if not pain_points:
        return "<p>Aucun pain point detecte cette semaine.</p>"

    if not GEMINI_API_KEY and not GROQ_API_KEY:
        # Fallback simple
        lines = ["<h2>Pain points detectes (top 10)</h2>", "<ul>"]
        for p in pain_points[:10]:
            lines.append(f'<li><strong>[{p["source"]}]</strong> <a href="{p["link"]}">{p["title"]}</a></li>')
        lines.append("</ul>")
        return "\n".join(lines)

    # Contexte pour le LLM
    ctx_lines = []
    for p in pain_points[:25]:
        ctx_lines.append(f"- [{p['source']} - score {p['pain_score']}] {p['title']}")
        if p.get("desc"):
            ctx_lines.append(f"  {p['desc'][:150]}")
        if p.get("link"):
            ctx_lines.append(f"  Lien: {p['link']}")
    ctx = "\n".join(ctx_lines)

    today = datetime.date.today().strftime("%d/%m/%Y")
    prompt = f"""Tu es KOFI, agent veille pour WULIX (agence automatisation IA freelance/PME).

Voici 25 posts Reddit/HN du {today} avec des mots-cles de pain points :

{ctx}

Mission : extrais les **10 IDEES D'APPS VALIDEES** les plus prometteuses (vraies demandes, pas du bruit).

Pour chaque idee, format HTML :

<div style="margin-bottom:20px;padding:12px;background:#f8f9ff;border-left:3px solid #7c3aed;border-radius:4px">
  <h3 style="margin:0 0 6px;color:#7c3aed">N. Titre court de l'idee</h3>
  <p><strong>Probleme :</strong> ...</p>
  <p><strong>Solution :</strong> ... (2 lignes max, technique simple Python/n8n/IA)</p>
  <p><strong>Difficulte :</strong> Facile/Moyen/Difficile · <strong>Potentiel :</strong> Faible/Moyen/Eleve</p>
  <p style="font-size:11px;color:#7c88a8"><strong>Source :</strong> <a href="LIEN">[source]</a></p>
</div>

Commence par <h2>10 idees d'apps validees — semaine du {today}</h2>.
Termine par <p><em>Selectionnees parmi {len(pain_points)} pain points detectes.</em></p>"""

    return _call_llm(prompt, max_tokens=2500) or generate_app_ideas_report_fallback(pain_points)


def generate_app_ideas_report_fallback(pain_points):
    lines = ["<h2>Pain points detectes (top 10)</h2>", "<ul>"]
    for p in pain_points[:10]:
        lines.append(f'<li><strong>[{p["source"]}]</strong> <a href="{p["link"]}">{p["title"]}</a></li>')
    lines.append("</ul>")
    return "\n".join(lines)


def _call_llm(prompt: str, max_tokens: int = 2000) -> str:
    """Appelle Groq (priorite) ou Gemini pour generer du contenu."""
    # Reuse la logique de generate_digest_gemini sans wrapper
    if GROQ_API_KEY:
        try:
            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=json.dumps({
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": 0.6,
                }).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {GROQ_API_KEY}"
                }
            )
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            log(f"Groq error: {e} — fallback Gemini")

    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
            req = urllib.request.Request(url,
                data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8"),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            log(f"Gemini error: {e}")
    return ""


def run_ideas():
    """Point d'entree mode 'idees d'apps validees'."""
    today = datetime.date.today().strftime("%d/%m/%Y")
    log(f"=== KOFI Idees d'apps — {today} ===")

    pain_points = collect_pain_points()
    log(f"Total : {len(pain_points)} pain points detectes")

    if not pain_points:
        log("Aucun pain point — arret")
        return

    log("Generation du rapport d'idees...")
    report_html = generate_app_ideas_report(pain_points)
    log(f"Rapport genere ({len(report_html)} caracteres)")

    # Sauvegarde
    out_dir = Path(__file__).parent / "content" / "ideas"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"idees_apps_{datetime.date.today().strftime('%Y%m%d')}.html"
    out_file.write_text(report_html, encoding="utf-8")
    log(f"Sauvegarde : {out_file}")

    # Email
    subject = f"[WULIX Ideas] 10 idees d'apps validees — {today}"
    ok = send_email(subject, report_html)

    if ok:
        log("=== KOFI Ideas termine avec succes ===")
    else:
        log("=== KOFI Ideas termine (email non envoye) ===")

    return {"status": "ok", "pain_points": len(pain_points), "email_sent": ok}


if __name__ == "__main__":
    import sys
    if "--ideas" in sys.argv:
        run_ideas()
    else:
        run()
