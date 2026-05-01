# 🎨 BRIEF DESIGN — WULIX + AISATOU

> À copier-coller dans **Claude Design** (claude.ai → Anthropic Labs)

---

## 🎯 OBJECTIF

Redesigner deux interfaces complémentaires :
1. **wulix.fr** — site agence d'automatisation IA (B2B, freelances + PME)
2. **AISATOU HUD** — interface interne d'assistance IA personnelle (cyberpunk Iron Man)

Les deux doivent partager une **identité visuelle cohérente** (couleurs, typo, langage graphique) tout en remplissant des rôles très différents.

---

## 🏢 IDENTITÉ DE MARQUE WULIX

- **Nom** : WULIX
- **Tagline** : *"Automatisation IA pour PME et freelances"*
- **Sous-titre** : *"Des agents IA qui travaillent à votre place. Python · n8n · Gemini · FastAPI"*
- **Fondateur** : Omar Sylla (auto-entrepreneur français)
- **Ton** : sérieux, technique, premium, mais accessible (pas Wall Street, pas startup naïve)
- **Inspiration design** : croisement entre **Linear**, **Vercel**, **Stripe**, **Anthropic** (clean modern dev) avec une touche **Iron Man / JARVIS** (HUD)
- **Cible** : freelances, PME, indé tech 25-45 ans, cherchant à automatiser leur business

---

## 🎨 PALETTE COULEURS ACTUELLE (à conserver/raffiner)

| Variable | Hex | Usage |
|---|---|---|
| `--cyan` | `#00d4ff` | Accent primaire, CTA, liens |
| `--purple` | `#a855f7` | Accent secondaire, IA/agents |
| `--gold` | `#e2b33a` | Highlights, prix, priorité |
| `--bg` | `#0a0015` | Fond principal (très sombre violet) |
| `--bg2` | `#0f0025` | Fond panneaux |
| `--text` | `#e2e8f0` | Texte clair |
| `--dim` | `#7c88a8` | Texte secondaire |
| `--green` | `#00dc82` | Succès, statut OK |
| `--red` | `#ef4444` | Erreur, alerte |
| `--orange` | `#f59e0b` | Warning |

**Tendance** : dark mode obligatoire. Le light mode est secondaire.

---

## 🔤 TYPOGRAPHIE ACTUELLE

- **Display / Headings** : `Orbitron` (futuriste, géométrique) — pour les titres et le HUD
- **Body** : `Inter` (lisible, moderne) — pour le texte courant
- **Mono** : `JetBrains Mono` ou `Fira Code` — pour le code

→ Ouvert à propositions si Claude Design propose mieux.

---

## 1️⃣ SITE WULIX.FR

### Pages à designer
1. **Home** (`/`) — landing principale
2. **Offre** (`/offre`) — page services (audit, automatisation, dev sur mesure)
3. **Blog** (`/blog`) — index articles SEO
4. **Article blog** — template article
5. **Contact / Devis** — formulaire
6. **Footer global** + **Header global**

### Structure Home actuelle
- Hero : titre + sous-titre + 2 CTA (Voir nos solutions / Demander un devis)
- Section "Nos services" : 3 cards (Scripts Python / Agents IA / Workflows n8n)
- Section "Comment ça marche" : timeline 3 étapes
- Section "Cas clients" / "Stack technique" : logos
- Section "Produits Gumroad" : 5 produits avec covers et prix
- FAQ
- Footer

### Direction artistique souhaitée
- **Premium dev tool aesthetic** : à la Linear/Vercel
- Beaucoup d'**espace blanc négatif** (même en dark mode)
- **Animations subtiles** : hover, scroll reveal, gradients animés
- **Composants modulaires** : cards avec hover lift + glow
- **Pas de stock photos** : illustrations vectorielles ou screenshots de produits
- **Code snippets** visibles dans le hero (pour montrer le côté technique)
- **Trust signals** : statuts services, métriques, témoignages quand on en aura

### Sections à créer si manquantes
- Une section **"Built with"** : Python, FastAPI, n8n, Gemini, Claude, Cloudflare (logos officiels)
- Une **bannière dynamique** affichant le statut WULIX en temps réel (uptime, derniers déploiements)
- Un **CTA flottant** "Discuter avec AISATOU" en bas à droite

