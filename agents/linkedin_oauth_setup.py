"""
WULIX — LinkedIn OAuth Setup
Obtient un Access Token avec le scope w_organization_social
pour poster sur la PAGE WULIX (pas le profil perso d'Omar).

Usage :
  python agents/linkedin_oauth_setup.py        → affiche l'URL d'autorisation
  python agents/linkedin_oauth_setup.py --code CODE  → échange le code contre un token
"""

import sys
import os
import json
import webbrowser
import requests
from pathlib import Path
from urllib.parse import urlencode, parse_qs, urlparse

# ─── Config ──────────────────────────────────────────────────────────────────
# Récupère les clés depuis .env
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

CLIENT_ID     = os.getenv("LINKEDIN_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
REDIRECT_URI  = "https://wulix.fr/linkedin/callback"   # doit être enregistrée dans l'app LinkedIn

# Scopes nécessaires pour poster sur la page entreprise
SCOPES = [
    "openid",
    "profile",
    "email",
    "w_member_social",       # posts perso
    "w_organization_social", # posts page entreprise ← ESSENTIEL
    "r_organization_social", # lecture stats page
]

TOKEN_FILE = Path(__file__).parent / "content" / ".linkedin_token"
TOKEN_META = Path(__file__).parent / "content" / ".linkedin_token_meta.json"

ORGANIZATION_URN = "urn:li:organization:112948321"  # Page WULIX

AUTH_URL  = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"


# ─── Étape 1 : Générer l'URL d'autorisation ──────────────────────────────────
def get_auth_url():
    if not CLIENT_ID:
        print("[ERREUR] LINKEDIN_CLIENT_ID manquant dans .env")
        print("  → Va sur https://www.linkedin.com/developers/apps et crée une app")
        print("  → Ajoute LINKEDIN_CLIENT_ID et LINKEDIN_CLIENT_SECRET dans .env")
        return None

    params = {
        "response_type": "code",
        "client_id"    : CLIENT_ID,
        "redirect_uri" : REDIRECT_URI,
        "scope"        : " ".join(SCOPES),
        "state"        : "wulix_mariama_2026",
    }
    url = AUTH_URL + "?" + urlencode(params)
    return url


# ─── Étape 2 : Échanger le code contre un token ──────────────────────────────
def exchange_code(code: str):
    if not CLIENT_ID or not CLIENT_SECRET:
        print("[ERREUR] LINKEDIN_CLIENT_ID / LINKEDIN_CLIENT_SECRET manquants dans .env")
        return None

    r = requests.post(TOKEN_URL, data={
        "grant_type"   : "authorization_code",
        "code"         : code,
        "redirect_uri" : REDIRECT_URI,
        "client_id"    : CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }, timeout=15)

    if not r.ok:
        print(f"[ERREUR] {r.status_code}: {r.text}")
        return None

    data = r.json()
    token = data.get("access_token", "")
    expires_in = data.get("expires_in", 0)

    if not token:
        print(f"[ERREUR] Pas de token dans la réponse : {data}")
        return None

    # Sauvegarde du token
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(token, encoding="utf-8")

    # Métadonnées (expiration, scopes)
    meta = {
        "expires_in"  : expires_in,
        "scope"       : data.get("scope", " ".join(SCOPES)),
        "token_type"  : data.get("token_type", "Bearer"),
        "saved_at"    : __import__("datetime").datetime.now().isoformat(),
    }
    TOKEN_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"[OK] Token sauvegarde dans {TOKEN_FILE}")
    print(f"[OK] Expiration : {expires_in // 3600} heures (~{expires_in // 86400} jours)")
    print(f"[OK] Scopes : {data.get('scope', '?')}")

    # Vérification : peut-on poster sur la page WULIX ?
    verify_org_access(token)

    return token


# ─── Vérification de l'accès à la page org ───────────────────────────────────
def verify_org_access(token: str):
    """Vérifie que le token permet de poster sur la page WULIX."""
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    org_id = ORGANIZATION_URN.split(":")[-1]
    url = f"https://api.linkedin.com/v2/organizations/{org_id}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.ok:
            data = r.json()
            name = data.get("localizedName", "?")
            print(f"[OK] Acces confirme a la page : {name} ({ORGANIZATION_URN})")
        elif r.status_code == 403:
            print("[ERREUR 403] Le token n'a pas acces a la page WULIX.")
            print("  → Verifie que ton compte est ADMIN de la page LinkedIn WULIX")
            print("  → Et que le scope w_organization_social est bien autorise")
        else:
            print(f"[WARN] Verification page : {r.status_code} — {r.text[:100]}")
    except Exception as e:
        print(f"[WARN] Impossible de verifier l'acces : {e}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if "--code" in sys.argv:
        idx = sys.argv.index("--code")
        if idx + 1 >= len(sys.argv):
            print("[ERREUR] Fournis le code : python linkedin_oauth_setup.py --code <CODE>")
            sys.exit(1)
        code = sys.argv[idx + 1]
        exchange_code(code)

    elif "--verify" in sys.argv:
        if TOKEN_FILE.exists():
            token = TOKEN_FILE.read_text(encoding="utf-8").strip()
            verify_org_access(token)
        else:
            print("[ERREUR] Aucun token sauvegarde. Lance d'abord sans argument.")

    else:
        # Étape 1 : Affiche l'URL
        url = get_auth_url()
        if url:
            print("\n" + "="*65)
            print("LINKEDIN OAUTH — Configuration page WULIX")
            print("="*65)
            print("\n1. Ouvre cette URL dans ton navigateur :")
            print(f"\n   {url}\n")
            print("2. Connecte-toi avec le compte Omar Sylla (admin de la page WULIX)")
            print("3. Autorise l'application")
            print("4. Tu seras redirigé vers wulix.fr/linkedin/callback?code=XXXX")
            print("5. Copie le parametre 'code' et lance :")
            print("   python agents/linkedin_oauth_setup.py --code <CODE>\n")
            print("="*65)

            if "--open" in sys.argv:
                webbrowser.open(url)
