#!/usr/bin/env python3
"""
    █████╗ ██╗███████╗ █████╗ ████████╗ ██████╗ ██╗   ██╗
   ██╔══██╗██║██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██║   ██║
   ███████║██║███████╗███████║   ██║   ██║   ██║██║   ██║
   ██╔══██║██║╚════██║██╔══██║   ██║   ██║   ██║██║   ██║
   ██║  ██║██║███████║██║  ██║   ██║   ╚██████╔╝╚██████╔╝
   ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝  ╚═╝    ╚═════╝  ╚═════╝

Agente Intelligente pour la Supervision, l'Automatisation
des Taches et l'Organisation Universelle
"""

import asyncio
import json
import os
import re
import sys
import types
from pathlib import Path

import requests

# ─── Patch OpenJarvis (module traces manquant dans v0.1.0) ───────────────────
def _patch_openjarvis():
    _t = types.ModuleType('openjarvis.traces')
    _ts = types.ModuleType('openjarvis.traces.store')
    class _TraceStore:
        def __init__(self, *a, **kw): pass
        def save(self, *a, **kw): pass
        def load(self, *a, **kw): return []
    _ts.TraceStore = _TraceStore
    sys.modules.setdefault('openjarvis.traces', _t)
    sys.modules.setdefault('openjarvis.traces.store', _ts)

_patch_openjarvis()

# ─── Chargement des outils OpenJarvis ────────────────────────────────────────
_OJ_TOOLS = {}
try:
    import openjarvis.tools  # déclenche l'enregistrement
    from openjarvis.core.registry import ToolRegistry
    _OJ_TOOLS = {name: ToolRegistry.get(name)() for name in [
        'calculator', 'shell_exec', 'code_interpreter', 'http_request', 'think'
    ] if ToolRegistry.contains(name)}
except Exception:
    pass
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.theme import Theme

from tools import (
    get_datetime, list_files, load_memory,
    open_application, open_url, read_file,
    recall, remember, forget, search_web, write_file,
    notify, remind,
    get_clipboard, set_clipboard,
    volume_up, volume_down, volume_mute_toggle,
    youtube_search_play, open_youtube_url,
    take_screenshot, set_volume, mute,
    get_unread_emails, search_emails, send_email, draft_email,
    get_calendar_today, get_calendar_range, create_meeting,
    gmail_unread, gmail_search, gmail_send,
    gcal_today, gcal_range, gcal_create,
)
from voice.stt import listen
from voice.tts import speak
from tools.n8n_tool import trigger_webhook, list_workflows, activate_workflow
from tools.clipboard_history import (
    get_clipboard_history, get_last_clipboard, restore_clipboard,
    clear_clipboard_history, start_clipboard_watcher, ClipboardHistory,
)
from tools.file_watcher import start_watching, stop_watching, get_recent_files, list_watchers
from tools.ocr_screen import extract_text_from_screen, extract_text_from_image, find_text_on_screen
from tools.google_workspace import (
    create_doc, append_to_doc, read_doc,
    create_sheet, append_to_sheet, read_sheet, list_drive_files,
)

# ─── Setup ───────────────────────────────────────────────────────────────────

load_dotenv()
BASE_DIR   = Path(__file__).parent
MEMORY_FILE = BASE_DIR / "memory" / "facts.md"

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

aisatou_theme = Theme({
    "aisatou": "bold magenta",
    "user":    "bold white",
    "tool":    "dim magenta",
    "error":   "bold red",
    "dim":     "dim white",
    "info":    "cyan",
})
console = Console(theme=aisatou_theme)

# ─── Outils disponibles ───────────────────────────────────────────────────────

TOOL_MAP = {
    "search_web":       lambda i: search_web(i["query"]),
    "remember":         lambda i: remember(i["fact"], MEMORY_FILE, i.get("category","faits")),
    "recall":           lambda i: recall(i.get("query", ""), MEMORY_FILE),
    "forget":           lambda i: forget(i["query"], MEMORY_FILE),
    "open_application": lambda i: open_application(i["name"]),
    "open_url":         lambda i: open_url(i["url"]),
    "get_datetime":     lambda i: get_datetime(),
    "read_file":        lambda i: read_file(i["path"]),
    "write_file":       lambda i: write_file(i["path"], i["content"]),
    "list_files":       lambda i: list_files(i["path"]),
    # Notifications
    "notify":               lambda i: notify(i["title"], i["message"], i.get("duration","short")),
    "remind":               lambda i: remind(i["message"], int(i.get("minutes",0)), int(i.get("seconds",30))),
    # Système avancé
    "get_clipboard":        lambda i: get_clipboard(),
    "set_clipboard":        lambda i: set_clipboard(i["text"]),
    "take_screenshot":      lambda i: take_screenshot(i.get("filename","")),
    "set_volume":           lambda i: set_volume(int(i["level"])),
    "mute":                 lambda i: mute(),
    "volume_up":            lambda i: volume_up(int(i.get("steps", 5))),
    "volume_down":          lambda i: volume_down(int(i.get("steps", 5))),
    "volume_mute":          lambda i: volume_mute_toggle(),
    "youtube_play":         lambda i: youtube_search_play(i["query"], i.get("fullscreen", True)),
    "open_youtube_url":     lambda i: open_youtube_url(i["url"]),
    # Outlook
    "outlook_unread":       lambda i: get_unread_emails(int(i.get("count",10))),
    "outlook_search":       lambda i: search_emails(i["query"], int(i.get("count",5))),
    "outlook_send":         lambda i: send_email(i["to"], i["subject"], i["body"]),
    "outlook_draft":        lambda i: draft_email(i["to"], i["subject"], i["body"]),
    "outlook_calendar_today": lambda i: get_calendar_today(),
    "outlook_calendar_week":  lambda i: get_calendar_range(int(i.get("days",7))),
    "outlook_create_meeting": lambda i: create_meeting(
        i["subject"], i["start"], int(i.get("duration_min",60)),
        i.get("location",""), i.get("body","")),
    # Gmail
    "gmail_unread":         lambda i: gmail_unread(int(i.get("count",10))),
    "gmail_search":         lambda i: gmail_search(i["query"], int(i.get("count",5))),
    "gmail_send":           lambda i: gmail_send(i["to"], i["subject"], i["body"]),
    "gcal_today":           lambda i: gcal_today(),
    "gcal_week":            lambda i: gcal_range(int(i.get("days",7))),
    "gcal_create":          lambda i: gcal_create(
        i["summary"], i["start"], int(i.get("duration_min",60)), i.get("description","")),
}

