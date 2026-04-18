#!/usr/bin/env python3
"""
BINTOU + MARIAMA — Recherche nom de marque
Trouve un nom d'entreprise original, disponible et percutant
"""

import sys
import json
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from agents.base_agent import BaseAgent

class BrandResearcher(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Bintou+Mariama",
            role="Experte en branding, naming et positionnement marketing",
            goal="Trouver le nom de marque parfait pour une agence IA française",
            backstory="""Tu es une experte en naming d'entreprises tech/IA en France.
Tu connais les règles : nom mémorable, court (2 syllabes idéal), prononçable en français et en anglais,
extension .fr et .com disponibles, pas de marque déposée existante, fort en SEO.
Le projet : agence d'automatisation IA pour PME et freelances français. Services : agents Python,
automatisation workflow, contenu LinkedIn, site SEO automatique.
Fondateur : Omar Sylla, développeur Python/IA basé en France."""
        )

def main():
    print("\n[BINTOU] Demarrage — recherche nom de marque")
    print("[MARIAMA] Co-pilote branding actif")
    print("-" * 50)

    agent = BrandResearcher()

    # ETAPE 1 : Génération de 20 noms candidats
    print("\n[1/4] Generation de 20 noms candidats...")
    prompt_noms = """Génère 20 noms d'entreprise originaux pour une agence d'automatisation IA française.

CONTRAINTES ABSOLUES :
- Maximum 2-3 syllabes
- Prononçable facilement en français ET en anglais
- Ne commence pas par "AI" ou "Bot" (trop générique)
- Pas de tirets, pas de chiffres
- Évite les noms déjà connus (WULIX, Nexflow, Zapier, Make, n8n)
- Idéalement : évoque vitesse, intelligence, flux, automatisation, Afrique/modernité

CATÉGORIES à explorer :
- Mots fusion (ex: 2 mots fusionnés)
- Mots inventés sonores
- Racines latines/grecques réinterprétées
- Inspiration afrofuturiste (prénom ou mot africain modernisé)
- Onomatopées tech

Pour chaque nom, donne :
NOM | Signification/inspiration | Score mémorisation (1-10) | Extension probable libre

Format tableau markdown."""

    noms_raw = agent.think(prompt_noms, max_tokens=1200)
    print(noms_raw)

    # ETAPE 2 : Top 5 sélection
    print("\n[2/4] Selection du TOP 5...")
    prompt_top5 = f"""Parmi ces noms proposés :
{noms_raw}

Sélectionne le TOP 5 selon ces critères pondérés :
- Mémorabilité (30%)
- Disponibilité probable .fr + .com (25%)
- Cohérence avec IA/automatisation (20%)
- Originalité (15%)
- Facilité de prononciation internationale (10%)

Pour chaque finaliste, donne :
1. Le nom
2. Tagline en 5 mots max
3. Pourquoi ce nom gagne
4. Risques potentiels
5. Adresse email suggérée (contact@nom.fr)

Format : 5 fiches claires et séparées."""

    top5 = agent.think(prompt_top5, max_tokens=1000)
    print(top5)

    # ETAPE 3 : Analyse marché
    print("\n[3/4] Analyse concurrence et positionnement...")
    prompt_marche = """Pour une agence IA française ciblant PME/freelances :

1. CONCURRENTS DIRECTS à analyser (noms + positionnement) :
   - Zapier, Make, n8n (outils)
   - Agences IA françaises émergentes
   - Freelances sur Malt/Fiverr en automatisation Python

2. POSITIONNEMENT RECOMMANDÉ :
   - Comment se différencier du marché ?
   - Quel angle unique (prix, service, technologie, culture) ?

3. BESOINS pour avancer :
   - Ce dont on a besoin pour créer la marque complète
   - Budget estimé (domaine, logo, etc.)
   - Timeline réaliste

Sois concise et actionnable."""

    marche = agent.think(prompt_marche, max_tokens=800)
    print(marche)

    # ETAPE 4 : Besoins des agents
    print("\n[4/4] Rapport des besoins — toute l'equipe...")
    prompt_besoins = """Tu represents toute l'equipe WULIX (10 agents IA).
Chaque agent doit indiquer ce dont il a besoin pour avancer sur sa mission.

Format pour chaque agent :
AGENT (role) — BESOIN PRINCIPAL — BLOCAGE ACTUEL

Agents :
- BINTOU (Scout/Prospection) : cherche des clients
- MARIAMA (Comms) : gère contenu LinkedIn/Twitter
- SEYDOU (Closer) : répond aux prospects
- KOUMBA (SEO) : écrit articles de blog
- FATOU (Finance) : suit les revenus
- AMINATA (RH) : gère l'équipe
- MODIBO (Juridique) : documents légaux
- ADAMA (DSI) : sécurité et infra
- DJENEBA (Stratégie) : plan trimestriel
- AISATOU (DG) : coordination générale

Contexte actuel : site en ligne sur Netlify, nom de domaine non acheté, 0 euro de revenus, profils sociaux non créés, SIRET inconnu."""

    besoins = agent.think(prompt_besoins, max_tokens=1000)
    print(besoins)

    # Sauvegarde
    output = {
        "date": datetime.now().isoformat(),
        "agents": "Bintou + Mariama",
        "noms_generes": noms_raw,
        "top5": top5,
        "analyse_marche": marche,
        "besoins_equipe": besoins
    }

    out_file = BASE_DIR / "agents" / "brand_research.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Rapport sauvegarde : {out_file}")

if __name__ == "__main__":
    main()
