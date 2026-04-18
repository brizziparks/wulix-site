# Guide de Déploiement SEO — wulix.fr
## Rédigé par l'Agent SEO WULIX | 18 avril 2026

---

## 1. Déployer sitemap.xml + robots.txt sur Netlify

**Option A — Drag & drop :**
1. app.netlify.com → sélectionne wulix.fr → **Deploys**
2. Glisse le dossier `ui/` complet dans la zone de drop
3. Les fichiers doivent être à la **racine du dossier publié** (vérifie dans Site settings → Build & deploy → Publish directory)

**Option B — Via repo Git (recommandé) :**
```bash
cp ui/sitemap.xml public/sitemap.xml
cp ui/robots.txt public/robots.txt
git add public/sitemap.xml public/robots.txt
git commit -m "SEO: ajout sitemap.xml et robots.txt"
git push origin main
```

**Option C — Netlify CLI :**
```bash
netlify deploy --prod --dir=ui
```

**Vérification :**
- https://wulix.fr/sitemap.xml → HTTP 200
- https://wulix.fr/robots.txt → HTTP 200

---

## 2. Google Search Console — Configuration complète

1. Va sur **search.google.com/search-console**
2. Clique **"Ajouter une propriété"** → **"Préfixe d'URL"** → entre `https://wulix.fr/`
3. **Méthode de vérification recommandée pour Netlify : balise meta HTML**

```html
<meta name="google-site-verification" content="VOTRE_CODE_GSC" />
```

Colle cette balise dans le `<head>` de ton site → déploie → clique **Vérifier** dans GSC

4. **Soumettre le sitemap :**
   - GSC → Index → Sitemaps
   - Entre `sitemap.xml` → **Envoyer**

5. **Demander l'indexation :**
   - GSC → Inspection d'URL → entre `https://wulix.fr/`
   - Clique **"Demander l'indexation"**

---

## 3. Améliorations SEO rapides pour wulix.fr

### Meta tags essentielles
```html
<title>WULIX — Automatisation IA & Scripts Python pour Freelances et PME</title>
<meta name="description" content="WULIX conçoit des scripts Python et workflows n8n sur mesure. Automatisez vos tâches répétitives en 48-72h. Dès 50€." />
<link rel="canonical" href="https://wulix.fr/" />
```

### Open Graph (réseaux sociaux)
```html
<meta property="og:type" content="website" />
<meta property="og:url" content="https://wulix.fr/" />
<meta property="og:title" content="WULIX — Automatisation IA pour Freelances & PME" />
<meta property="og:description" content="Scripts Python, agents IA, workflows n8n. Livraison 48-72h. Dès 50€." />
<meta property="og:image" content="https://wulix.fr/og-image.jpg" />
<!-- Image recommandée : 1200x630px -->
```

### Structured Data JSON-LD (schema.org)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "WULIX",
  "url": "https://wulix.fr",
  "email": "contact@wulix.fr",
  "description": "Agence IA spécialisée en automatisation Python et workflows n8n pour freelances et PME.",
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "FR"
  },
  "serviceType": ["Automatisation Python", "Agents IA", "Workflows n8n"],
  "priceRange": "50€ - 500€"
}
</script>
```

---

## 4. Checklist SEO 30 jours

### Semaine 1 — Techniques de base
- [ ] Déployer sitemap.xml sur Netlify
- [ ] Déployer robots.txt sur Netlify
- [ ] Vérifier HTTP 200 sur les deux URLs
- [ ] Vérifier propriété dans Google Search Console
- [ ] Soumettre le sitemap dans GSC
- [ ] Ajouter meta title + description page d'accueil
- [ ] Vérifier HTTPS actif (auto sur Netlify)
- [ ] PageSpeed > 80 sur mobile (pagespeed.web.dev)

### Semaine 2 — Contenu & Structure
- [ ] Ajouter Open Graph sur toutes les pages
- [ ] Créer og-image.jpg (1200x630px) — peut être la cover WULIX Canva
- [ ] Implémenter structured data JSON-LD
- [ ] Valider sur Rich Results Test (search.google.com/test/rich-results)
- [ ] H1 unique par page avec mot-clé principal
- [ ] Attributs alt sur toutes les images
- [ ] Vérifier liens cassés (broken links checker)

### Semaine 3 — Indexation & Pages
- [ ] Demander indexation manuelle dans GSC pour chaque page
- [ ] Vérifier rapport "Couverture" dans GSC
- [ ] Créer page /cgv (avec le contenu MODIBO)
- [ ] Créer page /contact
- [ ] Lien sitemap dans le footer du site
- [ ] Soumettre sur Bing Webmaster Tools (bing.com/webmasters)

### Semaine 4 — Autorité & Suivi
- [ ] Créer profil Google Business (si pertinent)
- [ ] 2-3 annuaires pro (Kompass, Societe.com)
- [ ] Partager wulix.fr sur LinkedIn + Twitter avec URL
- [ ] Installer Plausible Analytics (respect RGPD) ou GA4
- [ ] Vérifier premières impressions dans GSC
- [ ] Identifier 5 mots-clés cibles (ex: "script python automatisation", "agent ia freelance france")
- [ ] Rédiger 1er article blog ciblé
- [ ] Mettre à jour sitemap avec nouvelles pages
- [ ] Bilan 30j : impressions GSC, PageSpeed, pages indexées

---

## Mots-clés cibles prioritaires WULIX

| Mot-clé | Volume estimé | Difficulté | Priorité |
|---------|--------------|------------|---------|
| script python automatisation | Moyen | Faible | ⭐⭐⭐ |
| automatisation tâches python | Moyen | Faible | ⭐⭐⭐ |
| agent ia freelance | Faible | Faible | ⭐⭐⭐ |
| workflow n8n template | Moyen | Moyen | ⭐⭐ |
| automatisation pme france | Faible | Faible | ⭐⭐ |
| freelance automatisation python | Faible | Faible | ⭐⭐⭐ |

---

*Agent SEO WULIX | 18 avril 2026 | wulix.fr*