# ── Outils additionnels (vision, météo, math) ────────────────────────────────
try:
    from tools.vision_screen import vision_click, vision_type, vision_screenshot_describe
    _VISION_OK = True
except Exception:
    _VISION_OK = False

try:
    from tools.weather import get_weather, get_forecast, get_weather_alert
    _WEATHER_OK = True
except Exception:
    _WEATHER_OK = False

from tools.math_solver import solve as _math_solve, convert_units as _convert_units

# Injecter dans TOOL_MAP
if _VISION_OK:
    TOOL_MAP["vision_click"]    = lambda i: vision_click(i["instruction"])
    TOOL_MAP["vision_type"]     = lambda i: vision_type(i["instruction"], i["text"])
    TOOL_MAP["vision_describe"] = lambda i: vision_screenshot_describe(i.get("question", ""))

if _WEATHER_OK:
    TOOL_MAP["get_weather"]       = lambda i: get_weather(i.get("city", ""))
    TOOL_MAP["get_forecast"]      = lambda i: get_forecast(i.get("city", ""), int(i.get("days", 3)))
    TOOL_MAP["get_weather_alert"] = lambda i: get_weather_alert(i.get("city", ""))

TOOL_MAP["math_solve"]     = lambda i: _math_solve(i["expression"]) or "Expression non résolue localement."
TOOL_MAP["convert_units"]  = lambda i: _convert_units(float(i["value"]), i["from"], i["to"])

# N8n
TOOL_MAP["n8n_trigger"]        = lambda i: trigger_webhook(i["webhook"], i.get("data", {}))
TOOL_MAP["n8n_list_workflows"] = lambda i: list_workflows()
TOOL_MAP["n8n_activate"]       = lambda i: activate_workflow(i["id"], i.get("active", True))

# Clipboard history
TOOL_MAP["clipboard_history"]  = lambda i: get_clipboard_history(int(i.get("count", 10)))
TOOL_MAP["clipboard_get"]      = lambda i: get_last_clipboard(int(i.get("position", 1)))
TOOL_MAP["clipboard_restore"]  = lambda i: restore_clipboard(int(i.get("position", 1)))

# File watcher
TOOL_MAP["watch_folder"]       = lambda i: start_watching(i["folder"], i.get("name","default"), i.get("extensions"))
TOOL_MAP["unwatch_folder"]     = lambda i: stop_watching(i.get("name","default"))
TOOL_MAP["recent_files"]       = lambda i: get_recent_files(i.get("name","default"), int(i.get("count",10)))

# OCR
TOOL_MAP["ocr_screen"]         = lambda i: extract_text_from_screen(i.get("instruction",""))
TOOL_MAP["ocr_image"]          = lambda i: extract_text_from_image(i["path"], i.get("instruction",""))
TOOL_MAP["find_on_screen"]     = lambda i: find_text_on_screen(i["text"])

# Google Workspace
TOOL_MAP["gdocs_create"]       = lambda i: create_doc(i["title"], i.get("content",""))
TOOL_MAP["gdocs_append"]       = lambda i: append_to_doc(i["content"], i.get("doc_id"))
TOOL_MAP["gdocs_read"]         = lambda i: read_doc(i["doc_id"])
TOOL_MAP["gsheets_create"]     = lambda i: create_sheet(i["title"], i.get("headers"))
TOOL_MAP["gsheets_append"]     = lambda i: append_to_sheet(i["values"], i.get("sheet_id"))
TOOL_MAP["gsheets_read"]       = lambda i: read_sheet(i["sheet_id"], i.get("range","A1:Z100"))
TOOL_MAP["gdrive_list"]        = lambda i: list_drive_files(i.get("query",""), int(i.get("max",10)))

# ── Hermes Agent (NousResearch) — délégation tâches techniques lourdes ──────
try:
    from tools.hermes_tool import hermes_run, hermes_status, hermes_skills
    TOOL_MAP["hermes_run"]    = lambda i: hermes_run(i["task"], int(i.get("timeout", 180)))
    TOOL_MAP["hermes_status"] = lambda i: hermes_status()
    TOOL_MAP["hermes_skills"] = lambda i: hermes_skills()
except Exception as _e_hermes:
    pass  # Hermes optionnel

# ── Outils WULIX ─────────────────────────────────────────────────────────────
import subprocess as _sp
import json as _json_w
import datetime as _dt_w

def _run_wulix_agent(name: str) -> str:
    _agents_map = {
        "samba":  "agents/samba_agent.py",
        "ndeye":  "agents/ndeye_agent.py",
        "kofi":   "agents/veille_agent.py",
        "crew":   "agents/crewai_prospector.py",
        "lamine": "agents/lamine_agent.py",
        "kouman": "agents/prospecteur_agent.py",
        "faktour":"agents/facturation_agent.py",
    }
    script = _agents_map.get(name.lower())
    if not script:
        return f"Agent inconnu: {name}. Dispo: {', '.join(_agents_map.keys())}"
    try:
        r = _sp.run(["python", script], cwd=str(BASE_DIR),
                    capture_output=True, text=True, timeout=120)
        last = "\n".join((r.stdout or r.stderr).strip().split("\n")[-6:])
        return f"Agent {name} termine:\n{last}"
    except Exception as e:
        return f"Erreur {name}: {e}"

