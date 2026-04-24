"""
Météo — OpenWeatherMap API (gratuit, 60 req/min, clé requise).
Fournit température, description, alertes pour n'importe quelle ville.

Configurez OPENWEATHER_API_KEY dans .env
Clé gratuite : https://openweathermap.org/api (plan Free, pas de CB)
"""

import os
import requests

OPENWEATHER_URL  = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"
DEFAULT_CITY     = os.getenv("WEATHER_DEFAULT_CITY", "Paris")
DEFAULT_COUNTRY  = os.getenv("WEATHER_DEFAULT_COUNTRY", "fr")

# Descriptions météo FR
_DESCRIPTIONS_FR = {
    "clear sky":           "ciel dégagé",
    "few clouds":          "quelques nuages",
    "scattered clouds":    "nuages épars",
    "broken clouds":       "nuageux",
    "overcast clouds":     "couvert",
    "light rain":          "légère pluie",
    "moderate rain":       "pluie modérée",
    "heavy intensity rain":"forte pluie",
    "light snow":          "légère neige",
    "snow":                "neige",
    "thunderstorm":        "orage",
    "mist":                "brume",
    "fog":                 "brouillard",
    "drizzle":             "bruine",
    "shower rain":         "averses",
}


def _translate(desc: str) -> str:
    return _DESCRIPTIONS_FR.get(desc.lower(), desc)


def _get_api_key() -> str | None:
    key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    return key if key else None


def get_weather(city: str = "") -> str:
    """
    Retourne la météo actuelle pour la ville donnée.

    Args:
        city: Nom de la ville (ex: "Paris", "Lyon,fr"). Utilise DEFAULT_CITY si vide.

    Returns:
        Phrase décrivant la météo.
    """
    api_key = _get_api_key()
    if not api_key:
        return (
            "La météo n'est pas configurée. "
            "Ajoute OPENWEATHER_API_KEY dans le .env "
            "(clé gratuite sur openweathermap.org/api)."
        )

    target = (city.strip() or DEFAULT_CITY)
    if "," not in target:
        target = f"{target},{DEFAULT_COUNTRY}"

    try:
        r = requests.get(
            OPENWEATHER_URL,
            params={"q": target, "appid": api_key, "units": "metric", "lang": "fr"},
            timeout=6,
        )
        r.raise_for_status()
        d = r.json()

        ville   = d.get("name", city)
        pays    = d.get("sys", {}).get("country", "")
        temp    = round(d["main"]["temp"])
        feels   = round(d["main"]["feels_like"])
        desc    = d["weather"][0].get("description", "")
        humid   = d["main"]["humidity"]
        wind    = round(d.get("wind", {}).get("speed", 0) * 3.6)  # m/s → km/h

        return (
            f"À {ville} ({pays}), il fait {temp}°C (ressenti {feels}°C), "
            f"{desc}, humidité {humid}%, vent {wind} km/h."
        )

    except requests.exceptions.HTTPError as e:
        if r.status_code == 404:
            return f"Ville introuvable : {city}. Vérifie l'orthographe."
        return f"Erreur météo ({r.status_code}) : {e}"
    except Exception as e:
        return f"Erreur météo : {e}"


def get_forecast(city: str = "", days: int = 3) -> str:
    """
    Retourne les prévisions météo sur plusieurs jours.

    Args:
        city: Nom de la ville.
        days: Nombre de jours (1-5).

    Returns:
        Résumé des prévisions.
    """
    api_key = _get_api_key()
    if not api_key:
        return "OPENWEATHER_API_KEY manquant dans .env"

    target = (city.strip() or DEFAULT_CITY)
    if "," not in target:
        target = f"{target},{DEFAULT_COUNTRY}"

    days = max(1, min(days, 5))

    try:
        r = requests.get(
            OPENWEATHER_FORECAST,
            params={"q": target, "appid": api_key, "units": "metric", "lang": "fr", "cnt": days * 8},
            timeout=6,
        )
        r.raise_for_status()
        d = r.json()

        ville = d.get("city", {}).get("name", city)
        lines = [f"Prévisions {ville} sur {days} jours :"]

        # Regrouper par jour (1 entrée par jour : midi)
        seen_dates = set()
        for item in d.get("list", []):
            date_str = item["dt_txt"][:10]
            if date_str in seen_dates:
                continue
            if len(seen_dates) >= days:
                break
            seen_dates.add(date_str)
            temp  = round(item["main"]["temp"])
            desc  = item["weather"][0].get("description", "")
            lines.append(f"  {date_str} : {temp}°C, {desc}")

        return "\n".join(lines)

    except Exception as e:
        return f"Erreur prévisions : {e}"


def get_weather_alert(city: str = "") -> str:
    """
    Vérifie les conditions météo extrêmes (orage, forte pluie, neige, canicule).

    Returns:
        Alerte si conditions dangereuses, sinon "Aucune alerte".
    """
    result = get_weather(city)
    danger_keywords = ["orage", "tempête", "forte pluie", "neige", "grêle", "brouillard dense", "canicule"]
    if any(k in result.lower() for k in danger_keywords):
        return f"⚠️ ALERTE MÉTÉO — {result}"
    return f"Aucune alerte — {result}"
