#!/usr/bin/env python3
"""
WULIX — Équipe IA | CLI

  AISATOU (DG)       daily | briefing | plan
  MARIAMA (Comms)    publish
  BINTOU (Scout)     scout
  SEYDOU (Closer)    closer <msg>
  KOUMBA (SEO)       seo | seo batch 3 | seo niche tutos-ia
  FATOU (Finance)    fatou | fatou forecast
  AMINATA (RH)       aminata | aminata onboarding
  MODIBO (Juridique) modibo | modibo cgv | modibo contrat
  ADAMA (DSI)        adama | adama audit | adama roadmap
  DJENEBA (Stratégie)djeneba | djeneba kpis | djeneba opportunities
"""

import sys
import json
import os
from pathlib import Path

# Fix encodage console Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from agents import (
    Orchestrator, PublisherAgent, ScoutAgent, CloserAgent, SeoWriterAgent,
    FatouAgent, AminataAgent, ModiboAgent, AdamaAgent, DjenebaAgent,
)


def print_result(result: dict, verbose: bool = True):
    """Affiche le résultat de manière lisible."""
    print("\n" + "="*60)

    if "briefing" in result:
        briefing = result.get("briefing", result)
        if isinstance(briefing, dict):
            briefing = briefing.get("briefing", str(briefing))
        print(briefing)

    elif "results" in result:
        r = result["results"]
        if "briefing" in r:
            print(r["briefing"])
            print()
        if "publisher" in r:
            items = r["publisher"].get("results", [])
            if items:
                print(f"\n📝 POST LINKEDIN GÉNÉRÉ :")
                print("-"*40)
                print(items[0].get("content", ""))
        if "scout" in r:
            report = r["scout"].get("report", {})
            if isinstance(report, dict):
                print(f"\n🔍 OPPORTUNITÉS :")
                print(json.dumps(report, ensure_ascii=False, indent=2)[:500] + "...")

    elif "plan" in result:
        print("📅 PLAN DE LA SEMAINE :")
        print(json.dumps(result["plan"], ensure_ascii=False, indent=2))

    elif "message" in result:
        print("💬 MESSAGE D'APPROCHE :")
        print(result["message"])

    elif "response" in result:
        print("✉️ RÉPONSE FIVERR :")
        print(result["response"])

    else:
        print(json.dumps(result, ensure_ascii=False, indent=2)[:1000])

    print("="*60)


