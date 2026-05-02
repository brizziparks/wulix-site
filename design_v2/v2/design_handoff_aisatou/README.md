# Handoff: AISATOU HUD — Redesign inspiré wulix.fr v2

## Overview

AISATOU est l'interface de commande IA personnelle d'Omar Sylla (WULIX). C'est un HUD (Heads-Up Display) style Iron Man / JARVIS tournant en local (FastAPI + WebSocket), permettant de piloter 14 agents IA autonomes, monitorer les revenus Gumroad, surveiller CrowdSec, et chatter avec Claude/Gemini/Groq.

Ce handoff documente les **améliorations visuelles à apporter au HUD** en s'inspirant du design system wulix.fr v2 qui a été entièrement repensé : curseur custom, particles, scroll reveal, micro-interactions, icônes SVG propres, palette afrofuturiste cohérente.

---

## About the Design Files

Les fichiers dans ce bundle sont des **références de design créées en HTML** — des prototypes haute-fidélité montrant l'apparence et le comportement souhaités. La mission est de **recréer ces designs dans le codebase Python/FastAPI/HTML existant** (`hud/index.html` et `hud/mobile.html`) en conservant toute la logique backend (WebSocket, API agents, CrowdSec, etc.) et en appliquant uniquement les améliorations visuelles et UX documentées ici.

**Ne pas remplacer la logique JS existante** — seulement améliorer le CSS, enrichir les animations, et appliquer les nouveaux tokens de design.

---

## Fidelity

**Haute-fidélité (hifi)** — Les mocks sont pixel-perfect avec couleurs finales, typographie, espacements et interactions. Le développeur doit les recréer fidèlement dans `hud/index.html` et `hud/mobile.html`.

---

## Design Tokens

### Couleurs
```css
/* Identiques à wulix.fr pour cohérence de marque */
--bg:      #050510;   /* Fond HUD (plus sombre que site) */
--panel:   #0a0a1a;   /* Panneaux */
--panel2:  #06060e;   /* Panneaux secondaires */
--border:  #1a1a3a;   /* Bordures solides */
--accent:  #7c3aed;   /* Violet principal HUD */
--cyan:    #00e5ff;   /* Cyan HUD (légèrement plus vif que site #00d4ff) */
--green:   #00dc82;   /* Succès / agents actifs */
--orange:  #f59e0b;   /* Warning / busy */
--red:     #ef4444;   /* Erreur / danger */
--gold:    #e2b33a;   /* Revenus / highlights */
--text:    #e0e0f0;   /* Texte principal */
--muted:   #555577;   /* Texte atténué */
```

### Typographie
```css
--font-b: 'Inter', system-ui, sans-serif;         /* Corps / UI */
--font-m: 'JetBrains Mono', 'Courier New', mono;  /* Terminal / HUD */
/* Orbitron utilisé UNIQUEMENT pour logo AISATOU dans header */
/* Orbitron local: fonts/Orbitron-VariableFont_wght.ttf */
```

### Border radius HUD (plus compact que site)
```
4px  — éléments HUD sharps (inputs, boutons run)
6px  — agent cards, hex cells
8px  — badges, chips
10px — modals, sheets
```

### Glows & shadows
```css
/* Cyan glow (focus, actif) */
box-shadow: 0 0 12px rgba(0,229,255,.3);
/* Vert (agents actifs) */
filter: drop-shadow(0 0 6px rgba(0,220,130,.4));
/* Orange (busy) */
filter: drop-shadow(0 0 6px rgba(245,158,11,.4));
/* Text-shadow terminal */
text-shadow: 0 0 8px rgba(0,229,255,.8);
```

---

## Screens / Views

### 1. Desktop HUD (`hud/index.html`)

**Layout global:** `display:flex; flex-direction:column; height:100vh; overflow:hidden`

