"""File system tools."""

import os
from pathlib import Path


def read_file(path: str) -> str:
    """Read contents of a file."""
    try:
        p = Path(os.path.expandvars(path))
        if not p.exists():
            return f"File not found: {path}"
        if p.stat().st_size > 100_000:
            return f"File too large to read (>{p.stat().st_size // 1000}KB)"
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    try:
        p = Path(os.path.expandvars(path))
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Written {len(content)} characters to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def list_files(path: str) -> str:
    """List files in a directory."""
    try:
        p = Path(os.path.expandvars(path))
        if not p.exists():
            return f"Directory not found: {path}"
        if not p.is_dir():
            return f"Not a directory: {path}"

        items = []
        for item in sorted(p.iterdir()):
            prefix = "📁" if item.is_dir() else "📄"
            size = "" if item.is_dir() else f" ({item.stat().st_size // 1024}KB)"
            items.append(f"{prefix} {item.name}{size}")

        if not items:
            return f"Empty directory: {path}"
        return f"Contents of {path}:\n" + "\n".join(items)
    except Exception as e:
        return f"Error listing files: {str(e)}"
