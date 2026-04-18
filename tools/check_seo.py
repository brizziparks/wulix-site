"""WULIX - Verification SEO en ligne"""
import urllib.request
import urllib.error

URLS = [
    ("sitemap.xml",  "https://wulix.fr/sitemap.xml"),
    ("robots.txt",   "https://wulix.fr/robots.txt"),
    ("wulix.fr",     "https://wulix.fr/"),
]

print("=== Verification SEO wulix.fr ===\n")
all_ok = True
for nom, url in URLS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "WULIXBot/1.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        size = len(resp.read())
        print(f"[OK]  {nom:15} HTTP {resp.status}  ({size} octets)  {url}")
    except urllib.error.HTTPError as e:
        print(f"[ERR] {nom:15} HTTP {e.code}  {url}")
        all_ok = False
    except Exception as e:
        print(f"[ERR] {nom:15} {str(e)[:60]}")
        all_ok = False

print()
if all_ok:
    print("[OK] Tout est en ligne ! Prochaine etape : Google Search Console")
    print("     -> https://search.google.com/search-console")
    print("     -> Ajouter propriete : https://wulix.fr/")
    print("     -> Soumettre : sitemap.xml")
else:
    print("[!] Certaines URLs ne repondent pas. Verifie le deploiement Netlify.")
