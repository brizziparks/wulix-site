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

    # ── Recommandations ────────────────────────────────────────────────────────
    def recommend(self, context: str = "") -> str:
        """Génère un rapport de recommandations hebdomadaires dans le domaine de l'agent.
        Sauvegardé dans agents/recommandations/{name}_{date}.md"""
        prompt = f"""En tant que {self.name} ({self.role}), génère un rapport de recommandations concret pour WULIX cette semaine.

WULIX = agence IA solo (Omar Sylla, France). Stack : Python 3.11, FastAPI, Gemini API, Ollama, HTML/CSS/JS, Cloudflare Pages.
Revenus actuels : 0-50€/mois. Objectif : 500€/mois (freelance) + 300€/mois (SEO passif).
{f'Contexte additionnel : {context}' if context else ''}

Structure du rapport (markdown) :

## Analyse
2-3 constats clés dans ton domaine {self.role} cette semaine.

## Recommandations prioritaires

### 1. [Titre action — IMPACT FORT]
- **Quoi** : description précise (2 phrases)
- **Comment** : étapes concrètes pour WULIX
- **Effort** : XS / S / M / L
- **Résultat attendu** : métrique ou livrable précis

### 2. [Titre action — IMPACT MOYEN]
(même format)

### 3. [Titre action — QUICK WIN < 1h]
(même format)

## ⚠ Alerte (si urgent)
Un risque ou opportunité à saisir dans les 48h. Sinon, écrire "RAS".

---
*Rapport {self.name} · {__import__('datetime').date.today().strftime('%d/%m/%Y')}*

IMPORTANT : toutes les recommandations doivent être applicables MAINTENANT sur le système WULIX existant. Pas de théorie, pas de suggestions qui nécessitent un budget ou une équipe."""

        return self.think(prompt, max_tokens=900)

    def save_recommendation(self, content: str) -> "Path":
        """Sauvegarde la recommandation dans agents/recommandations/."""
        reco_dir = BASE_DIR / "agents" / "recommandations"
        reco_dir.mkdir(exist_ok=True)
        date_str  = __import__('datetime').date.today().strftime("%Y%m%d")
        filepath  = reco_dir / f"{self.name.lower()}_{date_str}.md"
        filepath.write_text(content, encoding="utf-8")
        return filepath

    # ── Méthode principale à surcharger ───────────────────────────────────────
    def run(self, task: dict) -> dict:
        """Exécute une tâche. À implémenter dans chaque agent."""
        raise NotImplementedError