def _get_today_leads() -> str:
    today = _dt_w.date.today().isoformat()
    leads_file = BASE_DIR / "agents" / "content" / "leads" / f"crew_leads_{today}.json"
    if not leads_file.exists():
        return f"Aucun leads pour {today}. Lance CREW d'abord."
    data = _json_w.loads(leads_file.read_text(encoding="utf-8"))
    leads = data.get("leads", [])
    if not leads:
        return "0 lead qualifie aujourd'hui."
    lines = [f"{len(leads)} leads — {today}:"]
    for i, lead in enumerate(leads[:5], 1):
        q = lead.get("qualif", {})
        lines.append(f"{i}. [{q.get('score','?')}/10] {lead['title'][:65]}")
        lines.append(f"   {lead['url']}")
        msg = lead.get("approach_message","")[:100]
        lines.append(f"   >> {msg}...")
    return "\n".join(lines)

def _deploy_wulix_site() -> str:
    try:
        r = _sp.run(
            ["powershell", "-File", r"C:\Users\USER\Scripts\WULIX\deploy_cloudflare.ps1"],
            capture_output=True, text=True, timeout=120
        )
        last = "\n".join((r.stdout or "").strip().split("\n")[-4:])
        return f"Deploy wulix.fr:\n{last}"
    except Exception as e:
        return f"Erreur deploy: {e}"

def _wulix_status() -> str:
    today = _dt_w.date.today().isoformat()
    leads_file = BASE_DIR / "agents" / "content" / "leads" / f"crew_leads_{today}.json"
    n_leads = 0
    if leads_file.exists():
        try:
            d = _json_w.loads(leads_file.read_text(encoding="utf-8"))
            n_leads = d.get("qualified_leads", 0)
        except Exception:
            pass
    logs = list((BASE_DIR / "agents" / "logs").glob("*.log"))
    return (f"WULIX status — {today}\n"
            f"Leads du jour : {n_leads}\n"
            f"Logs agents   : {len(logs)} fichiers\n"
            f"Site          : https://wulix.fr\n"
            f"Gumroad       : https://wulix.gumroad.com")

TOOL_MAP["run_wulix_agent"] = lambda i: _run_wulix_agent(i.get("name",""))
TOOL_MAP["get_today_leads"] = lambda i: _get_today_leads()
TOOL_MAP["deploy_wulix"]    = lambda i: _deploy_wulix_site()
TOOL_MAP["wulix_status"]    = lambda i: _wulix_status()

# Démarrer la surveillance clipboard en arrière-plan
ClipboardHistory.start()


def _oj_exec(tool_name: str, **kwargs) -> str:
    """Exécute un outil OpenJarvis et retourne le résultat."""
    if tool_name not in _OJ_TOOLS:
        return f"Outil OpenJarvis non disponible : {tool_name}"
    try:
        result = _OJ_TOOLS[tool_name].execute(**kwargs)
        return result.content if hasattr(result, 'content') else str(result)
    except Exception as e:
        return f"Erreur ({tool_name}): {e}"

# Outils OpenJarvis dans TOOL_MAP
_OJ_MAP = {
    "calculator":       lambda i: _oj_exec("calculator",       expression=i["expression"]),
    "shell_exec":       lambda i: _oj_exec("shell_exec",       command=i["command"]),
    "code_interpreter": lambda i: _oj_exec("code_interpreter", code=i["code"]),
    "http_request":     lambda i: _oj_exec("http_request",     url=i["url"], method=i.get("method","GET"), body=i.get("body","")),
    "think":            lambda i: _oj_exec("think",            thought=i["thought"]),
}
TOOL_MAP.update(_OJ_MAP)

def execute_tool(name: str, inputs: dict) -> str:
    if name in TOOL_MAP:
        try:
            return str(TOOL_MAP[name](inputs))
        except Exception as e:
            return f"Erreur ({name}): {e}"
    return f"Outil inconnu : {name}"

# ─── Prompt systeme ───────────────────────────────────────────────────────────

