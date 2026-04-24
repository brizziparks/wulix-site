"""
Résolveur mathématique offline — calculs instantanés sans appel API.
Inspiré de JARVIS (techenclair.fr) resoudre_math_localement().

Gère : opérations de base, puissances, racines, %, conversions courantes.
"""

import math
import re


# ── Préprocessing ─────────────────────────────────────────────────────────────

_WORD_TO_OP = [
    (r'\bfois\b',             '*'),
    (r'\bmultiplié par\b',    '*'),
    (r'\bdivisé par\b',       '/'),
    (r'\bdivisé\b',           '/'),
    (r'\bsur\b',              '/'),
    (r'\bplus\b',             '+'),
    (r'\bmoins\b',            '-'),
    (r'\bpuissance\b',        '**'),
    (r'\bau carré\b',         '**2'),
    (r'\bau cube\b',          '**3'),
    (r'\bmodulo\b',           '%'),
    (r'\bmod\b',              '%'),
]

_PREFIXES = [
    "combien font", "combien fait", "calcule", "résous", "calculer",
    "quel est le résultat de", "quel est", "donne-moi"
]

_SAFE_DICT = {
    "__builtins__": None,
    "sqrt":  math.sqrt,
    "cbrt":  lambda x: x ** (1/3),
    "pow":   math.pow,
    "abs":   abs,
    "round": round,
    "pi":    math.pi,
    "e":     math.e,
    "inf":   math.inf,
    "log":   math.log,
    "log10": math.log10,
    "sin":   math.sin,
    "cos":   math.cos,
    "tan":   math.tan,
}


def _preprocess(text: str) -> str:
    """Normalise le texte en expression mathématique évaluable."""
    t = text.lower().strip().rstrip("?!.")

    # Retirer les préfixes conversationnels
    for prefix in _PREFIXES:
        if t.startswith(prefix):
            t = t[len(prefix):].strip()
            break

    # Remplacer les mots par des opérateurs
    for pattern, op in _WORD_TO_OP:
        t = re.sub(pattern, op, t)

    # Racine carrée : "racine de 144" ou "racine carrée de 144"
    t = re.sub(r'racine\s+(?:carrée\s+)?de\s+', 'sqrt(', t)
    if 'sqrt(' in t and ')' not in t.split('sqrt(')[-1]:
        t += ')'

    # Pourcentage : "20% de 150"
    t = re.sub(r'(\d+(?:\.\d+)?)\s*%\s*de\s*(\d+(?:\.\d+)?)',
               r'(\1/100)*\2', t)

    # Virgule décimale → point
    t = re.sub(r'(\d),(\d)', r'\1.\2', t)

    return t


def solve(expression: str) -> str:
    """
    Résout une expression mathématique en français ou en notation standard.

    Args:
        expression: Texte brut (ex: "combien font 3 fois 12", "racine de 144", "20% de 150")

    Returns:
        Phrase avec le résultat, ou None si non résolvable localement.
    """
    if not expression or not expression.strip():
        return None

    processed = _preprocess(expression)

    # Extraire uniquement les caractères autorisés dans l'expression
    expr = re.sub(r'[^0-9+\-*/.**()%,. sqrt cbrt pow abs round log sin cos tan pi e]', '', processed).strip()

    if not expr or not any(c.isdigit() for c in expr):
        return None

    try:
        result = eval(expr, {"__builtins__": None}, _SAFE_DICT)

        # Formater le résultat
        if isinstance(result, (int, float)):
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 6)
                # Enlever les zéros inutiles
                result = f"{result:.6f}".rstrip('0').rstrip('.')
                try:
                    result = int(result) if '.' not in result else float(result)
                except Exception:
                    pass

        # Construire une phrase lisible
        # Nettoyer l'expression pour la voix
        expr_clean = (
            expr
            .replace("**", " puissance ")
            .replace("sqrt(", "racine de ")
            .replace("*", " fois ")
            .replace("/", " divisé par ")
            .replace("+", " plus ")
            .replace("-", " moins ")
            .replace("(", "").replace(")", "")
            .strip()
        )
        return f"{expr_clean} = {result}"

    except ZeroDivisionError:
        return "Division par zéro impossible."
    except Exception:
        return None


def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convertit des unités courantes.

    Supporte : km/miles, kg/lbs, celsius/fahrenheit, litres/gallons
    """
    conversions = {
        ("km", "miles"):    lambda v: round(v * 0.621371, 4),
        ("miles", "km"):    lambda v: round(v * 1.60934, 4),
        ("kg", "lbs"):      lambda v: round(v * 2.20462, 4),
        ("lbs", "kg"):      lambda v: round(v * 0.453592, 4),
        ("c", "f"):         lambda v: round(v * 9/5 + 32, 2),
        ("celsius", "fahrenheit"): lambda v: round(v * 9/5 + 32, 2),
        ("f", "c"):         lambda v: round((v - 32) * 5/9, 2),
        ("fahrenheit", "celsius"): lambda v: round((v - 32) * 5/9, 2),
        ("l", "gallons"):   lambda v: round(v * 0.264172, 4),
        ("gallons", "l"):   lambda v: round(v * 3.78541, 4),
        ("m", "ft"):        lambda v: round(v * 3.28084, 4),
        ("ft", "m"):        lambda v: round(v * 0.3048, 4),
        ("m", "feet"):      lambda v: round(v * 3.28084, 4),
    }
    key = (from_unit.lower().strip(), to_unit.lower().strip())
    fn = conversions.get(key)
    if fn:
        result = fn(value)
        return f"{value} {from_unit} = {result} {to_unit}"
    return f"Conversion {from_unit} → {to_unit} non disponible."
