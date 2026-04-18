"""
Base Agent — Classe de base pour tous les agents AISATOU
Chaque agent spécialisé hérite de cette classe.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")


class BaseAgent:
    """Agent IA de base avec backend Gemini (ou Ollama en fallback)."""

    def __init__(self, name: str, role: str, goal: str, backstory: str):
        self.name      = name
        self.role      = role
        self.goal      = goal
        self.backstory = backstory
        self._client   = None
        self._log_path = BASE_DIR / "agents" / "logs" / f"{name.lower()}.log"
        self._log_path.parent.mkdir(exist_ok=True)

    # ── Client Gemini ──────────────────────────────────────────────────────────
    def _get_client(self):
        if self._client:
            return self._client
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=api_key)
                return self._client
            except Exception:
                pass
        return None

    # ── Appel IA ───────────────────────────────────────────────────────────────
    def think(self, prompt: str, max_tokens: int = 2048) -> str:
        """Appelle le LLM avec le prompt donné. Gemini d'abord, Ollama en fallback."""
        system = f"""Tu es {self.name}, un agent IA spécialisé.
Rôle : {self.role}
Objectif : {self.goal}
Contexte : {self.backstory}

Réponds toujours en français. Sois précis, concis et orienté résultat."""

        client = self._get_client()
        if client:
            try:
                from google.genai import types as _gtypes
                resp = client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=prompt,
                    config=_gtypes.GenerateContentConfig(
                        system_instruction=system,
                        temperature=0.8,
                        max_output_tokens=max_tokens,
                    ),
                )
                return resp.text.strip()
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    pass  # fallback Ollama
                else:
                    raise

        # Fallback Ollama
        try:
            import requests
            ollama_model = os.getenv("OLLAMA_FALLBACK_MODEL", "llama3.2:3b")
            payload = {
                "model": ollama_model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": prompt},
                ],
                "stream": False,
                "options": {"temperature": 0.8, "num_predict": max_tokens},
            }
            r = requests.post("http://localhost:11434/api/chat", json=payload, timeout=120)
            r.raise_for_status()
            return r.json()["message"]["content"].strip()
        except Exception as e:
            return f"[Erreur agent {self.name}]: {e}"

    # ── Logs ───────────────────────────────────────────────────────────────────
    def log(self, message: str, level: str = "INFO"):
        ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{ts}] [{level}] [{self.name}] {message}"
        print(entry)
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(entry + "\n")

    # ── Méthode principale à surcharger ───────────────────────────────────────
    def run(self, task: dict) -> dict:
        """Exécute une tâche. À implémenter dans chaque agent."""
        raise NotImplementedError