```
┌─────────────────────────────────────────────────────────┐
│  HEADER (64px) — orb + titre + status + model select    │
├──────────┬──────────────────────────────┬───────────────┤
│ SIDEBAR  │   NEXUS CENTER               │ RIGHT PANEL   │
│ (250px)  │   ┌──────────┬───────────┐  │ (290px)       │
│ agents   │   │ OPS      │  CHAT     │  │ quick actions │
│ accordion│   │ panel    │  panel    │  │ revenue       │
│          │   │ (300px)  │  (flex:1) │  │ metrics       │
│          │   └──────────┴───────────┘  │ crowdsec      │
│          │   scan-line animée          │ todo          │
└──────────┴──────────────────────────────┴───────────────┘
│  (pas de footer — fullscreen)                           │
```

#### A. Header améliorations

**Actuellement:** header basique avec logo texte.
**Cible:** 

```html
<header style="
  background: #0a0a1a;
  border-bottom: 1px solid #7c3aed;
  padding: 10px 20px;
  display: flex; align-items: center; gap: 12px;
  height: 56px; flex-shrink: 0;
">
  <!-- Orbe animé (remplace le simple texte "AI") -->
  <div class="orb" style="
    width: 34px; height: 34px; border-radius: 50%;
    background: radial-gradient(circle, #00e5ff 0%, #7c3aed 55%, transparent 100%);
    box-shadow: 0 0 14px rgba(0,229,255,.5);
    flex-shrink: 0;
  ">
    <!-- Animation CSS: pulse quand AISATOU parle -->
    <!-- .orb.speaking → animation: orbPulse .4s ease-in-out infinite alternate -->
  </div>
  
  <!-- Logo Orbitron local -->
  <div style="
    font-family: 'Orbitron', monospace; font-size: 18px; font-weight: 900;
    color: #00e5ff; letter-spacing: 3px;
  ">AI<span style="color:#7c3aed">SATOU</span></div>
  
  <!-- Status pills + model select (existants, améliorer style) -->
</header>
```

**Animation orbe speaking:**
```css
@keyframes orbPulse {
  from { transform: scale(1); box-shadow: 0 0 14px rgba(0,229,255,.5); }
  to   { transform: scale(1.25); box-shadow: 0 0 28px rgba(0,229,255,.9); }
}
.orb.speaking { animation: orbPulse .4s ease-in-out infinite alternate; }
```
→ Déclencher `.speaking` quand `voice_state === 'speaking'` (déjà géré dans le JS existant).

---

#### B. Scanlines background (amélioration)

Ajouter sur `.nexus-chat::before` et `body`:
```css
body {
  background-image: repeating-linear-gradient(
    0deg, transparent, transparent 39px,
    rgba(0,229,255,.012) 39px, rgba(0,229,255,.012) 40px
  );
}
```

---

#### C. Hex Grid — amélioration états

Les états existants sont bien. Ajouter:
```css
.hex-cell { transition: all .2s; }
.hex-cell:hover { transform: scale(1.12); z-index: 2; }

/* État "busy" (agent en cours d'exécution) */
.hex-cell.busy {
  background: linear-gradient(135deg, #1a100a, #2a1a0d);
  filter: drop-shadow(0 0 8px rgba(245,158,11,.5));
}
/* Activer .busy via JS quand runTask() est appelé, retirer à la fin */
```

**Comment:** dans `setHexBusy(agentId, busy)` existant — la logique est déjà là, juste appliquer le style CSS ci-dessus.

---

#### D. Ops Feed — animation entrée

```css
@keyframes opsFadeIn {
  from { opacity: 0; transform: translateX(-8px); }
  to   { opacity: 1; transform: translateX(0); }
}
.ops-entry { animation: opsFadeIn .4s ease; }
```

---

#### E. Chat — icônes SVG pour le bouton send

Remplacer `EXEC ➤` par :
```html
<button id="send-btn" style="/* styles existants */">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
    <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
  </svg>
</button>
```

---

#### F. Revenue widget — progress bar animée

```css
.rev-progress-fill {
  transition: width .8s cubic-bezier(.22,1,.36,1);
}
```
→ Animer lors du rafraîchissement des données (déjà mis à jour via `refreshRevenue()`).

---

#### G. Quick Actions — états visuels améliorés

