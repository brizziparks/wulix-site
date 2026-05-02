#!/bin/bash
# Setup les routines cron Hermes pour WULIX
# A lancer dans WSL2 Ubuntu : bash /mnt/c/.../setup_hermes_cron.sh

set -e
HERMES=/usr/local/bin/hermes
WORKDIR=/root/wulix-cron

mkdir -p "$WORKDIR"

# Routine 1 : Idées d'apps validées (chaque jour à 6h)
PROMPT_IDEES='Recherche aujourd hui sur Reddit (r/SaaS, r/EntrepreneurRideAlong, r/SideProject, r/automate), Hacker News (news.ycombinator.com), et Product Hunt les 5 problemes les plus recents et mentionnes par des freelances ou PME qui pourraient etre resolus par une app simple ou un script Python.

Pour chaque idee, donne :
1. Le probleme expose (1 ligne)
2. Le pain point (1 phrase)
3. Une solution technique en 2 lignes
4. Source / lien direct
5. Difficulte estimee (Facile / Moyen / Difficile)
6. Potentiel revenue (Faible / Moyen / Eleve)

Format : markdown propre.
Sauvegarde dans /root/wulix-cron/idees_apps_du_jour.md (ecrase le precedent).
Ajoute la date du jour en haut.'

$HERMES cron create "0 6 * * *" "$PROMPT_IDEES" \
  --name wulix-idees-apps \
  --deliver local \
  --workdir "$WORKDIR"

echo "[OK] Routine 1 cree : wulix-idees-apps (chaque jour 6h)"

# Routine 2 : Veille concurrentielle WULIX (3x par semaine)
PROMPT_VEILLE='Veille concurrentielle pour WULIX (agence automatisation IA freelance/PME).

Recherche cette semaine :
1. Nouveaux outils no-code/IA lances (Lindy, Sim Studio, Make, n8n, Zapier alternatives)
2. Articles sur la creation de produits digitaux a moins de 50 EUR
3. Tendances Reddit r/digitalnomad, r/freelance, r/Upwork
4. Threads Twitter/X sur lautomatisation pour solo founders

Format un rapport markdown avec : titre, 3 sections (Outils / Strategies / Tendances), 5 bullets max par section, sources.
Sauvegarde dans /root/wulix-cron/veille_hebdo.md (ajoute - ne remplace pas).'

$HERMES cron create "0 7 * * 1,3,5" "$PROMPT_VEILLE" \
  --name wulix-veille-hebdo \
  --deliver local \
  --workdir "$WORKDIR"

echo "[OK] Routine 2 cree : wulix-veille-hebdo (lun/mer/ven 7h)"

# Liste les routines
echo ""
echo "=== Routines actives ==="
$HERMES cron list

echo ""
echo "[OK] Setup termine. Logs : $WORKDIR/"