### Contraintes techniques
- HTML/CSS/JS pur (pas de framework lourd)
- Hébergement Cloudflare Pages (statique uniquement)
- Doit charger en < 1.5s sur mobile
- Score Lighthouse 95+

---

## 2️⃣ AISATOU HUD (interface interne)

### Contexte
AISATOU = "Agente Intelligente pour la Supervision, l'Automatisation des Tâches et l'Organisation Universelle". C'est l'assistante IA personnelle d'Omar tournant en local sur `localhost:7777` (FastAPI + WebSocket).

### Layout actuel (à conserver dans la philosophie)
3 colonnes :
- **Gauche** : sidebar agents (15 agents IA classés en groupes)
- **Centre** : NEXUS Command Center (chat + missions + flux ops)
- **Droite** : Quick Actions, Revenus NDEYE, Pipeline, CrowdSec, Todo, Journal

### Direction artistique HUD
- **Iron Man / JARVIS aesthetic** assumé (le côté holographique/HUD est voulu)
- **Lignes scan**, **glow effects**, **hex grids**, **animations radar**
- Mais **pas de fioritures gratuites** — chaque élément doit transmettre une info
- **Densité d'information élevée** mais hiérarchisée (l'œil sait où regarder)
- **Animations purposeful** : pulse quand un agent travaille, glow quand un seuil est franchi

### Composants à améliorer
- **Hex grid agents** (15 agents) : actuellement statique → animation hover + drag-rearrange
- **Widget revenus** : graphique sparkline + projection animée
- **Widget CrowdSec** : carte du monde des IPs bloquées (mini)
- **Chat AISATOU** : bulles avec indication du modèle utilisé (Gemini/Groq/Ollama)
- **Mission countdown** : timer style holographique
- **Mode "focus"** : un click qui zoom sur un agent et fade les autres

### Mobile
Une **vue mobile spécifique** existe (`/mobile`) → simplifiée, chat-first. À redesigner aussi.

---

## 🔗 LIENS UTILES POUR CLAUDE DESIGN

- **Site actuel live** : https://wulix.fr
- **Repo** : `C:\Users\USER\.claude\projects\projet jarvis\` (uploader les fichiers `ui/index.html`, `ui/offre.html`, `ui/blog.html`, `hud/index.html`)
- **Logo actuel** : `ui/wulix_logo.svg` + `ui/wulix_logo.png`
- **OG image** : `ui/og-image.jpg` (1200x630)
- **Covers Gumroad existants** : `ui/covers/*.png`

---

## 📦 LIVRABLES ATTENDUS

1. **Maquettes haute-fidélité** des 6 pages WULIX (desktop + mobile)
2. **Maquettes haute-fidélité** du HUD AISATOU (desktop + mobile)
3. **Design system documenté** : couleurs, typo, espacements, composants réutilisables
4. **Guide d'implémentation** : structure CSS suggérée (variables, classes utilitaires)
5. **Assets** : icônes SVG custom, illustrations, gradients animés (si possible code CSS)

---

## ✅ CRITÈRES DE SUCCÈS

- [ ] Cohérence visuelle entre wulix.fr et AISATOU
- [ ] Identité forte et reconnaissable (pas un énième template Tailwind)
- [ ] Clean modern dev premium feel sur le site
- [ ] HUD impressionnant mais fonctionnel (pas un screensaver)
- [ ] Toutes les fonctionnalités existantes du HUD préservées (15 agents, CrowdSec, NDEYE revenue, todos, etc.)
- [ ] Mobile-first thinking (même si desktop est priorité)
- [ ] Performance : LCP < 1.5s, animations 60fps

---

## ⚠️ À NE PAS FAIRE

- Pas de **glassmorphism** générique (déjà vu partout)
- Pas de **dégradés flashy** non-purposeful
- Pas de **stock photos** corporate
- Pas de **emojis** dans les titres (sauf dans les badges UI fonctionnels)
- Ne pas faire un site **light mode** par défaut (la marque est dark-first)
- Ne pas tomber dans le piège **trop "cyberpunk"** : on garde un côté pro

---

> Une fois les maquettes prêtes, exporte-les en PNG/SVG + uploade le résumé du design system. Claude Code (l'agent qui implémente) prendra le relais pour coder tout ça dans le repo.
