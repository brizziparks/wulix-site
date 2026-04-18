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
    take_screenshot, set_volume, mute,
    get_unread_emails, search_emails, send_email, draft_email,
    get_calendar_today, get_calendar_range, create_meeting,
    gmail_unread, gmail_search, gmail_send,
    gcal_today, gcal_range, gcal_create,
)
from voice.stt import listen
from voice.tts import speak

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

    # Detection du backend
    claude_client = get_claude_client()
    use_ollama    = is_ollama_running()

    if not use_ollama and not claude_client:
        console.print("[error]Aucun backend disponible.[/]")
        console.print("[dim]Demarre Ollama (ollama serve) ou ajoute ANTHROPIC_API_KEY dans .env[/]")
        sys.exit(1)

    backend_name = f"Ollama ({OLLAMA_MODEL})" if use_ollama else "Claude API"

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
    console.print("[dim]  'au revoir' ou 'exit' pour quitter.\n[/]")

    async def ask(user_input: str) -> str:
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
