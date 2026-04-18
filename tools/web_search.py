"""Web search tool using DuckDuckGo (no API key required)."""

from duckduckgo_search import DDGS


def search_web(query: str, max_results: int = 5) -> str:
    """Search the web and return formatted results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return f"No results found for: {query}"

        lines = [f"Search results for: {query}\n"]
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. {r.get('title', 'No title')}")
            lines.append(f"   {r.get('body', '')[:200]}")
            lines.append(f"   Source: {r.get('href', '')}\n")

        return "\n".join(lines)

    except Exception as e:
        return f"Search error: {str(e)}"
