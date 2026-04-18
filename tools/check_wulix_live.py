"""WULIX - Verification live wulix.fr"""
import requests

URLS = [
    ("https://wulix.fr/",                   "index",           [200]),
    ("https://wulix.fr/og-image.jpg",        "og-image.jpg",    [200]),
    ("https://wulix.fr/cgv.html",            "cgv.html",        [200]),
    ("https://wulix.fr/mentions-legales.html","mentions.html",  [200]),
    ("https://wulix.fr/404.html",            "404.html",        [200]),
    ("https://wulix.fr/sitemap.xml",         "sitemap.xml",     [200]),
    ("https://wulix.fr/robots.txt",          "robots.txt",      [200]),
]

H = {"User-Agent": "WULIXBot/1.0"}
print("=== Verification live wulix.fr ===\n")
ok_total = 0
for url, label, codes in URLS:
    try:
        r = requests.get(url, headers=H, timeout=10)
        ok = r.status_code in codes
        og = "  og:image=OK" if label == "index" and "og:image" in r.text else ""
        print(f"[{'OK' if ok else 'KO'}] {label:25} HTTP {r.status_code}  {len(r.content):>8} octets{og}")
        if ok: ok_total += 1
    except Exception as e:
        print(f"[KO] {label:25} ERREUR: {e}")

print(f"\n{ok_total}/{len(URLS)} tests OK")
