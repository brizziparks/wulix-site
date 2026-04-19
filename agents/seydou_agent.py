"""
SEYDOU — Agent Marketing Automation
Gère la publication Twitter/X + calendrier éditorial automatique
"""
import os
import json
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] SEYDOU | {msg}"
    print(line)
    with open(LOG_DIR / "seydou.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

def get_next_tweet():
    """Lit le prochain tweet à poster depuis tweets_8semaines.md"""
    tweets_file = CONTENT_DIR / "tweets_8semaines.md"
    if not tweets_file.exists():
        log("ERREUR: tweets_8semaines.md introuvable")
        return None

    content = tweets_file.read_text(encoding="utf-8")
    blocks = [b.strip() for b in content.split("---") if b.strip()]

    # Cherche le prochain tweet non posté
    posted_file = CONTENT_DIR / "tweets_posted.json"
    posted = json.loads(posted_file.read_text()) if posted_file.exists() else []

    for i, block in enumerate(blocks):
        if i not in posted and "##" in block:
            # Extrait le contenu du tweet (entre les balises >)
            lines = block.split("\n")
            tweet_lines = []
            in_quote = False
            for line in lines:
                if line.startswith(">"):
                    tweet_lines.append(line[1:].strip())
                    in_quote = True
                elif in_quote and line.strip() == "":
                    break
            tweet_text = "\n".join(tweet_lines)
            return {"index": i, "text": tweet_text, "block": block}

    log("Tous les tweets ont été postés — cycle terminé")
    return None

def post_to_twitter(tweet_text: str) -> bool:
    """
    Publication Twitter via API v2
    Nécessite: TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_API_SECRET,
               TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET dans .env
    """
    try:
        import tweepy
        from dotenv import load_dotenv
        load_dotenv(BASE_DIR.parent / ".env")

        client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        response = client.create_tweet(text=tweet_text)
        log(f"Tweet publié — ID: {response.data['id']}")
        return True
    except ImportError:
        log("tweepy non installé — pip install tweepy")
        return False
    except Exception as e:
        log(f"Erreur Twitter API: {e}")
        return False

def generate_weekly_content():
    """Génère du nouveau contenu si la file est vide"""
    themes = [
        "automatisation Python pour débutants",
        "n8n vs Make.com : comparaison honnête",
        "5 minutes par jour pour économiser 5h par semaine",
        "cas client : 0 email manuel depuis 1 mois",
        "IA locale vs cloud : ce que j'utilise vraiment"
    ]

    posts = []
    for theme in themes:
        posts.append({
            "theme": theme,
            "status": "draft",
            "created": datetime.datetime.now().isoformat()
        })

    queue_file = CONTENT_DIR / "seydou_queue.json"
    with open(queue_file, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    log(f"{len(posts)} posts en file d'attente générés")
    return posts

def run(action="post"):
    log(f"Démarrage SEYDOU — action: {action}")

    if action == "post":
        tweet = get_next_tweet()
        if tweet:
            log(f"Prochain tweet (index {tweet['index']}):\n{tweet['text'][:100]}...")
            # En mode dry-run par défaut — mettre DRY_RUN=false pour publier
            dry_run = os.getenv("SEYDOU_DRY_RUN", "true").lower() == "true"
            if dry_run:
                log("[DRY RUN] Tweet non publié. Mettre SEYDOU_DRY_RUN=false pour activer.")
                print("\n--- TWEET PRÉVU ---")
                print(tweet["text"])
                print("-------------------\n")
            else:
                success = post_to_twitter(tweet["text"])
                if success:
                    posted_file = CONTENT_DIR / "tweets_posted.json"
                    posted = json.loads(posted_file.read_text()) if posted_file.exists() else []
                    posted.append(tweet["index"])
                    with open(posted_file, "w") as f:
                        json.dump(posted, f)
        else:
            log("Aucun tweet disponible — génération de nouveau contenu")
            generate_weekly_content()

    elif action == "generate":
        generate_weekly_content()

    log("SEYDOU terminé")

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "post"
    run(action)