def main():
    args = sys.argv[1:]
    cmd  = args[0] if args else "daily"

    print(f"\n🤖 WULIX Agents — {cmd.upper()}")

    if cmd == "daily":
        boss = Orchestrator()
        result = boss.run({"mode": "daily"})
        print_result(result)

    elif cmd == "briefing":
        boss = Orchestrator()
        result = boss.run({"mode": "briefing"})
        print_result(result)

    elif cmd == "plan":
        boss = Orchestrator()
        result = boss.run({"mode": "plan"})
        print_result(result)

    elif cmd == "publish":
        platform = args[1] if len(args) > 1 else "linkedin"
        mode     = args[2] if len(args) > 2 else "single"
        agent = PublisherAgent()
        result = agent.run({"mode": mode, "platform": platform})
        items = result.get("results", [])
        for item in items:
            print(f"\n📝 [{item['platform'].upper()}] — {item['topic']}")
            print("-"*50)
            content = item.get("content", "")
            if isinstance(content, list):
                for tweet in content:
                    print(tweet)
                    print()
            else:
                print(content)

    elif cmd == "scout":
        mode = args[1] if len(args) > 1 else "opportunities"
        agent = ScoutAgent()
        result = agent.run({"mode": mode})
        print_result(result)

    elif cmd == "closer":
        if len(args) > 1:
            msg = " ".join(args[1:])
            agent = CloserAgent()
            result = agent.run({"mode": "fiverr", "data": {"client_message": msg}})
        else:
            # Mode LinkedIn par défaut
            agent = CloserAgent()
            result = agent.run({
                "mode": "linkedin",
                "data": {"secteur": "startup", "probleme": "automatisation", "contexte": ""}
            })
        print_result(result)

    elif cmd == "profiles":
        agent = PublisherAgent()
        result = agent.setup_profiles()
        print("\n" + "="*60)
        print("✅ PROFILS GÉNÉRÉS — agents/profiles_setup.json")
        print("="*60)
        import json as _j
        for platform, data in result.items():
            if platform == "generated_at":
                continue
            print(f"\n{'─'*40}")
            print(f"  {platform.upper()}")
            print('─'*40)
            print(_j.dumps(data, ensure_ascii=False, indent=2)[:800])

    elif cmd == "weekly":
        agent = PublisherAgent()
        result = agent.run({"mode": "weekly", "platform": "linkedin"})
        print(f"\n✅ {result['items_generated']} posts générés dans agents/content_queue.json")

    elif cmd == "seo":
        agent = SeoWriterAgent()
        # Modes : seo | seo batch 3 | seo niche tutos-ia | seo niche automatisation
        if len(args) > 1 and args[1] == "batch":
            count = int(args[2]) if len(args) > 2 else 3
            result = agent.run({"mode": "batch", "niche": "all", "count": count})
        elif len(args) > 1 and args[1] == "niche":
            niche = args[2] if len(args) > 2 else "all"
            result = agent.run({"mode": "single", "niche": niche})
        else:
            result = agent.run({"mode": "single", "niche": "all"})

        articles = result.get("results", [])
        print(f"\n📝 SEO Writer — {result.get('articles_generated', 0)} article(s) généré(s)")
        for art in articles:
            if art["status"] == "success":
                print(f"  ✅ [{art['niche']}] {art['title']} ({art['word_count']} mots)")
                print(f"     → {art['file']}")
            else:
                print(f"  ❌ {art['slug']} — {art.get('error', '?')}")

    # ── Direction spécialisée ────────────────────────────────────────────────
    elif cmd == "fatou":
        mode = args[1] if len(args) > 1 else "monthly_report"
        agent = FatouAgent()
        result = agent.run({"mode": mode, "context": {}})
        content = result.get("report", {}).get("rapport") or result.get("forecast") or result.get("invoice", {}).get("content", "")
        print(f"\n💰 FATOU (Finance) — {mode.upper()}")
        print("-"*50)
        print(content[:1000] if content else json.dumps(result, ensure_ascii=False, indent=2)[:500])

    elif cmd == "aminata":
        mode = args[1] if len(args) > 1 else "weekly_report"
        agent = AminataAgent()
        result = agent.run({"mode": mode, "context": {}})
        content = result.get("report") or result.get("content", "")
        print(f"\n👥 AMINATA (RH) — {mode.upper()}")
        print("-"*50)
        print(content[:1000] if content else json.dumps(result, ensure_ascii=False, indent=2)[:500])

    elif cmd == "modibo":
        mode = args[1] if len(args) > 1 else "mentions"
        agent = ModiboAgent()
        result = agent.run({"mode": mode})
        content = result.get("content") or result.get("reponse", "")
        print(f"\n⚖️ MODIBO (Juridique) — {mode.upper()}")
        print("-"*50)
        print(content[:1000] if content else json.dumps(result, ensure_ascii=False, indent=2)[:500])

    elif cmd == "adama":
        mode    = args[1] if len(args) > 1 else "veille"
        domaine = args[2] if len(args) > 2 else "ia-automatisation"
        agent   = AdamaAgent()
        result  = agent.run({"mode": mode, "domaine": domaine})
        content = result.get("content", "")
        print(f"\n🖥️ ADAMA (DSI) — {mode.upper()}")
        print("-"*50)
        print(content[:1000] if content else json.dumps(result, ensure_ascii=False, indent=2)[:500])

    elif cmd == "djeneba":
        mode     = args[1] if len(args) > 1 else "quarterly_plan"
        audience = args[2] if len(args) > 2 else "pme"
        agent    = DjenebaAgent()
        result   = agent.run({"mode": mode, "audience": audience})
        content  = result.get("content", "")
        print(f"\n📊 DJENEBA (Stratégie) — {mode.upper()}")
        print("-"*50)
        print(content[:1000] if content else json.dumps(result, ensure_ascii=False, indent=2)[:500])

    elif cmd == "pipeline":
        mode  = args[1] if len(args) > 1 else "full"
        niche = args[2] if len(args) > 2 else "all"
        import importlib.util, pathlib
        spec   = importlib.util.spec_from_file_location("pipeline", BASE_DIR / "pipeline.py")
        mod    = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.run_pipeline(mode, niche)

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
