# 👥 Équipe WULIX — 14 Agents IA

## Agents Opérationnels

| Agent | Fichier | Rôle | Fréquence |
|-------|---------|------|-----------|
| **MARIAMA** | publisher_agent.py | Posts LinkedIn | Lundi 9h (Make.com) |
| **FATOU** | fatou_agent.py | Finance & projections | Vendredi 18h |
| **MODIBO** | modibo_agent.py | CGV, mentions légales | Sur demande |
| **BINTOU** | scout_agent.py | Opportunités clients | Mercredi 9h |
| **DJENEBA** | djeneba_agent.py | Stratégie & KPIs | 1er du mois |
| **AMINATA** | aminata_agent.py | RH & rapports hebdo | Vendredi 17h |
| **ADAMA** | adama_agent.py | Audit technique | Dimanche 2h |
| **KOUMBA** | seo_writer_agent.py | Articles SEO | Sur demande |

## Nouveaux Agents (Avril 2026)

| Agent | Fichier | Rôle | Fréquence |
|-------|---------|------|-----------|
| **SEYDOU** | seydou_agent.py | Twitter/X + calendrier éditorial | Mar/Jeu 10h30 |
| **IBRAHIMA** | ibrahima_agent.py | Design : covers, visuals, avatar | Sur demande |
| **ROKHAYA** | rokhaya_agent.py | CRM : emails acheteurs + follow-up | Quotidien 9h |
| **SAMBA** | samba_agent.py | SEO continu : 1 article/semaine | Lundi 10h |
| **LAMINE** | lamine_agent.py | Support client : tri emails + réponses auto | Quotidien 8h30 |
| **NDEYE** | ndeye_agent.py | Analytics : stats Gumroad/Fiverr + rapport | Quotidien 8h05 |

## Variables d'environnement requises (.env)

```env
# Gmail
GMAIL_USER=omarichard284@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx

# Gumroad
GUMROAD_ACCESS_TOKEN=xxx

# LinkedIn
LINKEDIN_ACCESS_TOKEN=xxx
LINKEDIN_ORGANIZATION_ID=112948321

# Twitter/X (pour SEYDOU)
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
TWITTER_ACCESS_TOKEN=xxx
TWITTER_ACCESS_SECRET=xxx

# Mode dry-run (true = simulation, false = publication réelle)
SEYDOU_DRY_RUN=true
```

## Lancer manuellement un agent

```bash
cd "C:\Users\USER\.claude\projects\projet jarvis"
python agents\ndeye_agent.py          # Rapport revenus du jour
python agents\rokhaya_agent.py        # Emails acheteurs
python agents\seydou_agent.py post    # Tweet
python agents\samba_agent.py          # Article SEO
python agents\ibrahima_agent.py avatar # Génère avatar Malt
python agents\lamine_agent.py         # Support client
```

## Architecture d'automatisation

```
8h00  → LAMINE lit inbox + répond auto
8h05  → NDEYE génère rapport revenus + envoie email
9h00  → ROKHAYA envoie emails acheteurs + follow-ups
9h30  → BINTOU cherche opportunités clients
10h00 → SAMBA publie article SEO (lundi uniquement)
10h30 → SEYDOU poste tweet (mar/jeu uniquement)
Lundi → MARIAMA publie post LinkedIn (Make.com)
Vendredi → AMINATA rapport hebdo + FATOU bilan financier
```
