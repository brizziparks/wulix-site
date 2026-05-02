"""Fix mojibake dans blog.html - decode cp1252"""
from pathlib import Path
import sys

blog = Path(r"C:\Users\USER\.claude\projects\projet jarvis\ui\blog.html")
content = blog.read_text(encoding="utf-8")

def safe_print(msg):
    sys.stdout.buffer.write((msg + "\n").encode("utf-8", "replace"))

def mojibake_cp1252(char):
    try:
        return char.encode("utf-8").decode("cp1252")
    except Exception:
        return None

chars = [
    "\xe9", "\xe8", "\xea", "\xeb",
    "\xe0", "\xe2",
    "\xf9", "\xfb",
    "\xee", "\xef",
    "\xf4",
    "\xe7",
    "\xc0", "\xc9",
    "œ",  # oe
    "’",  # '
    "“",  # "
    "”",  # "
    "‘",  # '
    "…",  # ...
    "–",  # en-dash
    "—",  # em-dash
    "→",  # ->
    "€",  # euro
]

count = 0
for c in chars:
    moji = mojibake_cp1252(c)
    if moji and moji != c and moji in content:
        n = content.count(moji)
        content = content.replace(moji, c)
        count += n
        safe_print("fixed " + str(n) + "x: " + repr(moji) + " -> " + c)

blog.write_text(content, encoding="utf-8")
safe_print("\n[OK] " + str(count) + " corrections dans blog.html")
