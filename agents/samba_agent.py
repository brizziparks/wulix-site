"""
SAMBA — Agent SEO Continu
Publie 1 article/semaine auto dans blog.html, surveille les positions
"""
import os
import json
import datetime
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
UI_DIR = BASE_DIR.parent / "ui"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] SAMBA | {msg}"
    print(line)
    with open(LOG_DIR / "samba.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

ARTICLE_TOPICS = [
    {
        "title": "Comment automatiser ses relances clients avec Python en 30 minutes",
        "keyword": "automatiser relances clients python",
        "intro": "Vous perdez du temps à relancer manuellement vos clients ? Voici comment Python peut le faire pour vous en 30 minutes de setup.",
        "sections": [
            ("Le problème : les relances manuelles coûtent cher", "Chaque email de relance envoyé manuellement représente 3 à 5 minutes de travail. Multiplié par 20 clients actifs, c'est 1h30 par semaine minimum."),
            ("La solution Python en 3 étapes", "1. Lire votre liste clients depuis un CSV\\n2. Vérifier qui n'a pas payé ou répondu\\n3. Envoyer l'email personnalisé automatiquement"),
            ("Le code complet", "Notre script email_relancer.py du Pack Scripts Python fait exactement ça. Configurez-le une fois, il tourne tout seul."),
            ("Résultat attendu", "Nos clients réduisent leur temps de relance de 90%. Un consultant a récupéré 6h par mois.")
        ]
    },
    {
        "title": "n8n vs Make.com : lequel choisir pour automatiser votre business ?",
        "keyword": "n8n vs make.com automatisation",
        "intro": "Deux outils d'automatisation no-code dominent le marché. Voici une comparaison honnête pour choisir celui qui vous convient.",
        "sections": [
            ("n8n : open-source et puissant", "n8n s'installe sur votre propre serveur. Zéro coût récurrent, données chez vous, personnalisation totale."),
            ("Make.com : simple et rapide", "Make.com est cloud, plus intuitif pour les débutants. Idéal pour démarrer sans serveur."),
            ("Notre recommandation", "TPE avec budget limité et données sensibles → n8n. Indépendant qui veut aller vite → Make.com."),
            ("Et WULIX dans tout ça ?", "On maîtrise les deux. On vous aide à choisir et configurer selon votre situation réelle.")
        ]
    },
    {
        "title": "5 tâches que vous pouvez automatiser ce week-end (sans coder)",
        "keyword": "automatisation sans code débutant",
        "intro": "Vous pensez que l'automatisation c'est réservé aux développeurs ? Ces 5 exemples prouvent le contraire.",
        "sections": [
            ("1. Sauvegarder vos fichiers automatiquement", "Google Drive + Make.com : chaque nouveau fichier dans un dossier est automatiquement sauvegardé. Setup : 10 min."),
            ("2. Répondre aux formulaires de contact", "Un formulaire reçu → email de confirmation envoyé → notification Slack. Zéro code, 15 min."),
            ("3. Planifier vos posts LinkedIn", "Google Sheets + n8n → LinkedIn. Remplissez la feuille le dimanche, les posts partent toute la semaine."),
            ("4. Facturer automatiquement", "Stripe + n8n → PDF facture généré et envoyé dès qu'un paiement arrive."),
            ("5. Veille concurrentielle", "Notre script surveille les prix de vos concurrents et vous envoie un email si ça change.")
        ]
    }
]

def generate_article_html(topic: dict) -> str:
    """Génère le HTML d'un article SEO"""
    today = datetime.date.today().strftime("%d %B %Y")
    sections_html = ""
    for title, content in topic["sections"]:
        sections_html += f"""
            <h2>{title}</h2>
            <p>{content.replace(chr(10), '</p><p>')}</p>
        """

    return f"""
    <article data-id="samba_{datetime.date.today().strftime('%Y%m%d')}" style="display:none;">
        <button onclick="showListe()" style="background:none;border:none;color:#7c3aed;cursor:pointer;font-size:14px;margin-bottom:24px;">← Retour au blog</button>
        <h1 style="font-size:clamp(1.5rem,4vw,2.2rem);font-weight:800;line-height:1.2;margin-bottom:16px;">{topic['title']}</h1>
        <div style="color:#9ca3af;font-size:14px;margin-bottom:32px;">
            Par <strong>Omar Sylla</strong> · WULIX Agency · {today}
        </div>
        <p style="font-size:18px;color:#d1d5db;margin-bottom:32px;font-style:italic;">{topic['intro']}</p>
        {sections_html}
        <div style="background:#1a1a2e;border-left:4px solid #7c3aed;padding:24px;border-radius:8px;margin-top:40px;">
            <p style="margin:0;font-weight:600;">Besoin d'aide pour automatiser ?</p>
            <p style="margin:8px 0 0;color:#9ca3af;">WULIX Agency configure tout pour vous. <a href="/" style="color:#7c3aed;">Contactez-nous →</a></p>
        </div>
    </article>
    """

def get_unused_topic() -> dict:
    """Retourne un topic non encore publié"""
    posted_file = BASE_DIR / "content" / "samba_posted.json"
    posted = json.loads(posted_file.read_text()) if posted_file.exists() else []

    for i, topic in enumerate(ARTICLE_TOPICS):
        if i not in posted:
            return i, topic

    log("Tous les articles de base publiés — génération nécessaire")
    return 0, ARTICLE_TOPICS[0]  # Cycle

def add_article_to_blog(topic: dict, topic_index: int):
    """Injecte le nouvel article dans blog.html"""
    blog_file = UI_DIR / "blog.html"
    if not blog_file.exists():
        log(f"ERREUR: blog.html introuvable dans {UI_DIR}")
        return False

    content = blog_file.read_text(encoding="utf-8")

    # Ajoute la carte dans la liste
    today = datetime.date.today().strftime("%d/%m/%Y")
    article_id = f"samba_{datetime.date.today().strftime('%Y%m%d')}"

    card_html = f"""
            <div class="card" onclick="showArticle('{article_id}')">
                <div class="card-tag">Automatisation</div>
                <h2>{topic['title']}</h2>
                <p>{topic['intro'][:120]}...</p>
                <div class="card-meta">{today} · 4 min de lecture</div>
            </div>"""

    # Insère avant la fermeture du grid
    content = content.replace(
        "<!-- SAMBA_INSERT_POINT -->",
        card_html + "\n            <!-- SAMBA_INSERT_POINT -->"
    )

    # Ajoute l'article complet
    article_html = generate_article_html(topic)
    content = content.replace(
        "<!-- SAMBA_ARTICLES_POINT -->",
        article_html + "\n    <!-- SAMBA_ARTICLES_POINT -->"
    )

    blog_file.write_text(content, encoding="utf-8")

    # Marque comme publié
    posted_file = BASE_DIR / "content" / "samba_posted.json"
    posted = json.loads(posted_file.read_text()) if posted_file.exists() else []
    posted.append(topic_index)
    with open(posted_file, "w") as f:
        json.dump(posted, f)

    log(f"Article ajouté au blog: {topic['title']}")
    return True

def check_sitemap(topic: dict):
    """Met à jour sitemap.xml avec le nouvel article"""
    sitemap_file = UI_DIR / "sitemap.xml"
    if not sitemap_file.exists():
        return

    content = sitemap_file.read_text(encoding="utf-8")
    today = datetime.date.today().isoformat()

    # Blog URL déjà dans le sitemap, on met juste à jour lastmod
    content = re.sub(
        r'(<loc>https://wulix\.fr/blog\.html</loc>\s*<lastmod>)[^<]*(</lastmod>)',
        f'\\g<1>{today}\\g<2>',
        content
    )
    sitemap_file.write_text(content, encoding="utf-8")
    log(f"Sitemap mis à jour — blog lastmod: {today}")

def run():
    log("Démarrage SAMBA — publication hebdomadaire")

    topic_index, topic = get_unused_topic()
    log(f"Article sélectionné: {topic['title']}")

    success = add_article_to_blog(topic, topic_index)
    if success:
        check_sitemap(topic)
        log("Publication réussie")

    log("SAMBA terminé")

if __name__ == "__main__":
    run()
