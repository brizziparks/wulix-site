# 🌐 PROMPT CLAUDE DESIGN — Refonte wulix.fr

> À coller dans Claude Design, en utilisant le **même design system WULIX** déjà généré.
> Tu n'as PAS besoin de recréer le design system, il est déjà actif.

---

## 📋 PROMPT À COPIER

```
Crée les maquettes haute-fidélité du site wulix.fr en utilisant le design system
WULIX déjà actif. Génère 5 pages en parallèle, desktop + mobile.

CONTEXTE
WULIX est une agence d'automatisation IA pour freelances et PME françaises.
Stack technique visible : Python · FastAPI · n8n · Gemini · Claude · Cloudflare.
Fondateur : Omar Sylla (auto-entrepreneur). 5 produits Gumroad.
URL : https://wulix.fr (déjà online, à redesigner sans casser le SEO).
Ton : premium dev tool style Linear/Vercel/Stripe, dark mode obligatoire,
sérieux mais accessible.

PAGES À GÉNÉRER (en parallèle si possible)

1. HOME (/index.html)
   Sections (cet ordre) :
   - Nav sticky avec logo + 5 liens + CTA "Demander un devis"
   - Hero plein écran : titre Orbitron animé "L'IA qui travaille à votre place",
     sous-titre, 2 CTA (Fiverr + Devis), 4 stats (48h délai · 100% custom · 10x productivité · 5★)
   - "Built with" : logos stack (Python, FastAPI, n8n, Gemini, Claude, Cloudflare)
   - 3 services en cards hover-lift : Scripts Python (29€), Agents IA, Workflows n8n
   - "Comment ça marche" : timeline 3 étapes (Audit gratuit → Devis 48h → Livraison 5-10j)
   - Grid 5 produits Gumroad avec covers et prix (29€/19€/9€/5€/Bundle 45€ avec badge or)
   - "Pourquoi WULIX" : 4 trust signals en 2x2
   - FAQ accordéon 6 questions
   - CTA final avec gradient hero animé "Prêt à automatiser ?"
   - Footer 4 colonnes

2. OFFRE (/offre.html)
   - Hero "Nos prestations sur mesure"
   - 3 packs détaillés en pricing cards (Audit 30€ / Automatisation 200-500€ / Dev sur mesure 800€+)
     Inclus / Non-inclus / Délai / CTA pour chaque pack
   - "Comment travaille-t-on ensemble" : process en 5 étapes avec illustrations
   - Témoignages (placeholder pour quand on en aura)
   - FAQ pricing dédiée (6 questions sur les tarifs et modalités)
   - CTA "Demander un devis personnalisé" en gros à la fin

3. BLOG INDEX (/blog.html)
   - Hero "Articles & guides automatisation IA"
   - Filtres par catégorie : Python · n8n · IA · Stratégie · Tutoriels
   - Grid 12 articles (6+6) avec card : cover, titre, extrait, date, temps lecture, CTA "Lire"
   - Sidebar (desktop) : Newsletter inscription email + 3 articles populaires
   - Pagination ou load-more

4. ARTICLE BLOG (/blog/{slug}.html — template)
   - Breadcrumb : Accueil > Blog > Catégorie > Article
   - Hero article : titre, meta (date, auteur Omar Sylla, temps lecture, catégorie)
   - Sommaire flottant à gauche (desktop, sticky)
   - Corps article markdown : titres h2/h3, paragraphes, code blocks avec copy button,
     citations, callouts info/warning, images
   - CTA conversion en milieu d'article (after section 2)
   - CTA conversion en bas : "Cet article t'a aidé ? Discute avec WULIX pour appliquer ça"
   - 3 articles liés en bas
   - Footer

5. CONTACT/DEVIS (/contact.html — nouvelle page)
   - Hero "Discutons de votre projet"
   - Formulaire de devis structuré :
     * Nom, email, entreprise (champs requis)
     * Type de projet (radio: Audit / Automatisation / Dev sur mesure / Autre)
     * Budget approximatif (select : <500€ / 500-2000€ / 2000-5000€ / 5000€+ / Pas sûr)
     * Délai souhaité (select : Urgent / 1 mois / 3 mois / Flexible)
     * Description (textarea, 5 lignes min)
     * Message envoie webhook Make.com pour notif
   - Sidebar : alternatives directes (Email contact@wulix.fr, Fiverr, Calendly RDV 30 min)
   - Mention "Réponse sous 24h ouvré" + "Pas de spam, pas de commercial agressif"

CONTRAINTES TECHNIQUES STRICTES
- HTML/CSS/JS pur — pas de framework lourd (React/Vue interdits)
- Compatible Cloudflare Pages (statique uniquement)
- Lighthouse 95+ obligatoire (LCP < 1.5s, CLS < 0.1, TBT minimal)
- Mobile-first responsive (375px → 1920px)
- Accessibilité AA : contraste, focus rings, alt text, ARIA where needed
- Préserver les meta SEO existants (description, og:image, JSON-LD Organization)
- Préserver les liens existants (Fiverr, Gumroad, blog articles existants)
- Dark mode par défaut (pas de toggle nécessaire)

INTERDIT
- Pas de glassmorphism générique vu partout
- Pas de stock photos corporate (Unsplash autorisé uniquement pour blog covers placeholder)
- Pas de témoignages bidons (skip cette section, j'en mettrai quand j'en aurai des vrais)
- Pas de logos clients fake
- Pas de "100k+ utilisateurs" — on est honnêtes (pas de fake metrics)
- Pas de chatbot embed (j'ai déjà AISATOU)

TON ÉDITORIAL
- Direct, pas de bullshit, pas de promesses farfelues
- "Vous" et non "tu" sur le site (B2B)
- Garantie satisfaction 7 jours mentionnée discrètement (pas comme un argument de vente)
- Pas de superlatifs gratuits ("le meilleur", "le plus rapide" interdits)

LIVRE-MOI : 5 maquettes haute-fidélité (HTML/CSS prêt à copier-coller dans le repo).
Format : un fichier HTML par page, CSS dans le design system commun déjà actif.
```

---

## 📦 Comment l'utiliser

1. **Va sur claude.ai/design**
2. Tu es **toujours dans le projet "WULIX Design System"** (le même que pour AISATOU)
3. Dans la zone "Describe what you want to create...", **colle le prompt** ci-dessus
4. Choisis **High fidelity** + **From template** OU **Prototype**
5. Lance et attend ~10-15 min (5 pages c'est plus long que 2)

## 🎁 Une fois les maquettes prêtes

Tu télécharges le zip et tu me le ramènes — j'intègre tout ça dans `ui/` du repo, je conserve les meta SEO existants, les liens Gumroad/Fiverr, les routes Cloudflare, et je redéploie en prod.

---

## 🟢 État actuel (en attendant les maquettes Claude Design)

Les pages actuelles ont **déjà bénéficié** de :
- ✅ Tokens unifiés (palette, typo, gradients) synchronisés avec AISATOU
- ✅ Gradient hero animé sur le titre H1 (cyan → violet → or, shine 6s)
- ✅ Hover-lift sur les service-cards et pricing-cards
- ✅ Shimmer effect sur la card "popular"
- ✅ Fonts JetBrains Mono ajoutées (pour les futurs code blocks)
- ✅ Utilities `.text-gradient`, `.glow-cyan`, `.btn-cta`, `.shimmer`, `.fade-in`
- ✅ Selection highlight cyan

→ Le site est déjà cohérent visuellement avec AISATOU. La refonte structurelle/UX viendra avec les maquettes Claude Design.