```css
.qa-btn.running {
  border-color: var(--orange); color: var(--orange);
  animation: pulse 1s ease-in-out infinite;
}
.qa-btn.done {
  border-color: var(--green); color: var(--green);
}
/* Shimmer au hover sur le bouton "Lancer tous les agents" */
.qa-btn.all-agents {
  position: relative; overflow: hidden;
}
.qa-btn.all-agents::after {
  content: ''; position: absolute; top: -50%; left: -60%; width: 40%; height: 200%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.1), transparent);
  transform: skewX(-15deg); transition: left .4s;
}
.qa-btn.all-agents:hover::after { left: 140%; }
```

---

### 2. Mobile HUD (`hud/mobile.html`)

**Référence:** `aisatou-hud-mobile.html` dans le design system.

Le fichier existant `hud/mobile.html` est plus basique. Voici les améliorations à apporter:

#### Structure cible
```
┌───────────────────────────┐
│ HEADER (56px)             │
│ [orb] AISATOU  [model ▾]  │
├───────────────────────────┤
│ QUICK ACTIONS (chips)     │
│ [📝 Publier] [💼 LinkedIn]│
├───────────────────────────┤
│                           │
│ CHAT (flex:1, scroll)     │
│ messages AI + user + tool │
│                           │
├───────────────────────────┤
│ INPUT BAR                 │
│ › [textarea] [🎙] [➤]    │
├───────────────────────────┤
│ BOTTOM NAV (4 tabs)       │
│ 💬Chat 🤖Agents 🛡Sécu 💰│
└───────────────────────────┘
```

#### Bottom sheets (nouvelles)

3 sheets à implémenter en slide-up depuis le bas:

**Sheet Agents** — hex grid 14 agents + liste quick-run + countdowns missions
**Sheet CrowdSec** — stats (alertes/IPs), infos NAS, bouton refresh  
**Sheet Revenus** — montant jour, progress objectif 500€, historique ventes

```css
.sheet {
  position: fixed; left: 0; right: 0; bottom: 0; z-index: 51;
  background: #0a0a1a;
  border-top: 1px solid #7c3aed;
  border-radius: 20px 20px 0 0;
  transform: translateY(100%);
  transition: transform .35s cubic-bezier(.32,1,.36,1);
  max-height: 80vh;
  display: flex; flex-direction: column;
}
.sheet.open { transform: translateY(0); }
```

**Overlay:**
```css
.sheet-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,.7); backdrop-filter: blur(4px);
  z-index: 50; opacity: 0; pointer-events: none; transition: opacity .3s;
}
.sheet-overlay.open { opacity: 1; pointer-events: all; }
```

---

## Interactions & Behavior

### Orbe speaking
- Écouter `msg.type === 'voice_state'` dans le WebSocket (déjà géré)
- `state === 'speaking'` → ajouter `.speaking` sur `.orb`
- `state === 'idle'` ou `'voice_off'` → retirer `.speaking`

### Quick actions chips (mobile)
- Au clic → état `.running` (bordure orange, animation pulse)
- Envoyer via WebSocket comme le fait le desktop
- Après réponse → état `.done` (bordure verte, 2s), puis reset

### Bottom nav → Bottom sheets
```javascript
function openSheet(name) {
  document.getElementById('sheet-overlay').classList.add('open');
  document.getElementById('sheet-' + name).classList.add('open');
}
function closeSheet() {
  document.getElementById('sheet-overlay').classList.remove('open');
  document.querySelectorAll('.sheet').forEach(s => s.classList.remove('open'));
}
// Fermer au clic overlay
document.getElementById('sheet-overlay').addEventListener('click', closeSheet);
```

### Model selector (mobile)
```javascript
// Dropdown toggle au clic sur .model-pill
// Fermer au clic extérieur
// À la sélection: mettre à jour le label + envoyer via WS si nécessaire
```

---

## Animations globales à ajouter

### 1. Scan line (déjà présente, vérifier)
```css
.scan-line {
  position: absolute; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, rgba(0,229,255,.15), rgba(124,58,237,.2), transparent);
  animation: scanMove 6s linear infinite;
  pointer-events: none;
}
@keyframes scanMove { 0%{top:0%} 100%{top:100%} }
```

### 2. Pulse dots status
```css
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
.dot.on { background: #00dc82; animation: pulse 2s infinite; }
```

