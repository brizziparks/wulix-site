#!/usr/bin/env python3
"""
AISATOU HUD â€" Interface Iron Man
Serveur FastAPI + WebSocket + interface web holographique
"""

import asyncio
import json
from datetime import datetime
import os
import sys
import secrets
import webbrowser
from pathlib import Path

import subprocess
import threading
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# â"€â"€â"€ Chemin du projet â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

import requests as _req
from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env", override=True)  # Charge .env avant tout

from aisatou import (
    get_claude_client, is_ollama_running,
    run_turn_ollama, run_turn_claude, run_turn_gemini,
    get_gemini_client, GEMINI_MODELS,
    get_groq_client, run_turn_groq, GROQ_MODELS,
    OLLAMA_MODEL, execute_tool,
)

# ── Voix (optionnel — si edge-tts + pygame installés) ───────────────────────
try:
    from voice.tts import speak as tts_speak, stop_speaking, set_ws_broadcaster
    from voice.stt import listen as stt_listen, list_microphones
    from voice.wake_word import WakeWordDetector
    VOICE_AVAILABLE = True
except Exception as _ve:
    VOICE_AVAILABLE = False
    print(f"[HUD] Mode voix non disponible : {_ve}")

# Modèle par défaut — lit AISATOU_MODEL depuis .env
_default_model = OLLAMA_MODEL

# ── Pool WebSocket pour broadcast voix ──────────────────────────────────────
_ws_pool: set = set()   # toutes les connexions actives
_voice_mode: bool = False  # voix activée globalement

# ── Sécurité — Authentification HTTP Basic ─────────────────────────────────
security = HTTPBasic()

# Mot de passe depuis .env
HUD_USER     = os.environ.get("HUD_USER", "aisatou")
HUD_PASSWORD = os.environ.get("HUD_PASSWORD", "WULIX2026")

def verify_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """Verifie les identifiants HTTP Basic. Protege toutes les routes."""
    correct_user = secrets.compare_digest(credentials.username.encode(), HUD_USER.encode())
    correct_pass = secrets.compare_digest(credentials.password.encode(), HUD_PASSWORD.encode())
    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=401,
            detail="Acces refuse",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# â"€â"€â"€ App FastAPI â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
app = FastAPI(title="AISATOU HUD", docs_url=None, redoc_url=None)  # Désactive /docs public
app.mount("/ui", StaticFiles(directory=BASE_DIR / "ui"), name="ui")
app.mount("/hud", StaticFiles(directory=BASE_DIR / "hud"), name="hud")


@app.get("/")
async def root(user: str = Depends(verify_auth)):
    return FileResponse(BASE_DIR / "hud" / "index.html")


@app.get("/mobile")
async def mobile(user: str = Depends(verify_auth)):
    """Interface mobile optimisée — accessible depuis téléphone via aisatou.rosmedia.fr/mobile"""
    return FileResponse(BASE_DIR / "hud" / "mobile.html")

# ── Historique conversations ─────────────────────────────────────────────────
_HISTORY_DIR = BASE_DIR / "memory" / "conversations"
_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
_session_file: dict = {}   # websocket_id -> Path


def _get_session_file(ws_id: str) -> "Path":
    """Retourne (et cree si besoin) le fichier JSON de la session courante."""
    if ws_id not in _session_file:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        _session_file[ws_id] = _HISTORY_DIR / f"session_{ts}.json"
        _session_file[ws_id].write_text(
            '{"session": "' + ts + '", "messages": []}',
            encoding="utf-8"
        )
    return _session_file[ws_id]


def _save_exchange(ws_id: str, user_msg: str, ai_msg: str):
    """Ajoute un echange dans le fichier JSON de session."""
    try:
        path = _get_session_file(ws_id)
        data = json.loads(path.read_text(encoding="utf-8"))
        data["messages"].append({
            "ts": datetime.now().isoformat(),
            "user": user_msg,
            "assistant": ai_msg,
        })
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"[history] Erreur sauvegarde : {e}")


