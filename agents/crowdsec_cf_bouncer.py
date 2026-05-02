"""
CrowdSec Cloudflare Bouncer pour wulix.fr
Recupere les decisions CrowdSec locales et les applique via Cloudflare Firewall API
Lance : python agents/crowdsec_cf_bouncer.py
Planifier toutes les 15 min via schtasks
"""
import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

CF_TOKEN   = os.getenv("CLOUDFLARE_API_TOKEN", "")
CF_ZONE    = os.getenv("CLOUDFLARE_ZONE_ID",   "ca18c06f4da6c660e5000d947665d350")
CS_API_KEY = os.getenv("CROWDSEC_API_KEY", "")
NAS_IP     = "192.168.1.4"
CS_PORT    = 8080

def get_crowdsec_bans():
    try:
        headers = {"X-Api-Key": CS_API_KEY} if CS_API_KEY else {}
        r = requests.get(f"http://{NAS_IP}:{CS_PORT}/v1/decisions?type=ban", headers=headers, timeout=5)
        if r.ok:
            return [d["value"] for d in (r.json() or []) if d.get("type") == "ban"]
    except Exception as e:
        print(f"[CS] NAS injoignable : {e}")
    return []

def get_cf_rules():
    if not CF_TOKEN:
        return []
    try:
        r = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE}/firewall/rules",
            headers={"Authorization": f"Bearer {CF_TOKEN}", "Content-Type": "application/json"},
            timeout=10
        )
        if r.ok:
            return r.json().get("result", [])
    except Exception as e:
        print(f"[CF] Erreur : {e}")
    return []

def block_ip_cf(ip):
    if not CF_TOKEN:
        print(f"[CF] Pas de token CF - simulation block {ip}")
        return False
    try:
        payload = [{
            "filter": {"expression": f'ip.src eq {ip}'},
            "action": "block",
            "description": f"CrowdSec ban - {ip}"
        }]
        r = requests.post(
            f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE}/firewall/rules",
            headers={"Authorization": f"Bearer {CF_TOKEN}", "Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        return r.ok
    except Exception as e:
        print(f"[CF] Erreur block {ip} : {e}")
        return False

def main():
    print("[CrowdSec CF Bouncer] Demarrage...")
    bans = get_crowdsec_bans()
    print(f"[CS] {len(bans)} IPs bannies trouvees")
    if not bans:
        print("[OK] Aucune IP a bloquer")
        return
    blocked = 0
    for ip in bans[:50]:  # max 50 IPs par run
        if block_ip_cf(ip):
            blocked += 1
            print(f"[CF] Bloque : {ip}")
    print(f"[OK] {blocked}/{len(bans)} IPs appliquees sur Cloudflare")

if __name__ == "__main__":
    main()
