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
# Redirect URI : serveur local pour récupérer le code automatiquement
# (à enregistrer dans l'app LinkedIn : http://localhost:8765/callback)
REDIRECT_URI  = "http://localhost:8765/callback"

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
def auto_capture_code():
    """Démarre un mini serveur HTTP local sur :8765 pour capturer le code OAuth.
    L'utilisateur clique le lien → LinkedIn redirige sur localhost:8765/callback?code=...
    → on récupère le code, on l'échange contre un token, et on ferme le serveur.
    """
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import threading

    captured = {"code": None, "error": None, "state": None}

    class CallbackHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # silencieux

        def do_GET(self):
            parsed = urlparse(self.path)
            if not parsed.path.startswith("/callback"):
                self.send_response(404)
                self.end_headers()
                return
            params = parse_qs(parsed.query)
            captured["code"]  = params.get("code",  [None])[0]
            captured["error"] = params.get("error", [None])[0]
            captured["state"] = params.get("state", [None])[0]

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            if captured["code"]:
                html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>WULIX LinkedIn OAuth</title>
<style>body{font-family:system-ui,sans-serif;background:#0a0015;color:#e2e8f0;text-align:center;padding:80px 20px}
.box{max-width:520px;margin:0 auto;background:#0f0025;border:1px solid #00d4ff;border-radius:12px;padding:40px}
h1{color:#00dc82;margin:0 0 16px}p{color:#7c88a8;line-height:1.6}
.code{font-family:monospace;background:#1a0030;padding:8px 12px;border-radius:6px;font-size:11px;word-break:break-all}</style>
</head><body><div class="box"><h1>OK Code recu</h1>
<p>Tu peux fermer cet onglet. Le terminal continue automatiquement.</p>
<div class="code">""" + captured["code"][:30] + "..." + """</div></div></body></html>"""
            else:
                html = """<!DOCTYPE html><html><head><meta charset="utf-8"></head>
<body style="font-family:system-ui;background:#0a0015;color:#ef4444;text-align:center;padding:80px">
<h1>Erreur OAuth</h1><p>""" + (captured["error"] or "Code manquant") + """</p></body></html>"""

            self.wfile.write(html.encode("utf-8"))

    server = HTTPServer(("localhost", 8765), CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    # Ouvre l'URL d'autorisation
    url = get_auth_url()
    if not url:
        server.shutdown()
        return None

    print("\n" + "="*65)
    print("LINKEDIN OAUTH — Page WULIX")
    print("="*65)
    print("\n[1] Ouverture du navigateur sur LinkedIn...")
    print("[2] Connecte-toi avec le compte admin de la page WULIX")
    print("[3] Autorise l'application")
    print("[4] Le code sera capture automatiquement par le serveur local\n")

    webbrowser.open(url)

    # Attend jusqu'à 5 minutes le code
    print("[INFO] Serveur local sur http://localhost:8765 — en attente du code...")
    import time
    timeout = 300
    start = time.time()
    while captured["code"] is None and captured["error"] is None:
        time.sleep(0.5)
        if time.time() - start > timeout:
            print("[ERREUR] Timeout (5 min) — relance le script")
            server.shutdown()
            return None

    server.shutdown()

    if captured["error"]:
        print(f"[ERREUR] OAuth: {captured['error']}")
        return None

    print(f"\n[OK] Code recu, echange contre un token...")
    return exchange_code(captured["code"])


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

    elif "--manual" in sys.argv:
        # Mode manuel : juste affiche l'URL (pour quand le serveur local ne peut pas tourner)
        url = get_auth_url()
        if url:
            print("\nOuvre cette URL :\n")
            print(f"  {url}\n")
            print("Apres autorisation, copie le 'code' dans l'URL de retour et lance :")
            print("  python agents/linkedin_oauth_setup.py --code <CODE>\n")

    else:
        # Mode AUTO (défaut) : serveur local + capture auto
        auto_capture_code()