@app.get("/history")
async def list_history(user: str = Depends(verify_auth)):
    """Liste les fichiers de conversation sauvegardes."""
    files = sorted(_HISTORY_DIR.glob("session_*.json"), reverse=True)
    result = []
    for f in files[:50]:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            result.append({
                "file": f.name,
                "session": data.get("session", ""),
                "count": len(data.get("messages", [])),
            })
        except Exception:
            pass
    return {"history": result}


@app.get("/history/{filename}")
async def download_history(filename: str, user: str = Depends(verify_auth)):
    """Telecharge un fichier de conversation."""
    path = _HISTORY_DIR / filename
    if not path.exists() or not path.name.startswith("session_"):
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    return FileResponse(path, media_type="application/json", filename=filename)




@app.get("/status")
async def status(user: str = Depends(verify_auth)):
    claude = get_claude_client() is not None
    ollama = is_ollama_running()
    model  = f"Ollama/{_default_model}" if ollama else ("Claude API" if claude else "Aucun")
    return {"backend": model, "ollama": ollama, "claude": claude}


@app.get("/models")
async def models(user: str = Depends(verify_auth)):
    """Liste des modÃ¨les disponibles (Ollama + Gemini si clÃ© configurÃ©e)."""
    names = []
    # ModÃ¨les Ollama
    try:
        r = _req.get("http://localhost:11434/api/tags", timeout=3)
        names = [m["name"] for m in r.json().get("models", [])]
    except Exception:
        pass
    if not names:
        names = [OLLAMA_MODEL]
    # ModÃ¨les Gemini si clÃ© disponible
    if get_gemini_client():
        names += ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash"]
    if get_groq_client():
        names += ["llama-3.3-70b-versatile", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"]
    return {"models": names}


# â"€â"€â"€ Fichiers JSON des agents â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
AGENTS_DIR     = BASE_DIR / "agents"
CONTENT_QUEUE  = AGENTS_DIR / "content_queue.json"
PROSPECTS_FILE = AGENTS_DIR / "prospects.json"
OUTREACH_FILE  = AGENTS_DIR / "outreach_queue.json"
DAILY_REPORT   = AGENTS_DIR / "daily_report.json"
BLOG_QUEUE     = AGENTS_DIR / "blog_queue.json"
TASKS_CONFIG   = AGENTS_DIR / "tasks_config.json"
TASKS_LOG      = AGENTS_DIR / "tasks_log.json"

_agent_tasks: dict = {}  # {task_id: {"status": ..., "output": ...}}


def _load_json(path: Path) -> list | dict:
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


@app.get("/agents/status")
async def agents_status(user: str = Depends(verify_auth)):
    """Statut rapide des agents : taille des files, dernier rapport."""
    content   = _load_json(CONTENT_QUEUE)
    prospects = _load_json(PROSPECTS_FILE)
    outreach  = _load_json(OUTREACH_FILE)
    report    = _load_json(DAILY_REPORT)

    last_run = report.get("date", "Jamais") if isinstance(report, dict) else "Jamais"
    return {
        "content_queue":   len(content)   if isinstance(content, list) else 0,
        "prospects":       len(prospects) if isinstance(prospects, list) else 0,
        "outreach_queue":  len(outreach)  if isinstance(outreach, list) else 0,
        "last_daily_run":  last_run,
        "running_tasks":   list(_agent_tasks.keys()),
    }


@app.get("/agents/content")
async def agents_content(user: str = Depends(verify_auth)):
    """Retourne la file de contenu LinkedIn/Twitter."""
    items = _load_json(CONTENT_QUEUE)
    return {"items": items if isinstance(items, list) else [], "count": len(items) if isinstance(items, list) else 0}


@app.get("/agents/prospects")
async def agents_prospects(user: str = Depends(verify_auth)):
    """Retourne les prospects identifiÃ©s."""
    items = _load_json(PROSPECTS_FILE)
    return {"items": items if isinstance(items, list) else [], "count": len(items) if isinstance(items, list) else 0}


@app.get("/agents/outreach")
async def agents_outreach(user: str = Depends(verify_auth)):
    """Retourne les messages d'approche prÃªts."""
    items = _load_json(OUTREACH_FILE)
    return {"items": items if isinstance(items, list) else [], "count": len(items) if isinstance(items, list) else 0}


@app.post("/agents/run/{agent_name}")
async def run_agent(agent_name: str, background_tasks: BackgroundTasks, user: str = Depends(verify_auth)):
    """Lance un agent en arriÃ¨re-plan. agent_name: daily|briefing|publish|scout|closer|plan"""
    valid = {
        "daily", "briefing", "publish", "scout", "closer", "plan", "seo",
        "fatou", "aminata", "modibo", "adama", "djeneba",
    }
    if agent_name not in valid:
        return JSONResponse(status_code=400, content={"error": f"Agent inconnu: {agent_name}"})

    task_id = f"{agent_name}_{int(__import__('time').time())}"
    _agent_tasks[task_id] = {"status": "running", "agent": agent_name, "output": ""}

    def _run():
        try:
            script = str(BASE_DIR / "run_agents.py")
            env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
            result = subprocess.run(
                [sys.executable, script, agent_name],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=120, env=env, cwd=str(BASE_DIR)
            )
            output = result.stdout + result.stderr
            _agent_tasks[task_id] = {"status": "done", "agent": agent_name, "output": output}
        except subprocess.TimeoutExpired:
            _agent_tasks[task_id] = {"status": "timeout", "agent": agent_name, "output": "Timeout (120s)"}
        except Exception as e:
            _agent_tasks[task_id] = {"status": "error", "agent": agent_name, "output": str(e)}
        finally:
            # Nettoie les vieilles tÃ¢ches terminÃ©es (garde les 5 derniÃ¨res)
            done = [(k, v) for k, v in _agent_tasks.items() if v["status"] != "running"]
            for k, _ in done[:-5]:
                _agent_tasks.pop(k, None)

    background_tasks.add_task(_run)
    return {"task_id": task_id, "status": "started", "agent": agent_name}


@app.post("/pipeline/run")
async def run_pipeline(background_tasks: BackgroundTasks, user: str = Depends(verify_auth), mode: str = "full", niche: str = "all"):
    """Lance le pipeline WULIX : SEO â†' Build â†' Deploy Netlify.
    mode: full | seo | build | deploy
    """
    task_id = f"pipeline_{mode}_{int(__import__('time').time())}"
    _agent_tasks[task_id] = {"status": "running", "agent": f"pipeline_{mode}", "output": ""}

    def _run():
        try:
            script = str(BASE_DIR / "pipeline.py")
            env    = {**os.environ, "PYTHONIOENCODING": "utf-8"}
            result = subprocess.run(
                [sys.executable, script, mode, niche],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=300, env=env, cwd=str(BASE_DIR)
            )
            output = result.stdout + result.stderr
            _agent_tasks[task_id] = {"status": "done", "agent": f"pipeline_{mode}", "output": output}
        except subprocess.TimeoutExpired:
            _agent_tasks[task_id] = {"status": "timeout", "agent": "pipeline", "output": "Timeout (300s)"}
        except Exception as e:
            _agent_tasks[task_id] = {"status": "error", "agent": "pipeline", "output": str(e)}
        finally:
            done = [(k, v) for k, v in _agent_tasks.items() if v["status"] != "running"]
            for k, _ in done[:-5]:
                _agent_tasks.pop(k, None)

    background_tasks.add_task(_run)
    return {"task_id": task_id, "status": "started", "mode": mode}


@app.get("/health")
async def health():
    """Health check public (pas d'auth). Utile pour monitoring Uptime Robot etc."""
    import datetime as _dt
    return {
        "status": "ok",
        "service": "aisatou-hud",
        "ts": _dt.datetime.now().isoformat(),
        "version": "2.0"
    }


@app.get("/agents/revenue")
async def agents_revenue(user: str = Depends(verify_auth)):
    """Retourne les dernières données de revenus NDEYE (finance/rapport_YYYYMMDD.json)."""
    finance_dir = AGENTS_DIR / "finance"
    if not finance_dir.exists():
        return {"error": "Dossier finance introuvable — lancer NDEYE d'abord"}

    # Trouve le rapport JSON le plus récent
    reports = sorted(finance_dir.glob("rapport_*.json"), reverse=True)
    if not reports:
        return {"error": "Aucun rapport NDEYE disponible — lancer la tâche daily_report"}

    try:
        data = json.loads(reports[0].read_text(encoding="utf-8"))
        # Calcule la projection mensuelle
        import datetime as _dt
        jour = _dt.date.today().day or 1
        total = data.get("total_revenue", 0)
        projection = round(total / jour * 30, 2)
        obj = 500.0
        pct = round(total / obj * 100, 1) if obj else 0
        return {
            "date":          data.get("date", "—"),
            "total_revenue": total,
            "total_sales":   data.get("total_sales", 0),
            "projection":    projection,
            "objectif":      obj,
            "pct_objectif":  pct,
            "platforms":     data.get("stats", []),
            "source_file":   reports[0].name,
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/pipeline/log")
async def pipeline_log(user: str = Depends(verify_auth)):
    """Retourne les derniers runs du pipeline."""
    log_file = BASE_DIR / "agents" / "pipeline_log.json"
    if log_file.exists():
        try:
            import json as _json
            logs = _json.loads(log_file.read_text(encoding="utf-8"))
            return {"logs": logs[-10:], "count": len(logs)}
        except Exception:
            pass
    return {"logs": [], "count": 0}


@app.get("/agents/recommendations")
async def agents_recommendations(user: str = Depends(verify_auth)):
    """Liste les fichiers de recommandations générés par les agents dans agents/recommandations/."""
    reco_dir = AGENTS_DIR / "recommandations"
    if not reco_dir.exists():
        return {"items": [], "count": 0}

    items = []
    for f in sorted(reco_dir.glob("*.md"), reverse=True)[:20]:
        try:
            parts = f.stem.split("_")  # nom_YYYYMMDD
            agent_name = parts[0].upper() if parts else "?"
            date_str   = parts[1] if len(parts) > 1 else "?"
            # Formater la date
            if len(date_str) == 8:
                date_fmt = f"{date_str[6:8]}/{date_str[4:6]}/{date_str[:4]}"
            else:
                date_fmt = date_str
            preview = f.read_text(encoding="utf-8")[:200].replace("\n", " ").strip()
            items.append({
                "agent":   agent_name,
                "date":    date_fmt,
                "file":    f.name,
                "preview": preview,
            })
        except Exception:
            pass

    return {"items": items, "count": len(items)}


@app.get("/agents/recommendations/{filename}")
async def get_recommendation(filename: str, user: str = Depends(verify_auth)):
    """Retourne le contenu complet d'un fichier de recommandations."""
    reco_dir = AGENTS_DIR / "recommandations"
    # Sécurité : uniquement des .md dans le dossier recommandations
    if not filename.endswith(".md") or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Fichier invalide")
    filepath = reco_dir / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    return {"filename": filename, "content": filepath.read_text(encoding="utf-8")}


@app.get("/agents/blog")
async def agents_blog(user: str = Depends(verify_auth)):
    """Retourne la file des articles SEO gÃ©nÃ©rÃ©s."""
    items = _load_json(BLOG_QUEUE)
    return {"items": items if isinstance(items, list) else [], "count": len(items) if isinstance(items, list) else 0}


@app.get("/agents/task/{task_id}")
async def get_task(task_id: str, user: str = Depends(verify_auth)):
    task = _agent_tasks.get(task_id)
    if not task:
        return JSONResponse(status_code=404, content={"error": "Tache introuvable"})
    return task


# ── Tasks config ──────────────────────────────────────────────────────────────
@app.get("/agents/tasks")
async def get_tasks_config(user: str = Depends(verify_auth)):
    """Retourne la config complete des taches par agent."""
    if TASKS_CONFIG.exists():
        try:
            cfg = json.loads(TASKS_CONFIG.read_text(encoding="utf-8"))
            # Enrichit avec le log des dernieres executions
            log = _load_tasks_log()
            for agent_id, agent_data in cfg.items():
                for task in agent_data.get("tasks", []):
                    key = f"{agent_id}/{task['id']}"
                    task["last_run"]    = log.get(key, {}).get("last_run", None)
                    task["last_status"] = log.get(key, {}).get("status", None)
            return cfg
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    return {}


def _load_tasks_log() -> dict:
    if TASKS_LOG.exists():
        try:
            return json.loads(TASKS_LOG.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save_tasks_log(log: dict):
    TASKS_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


@app.post("/agents/run_task/{agent_id}/{task_id}")
async def run_agent_task(
    agent_id: str, task_id: str,
    background_tasks: BackgroundTasks,
    user: str = Depends(verify_auth)
):
    """Lance une tache specifique d'un agent."""
    if not TASKS_CONFIG.exists():
        return JSONResponse(status_code=404, content={"error": "tasks_config.json introuvable"})

    cfg = json.loads(TASKS_CONFIG.read_text(encoding="utf-8"))
    agent_cfg = cfg.get(agent_id)
    if not agent_cfg:
        return JSONResponse(status_code=404, content={"error": f"Agent inconnu: {agent_id}"})

    task_cfg = next((t for t in agent_cfg.get("tasks", []) if t["id"] == task_id), None)
    if not task_cfg:
        return JSONResponse(status_code=404, content={"error": f"Tache inconnue: {task_id}"})

    cmd_args = task_cfg.get("cmd", [agent_id])
    run_key  = f"{agent_id}/{task_id}"
    full_id  = f"{agent_id}_{task_id}_{int(__import__('time').time())}"
    _agent_tasks[full_id] = {"status": "running", "agent": agent_id, "task": task_id, "output": ""}

    def _run():
        import time as _time
        try:
            script = str(BASE_DIR / "run_agents.py")
            env    = {**os.environ, "PYTHONIOENCODING": "utf-8"}
            result = subprocess.run(
                [sys.executable, script] + cmd_args,
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=180, env=env, cwd=str(BASE_DIR)
            )
            output = result.stdout + result.stderr
            status = "done" if result.returncode == 0 else "error"
            _agent_tasks[full_id] = {"status": status, "agent": agent_id, "task": task_id, "output": output}
        except subprocess.TimeoutExpired:
            status = "timeout"
            _agent_tasks[full_id] = {"status": "timeout", "agent": agent_id, "task": task_id, "output": "Timeout (180s)"}
        except Exception as e:
            status = "error"
            _agent_tasks[full_id] = {"status": "error", "agent": agent_id, "task": task_id, "output": str(e)}
        finally:
            # Sauvegarde le dernier run dans le log
            log = _load_tasks_log()
            log[run_key] = {
                "last_run": __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": _agent_tasks.get(full_id, {}).get("status", "?")
            }
            _save_tasks_log(log)
            # Nettoyage
            done = [(k, v) for k, v in _agent_tasks.items() if v["status"] != "running"]
            for k, _ in done[:-10]:
                _agent_tasks.pop(k, None)

    background_tasks.add_task(_run)
    return {"task_id": full_id, "status": "started", "agent": agent_id, "task": task_id}


async def _broadcast_all(data: dict):
    """Envoie un message JSON à toutes les connexions WebSocket actives."""
    dead = set()
    for ws in list(_ws_pool):
        try:
            await ws.send_json(data)
        except Exception:
            dead.add(ws)
    _ws_pool.difference_update(dead)


async def _voice_state_broadcaster(state: str):
    """Callback injecté dans tts.py pour broadcaster l'état vocal au HUD."""
    await _broadcast_all({"type": "voice_state", "state": state})


# Configure le broadcaster TTS dès le démarrage (si voix dispo)
if VOICE_AVAILABLE:
    set_ws_broadcaster(_voice_state_broadcaster)




async def _morning_briefing(send_fn) -> None:
    """Envoie un briefing automatique : emails + agenda."""
    import asyncio
    try:
        from tools.gmail import gmail_unread, gcal_today
        await asyncio.sleep(0.8)
        parts = []
        try:
            emails = gmail_unread(max_results=5)
            if isinstance(emails, list) and emails:
                parts.append("**" + str(len(emails)) + " email(s) non lu(s) :**")
                for e in emails[:3]:
                    subj = e.get("subject", "(sans objet)")
                    sender = e.get("from", "?").split("<")[0].strip()
                    parts.append("  - *" + sender + "* : " + subj)
                if len(emails) > 3:
                    parts.append("  - ... et " + str(len(emails) - 3) + " autre(s)")
            else:
                parts.append("Aucun email non lu.")
        except Exception:
            parts.append("Gmail non disponible.")
        try:
            events = gcal_today()
            if isinstance(events, list) and events:
                parts.append("")
                parts.append("**Agenda du jour (" + str(len(events)) + " evenement(s)) :**")
                for ev in events[:4]:
                    t = ev.get("start", {}).get("dateTime", ev.get("start", {}).get("date", ""))
                    if "T" in t:
                        t = t.split("T")[1][:5]
                    parts.append("  - " + t + " : " + ev.get("summary", "?"))
            else:
                parts.append("")
                parts.append("Aucun evenement aujourd hui.")
        except Exception:
            parts.append("Calendrier non disponible.")
        date_str = datetime.now().strftime("%d/%m/%Y")
        header = "Bonjour Omar ! Voici ton briefing du " + date_str + " :"
        body = (chr(10)).join(parts)
        greeting = header + chr(10) + chr(10) + body
        await send_fn({"type": "response", "text": greeting})
    except Exception:
        pass


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    global _voice_mode
    await websocket.accept()
    _ws_pool.add(websocket)

    # Briefing auto au demarrage de session
    asyncio.ensure_future(_morning_briefing(
        lambda d: websocket.send_json(d),
        None
    ))

    # ── État par session (multi-utilisateur) â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
    conversation: list = []
    session_model: str = _default_model
    claude_client  = get_claude_client()
    gemini_client  = get_gemini_client()
    groq_client    = get_groq_client()
    use_ollama     = is_ollama_running()

    async def send(data: dict):
        try:
            await websocket.send_json(data)
        except Exception:
            pass

    async def get_ai_response(user_text: str) -> str:
        try:
            if session_model in GEMINI_MODELS and gemini_client:
                return await run_turn_gemini(gemini_client, conversation, user_text, model_name=session_model)
            elif session_model in GROQ_MODELS and groq_client:
                return await run_turn_groq(groq_client, conversation, user_text, model=session_model)
            elif use_ollama:
                return await run_turn_ollama(conversation, user_text, model=session_model)
            elif claude_client:
                return await run_turn_claude(claude_client, conversation, user_text)
            elif groq_client:
                # Fallback Groq si rien d'autre dispo
                return await run_turn_groq(groq_client, conversation, user_text)
            else:
                return "Aucun backend IA disponible (Gemini, Groq, Ollama, Claude)."
        except Exception as e:
            return f"Erreur : {e}"

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            msg_type = data.get("type")
            # Rétrocompatibilité : si pas de type mais un champ "text", traiter comme message
            if not msg_type and data.get("text"):
                msg_type = "message"

            if msg_type == "ping":
                await send({"type": "pong"})
                continue

            if msg_type == "settings":
                new_model = data.get("model", "").strip()
                if new_model:
                    session_model = new_model
                await send({"type": "settings_ok", "model": session_model})
                continue

            # Voix : activer / desactiver
            if msg_type == "voice_toggle":
                if not VOICE_AVAILABLE:
                    await send({"type": "voice_state", "state": "unavailable",
                                "msg": "edge-tts ou pygame non installe"})
                    continue
                _voice_mode = not _voice_mode
                await send({"type": "voice_state",
                            "state": "voice_on" if _voice_mode else "voice_off"})
                continue

            # Voix : arreter la parole
            if msg_type == "stop_audio":
                if VOICE_AVAILABLE:
                    stop_speaking()
                await send({"type": "voice_state", "state": "idle"})
                continue

            # Message texte principal
            if msg_type == "message":
                user_text = data.get("text", "").strip()
                if not user_text:
                    continue

                await send({"type": "thinking"})
                response = await get_ai_response(user_text)
                await send({"type": "response", "text": response})
                _save_exchange(str(id(websocket)), user_text, response)

                # TTS si mode voix actif
                if _voice_mode and VOICE_AVAILABLE:
                    async def _vol_cb(vol: float, _ws=websocket):
                        try:
                            await _ws.send_json({"type": "voice_volume", "volume": vol})
                        except Exception:
                            pass
                    asyncio.ensure_future(tts_speak(response, volume_callback=_vol_cb))

                continue

            # Message vocal (texte transcrit par navigateur)
            if msg_type == "voice_message":
                user_text = data.get("text", "").strip()
                if not user_text:
                    continue
                await send({"type": "thinking"})
                response = await get_ai_response(user_text)
                await send({"type": "response", "text": response})
                _save_exchange(str(id(websocket)), user_text, response)
                if VOICE_AVAILABLE:
                    async def _vol_cb2(vol: float, _ws=websocket):
                        try:
                            await _ws.send_json({"type": "voice_volume", "volume": vol})
                        except Exception:
                            pass
                    asyncio.ensure_future(tts_speak(response, volume_callback=_vol_cb2))

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        _ws_pool.discard(websocket)


# â"€â"€â"€ Lancement â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
def _create_tray_icon(url: str):
    """Cree une icone systray AISATOU avec menu contextuel."""
    try:
        import pystray
        from PIL import Image, ImageDraw
        import keyboard

        def make_icon():
            img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse([2, 2, 62, 62], fill=(124, 58, 237, 255))
            draw.text((20, 18), "A", fill=(255, 255, 255, 255))
            return img

        def open_hud(icon=None, item=None):
            webbrowser.open(url)

        def quit_app(icon, item):
            icon.stop()
            os._exit(0)

        menu = pystray.Menu(
            pystray.MenuItem("Ouvrir AISATOU", open_hud, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quitter", quit_app),
        )
        icon = pystray.Icon("AISATOU", make_icon(), "AISATOU — IA active", menu)

        try:
            keyboard.add_hotkey("ctrl+shift+a", open_hud)
            print("  Raccourci global : Ctrl+Shift+A -> ouvre AISATOU")
        except Exception as e:
            print(f"  [tray] Raccourci non disponible : {e}")

        icon.run()

    except Exception as e:
        print(f"  [tray] Systray non disponible : {e}")


def _run_uvicorn(port: int):
    """Lance uvicorn dans un thread separe."""
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")


def main():
    import threading, time

    port = 7777
    url  = f"http://localhost:{port}"

    print("AISATOU HUD demarre sur " + url)
    print("  Appuie sur Ctrl+C pour arreter.")
    print("  Raccourci global : Ctrl+Shift+A")

    # Lance uvicorn dans un thread (libere le main thread pour le tray)
    server_thread = threading.Thread(target=_run_uvicorn, args=(port,), daemon=True)
    server_thread.start()

    # Ouvre le navigateur apres demarrage
    def open_browser():
        time.sleep(2.0)
        webbrowser.open(url)
    threading.Thread(target=open_browser, daemon=True).start()

    # Lance le raccourci global
    try:
        import keyboard
        keyboard.add_hotkey("ctrl+shift+a", lambda: webbrowser.open(url))
        print("  [OK] Raccourci Ctrl+Shift+A actif")
    except Exception as e:
        print(f"  [warn] Raccourci non disponible : {e}")

    # pystray dans le thread principal (obligatoire sur Windows)
    try:
        import pystray
        from PIL import Image, ImageDraw

        def make_icon():
            img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse([2, 2, 62, 62], fill=(124, 58, 237, 255))
            draw.ellipse([8, 8, 56, 56], fill=(80, 20, 180, 255))
            draw.text((22, 18), "A", fill=(255, 255, 255, 255))
            return img

        def open_hud(icon=None, item=None):
            webbrowser.open(url)

        def quit_app(icon, item):
            icon.stop()
            os._exit(0)

        menu = pystray.Menu(
            pystray.MenuItem("Ouvrir AISATOU", open_hud, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quitter", quit_app),
        )
        icon = pystray.Icon("AISATOU", make_icon(), "AISATOU — IA active", menu)
        print("  [OK] Tray icon actif — clic droit pour menu")
        icon.run()  # bloquant dans le thread principal

    except Exception as e:
        print(f"  [warn] Tray icon non disponible : {e}")
        server_thread.join()  # attend si pas de tray


if __name__ == "__main__":
    main()