### 3. Countdown timer (déjà présent, conserver)
Vérifier que `setInterval(updateCountdowns, 1000)` tourne bien.

### 4. Toast notifications (déjà présentes)
Ajouter slide-in depuis la droite:
```css
@keyframes toastIn {
  from { transform: translateX(120%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}
.toast { animation: toastIn .3s ease; }
```

---

## Assets

| Asset | Chemin | Usage |
|---|---|---|
| Orbitron (variable font) | `fonts/Orbitron-VariableFont_wght.ttf` | Logo AISATOU header |
| Inter | Google Fonts CDN | Corps / UI |
| JetBrains Mono | Google Fonts CDN | Terminal, ops feed, input |
| Logo WULIX | `assets/wulix_logo.png` | Optionnel dans sidebar |

---

## Files de référence dans le design system

| Fichier | Description |
|---|---|
| `aisatou-hud-mobile.html` | **Référence principale mobile** — structure complète avec bottom sheets |
| `ui_kits/aisatou-hud/index.html` | **Référence desktop** — layout complet statique |
| `preview/components-hud-cells.html` | Hex grid + agent accordion (composant isolé) |
| `preview/components-hud-ops.html` | Ops feed + countdowns + scan line (composant isolé) |
| `colors_and_type.css` | Tous les tokens CSS du design system |
| `README.md` | Documentation complète du design system WULIX |

---

## Checklist d'implémentation

### Desktop (`hud/index.html`)
- [ ] Ajouter orbe animé dans le header (remplace le simple "A" ou logo texte)
- [ ] Appliquer font Orbitron locale au logo "AISATOU" du header
- [ ] Ajouter scanlines CSS sur `body`
- [ ] Améliorer états `.busy` sur hex cells (déjà `.active`/`.warn` présents)
- [ ] Ajouter `opsFadeIn` animation sur nouvelles entrées ops feed
- [ ] Remplacer `EXEC ➤` par icône SVG send
- [ ] Ajouter `.running`/`.done` CSS sur quick action buttons
- [ ] Ajouter shimmer sur bouton "Lancer tous les agents"
- [ ] Animer `.rev-progress-fill` avec transition cubic-bezier
- [ ] Ajouter `transition: width .1s linear` sur progress bar nav (si barre de lecture ajoutée)

### Mobile (`hud/mobile.html`)
- [ ] Restructurer layout: header → quick-actions → chat → input-bar → bottom-nav
- [ ] Implémenter orbe animé dans header
- [ ] Ajouter sélecteur de modèle (dropdown) dans header
- [ ] Créer 5 quick-action chips (Publier/LinkedIn/Rapport/Leads/Deploy)
- [ ] Créer bottom-nav 4 onglets (Chat/Agents/Sécu/Revenus)
- [ ] Implémenter Sheet Agents (hex grid + run list + countdowns)
- [ ] Implémenter Sheet CrowdSec (stats + refresh)
- [ ] Implémenter Sheet Revenus (amount + progress + historique)
- [ ] Overlay backdrop + fermeture au clic
- [ ] Connecter sheets aux données WebSocket existantes
- [ ] Toast notifications slide-in

---

## Notes importantes

1. **Ne pas casser le WebSocket** — toute la logique de communication avec le backend FastAPI doit rester intacte. Les améliorations sont purement CSS/HTML/animation.

2. **Backend endpoints à conserver:**
   - `GET /agents/tasks` — liste des agents et leurs tâches
   - `POST /agents/run/{name}` — lancer un agent
   - `GET /agents/revenue` — données revenus NDEYE
   - `GET /agents/crowdsec` — données sécurité
   - `WebSocket /ws` — chat bidirectionnel

3. **Modèles disponibles** — déjà chargés via `GET /models`. Le sélecteur mobile doit utiliser la même liste.

4. **Performance** — le HUD tourne en local (LAN/localhost), donc pas de contrainte Lighthouse. Priorité à la fluidité des animations (60fps).

5. **Dark-only** — ne pas implémenter le mode clair sur mobile (la version desktop l'a mais c'est optionnel). Rester dark-first.