def get_system_prompt() -> str:
    memory = load_memory(MEMORY_FILE)
    now = get_datetime()
    tools_desc = """
Tu peux utiliser ces outils en repondant avec ce format JSON exact sur une seule ligne :
TOOL: {"name": "nom_outil", "args": {...}}

Outils disponibles :
- search_web(query)                        : chercher sur internet
- remember(fact)                           : sauvegarder un fait en memoire
- recall(query)                            : lire la memoire
- open_application(name)                   : ouvrir une app
- open_url(url)                            : ouvrir un site
- get_datetime()                           : date et heure
- read_file(path)                          : lire un fichier
- write_file(path, content)                : ecrire un fichier
- list_files(path)                         : lister un dossier
- notify(title, message, duration?)        : notification Windows toast
- remind(message, minutes?, seconds?)      : rappel programme
- get_clipboard()                          : lire le presse-papiers
- set_clipboard(text)                      : copier dans le presse-papiers
- take_screenshot(filename?)               : prendre une capture d'ecran
- set_volume(level)                        : regler le volume (0-100)
- mute()                                   : couper/retablir le son
- volume_up(steps?)                        : monter le volume (1-20 crans)
- volume_down(steps?)                      : baisser le volume (1-20 crans)
- volume_mute()                            : couper/retablir le son
- youtube_play(query, fullscreen?)         : chercher et lancer une video YouTube
- open_youtube_url(url)                    : ouvrir une URL YouTube directe
- get_weather(city?)                       : meteo actuelle (ville ou Paris par defaut)
- get_forecast(city?, days?)               : previsions meteo 1-5 jours
- get_weather_alert(city?)                 : alerte meteo si conditions extremes
- math_solve(expression)                   : calcul mathematique instantane offline
- convert_units(value, from, to)           : convertir unites (km/miles, kg/lbs, c/f, l/gallons)
- vision_click(instruction)               : cliquer sur un element de l'ecran via IA vision
- vision_type(instruction, text)          : cliquer+taper dans un champ via IA vision
- vision_describe(question?)              : decrire ou analyser l'ecran actuel
- ocr_screen(instruction?)               : extraire le texte visible a l'ecran
- ocr_image(path, instruction?)          : extraire le texte d'une image
- find_on_screen(text)                   : verifier si un texte est visible a l'ecran
- n8n_trigger(webhook, data?)            : declencher un workflow N8n via webhook
- n8n_list_workflows()                   : lister les workflows N8n actifs
- n8n_activate(id, active?)              : activer/desactiver un workflow N8n
- hermes_run(task, timeout?)             : DELEGUER une tache technique lourde a Hermes Agent (Linux WSL2). A utiliser pour : refactor de code complexe, browser automation, taches qui demandent un sandbox isole, generation de diagrammes/manim/ascii art. Timeout par defaut 180s. Reponds avec le resultat de Hermes.
- hermes_status()                        : verifier que Hermes Agent est installe et fonctionnel
- hermes_skills()                        : lister les 89 skills built-in de Hermes (architecture-diagram, design-md, manim-video, opencode, etc.)
- clipboard_history(count?)              : historique des derniers textes copies
- clipboard_get(position?)               : recuperer une copie specifique (1=derniere)
- clipboard_restore(position?)           : remettre une ancienne copie dans le presse-papiers
- watch_folder(folder, name?, extensions?): surveiller un dossier pour nouveaux fichiers
- unwatch_folder(name?)                  : arreter la surveillance d'un dossier
- recent_files(name?, count?)            : lister les fichiers recemment detectes
- gdocs_create(title, content?)          : creer un Google Doc
- gdocs_append(content, doc_id?)         : ajouter du texte a un Google Doc
- gdocs_read(doc_id)                     : lire le contenu d'un Google Doc
- gsheets_create(title, headers?)        : creer une Google Sheet
- gsheets_append(values, sheet_id?)      : ajouter des lignes a une Sheet
- gsheets_read(sheet_id, range?)         : lire des donnees d'une Sheet
- gdrive_list(query?, max?)              : lister les fichiers Google Drive
- outlook_unread(count?)                   : lire emails non lus Outlook
- outlook_search(query, count?)            : rechercher emails Outlook
- outlook_send(to, subject, body)          : envoyer email Outlook
- outlook_draft(to, subject, body)         : creer brouillon Outlook
- outlook_calendar_today()                 : agenda Outlook aujourd'hui
- outlook_calendar_week(days?)             : agenda Outlook semaine
- outlook_create_meeting(subject, start, duration_min?, location?, body?) : creer RDV Outlook (start: JJ/MM/AAAA HH:MM)
- gmail_unread(count?)                     : lire emails non lus Gmail
- gmail_search(query, count?)              : rechercher emails Gmail
- gmail_send(to, subject, body)            : envoyer email Gmail
- gcal_today()                             : agenda Google Calendar aujourd'hui
- gcal_week(days?)                         : agenda Google Calendar semaine
- gcal_create(summary, start, duration_min?, description?) : creer evenement GCal
- calculator(expression)                   : calculer une expression mathematique
- shell_exec(command)                      : executer une commande shell/PowerShell
- code_interpreter(code)                   : executer du code Python
- http_request(url, method?, body?)        : faire une requete HTTP
- think(thought)                           : raisonner etape par etape

── Outils WULIX (gestion agence) ──
- run_wulix_agent(name)                    : lancer un agent WULIX (samba/ndeye/kofi/crew/lamine/faktour)
- get_today_leads()                        : leads qualifies du jour (Reddit/web)
- deploy_wulix()                           : deployer wulix.fr sur Cloudflare Pages
- wulix_status()                           : statut general WULIX (leads, logs, sites)

Apres avoir vu le resultat d'un outil, reponds normalement a l'utilisateur.
N'utilise les outils que quand c'est utile.
"""
    return f"""Tu es AISATOU (Agente Intelligente pour la Supervision, l'Automatisation des Taches et l'Organisation Universelle).

Prenom soninkee d'Afrique de l'Ouest. Tu es intelligente, chaleureuse, directe et competente.

Langue : francais par defaut, anglais si l'utilisateur ecrit en anglais.
Date/heure : {now}
Memoire : {memory.strip() if memory.strip() else "Aucune memoire."}

Reponses courtes et concises (optimise pour la voix).
{tools_desc}"""

# ─── Backend Ollama ───────────────────────────────────────────────────────────

OLLAMA_URL   = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("AISATOU_MODEL", "mistral")

# ─── Backend Gemini ───────────────────────────────────────────────────────────

GEMINI_MODELS = {
    "gemini-2.5-flash", "gemini-2.5-pro",
    "gemini-2.0-flash", "gemini-2.0-flash-lite",
    "gemini-1.5-flash", "gemini-1.5-pro",
}

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        return client
    except ImportError:
        return None

