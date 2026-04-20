#!/usr/bin/env python3
"""
AISATOU HUD â€" Interface Iron Man
Serveur FastAPI + WebSocket + interface web holographique
"""

import asyncio
import json
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
    OLLAMA_MODEL, execute_tool,
)

# Modèle par défaut — lit AISATOU_MODEL depuis .env
_default_model = OLLAMA_MODEL

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


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()

    # â"€â"€ Ã‰tat par session (multi-utilisateur) â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
    conversation: list = []
    session_model: str = _default_model
    claude_client  = get_claude_client()
    gemini_client  = get_gemini_client()
    use_ollama     = is_ollama_running()

    async def send(data: dict):
        try:
            await websocket.send_json(data)
        except Exception:
            pass

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            msg_type = data.get("type")

            if msg_type == "ping":
                await send({"type": "pong"})
                continue

            if msg_type == "settings":
                new_model = data.get("model", "").strip()
                if new_model:
                    session_model = new_model  # modÃ¨le propre Ã  cette session
                await send({"type": "settings_ok", "model": session_model})
                continue

            if msg_type == "message":
                user_text = data.get("text", "").strip()
                if not user_text:
                    continue

                await send({"type": "thinking"})

                try:
                    if session_model in GEMINI_MODELS and gemini_client:
                        response = await run_turn_gemini(gemini_client, conversation, user_text, model_name=session_model)
                    elif use_ollama:
                        response = await run_turn_ollama(conversation, user_text, model=session_model)
                    elif claude_client:
                        response = await run_turn_claude(claude_client, conversation, user_text)
                    else:
                        response = "Aucun backend IA disponible."
                except Exception as e:
                    response = f"Erreur : {e}"

                await send({"type": "response", "text": response})

    except WebSocketDisconnect:
        pass
    except Exception:
        pass


# â"€â"€â"€ Lancement â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
def main():
    import threading, time

    port = 7777
    url  = f"http://localhost:{port}"

    print(f"\n  AISATOU HUD demarre sur {url}")
    print("  Appuie sur Ctrl+C pour arreter.\n")

    # Ouvre le navigateur dans un thread sÃ©parÃ© pour Ã©viter les conflits d'event loop
    def open_browser():
        time.sleep(1.5)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")


if __name__ == "__main__":
    main()


