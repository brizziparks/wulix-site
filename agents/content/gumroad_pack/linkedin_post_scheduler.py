# =============================================================================
# WULIX — Pack Automatisation PME
# Script  : linkedin_post_scheduler.py
# Version : 1.0.0
# Auteur  : WULIX (wulix.fr)
# Licence : Usage commercial autorisé — redistribution interdite
# =============================================================================
# DESCRIPTION :
#   Lit un fichier posts.txt (posts séparés par ---) et les publie
#   automatiquement sur LinkedIn via l'API officielle (OAuth2).
#   Délai configurable entre chaque publication.
#
# UTILISATION :
#   1. Crée une app LinkedIn sur https://developer.linkedin.com
#   2. Obtiens ton Access Token OAuth2 (scope : w_member_social)
#   3. Remplis ACCESS_TOKEN ci-dessous
#   4. Crée un fichier posts.txt avec tes posts séparés par ---
#   5. Lance : python linkedin_post_scheduler.py
#
# FORMAT posts.txt :
#   Premier post ici.
#   Peut être sur plusieurs lignes.
#   ---
#   Deuxième post ici.
#   ---
#
# DÉPENDANCES :
#   pip install requests
# =============================================================================

import requests
import json
import time
from datetime import datetime
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

ACCESS_TOKEN         = "ton_access_token_linkedin"
DELAI_ENTRE_POSTS    = 300    # Secondes entre chaque post (min recommandé : 300)
FICHIER_POSTS        = "posts.txt"
MODE_TEST            = True   # True = affiche sans publier
VISIBILITE           = "PUBLIC"  # "PUBLIC" ou "CONNECTIONS"

API_BASE_URL    = "https://api.linkedin.com/v2"
API_PROFILE_URL = f"{API_BASE_URL}/userinfo"
API_POST_URL    = f"{API_BASE_URL}/ugcPosts"


def get_headers():
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type" : "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }


def obtenir_profil_linkedin():
    try:
        response = requests.get(API_PROFILE_URL, headers=get_headers(), timeout=10)
        response.raise_for_status()
        data = response.json()
        user_id = data.get('sub')
        if not user_id:
            print("[ERREUR] Impossible de récupérer l'ID utilisateur LinkedIn")
            return None
        urn = f"urn:li:person:{user_id}"
        print(f"[INFO] Profil connecté : {data.get('name', 'Inconnu')} ({urn})")
        return urn
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("[ERREUR] Token LinkedIn invalide ou expiré.")
        else:
            print(f"[ERREUR] API LinkedIn : {e}")
        return None
    except Exception as e:
        print(f"[ERREUR] Connexion LinkedIn : {e}")
        return None


def publier_post(urn_auteur, texte_post):
    payload = {
        "author"         : urn_auteur,
        "lifecycleState" : "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary"   : {"text": texte_post},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": VISIBILITE
        }
    }
    try:
        response = requests.post(
            API_POST_URL,
            headers=get_headers(),
            data=json.dumps(payload),
            timeout=15
        )
        response.raise_for_status()
        post_id = response.headers.get('x-restli-id', 'N/A')
        print(f"[PUBLIÉ] Post ID : {post_id}")
        return True
    except requests.exceptions.HTTPError as e:
        print(f"[ERREUR] Publication : {e.response.status_code} — {e.response.text}")
        return False
    except Exception as e:
        print(f"[ERREUR] Publication : {e}")
        return False


def lire_posts(chemin_fichier):
    if not Path(chemin_fichier).exists():
        print(f"[ERREUR] Fichier introuvable : {chemin_fichier}")
        return []
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
        posts = [p.strip() for p in contenu.split('---') if p.strip()]
        print(f"[INFO] {len(posts)} post(s) chargé(s)")
        return posts
    except Exception as e:
        print(f"[ERREUR] Lecture : {e}")
        return []


def main():
    print("=" * 55)
    print("  WULIX — LinkedIn Post Scheduler")
    print(f"  {datetime.today().strftime('%d/%m/%Y %H:%M')} | Test : {MODE_TEST}")
    print("=" * 55)

    posts = lire_posts(FICHIER_POSTS)
    if not posts:
        print("[FIN] Aucun post à publier.")
        return

    urn_auteur = None
    if not MODE_TEST:
        urn_auteur = obtenir_profil_linkedin()
        if not urn_auteur:
            print("[FIN] Impossible de se connecter.")
            return

    publies = erreurs = 0

    for i, post in enumerate(posts, 1):
        apercu = post[:80].replace('\n', ' ')
        print(f"\n[{i}/{len(posts)}] {apercu}{'...' if len(post) > 80 else ''}")

        if MODE_TEST:
            print("  [TEST] Publication simulée")
            publies += 1
        else:
            if publier_post(urn_auteur, post):
                publies += 1
            else:
                erreurs += 1
            if i < len(posts):
                print(f"  Pause {DELAI_ENTRE_POSTS}s...")
                time.sleep(DELAI_ENTRE_POSTS)

    print(f"\n  Résumé : {publies} publié(s) | {erreurs} erreur(s)")


if __name__ == "__main__":
    main()