async def run_turn_gemini(client, conversation: list, user_input: str, model_name: str = None) -> str:
    """Tour de conversation avec Gemini 2.x (avec outils ReAct).
    Si quota épuisé (429), bascule automatiquement sur Ollama/mistral.
    """
    from google import genai as _genai
    from google.genai import types as _gtypes

    if not model_name:
        model_name = OLLAMA_MODEL if OLLAMA_MODEL in GEMINI_MODELS else "gemini-2.0-flash"
    system = get_system_prompt()

    # Construire l'historique au format Gemini
    history = []
    for msg in conversation[-10:]:
        role = "user" if msg["role"] == "user" else "model"
        content = msg["content"] if isinstance(msg["content"], str) else str(msg["content"])
        history.append(_gtypes.Content(role=role, parts=[_gtypes.Part(text=content)]))

    max_iterations = 5
    current_input = user_input
    try:
        for _ in range(max_iterations):
            contents = history + [_gtypes.Content(role="user", parts=[_gtypes.Part(text=current_input)])]
            resp = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=_gtypes.GenerateContentConfig(
                    system_instruction=system,
                    temperature=0.7,
                    max_output_tokens=2048,
                ),
            )
            response_text = resp.text.strip()

            tool_name, tool_args = parse_tool_call(response_text)
            if tool_name:
                console.print(f"  [tool]>> {tool_name}({str(tool_args)[:60]})[/]")
                tool_result = execute_tool(tool_name, tool_args or {})
                current_input = f"Resultat de {tool_name}: {tool_result}\n\nMaintenant reponds a l'utilisateur."
                history.append(_gtypes.Content(role="user",  parts=[_gtypes.Part(text=current_input)]))
                history.append(_gtypes.Content(role="model", parts=[_gtypes.Part(text=response_text)]))
            else:
                clean = re.sub(r'TOOL:\s*\{.*?\}', '', response_text, flags=re.DOTALL).strip()
                conversation.append({"role": "user",      "content": user_input})
                conversation.append({"role": "assistant", "content": clean})
                return clean
    except Exception as e:
        err_str = str(e)
        # Quota Gemini dépassé → fallback Ollama
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
            console.print("  [dim]Gemini quota dépassé → fallback Ollama/mistral[/]")
            if is_ollama_running():
                return await run_turn_ollama(conversation, user_input, model="mistral")
            return "⚠️ Quota Gemini épuisé pour aujourd'hui et Ollama n'est pas disponible. Réessaie demain ou change de modèle dans les paramètres."
        raise

    return response_text

def is_ollama_running() -> bool:
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return r.status_code == 200
    except Exception:
        return False

def ollama_chat(messages: list, model: str = None) -> str:
    """Appel simple au chat Ollama."""
    payload = {
        "model": model or OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 512},
    }
    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["message"]["content"].strip()

def parse_tool_call(text: str):
    """Detecte si la reponse contient un appel d'outil TOOL: {...}"""
    match = re.search(r'TOOL:\s*(\{.*\})', text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            return data.get("name"), data.get("args", {})
        except json.JSONDecodeError:
            return None, None
    return None, None

async def run_turn_ollama(conversation: list, user_input: str, model: str = None) -> str:
    """Tour de conversation avec Ollama + gestion des outils (ReAct)."""
    system = get_system_prompt()
    messages = [{"role": "system", "content": system}]

    # Ajouter l'historique (derniers 10 messages pour eviter le depassement de contexte)
    for msg in conversation[-10:]:
        role = msg["role"]
        content = msg["content"]
        if isinstance(content, str):
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_input})

    max_iterations = 5
    for _ in range(max_iterations):
        response_text = ollama_chat(messages, model=model)

        tool_name, tool_args = parse_tool_call(response_text)
        if tool_name:
            console.print(f"  [tool]>> {tool_name}({str(tool_args)[:60]})[/]")
            tool_result = execute_tool(tool_name, tool_args or {})

            # Ajouter la reponse outil et demander la suite
            messages.append({"role": "assistant", "content": response_text})
            messages.append({
                "role": "user",
                "content": f"Resultat de {tool_name}: {tool_result}\n\nMaintenant reponds a l'utilisateur."
            })
        else:
            # Reponse finale — nettoyer les artefacts eventuels
            clean = re.sub(r'TOOL:\s*\{.*?\}', '', response_text, flags=re.DOTALL).strip()
            conversation.append({"role": "user", "content": user_input})
            conversation.append({"role": "assistant", "content": clean})
            return clean

    return response_text

# ─── Backend Groq (Llama 3.3-70B, gratuit, très rapide) ──────────────────────

