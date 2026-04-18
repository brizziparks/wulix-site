# ── Équipe WULIX ──────────────────────────────────────────────────────────────
# Direction
from .orchestrator import Orchestrator          # AISATOU — DG

# Communication & Content
from .publisher_agent import PublisherAgent     # MARIAMA — Communication
from .seo_writer_agent import SeoWriterAgent    # KOUMBA — SEO Writer

# Business
from .scout_agent import ScoutAgent             # BINTOU — Scout
from .closer_agent import CloserAgent           # SEYDOU — Commercial

# Direction spécialisée
from .fatou_agent import FatouAgent             # FATOU — Finance
from .aminata_agent import AminataAgent         # AMINATA — RH & Missions
from .modibo_agent import ModiboAgent           # MODIBO — Juridique
from .adama_agent import AdamaAgent             # ADAMA — DSI
from .djeneba_agent import DjenebaAgent         # DJENEBA — Stratégie

__all__ = [
    "Orchestrator",
    "PublisherAgent", "SeoWriterAgent",
    "ScoutAgent", "CloserAgent",
    "FatouAgent", "AminataAgent", "ModiboAgent", "AdamaAgent", "DjenebaAgent",
]
