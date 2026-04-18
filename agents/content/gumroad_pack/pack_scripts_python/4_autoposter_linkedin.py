# -*- coding: utf-8 -*-
"""
WULIX — Script 4 : Auto-poster LinkedIn
========================================
Publie automatiquement un post sur LinkedIn via l'API officielle.
Lit les posts a publier depuis un fichier posts.txt (un post par ligne).

Usage :
    pip install requests
    python 4_autoposter_linkedin.py

Prerequis :
    1. Creer une application LinkedIn Developer : https://www.linkedin.com/developers/
    2. Activer les permissions : w_member_social, r_liteprofile
    3. Obtenir un Access Token OAuth 2.0
    4. Renseigner ACCESS_TOKEN et URN_AUTEUR ci-dessous

Note : Le script publie le premier post non encore envoye dans posts.txt
"""

import requests
import json
import datetime
import os

# === CONFIG — renseigne tes valeurs ===
ACCESS_TOKEN = "VOTRE_ACCESS_TOKEN_LINKEDIN"
URN_AUTEUR   = "urn:li:person:VOTRE_ID_LINKEDIN"   # Ex: urn:li:person:abc123XYZ
FICHIER_POSTS = "posts.txt"
LOG_FILE      = "linkedin_log.txt"
# ======================================

API_URL = "https://api.linkedin.com/v2/ugcPosts"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type":  "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

def charger_prochain_post():
    """Lit posts.txt et retourne le premier post non envoye (non prefixe par [DONE])."""
    if not os.path.exists(FICHIER_POSTS):
        exemple = """[A PUBLIER] Hello LinkedIn ! Voici mon post automatise par WULIX.
[A PUBLIER] Automatisation IA : comment j'ai gagne 3h par semaine avec Python.
[A PUBLIER] Nouveau produit disponible sur wulix.fr — lien en commentaire !
"""
        with open(FICHIER_POSTS, "w", encoding="utf-8") as f:
            f.write(exemple)
        print(f"[INFO] Fichier {FICHIER_POSTS} cree avec des exemples.")
        return None, -1

    with open(FICHIER_POSTS, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    for i, ligne in enumerate(lignes):
        if ligne.strip().startswith("[A PUBLIER]"):
            texte = ligne.strip().replace("[A PUBLIER]", "").strip()
            return texte, i
    return None, -1

def marquer_comme_envoye(index):
    with open(FICHIER_POSTS, "r", encoding="utf-8") as f:
        lignes = f.readlines()
    lignes[index] = lignes[index].replace("[A PUBLIER]", "[DONE]")
    with open(FICHIER_POSTS, "w", encoding="utf-8") as f:
        f.writelines(lignes)

def publier_post(texte):
    payload = {
        "author": URN_AUTEUR,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": texte},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)

    if resp.status_code == 201:
        return True, resp.headers.get("X-RestLi-Id", "ID inconnu")
    else:
        return False, f"HTTP {resp.status_code} : {resp.text[:200]}"

def logger(message):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {message}\n")
    print(f"[{ts}] {message}")

def main():
    if ACCESS_TOKEN == "VOTRE_ACCESS_TOKEN_LINKEDIN":
        print("[ERREUR] Configure ACCESS_TOKEN et URN_AUTEUR avant d'utiliser ce script.")
        print("[INFO] Guide : https://www.linkedin.com/developers/apps")
        return

    texte, index = charger_prochain_post()
    if not texte:
        logger("[INFO] Aucun post a publier dans posts.txt")
        return

    logger(f"[INFO] Post a publier : {texte[:80]}...")
    succes, detail = publier_post(texte)

    if succes:
        marquer_comme_envoye(index)
        logger(f"[OK] Post publie avec succes — ID: {detail}")
    else:
        logger(f"[ERREUR] Echec publication : {detail}")

if __name__ == "__main__":
    main()
