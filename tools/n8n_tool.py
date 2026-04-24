"""
N8n integration — déclenche des workflows via webhook ou API REST.
Omar a N8n sur n8n.rosmedia.fr (NAS 192.168.1.4:5678)

Config .env :
  N8N_URL=http://n8n.rosmedia.fr   (ou http://192.168.1.4:5678)
  N8N_API_KEY=ton_api_key          (Settings → API → Create API Key dans N8n)
"""

import os
import requests

N8N_URL     = os.getenv("N8N_URL", "http://192.168.1.4:5678").rstrip("/")
N8N_API_KEY = os.getenv("N8N_API_KEY", "")

def _headers() -> dict:
    h = {"Content-Type": "application/json"}
    if N8N_API_KEY:
        h["X-N8N-API-KEY"] = N8N_API_KEY
    return h


def trigger_webhook(webhook_path: str, data: dict = None) -> str:
    """
    Déclenche un webhook N8n.

    Args:
        webhook_path: Chemin du webhook (ex: "post-linkedin", "daily-report")
                      L'URL complète sera N8N_URL/webhook/webhook_path
        data:         Données JSON optionnelles à envoyer

    Returns:
        Réponse N8n ou message d'erreur.
    """
    url = f"{N8N_URL}/webhook/{webhook_path.lstrip('/')}"
    try:
        r = requests.post(url, json=data or {}, timeout=15)
        if r.status_code in (200, 201):
            try:
                resp = r.json()
                if isinstance(resp, dict):
                    msg = resp.get("message") or resp.get("status") or str(resp)[:120]
                else:
                    msg = str(resp)[:120]
                return f"Workflow déclenché ({webhook_path}) : {msg}"
            except Exception:
                return f"Workflow déclenché ({webhook_path}) — réponse : {r.text[:120]}"
        return f"Erreur N8n {r.status_code} : {r.text[:200]}"
    except requests.exceptions.ConnectionError:
        return f"N8n inaccessible ({N8N_URL}). Vérifie que le NAS est allumé."
    except Exception as e:
        return f"Erreur N8n : {e}"


def list_workflows() -> str:
    """
    Liste les workflows actifs sur N8n (nécessite N8N_API_KEY).

    Returns:
        Liste des workflows ou message d'erreur.
    """
    if not N8N_API_KEY:
        return "N8N_API_KEY non configuré — liste des workflows impossible."
    try:
        r = requests.get(
            f"{N8N_URL}/api/v1/workflows",
            headers=_headers(),
            timeout=8,
        )
        r.raise_for_status()
        wfs = r.json().get("data", [])
        if not wfs:
            return "Aucun workflow trouvé sur N8n."
        lines = ["Workflows N8n :"]
        for wf in wfs[:15]:
            status = "✅ actif" if wf.get("active") else "⏸ inactif"
            lines.append(f"  [{status}] {wf['name']} (id: {wf['id']})")
        return "\n".join(lines)
    except Exception as e:
        return f"Erreur liste N8n : {e}"


def get_workflow_status(workflow_id: str) -> str:
    """Retourne le statut d'un workflow par son ID."""
    if not N8N_API_KEY:
        return "N8N_API_KEY requis."
    try:
        r = requests.get(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            headers=_headers(),
            timeout=8,
        )
        r.raise_for_status()
        wf = r.json()
        status = "actif" if wf.get("active") else "inactif"
        return f"Workflow '{wf['name']}' — {status}"
    except Exception as e:
        return f"Erreur statut workflow : {e}"


def activate_workflow(workflow_id: str, active: bool = True) -> str:
    """Active ou désactive un workflow N8n."""
    if not N8N_API_KEY:
        return "N8N_API_KEY requis."
    try:
        r = requests.patch(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            json={"active": active},
            headers=_headers(),
            timeout=8,
        )
        r.raise_for_status()
        action = "activé" if active else "désactivé"
        return f"Workflow {workflow_id} {action}."
    except Exception as e:
        return f"Erreur activation workflow : {e}"
