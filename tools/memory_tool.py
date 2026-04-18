"""
Mémoire persistante structurée par catégories.
Stockage JSON + export markdown lisible.
"""

import json
from datetime import datetime
from pathlib import Path


CATEGORIES = {
    "profil":      "Profil & identité de l'utilisateur",
    "preferences": "Préférences & habitudes",
    "projets":     "Projets & objectifs en cours",
    "contacts":    "Contacts importants",
    "rappels":     "Rappels & tâches futures",
    "faits":       "Faits divers mémorisés",
}

def _get_json_path(memory_file) -> Path:
    p = Path(memory_file)
    return p.parent / "memory.json"

def _load_json(memory_file) -> dict:
    path = _get_json_path(memory_file)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {cat: [] for cat in CATEGORIES}

def _save_json(data: dict, memory_file):
    path = _get_json_path(memory_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    _export_markdown(data, memory_file)

def _export_markdown(data: dict, memory_file):
    """Génère facts.md lisible depuis le JSON."""
    lines = ["# Mémoire AISATOU\n"]
    for cat, label in CATEGORIES.items():
        entries = data.get(cat, [])
        if entries:
            lines.append(f"\n## {label}\n")
            for e in entries[-30:]:  # max 30 par catégorie
                lines.append(f"- [{e['date']}] {e['fact']}\n")
    Path(memory_file).write_text("".join(lines), encoding="utf-8")


def load_memory(memory_file) -> str:
    """Charge un résumé de la mémoire pour le prompt système."""
    data = _load_json(memory_file)
    lines = []
    for cat, label in CATEGORIES.items():
        entries = data.get(cat, [])
        if entries:
            lines.append(f"\n[{label.upper()}]")
            for e in entries[-5:]:  # 5 plus récents par catégorie dans le prompt
                lines.append(f"  - {e['fact']}")
    return "\n".join(lines) if lines else ""


def remember(fact: str, memory_file, category: str = "faits") -> str:
    """Sauvegarde un fait dans la catégorie appropriée."""
    if category not in CATEGORIES:
        category = _auto_categorize(fact)

    data = _load_json(memory_file)
    if cat_list := data.get(category):
        # Éviter les doublons proches
        if any(e["fact"].lower() == fact.lower() for e in cat_list[-10:]):
            return f"Déjà mémorisé : {fact}"

    entry = {
        "fact": fact,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "category": category,
    }
    data.setdefault(category, []).append(entry)
    _save_json(data, memory_file)
    return f"Mémorisé [{CATEGORIES.get(category, category)}] : {fact}"


def recall(query: str, memory_file) -> str:
    """Recherche dans la mémoire. Sans query = tout afficher."""
    data = _load_json(memory_file)

    if not query:
        # Résumé complet
        lines = []
        for cat, label in CATEGORIES.items():
            entries = data.get(cat, [])
            if entries:
                lines.append(f"\n{label.upper()} ({len(entries)} entrées) :")
                for e in entries[-8:]:
                    lines.append(f"  • {e['fact']}  [{e['date']}]")
        return "\n".join(lines) if lines else "Aucune mémoire."

    # Recherche par mot-clé
    query_lower = query.lower()
    results = []
    for cat, entries in data.items():
        for e in entries:
            if query_lower in e["fact"].lower():
                results.append(f"[{CATEGORIES.get(cat,cat)}] {e['fact']}  ({e['date']})")

    if results:
        return "\n".join(results)
    return f"Aucun souvenir trouvé pour : {query}"


def forget(query: str, memory_file) -> str:
    """Supprime les entrées contenant le mot-clé."""
    data = _load_json(memory_file)
    query_lower = query.lower()
    removed = 0
    for cat in data:
        before = len(data[cat])
        data[cat] = [e for e in data[cat] if query_lower not in e["fact"].lower()]
        removed += before - len(data[cat])
    if removed:
        _save_json(data, memory_file)
        return f"{removed} souvenir(s) supprimé(s)."
    return f"Rien trouvé à supprimer pour : {query}"


def _auto_categorize(fact: str) -> str:
    """Détecte automatiquement la catégorie d'un fait."""
    f = fact.lower()
    if any(w in f for w in ["je m'appelle", "j'habite", "mon nom", "je suis", "j'ai", "né", "nee"]):
        return "profil"
    if any(w in f for w in ["j'aime", "je préfère", "j'utilise", "mon modèle", "ma couleur", "favori"]):
        return "preferences"
    if any(w in f for w in ["projet", "travail", "objectif", "but", "démarrer", "créer", "développer"]):
        return "projets"
    if any(w in f for w in ["contact", "email", "téléphone", "collègue", "ami", "famille", "patron"]):
        return "contacts"
    if any(w in f for w in ["rappel", "penser", "oublier", "demain", "lundi", "rendez-vous", "deadline"]):
        return "rappels"
    return "faits"