GROQ_MODELS = {"llama-3.3-70b-versatile", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"}

def get_groq_client():
    """Retourne un client OpenAI-compatible pointant sur l'API Groq."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "VOTRE_CLE_ICI":
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    except ImportError:
        return None

async def run_turn_groq(client, conversation: list, user_input: str,
                        model: str = "llama-3.3-70b-versatile") -> str:
    """Tour de conversation avec Groq (OpenAI-compatible, avec outils ReAct)."""
    import asyncio
    system = get_system_prompt()
    messages = [{"role": "system", "content": system}]
    for msg in conversation[-10:]:
        if isinstance(msg.get("content"), str):
            messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_input})

    max_iterations = 5
    for _ in range(max_iterations):
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2048,
                )
            )
            response_text = response.choices[0].message.content.strip()
        except Exception as e:
            return f"Erreur Groq : {e}"

        tool_name, tool_args = parse_tool_call(response_text)
        if tool_name:
            console.print(f"  [tool]>> {tool_name}({str(tool_args)[:60]})[/]")
            tool_result = execute_tool(tool_name, tool_args or {})
            messages.append({"role": "assistant", "content": response_text})
            messages.append({
                "role": "user",
                "content": f"Resultat de {tool_name}: {tool_result}\n\nMaintenant reponds a l'utilisateur."
            })
        else:
            clean = re.sub(r'TOOL:\s*\{.*?\}', '', response_text, flags=re.DOTALL).strip()
            conversation.append({"role": "user",      "content": user_input})
            conversation.append({"role": "assistant", "content": clean})
            return clean

    return response_text

# ─── Backend Claude (fallback si token disponible) ────────────────────────────

def get_claude_client():
    try:
        import anthropic
        token = (os.environ.get("CLAUDE_CODE_OAUTH_TOKEN") or
                 os.environ.get("ANTHROPIC_API_KEY", ""))
        if token and not token.startswith("sk-ant-..."):
            return anthropic.Anthropic(api_key=token)
    except ImportError:
        pass
    return None

def _s(*props, req=None):
    """Helper raccourci pour input_schema."""
    return {"type":"object","properties":{p:{"type":"string"} for p in props},"required":req or []}

CLAUDE_TOOLS = [
    {"name": "search_web",       "description": "Rechercher sur internet.",          "input_schema": _s("query", req=["query"])},
    {"name": "remember",         "description": "Sauvegarder en memoire.",           "input_schema": _s("fact", req=["fact"])},
    {"name": "recall",           "description": "Lire la memoire.",                  "input_schema": _s("query")},
    {"name": "open_application", "description": "Ouvrir une application.",           "input_schema": _s("name", req=["name"])},
    {"name": "open_url",         "description": "Ouvrir une URL.",                   "input_schema": _s("url", req=["url"])},
    {"name": "get_datetime",     "description": "Date et heure.",                    "input_schema": {"type":"object","properties":{},"required":[]}},
    {"name": "read_file",        "description": "Lire un fichier.",                  "input_schema": _s("path", req=["path"])},
    {"name": "write_file",       "description": "Ecrire un fichier.",                "input_schema": _s("path","content", req=["path","content"])},
    {"name": "list_files",       "description": "Lister un repertoire.",             "input_schema": _s("path", req=["path"])},
    {"name": "notify",           "description": "Notification Windows toast.",       "input_schema": _s("title","message","duration", req=["title","message"])},
    {"name": "remind",           "description": "Programmer un rappel.",
     "input_schema": {"type":"object","properties":{"message":{"type":"string"},"minutes":{"type":"integer"},"seconds":{"type":"integer"}},"required":["message"]}},
    {"name": "get_clipboard",    "description": "Lire le presse-papiers.",           "input_schema": {"type":"object","properties":{},"required":[]}},
    {"name": "set_clipboard",    "description": "Copier dans le presse-papiers.",    "input_schema": _s("text", req=["text"])},
    {"name": "take_screenshot",  "description": "Prendre une capture d'ecran.",      "input_schema": _s("filename")},
    {"name": "set_volume",       "description": "Regler le volume (0-100).",
     "input_schema": {"type":"object","properties":{"level":{"type":"integer"}},"required":["level"]}},
    {"name": "mute",             "description": "Couper/retablir le son.",           "input_schema": {"type":"object","properties":{},"required":[]}},
    # Outlook
    {"name": "outlook_unread",   "description": "Lire emails non lus Outlook.",
     "input_schema": {"type":"object","properties":{"count":{"type":"integer"}},"required":[]}},
    {"name": "outlook_search",   "description": "Rechercher emails Outlook.",         "input_schema": _s("query", req=["query"])},
    {"name": "outlook_send",     "description": "Envoyer email via Outlook.",         "input_schema": _s("to","subject","body", req=["to","subject","body"])},
    {"name": "outlook_draft",    "description": "Creer brouillon Outlook.",           "input_schema": _s("to","subject","body", req=["to","subject","body"])},
    {"name": "outlook_calendar_today", "description": "Agenda Outlook aujourd'hui.", "input_schema": {"type":"object","properties":{},"required":[]}},
    {"name": "outlook_calendar_week",  "description": "Agenda Outlook semaine.",
     "input_schema": {"type":"object","properties":{"days":{"type":"integer"}},"required":[]}},
    {"name": "outlook_create_meeting", "description": "Creer RDV Outlook. start=JJ/MM/AAAA HH:MM",
     "input_schema": {"type":"object","properties":{
         "subject":{"type":"string"},"start":{"type":"string"},
         "duration_min":{"type":"integer"},"location":{"type":"string"},"body":{"type":"string"}
     },"required":["subject","start"]}},
    # Gmail
    {"name": "gmail_unread",     "description": "Lire emails non lus Gmail.",
     "input_schema": {"type":"object","properties":{"count":{"type":"integer"}},"required":[]}},
    {"name": "gmail_search",     "description": "Rechercher emails Gmail.",           "input_schema": _s("query", req=["query"])},
    {"name": "gmail_send",       "description": "Envoyer email via Gmail.",           "input_schema": _s("to","subject","body", req=["to","subject","body"])},
    {"name": "gcal_today",       "description": "Agenda Google Calendar aujourd'hui.","input_schema": {"type":"object","properties":{},"required":[]}},
    {"name": "gcal_week",        "description": "Agenda Google Calendar semaine.",
     "input_schema": {"type":"object","properties":{"days":{"type":"integer"}},"required":[]}},
    {"name": "gcal_create",      "description": "Creer evenement Google Calendar. start=JJ/MM/AAAA HH:MM",
     "input_schema": {"type":"object","properties":{
         "summary":{"type":"string"},"start":{"type":"string"},
         "duration_min":{"type":"integer"},"description":{"type":"string"}
     },"required":["summary","start"]}},
]

async def run_turn_claude(client, conversation: list, user_input: str) -> str:
    import anthropic as _anthropic
    conversation.append({"role": "user", "content": user_input})
    while True:
        resp = client.messages.create(
            model=os.getenv("AISATOU_CLAUDE_MODEL", "claude-opus-4-6"),
            max_tokens=1024,
            system=get_system_prompt(),
            tools=CLAUDE_TOOLS,
            messages=conversation,
        )
        if resp.stop_reason == "tool_use":
            results = []
            for block in resp.content:
                if block.type == "tool_use":
                    console.print(f"  [tool]>> {block.name}({str(block.input)[:60]})[/]")
                    results.append({"type": "tool_result", "tool_use_id": block.id,
                                    "content": execute_tool(block.name, block.input)})
            conversation.append({"role": "assistant", "content": resp.content})
            conversation.append({"role": "user",      "content": results})
        else:
            text = "".join(b.text for b in resp.content if hasattr(b, "text"))
            conversation.append({"role": "assistant", "content": resp.content})
            return text

# ─── Main ─────────────────────────────────────────────────────────────────────

async def main():
    use_voice    = "--voice" in sys.argv or "-v" in sys.argv
    use_wake     = "--wake"  in sys.argv or "-w" in sys.argv or use_voice
    conversation: list = []

    loop = asyncio.get_event_loop()

    # Detection du backend — priorité : Gemini > Groq > Ollama > Claude API
    gemini_client = get_gemini_client()
    groq_client   = get_groq_client()
    use_gemini    = gemini_client is not None
    use_groq      = groq_client is not None and not use_gemini
    claude_client = get_claude_client()
    use_ollama    = not use_gemini and not use_groq and is_ollama_running()

    if not use_gemini and not use_groq and not use_ollama and not claude_client:
        console.print("[error]Aucun backend disponible.[/]")
        console.print("[dim]Ajoute GEMINI_API_KEY ou GROQ_API_KEY dans .env[/]")
        sys.exit(1)

    if use_gemini:
        backend_name = f"Gemini ({os.getenv('AISATOU_MODEL', 'gemini-2.0-flash-lite')})"
    elif use_groq:
        backend_name = "Groq (llama-3.3-70b-versatile)"
    elif use_ollama:
        backend_name = f"Ollama ({OLLAMA_MODEL})"
    else:
        backend_name = "Claude API"

    # Banniere
    console.print()
    console.print(Panel.fit(
        "[aisatou]A.I.S.A.T.O.U.[/]\n"
        "[dim]Agente Intelligente pour la Supervision, l'Automatisation[/]\n"
        "[dim]des Taches et l'Organisation Universelle[/]\n"
        f"[dim]Backend : {backend_name}[/]",
        border_style="magenta",
        padding=(1, 4),
    ))

    mode_parts = []
    if use_voice: mode_parts.append("[magenta]Mode vocal[/]")
    if use_wake:  mode_parts.append("[magenta]Wake word actif — dis 'Aisatou'[/]")
    if not mode_parts: mode_parts.append("[dim]Mode texte  (--voice ou --wake pour le micro)[/]")
    console.print(f"  {' · '.join(mode_parts)}")
    n_tools = len(TOOL_MAP)
    console.print(f"  [dim]{n_tools} outils charges  ·  /help pour l'aide  ·  /leads  ·  /agents  ·  exit pour quitter[/]\n")

    async def groq_ask_httpx(user_input: str) -> str:
        """Appel Groq via httpx direct (contourne les blocages VPN du client OpenAI)."""
        import httpx as _hx
        import asyncio as _aio
        system = get_system_prompt()
        messages = [{"role": "system", "content": system}]
        for msg in conversation[-10:]:
            if isinstance(msg.get("content"), str):
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_input})
        for _ in range(5):
            r = await _aio.get_event_loop().run_in_executor(None, lambda: _hx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY','')}"},
                json={"model": "llama-3.3-70b-versatile", "messages": messages,
                      "max_tokens": 1024, "temperature": 0.7},
                timeout=30
            ))
            r.raise_for_status()
            response_text = r.json()["choices"][0]["message"]["content"].strip()
            tool_name, tool_args = parse_tool_call(response_text)
            if tool_name:
                console.print(f"  [tool]>> {tool_name}({str(tool_args)[:60]})[/]")
                tool_result = execute_tool(tool_name, tool_args or {})
                messages.append({"role": "assistant", "content": response_text})
                messages.append({"role": "user", "content": f"Resultat de {tool_name}: {tool_result}\n\nMaintenant reponds."})
            else:
                clean = re.sub(r'TOOL:\s*\{.*?\}', '', response_text, flags=re.DOTALL).strip()
                conversation.append({"role": "user", "content": user_input})
                conversation.append({"role": "assistant", "content": clean})
                return clean
        return response_text

    async def ask(user_input: str) -> str:
        if use_gemini:
            try:
                return await run_turn_gemini(gemini_client, conversation, user_input)
            except Exception as e:
                err = str(e)
                if "429" in err or "quota" in err.lower():
                    console.print("  [dim]Gemini quota — fallback Groq[/]")
                else:
                    raise
        # Fallback Groq (httpx direct, fonctionne sans VPN)
        try:
            return await groq_ask_httpx(user_input)
        except Exception as e:
            console.print(f"  [dim]Groq error: {e} — fallback Ollama[/]")
        if use_ollama:
            return await run_turn_ollama(conversation, user_input)
        return await run_turn_claude(claude_client, conversation, user_input)

    async def process_and_respond(user_input: str):
        """Traite une entrée et affiche/dit la réponse."""
        console.print(f"[user]Vous :[/] {user_input}")
        console.print("[dim magenta]  ...[/]", end="\r")
        response = await ask(user_input)
        console.print(" " * 20, end="\r")
        console.print(Panel(Text(response, style="white"),
                            title="[aisatou]AISATOU[/]", border_style="magenta"))
        if use_voice or use_wake:
            if wake_detector:
                wake_detector.pause()
            await speak(response)
            if wake_detector:
                wake_detector.resume()

    # Wake word detector
    wake_detector = None
    if use_wake:
        from voice.wake_word import WakeWordDetector
        # File d'attente thread-safe pour les commandes détectées
        import queue
        wake_queue: queue.Queue = queue.Queue()

        def on_wake(command: str):
            wake_queue.put(command or "__wake__")

        wake_detector = WakeWordDetector(on_wake=on_wake)
        wake_detector.start()
        notify("AISATOU", "Wake word actif — dis 'Aisatou' pour m'activer !", "short")

    # Salutation
    console.print("  [dim]Demarrage...[/]")
    greeting = await ask("Presente-toi en une phrase, dis que tu es prete. Chaleureuse et concise.")
    console.print(Panel(Text(greeting, style="white"), title="[aisatou]AISATOU[/]", border_style="magenta"))
    if use_voice or use_wake:
        if wake_detector: wake_detector.pause()
        await speak(greeting)
        if wake_detector: wake_detector.resume()

    # Boucle principale
    while True:
        try:
            # ── Mode wake word : attendre activation puis écouter commande ──
            if use_wake and wake_detector:
                # Afficher indicateur discret
                console.print("[dim]  En veille — dis 'Aisatou' ...[/]", end="\r")

                # Vérifier la file d'attente sans bloquer la boucle asyncio
                try:
                    command = wake_queue.get_nowait()
                except Exception:
                    await asyncio.sleep(0.15)
                    continue

                console.print(" " * 40, end="\r")

                if command and command != "__wake__":
                    # Commande dite en même temps que le wake word
                    await process_and_respond(command)
                else:
                    # Wake word seul — écouter la commande qui suit
                    console.print("[magenta]  Oui ? Je t'ecoute...[/]", end="\r")
                    await speak("Oui ?")
                    user_input = listen(timeout=6, phrase_limit=20)
                    console.print(" " * 30, end="\r")
                    if user_input:
                        await process_and_respond(user_input)
                    else:
                        console.print("[dim]  (rien entendu)[/]")
                continue

            # ── Mode vocal simple ──
            if use_voice:
                console.print("[magenta]A l'ecoute...[/]", end="\r")
                user_input = listen()
                if not user_input:
                    continue
                console.print(f"[user]Vous :[/] {user_input}")

            # ── Mode texte ──
            else:
                user_input = Prompt.ask("\n[user]Vous[/]")

            if not user_input:
                continue

            # ── Slash commands ────────────────────────────────────────────────
            if user_input.strip().startswith("/"):
                cmd = user_input.strip().lower().lstrip("/").split()[0]
                if cmd in ("help", "aide", "h", "?"):
                    console.print(Panel(
                        "[cyan]/help[/]    — cette aide\n"
                        "[cyan]/tools[/]   — liste de tous les outils\n"
                        "[cyan]/agents[/]  — agents WULIX disponibles\n"
                        "[cyan]/leads[/]   — leads qualifies du jour\n"
                        "[cyan]/deploy[/]  — deployer wulix.fr\n"
                        "[cyan]/status[/]  — statut WULIX\n"
                        "[cyan]/memory[/]  — voir la memoire\n"
                        "[cyan]/clear[/]   — effacer l'historique\n"
                        "[cyan]exit[/]     — quitter",
                        title="[aisatou]Commandes AISATOU[/]", border_style="magenta"
                    ))
                elif cmd in ("tools", "outils"):
                    tools_list = "  ".join(sorted(TOOL_MAP.keys()))
                    console.print(Panel(
                        "\n".join(f"• {t}" for t in sorted(TOOL_MAP.keys())),
                        title=f"[aisatou]{len(TOOL_MAP)} outils disponibles[/]", border_style="cyan"
                    ))
                elif cmd in ("agents",):
                    console.print(Panel(
                        "• [cyan]samba[/]   — SEO, publie 1 article/semaine\n"
                        "• [cyan]ndeye[/]   — Analytics, rapport ventes quotidien\n"
                        "• [cyan]kofi[/]    — Veille IA, digest quotidien\n"
                        "• [cyan]crew[/]    — Prospection, leads Reddit/web\n"
                        "• [cyan]lamine[/]  — Support, repond emails Gmail\n"
                        "• [cyan]faktour[/] — Facturation, PDF factures\n\n"
                        "Usage: dis 'lance l'agent crew' ou 'run_wulix_agent(crew)'",
                        title="[aisatou]Agents WULIX[/]", border_style="purple"
                    ))
                elif cmd in ("leads",):
                    console.print(Panel(
                        _get_today_leads(),
                        title="[aisatou]Leads du jour[/]", border_style="green"
                    ))
                elif cmd in ("deploy",):
                    console.print("[dim]  Deploiement en cours...[/]")
                    result_deploy = _deploy_wulix_site()
                    console.print(Panel(result_deploy, title="[aisatou]Deploy WULIX[/]", border_style="cyan"))
                elif cmd in ("status",):
                    console.print(Panel(_wulix_status(), title="[aisatou]WULIX Status[/]", border_style="gold1"))
                elif cmd in ("memory", "memoire"):
                    mem = load_memory(MEMORY_FILE)
                    console.print(Panel(mem[:2000] + ("..." if len(mem)>2000 else ""),
                                        title="[aisatou]Memoire[/]", border_style="dim"))
                elif cmd in ("clear", "reset"):
                    conversation.clear()
                    console.print("[dim]  Historique efface.[/]")
                else:
                    console.print(f"[dim]Commande inconnue: /{cmd} — tape /help[/]")
                continue
            # ─────────────────────────────────────────────────────────────────

            if user_input.strip().lower() in ("exit", "quit", "au revoir", "goodbye", "quitter"):
                bye = "Au revoir ! Reviens quand tu as besoin de moi."
                console.print(f"\n[dim magenta]{bye}[/]")
                if use_voice:
                    await speak(bye)
                if wake_detector:
                    wake_detector.stop()
                break

            console.print("[dim magenta]  ...[/]", end="\r")
            response = await ask(user_input)
            console.print(" " * 15, end="\r")

            console.print(Panel(Text(response, style="white"),
                                title="[aisatou]AISATOU[/]", border_style="magenta"))
            if use_voice:
                await speak(response)

        except KeyboardInterrupt:
            console.print("\n[dim magenta]AISATOU hors ligne.[/]")
            break
        except Exception as e:
            console.print(f"[error]Erreur : {e}[/]")


if __name__ == "__main__":
    asyncio.run(main())
