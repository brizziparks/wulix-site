"""
KOUMAN — Agent Prospecteur WULIX
Trouve des leads qualifiés sur Reddit, LinkedIn et forums freelance
"""
import os
import json
import datetime
import urllib.request
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LEADS_DIR = Path(__file__).parent / "content" / "leads"
LEADS_DIR.mkdir(parents=True, exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Mots-clés signalant un besoin d'automatisation IA
KEYWORDS_POSITIVE = [
    "automatisation", "automation", "workflow", "n8n", "make.com", "zapier",
    "gain de temps", "répétitif", "scraper", "python script", "freelance IA",
    "besoin dev", "cherche développeur", "mission python", "automatiser",
    "no-code", "low-code", "integration api", "besoin automatisation"
]

KEYWORDS_NEGATIVE = ["gratuit", "free", "unpaid", "bénévolat", "volunteer"]

# Sources Reddit (subreddits pertinents)
REDDIT_SOURCES = [
    "r/freelance_fr",
    "r/devops_fr",
    "r/python",
    "r/n8n",
    "r/zapier",
    "r/nocode",
    "r/entrepreneur",
]


def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] KOUMAN | {msg}"
    print(line)
    with open(LOG_DIR / "kouman.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def fetch_reddit_hot(subreddit: str, limit: int = 25) -> list:
    """Récupère les posts chauds d'un subreddit."""
    posts = []
    try:
        url = f"https://www.reddit.com/{subreddit}/hot.json?limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "WULIX-Prospecteur/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        for child in data.get("data", {}).get("children", []):
            p = child.get("data", {})
            posts.append({
                "title": p.get("title", ""),
                "text": p.get("selftext", "")[:500],
                "url": f"https://reddit.com{p.get('permalink', '')}",
                "score": p.get("score", 0),
                "subreddit": subreddit,
                "created": datetime.datetime.fromtimestamp(p.get("created_utc", 0)).isoformat()
            })
    except Exception as e:
        log(f"Erreur Reddit {subreddit}: {e}")
    return posts


def scorer_lead(post: dict) -> int:
    """Score un lead de 0 à 10."""
    texte = (post.get("title", "") + " " + post.get("text", "")).lower()
    score = 0
    for kw in KEYWORDS_POSITIVE:
        if kw.lower() in texte:
            score += 1
    for kw in KEYWORDS_NEGATIVE:
        if kw.lower() in texte:
            score -= 3
    return max(0, min(10, score))


def qualifier_lead_gemini(post: dict) -> dict:
    """Qualifie un lead avec Gemini et génère un message d'approche."""
    if not GEMINI_API_KEY:
        return {"score_ia": 0, "analyse": "Gemini non configuré", "message": ""}

    prompt = f"""Tu es KOUMAN, agent de prospection pour WULIX (agence automatisation IA).
Analyse ce post et dis si c'est un lead pour nos services :

Titre : {post['title']}
Texte : {post['text'][:300]}
Source : {post['subreddit']}

Réponds en JSON :
{{
  "pertinent": true/false,
  "besoin": "description courte du besoin",
  "score": 0-10,
  "message_approche": "message de 2-3 lignes pour répondre à ce post (naturel, pas commercial)"
}}"""

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={GEMINI_API_KEY}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 400, "temperature": 0.5}
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        # Extraire JSON
        if "```" in text:
            text = text.split("```")[1].lstrip("json").strip()
        return json.loads(text)
    except Exception as e:
        log(f"Gemini error: {e}")
        return {"pertinent": False, "score": 0, "message_approche": ""}


def prospecter() -> dict:
    """Lance la prospection sur toutes les sources."""
    today = datetime.date.today().isoformat()
    log(f"=== KOUMAN Prospection — {today} ===")

    all_posts = []
    for sub in REDDIT_SOURCES:
        posts = fetch_reddit_hot(sub, limit=15)
        log(f"  {sub}: {len(posts)} posts")
        all_posts.extend(posts)

    # Filtrage préliminaire
    candidats = []
    for p in all_posts:
        s = scorer_lead(p)
        if s >= 2:
            p["score_mots_cles"] = s
            candidats.append(p)

    candidats.sort(key=lambda x: x["score_mots_cles"], reverse=True)
    log(f"Candidats filtrés : {len(candidats)}/{len(all_posts)}")

    # Qualification Gemini (top 10 seulement pour économiser le quota)
    leads_qualifies = []
    for p in candidats[:10]:
        qualif = qualifier_lead_gemini(p)
        if qualif.get("pertinent") and qualif.get("score", 0) >= 5:
            p["qualif"] = qualif
            leads_qualifies.append(p)
            log(f"  Lead qualifié [{qualif.get('score', 0)}/10]: {p['title'][:60]}")

    # Sauvegarde
    out_file = LEADS_DIR / f"leads_{today}.json"
    result = {
        "date": today,
        "posts_analysés": len(all_posts),
        "candidats": len(candidats),
        "leads_qualifiés": len(leads_qualifies),
        "leads": leads_qualifies
    }
    out_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Leads sauvegardés : {out_file.name}")

    # Email résumé si leads trouvés
    if leads_qualifies:
        _envoyer_rapport_email(leads_qualifies, today)

    return result


def _envoyer_rapport_email(leads: list, date_str: str):
    """Envoie un email avec les leads du jour."""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    gmail_user = os.getenv("GMAIL_USER", "")
    gmail_pwd = os.getenv("GMAIL_APP_PASSWORD", "")
    if not gmail_pwd:
        log("Gmail non configuré — email skippé")
        return

    lines = [f"<h2>🎯 KOUMAN — {len(leads)} leads qualifiés — {date_str}</h2>", "<ul>"]
    for l in leads:
        q = l.get("qualif", {})
        lines.append(f"""<li>
  <strong>[{q.get('score', 0)}/10] {l['title'][:80]}</strong><br>
  Besoin : {q.get('besoin', '')}<br>
  Approche : <em>{q.get('message_approche', '')}</em><br>
  <a href="{l['url']}">Voir le post</a>
</li>""")
    lines.append("</ul><p><em>— Agent KOUMAN, WULIX</em></p>")
    body = "\n".join(lines)

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = gmail_user
        msg["To"] = gmail_user
        msg["Subject"] = f"[WULIX Prospection] {len(leads)} leads — {date_str}"
        msg.attach(MIMEText(body, "html", "utf-8"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(gmail_user, gmail_pwd)
            s.sendmail(gmail_user, gmail_user, msg.as_string())
        log(f"Email rapport envoyé")
    except Exception as e:
        log(f"Erreur email: {e}")


if __name__ == "__main__":
    result = prospecter()
    print(f"\nRésultat: {result['leads_qualifiés']} leads qualifiés sur {result['posts_analysés']} posts analysés")
