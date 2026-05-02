# =============================================================================
# WULIX — MARIAMA Publisher
# Script  : mariama_publisher.py
# Version : 1.0.0
# Auteur  : WULIX (wulix.fr)
# Description : Publie automatiquement les posts LinkedIn de MARIAMA
# =============================================================================

import requests
import json
import time
import os
from datetime import datetime
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

# Fichier de token (plus sécurisé que de mettre le token en dur)
TOKEN_FILE   = Path(__file__).parent / "content" / ".linkedin_token"
POSTS_FILE   = Path(__file__).parent / "content" / "posts.txt"
LOG_FILE     = Path(__file__).parent / "content" / "mariama_log.txt"

DELAI_ENTRE_POSTS = 300   # 5 minutes entre chaque post
MODE_TEST         = False  # False = publication réelle
VISIBILITE        = "PUBLIC"

# ✅ Toujours poster sur la PAGE WULIX (jamais le profil perso Omar)
USE_ORG_PAGE      = True   # True = page entreprise | False = profil perso

API_PROFILE_URL  = "https://api.linkedin.com/v2/userinfo"
API_POST_URL     = "https://api.linkedin.com/v2/ugcPosts"
ORGANIZATION_URN = "urn:li:organization:112948321"  # Page WULIX

# =============================================================================
# FONCTIONS
# =============================================================================

def lire_token():
    """Lit le token depuis le fichier sécurisé."""
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text(encoding='utf-8').strip()
    print("[ERREUR] Fichier token introuvable. Lance : python mariama_publisher.py --setup")
    return None


def get_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type" : "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }


def obtenir_urn(token):
    """Retourne l'URN à utiliser pour poster.
    USE_ORG_PAGE=True  → page WULIX (urn:li:organization:...)
    USE_ORG_PAGE=False → profil perso (urn:li:person:...)
    IMPORTANT : le token doit avoir le scope w_organization_social
    pour poster sur la page entreprise. Lance --setup-token si 403.
    """
    if USE_ORG_PAGE:
        # Vérification que le token est valide (userinfo léger)
        try:
            r = requests.get(API_PROFILE_URL, headers=get_headers(token), timeout=10)
            r.raise_for_status()
            data = r.json()
            name = data.get("name", "?")
            print(f"[INFO] Token valide — connecte en tant que : {name}")
            print(f"[INFO] Publication ciblee : PAGE WULIX ({ORGANIZATION_URN})")
        except Exception as e:
            print(f"[WARN] Verification token : {e}")
        return ORGANIZATION_URN

    # Profil perso (ancien comportement — deconseille)
    try:
        r = requests.get(API_PROFILE_URL, headers=get_headers(token), timeout=10)
        r.raise_for_status()
        data = r.json()
        person_id = data.get("sub") or data.get("id")
        if person_id:
            person_urn = f"urn:li:person:{person_id}"
            print(f"[WARN] Profil PERSO utilise : {data.get('name', '?')} ({person_urn})")
            return person_urn
        return ORGANIZATION_URN
    except Exception as e:
        print(f"[ERREUR] Connexion LinkedIn : {e}")
        return None


def publier_post(token, urn, texte):
    """Publie un post sur LinkedIn."""
    payload = {
        "author": urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary"   : {"text": texte},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": VISIBILITE
        }
    }
    try:
        r = requests.post(API_POST_URL, headers=get_headers(token),
                          data=json.dumps(payload), timeout=15)
        r.raise_for_status()
        post_id = r.headers.get('x-restli-id', 'N/A')
        return True, post_id
    except requests.exceptions.HTTPError as e:
        return False, f"{e.response.status_code}: {e.response.text}"
    except Exception as e:
        return False, str(e)


def lire_posts():
    """Lit et parse le fichier posts.txt."""
    if not POSTS_FILE.exists():
        print(f"[ERREUR] Fichier introuvable : {POSTS_FILE}")
        return []
    contenu = POSTS_FILE.read_text(encoding='utf-8')
    posts = [p.strip() for p in contenu.split('---') if p.strip()]
    print(f"[INFO] {len(posts)} post(s) chargé(s)")
    return posts


def logger(message):
    """Écrit dans le fichier log."""
    ligne = f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {message}\n"
    with open(LOG_FILE, 'a', encoding='utf-8', errors='replace') as f:
        f.write(ligne)
    print(ligne.strip().encode('cp1252', errors='replace').decode('cp1252'))


def publier_prochain_post():
    """Publie le prochain post non publié."""
    token = lire_token()
    if not token:
        return

    posts = lire_posts()
    if not posts:
        logger("[FIN] Aucun post à publier.")
        return

    # Lit l'index du dernier post publié
    index_file = Path(__file__).parent / "content" / ".post_index"
    index = int(index_file.read_text().strip()) if index_file.exists() else 0

    if index >= len(posts):
        logger("[FIN] Tous les posts ont été publiés. Réinitialise .post_index pour recommencer.")
        return

    post = posts[index]
    apercu = post[:60].replace('\n', ' ')
    logger(f"Publication post {index+1}/{len(posts)} : {apercu}...")

    if MODE_TEST:
        logger(f"[TEST] Simulation — post non envoyé")
        index_file.write_text(str(index + 1))
        return

    urn = obtenir_urn(token)
    if not urn:
        return

    succes, resultat = publier_post(token, urn, post)
    if succes:
        logger(f"[OK] Post publié — ID: {resultat}")
        index_file.write_text(str(index + 1))
    else:
        logger(f"[ERREUR] Publication échouée : {resultat}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys

    if "--setup" in sys.argv:
        # Mode setup : sauvegarde le token
        token = input("Colle ton Access Token LinkedIn : ").strip()
        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_FILE.write_text(token, encoding='utf-8')
        print(f"[OK] Token sauvegardé dans {TOKEN_FILE}")

    elif "--reset" in sys.argv:
        # Remet l'index à 0 pour recommencer le cycle
        index_file = Path(__file__).parent / "content" / ".post_index"
        index_file.write_text("0")
        print("[OK] Index réinitialisé — les posts recommenceront depuis le début")

    elif "--test" in sys.argv:
        # Test de connexion LinkedIn
        token = lire_token()
        if token:
            urn = obtenir_urn(token)
            if urn:
                print(f"[OK] Connexion LinkedIn réussie !")

    else:
        # Mode normal : publie le prochain post
        publier_prochain_post()
