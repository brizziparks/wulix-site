"""
FAKTOUR — Agent Facturation WULIX
Génère des factures PDF pour les ventes Gumroad
"""
import os
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

FACTURES_DIR = Path(__file__).parent / "content" / "factures"
FACTURES_DIR.mkdir(parents=True, exist_ok=True)

SELLER = {
    "nom": "Omar Sylla",
    "activite": "WULIX — Automatisation IA",
    "email": "contact@wulix.fr",
    "site": "wulix.fr",
    "ville": "Paris, France",
}

PRODUCTS = {
    "scripts-python": {"nom": "Pack Scripts Python", "prix": 29.0},
    "n8n-linkedin": {"nom": "Pipeline LinkedIn Automatisé", "prix": 19.0},
    "guide-automatisation": {"nom": "Guide Automatise 5 Tâches WULIX", "prix": 9.0},
    "prompts-ia": {"nom": "Pack 50 Prompts IA", "prix": 5.0},
}


def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] FAKTOUR | {msg}"
    print(line)
    with open(LOG_DIR / "faktour.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def generer_numero_facture():
    today = datetime.date.today()
    prefix = f"WUL-{today.strftime('%Y%m')}"
    existing = list(FACTURES_DIR.glob(f"{prefix}-*.json"))
    num = len(existing) + 1
    return f"{prefix}-{num:03d}"


def generer_facture_html(vente: dict) -> str:
    """Génère le HTML d'une facture."""
    numero = vente.get("numero", "WUL-000")
    date_str = vente.get("date", datetime.date.today().isoformat())
    acheteur = vente.get("acheteur", {})
    produit_key = vente.get("produit_key", "")
    produit = PRODUCTS.get(produit_key, {"nom": vente.get("produit_nom", "Produit WULIX"), "prix": vente.get("prix", 0)})
    prix_ht = produit["prix"]
    tva = 0  # micro-entreprise — TVA non applicable
    total = prix_ht

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; color: #1a1a2e; }}
  .header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px; }}
  .logo {{ font-size: 28px; font-weight: bold; color: #7c3aed; }}
  .facture-num {{ font-size: 13px; color: #666; text-align: right; }}
  h1 {{ color: #7c3aed; border-bottom: 2px solid #7c3aed; padding-bottom: 8px; }}
  .parties {{ display: flex; justify-content: space-between; margin: 20px 0; }}
  .partie {{ background: #f8f6ff; padding: 15px; border-radius: 8px; width: 45%; }}
  .partie h3 {{ color: #7c3aed; margin: 0 0 8px 0; font-size: 14px; }}
  table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
  th {{ background: #7c3aed; color: white; padding: 10px; text-align: left; }}
  td {{ padding: 10px; border-bottom: 1px solid #eee; }}
  .total-row {{ background: #f0f2f8; font-weight: bold; }}
  .footer {{ margin-top: 40px; font-size: 11px; color: #888; border-top: 1px solid #eee; padding-top: 15px; }}
  .tva-note {{ color: #666; font-size: 12px; }}
</style>
</head>
<body>
<div class="header">
  <div>
    <div class="logo">WULIX</div>
    <div style="font-size:13px;color:#666;margin-top:4px">{SELLER['activite']}</div>
  </div>
  <div class="facture-num">
    <strong>FACTURE N° {numero}</strong><br>
    Date : {date_str}<br>
    {SELLER['email']}<br>
    {SELLER['site']}
  </div>
</div>

<h1>Facture</h1>

<div class="parties">
  <div class="partie">
    <h3>VENDEUR</h3>
    <strong>{SELLER['nom']}</strong><br>
    {SELLER['activite']}<br>
    {SELLER['ville']}<br>
    {SELLER['email']}
  </div>
  <div class="partie">
    <h3>ACHETEUR</h3>
    <strong>{acheteur.get('nom', 'Client')}</strong><br>
    {acheteur.get('email', '')}<br>
    {acheteur.get('pays', '')}
  </div>
</div>

<table>
  <tr>
    <th>Description</th>
    <th>Qté</th>
    <th>Prix unitaire HT</th>
    <th>Total HT</th>
  </tr>
  <tr>
    <td>{produit['nom']}<br><small>Produit numérique — téléchargement immédiat</small></td>
    <td>1</td>
    <td>{prix_ht:.2f} €</td>
    <td>{prix_ht:.2f} €</td>
  </tr>
  <tr class="total-row">
    <td colspan="3">Total HT</td>
    <td>{prix_ht:.2f} €</td>
  </tr>
  <tr>
    <td colspan="3" class="tva-note">TVA</td>
    <td class="tva-note">Non applicable<br>(Art. 293 B CGI)</td>
  </tr>
  <tr class="total-row">
    <td colspan="3"><strong>TOTAL TTC</strong></td>
    <td><strong>{total:.2f} €</strong></td>
  </tr>
</table>

<p>Paiement effectué via Gumroad le {date_str}.</p>

<div class="footer">
  <strong>Mentions légales :</strong> TVA non applicable, article 293 B du CGI — Micro-entrepreneur.<br>
  Conformément à l'art. L.221-28 du Code de la consommation, aucun remboursement possible après téléchargement de produit numérique.<br>
  Pour toute question : {SELLER['email']}
</div>
</body>
</html>"""
    return html


def creer_facture(vente: dict) -> dict:
    """Crée une facture pour une vente et la sauvegarde."""
    numero = generer_numero_facture()
    vente["numero"] = numero
    if "date" not in vente:
        vente["date"] = datetime.date.today().isoformat()

    # Générer HTML
    html = generer_facture_html(vente)

    # Sauvegarder HTML
    html_path = FACTURES_DIR / f"{numero}.html"
    html_path.write_text(html, encoding="utf-8")

    # Sauvegarder JSON
    json_path = FACTURES_DIR / f"{numero}.json"
    json_path.write_text(json.dumps(vente, ensure_ascii=False, indent=2), encoding="utf-8")

    log(f"Facture créée : {numero} — {vente.get('produit_nom', '')} — {vente.get('prix', 0)}€")
    return {"numero": numero, "html_path": str(html_path), "json_path": str(json_path)}


def traiter_ventes_gumroad(ventes: list) -> list:
    """Traite une liste de ventes Gumroad et génère les factures."""
    factures = []
    for v in ventes:
        result = creer_facture(v)
        factures.append(result)
    return factures


def demo():
    """Démo : crée une facture exemple."""
    vente_exemple = {
        "produit_key": "prompts-ia",
        "produit_nom": "Pack 50 Prompts IA",
        "prix": 5.0,
        "acheteur": {
            "nom": "Jean Dupont",
            "email": "jean.dupont@example.com",
            "pays": "France"
        }
    }
    result = creer_facture(vente_exemple)
    log(f"Démo OK — {result['html_path']}")
    return result


if __name__ == "__main__":
    log("=== FAKTOUR démarré ===")
    demo()
    log("=== FAKTOUR terminé ===")
