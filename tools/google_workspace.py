"""
Google Workspace — Docs, Sheets, Drive.
Inspiré de JARVIS (techenclair.fr).

Nécessite : google-api-python-client, google-auth-oauthlib
Credentials : credentials.json OAuth2 dans le répertoire du projet
  (même credentials que Gmail/GCal déjà configurés)
"""

import json
import os
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]

_docs_service   = None
_sheets_service = None
_drive_service  = None
_last_doc_id    = None
_last_sheet_id  = None


def _get_creds():
    """Récupère ou renouvelle les credentials OAuth2 Google."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
    except ImportError:
        raise RuntimeError("google-api-python-client non installé — pip install google-api-python-client google-auth-oauthlib")

    token_path = BASE_DIR / "google_token_workspace.json"
    creds_path = BASE_DIR / "credentials.json"

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not creds_path.exists():
                raise FileNotFoundError(
                    "credentials.json introuvable. "
                    "Télécharge-le sur console.cloud.google.com "
                    "(APIs & Services → Credentials → OAuth 2.0 Client IDs)"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    return creds


def _docs():
    global _docs_service
    if _docs_service is None:
        from googleapiclient.discovery import build
        _docs_service = build("docs", "v1", credentials=_get_creds())
    return _docs_service


def _sheets():
    global _sheets_service
    if _sheets_service is None:
        from googleapiclient.discovery import build
        _sheets_service = build("sheets", "v4", credentials=_get_creds())
    return _sheets_service


def _drive():
    global _drive_service
    if _drive_service is None:
        from googleapiclient.discovery import build
        _drive_service = build("drive", "v3", credentials=_get_creds())
    return _drive_service


# ── Google Docs ───────────────────────────────────────────────────────────────

def create_doc(title: str, content: str = "") -> str:
    """
    Crée un Google Doc et l'ouvre dans le navigateur.

    Args:
        title:   Titre du document.
        content: Contenu initial (texte brut).
    """
    global _last_doc_id
    try:
        doc = _docs().documents().create(body={"title": title}).execute()
        doc_id = doc["documentId"]
        _last_doc_id = doc_id

        if content:
            _docs().documents().batchUpdate(
                documentId=doc_id,
                body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]}
            ).execute()

        url = f"https://docs.google.com/document/d/{doc_id}/edit"
        webbrowser.open(url)
        return f"Doc '{title}' créé et ouvert : {url}"
    except Exception as e:
        return f"Erreur Google Docs : {e}"


def append_to_doc(content: str, doc_id: str = None) -> str:
    """
    Ajoute du texte à un Google Doc existant.

    Args:
        content: Texte à ajouter.
        doc_id:  ID du document (utilise le dernier créé si absent).
    """
    global _last_doc_id
    target = doc_id or _last_doc_id
    if not target:
        return "Aucun document ouvert. Utilise create_doc() d'abord."
    try:
        doc      = _docs().documents().get(documentId=target).execute()
        end_idx  = doc["body"]["content"][-1]["endIndex"] - 1
        _docs().documents().batchUpdate(
            documentId=target,
            body={"requests": [{"insertText": {"location": {"index": end_idx}, "text": "\n" + content}}]}
        ).execute()
        _last_doc_id = target
        webbrowser.open(f"https://docs.google.com/document/d/{target}/edit")
        return f"Texte ajouté au document."
    except Exception as e:
        return f"Erreur ajout Google Docs : {e}"


def read_doc(doc_id: str) -> str:
    """Lit le contenu texte d'un Google Doc."""
    try:
        doc = _docs().documents().get(documentId=doc_id).execute()
        texts = []
        for elem in doc.get("body", {}).get("content", []):
            for pe in elem.get("paragraph", {}).get("elements", []):
                t = pe.get("textRun", {}).get("content", "")
                if t:
                    texts.append(t)
        return "".join(texts).strip()[:3000]
    except Exception as e:
        return f"Erreur lecture Google Docs : {e}"


# ── Google Sheets ─────────────────────────────────────────────────────────────

def create_sheet(title: str, headers: list = None) -> str:
    """
    Crée une Google Sheet et l'ouvre.

    Args:
        title:   Titre de la feuille.
        headers: Liste de headers pour la première ligne (optionnel).
    """
    global _last_sheet_id
    try:
        sheet = _sheets().spreadsheets().create(
            body={"properties": {"title": title}}
        ).execute()
        sheet_id    = sheet["spreadsheetId"]
        _last_sheet_id = sheet_id

        if headers:
            _sheets().spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range="A1",
                valueInputOption="RAW",
                body={"values": [headers]},
            ).execute()

        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
        webbrowser.open(url)
        return f"Sheet '{title}' créée et ouverte : {url}"
    except Exception as e:
        return f"Erreur Google Sheets : {e}"


def append_to_sheet(values: list, sheet_id: str = None, sheet_range: str = "A1") -> str:
    """
    Ajoute des lignes à une Google Sheet.

    Args:
        values:      Liste de lignes, chaque ligne est une liste. Ex: [["Omar", "Paris", 2026]]
        sheet_id:    ID de la feuille (utilise la dernière créée si absent).
        sheet_range: Plage de départ (défaut : "A1").
    """
    target = sheet_id or _last_sheet_id
    if not target:
        return "Aucune feuille ouverte. Utilise create_sheet() d'abord."
    try:
        _sheets().spreadsheets().values().append(
            spreadsheetId=target,
            range=sheet_range,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": values if isinstance(values[0], list) else [values]},
        ).execute()
        return f"{len(values)} ligne(s) ajoutée(s) à la feuille."
    except Exception as e:
        return f"Erreur ajout Google Sheets : {e}"


def read_sheet(sheet_id: str, sheet_range: str = "A1:Z100") -> str:
    """Lit des données depuis une Google Sheet."""
    try:
        result = _sheets().spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=sheet_range,
        ).execute()
        rows = result.get("values", [])
        if not rows:
            return "Feuille vide."
        lines = []
        for row in rows[:30]:
            lines.append(" | ".join(str(c) for c in row))
        return "\n".join(lines)
    except Exception as e:
        return f"Erreur lecture Google Sheets : {e}"


# ── Google Drive ──────────────────────────────────────────────────────────────

def list_drive_files(query: str = "", max_results: int = 10) -> str:
    """
    Liste les fichiers Google Drive récents ou par recherche.

    Args:
        query:       Termes de recherche (ex: "WULIX", "devis"). Vide = fichiers récents.
        max_results: Nombre maximum de résultats.
    """
    try:
        q = f"name contains '{query}'" if query else "trashed = false"
        results = _drive().files().list(
            q=q,
            pageSize=max_results,
            fields="files(id, name, mimeType, modifiedTime)",
            orderBy="modifiedTime desc",
        ).execute()
        files = results.get("files", [])
        if not files:
            return "Aucun fichier trouvé sur Google Drive."
        lines = [f"Fichiers Drive ({len(files)}) :"]
        for f in files:
            mtype = f["mimeType"].split(".")[-1].replace("vnd.google-apps.", "")
            lines.append(f"  [{mtype}] {f['name']} — {f['modifiedTime'][:10]}")
        return "\n".join(lines)
    except Exception as e:
        return f"Erreur Google Drive : {e}"
