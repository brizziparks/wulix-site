# Guide Programmes d'Affiliation WULIX
# Revenus passifs via recommandations d'outils

---

## Pourquoi l'affiliation ?

Chaque article SAMBA contient déjà des liens vers n8n, Make.com et Hostinger.
En activant ces programmes, **chaque clic qui convertit = commission automatique**.
Zéro effort supplémentaire — les liens sont déjà en place.

---

## 1. Make.com (Integromat) — Affiliation

**Commission :** 20% récurrent sur abonnement
**Cookie :** 90 jours
**Lien inscription :** https://www.make.com/en/affiliate-program

**Étapes :**
1. Aller sur https://www.make.com/en/affiliate-program
2. Cliquer "Become an affiliate"
3. Créer compte avec : omarichard284@gmail.com
4. Valider le compte Make.com existant si possible
5. Récupérer ton lien unique (ex: make.com/en/register?pc=WULIX)
6. **Remplacer dans samba_agent.py :** `https://www.make.com/en/register?pc=wulix` → ton vrai lien

**Paiement :** PayPal ou virement, seuil 50€

---

## 2. n8n — Affiliation (n8n Cloud)

**Commission :** 30% premier mois (programme partenaire)
**Lien inscription :** https://n8n.io/partner-program/

**Étapes :**
1. Aller sur https://n8n.io/partner-program/
2. Remplir le formulaire partenaire
3. Email : omarichard284@gmail.com
4. Décrire : "Créateur de contenu automatisation, blog wulix.fr, ~500 visiteurs/mois cible"
5. Après validation, récupérer ton lien unique
6. **Remplacer dans samba_agent.py :** `https://n8n.io/?utm_source=wulix` → ton vrai lien affilié

**Note :** n8n self-hosted est gratuit, la commission porte sur n8n Cloud uniquement.

---

## 3. Hostinger — Affiliation

**Commission :** 60% de la première commande (!)
**Cookie :** 30 jours
**Lien inscription :** https://www.hostinger.fr/affiliation

**Étapes :**
1. Aller sur https://www.hostinger.fr/affiliation
2. Cliquer "Rejoindre le programme"
3. Créer compte affilié
4. Dashboard : https://affiliates.hostinger.com
5. Récupérer ton lien (ex: hostinger.fr/vps-hosting?REFERRALCODE=WULIX)
6. **Remplacer dans samba_agent.py** l'URL Hostinger par ton vrai lien

**Potentiel :** VPS Hostinger = 4-20€/mois → commission 2,40-12€ par vente

---

## 4. Gumroad — Affiliation (Discover)

**Commission :** 10% sur les ventes via Discover
**Pas d'inscription :** Automatique si produits dans Gumroad Discover

**Action :**
- Vérifier que les 3 produits sont dans "Gumroad Discover"
- URL : https://app.gumroad.com/products → chaque produit → "Discover settings"
- Activer "Include in Discover" pour chaque produit

---

## 5. Zapier — Affiliation (bonus)

**Commission :** 20-25% récurrent
**Lien :** https://zapier.com/platform/partner

---

## Résumé des actions à faire (par ordre de priorité)

| Priorité | Programme | Commission | Temps setup |
|----------|-----------|-----------|-------------|
| 1 | Hostinger | 60% first sale | 10 min |
| 2 | Make.com | 20% récurrent | 10 min |
| 3 | n8n | 30% first month | 15 min |
| 4 | Zapier | 25% récurrent | 10 min |

---

## Estimation revenus affiliation (scénario réaliste)

Hypothèse : blog wulix.fr atteint 500 visiteurs/mois (M+2)
- 2% cliquent un lien affilié = 10 clics/mois
- 10% convertissent = 1 vente/mois

| Outil | Commande moy. | Commission | Revenu/mois |
|-------|--------------|------------|-------------|
| Hostinger VPS | 40€/an | 60% | 24€ |
| Make.com | 9€/mois | 20% | 1,80€/mois |
| n8n Cloud | 20€/mois | 30% | 6€ |
| **Total estimé** | | | **~30€/mois** |

Avec 2000 visiteurs/mois → ~120€/mois passifs supplémentaires.

---

## Mise à jour des liens dans le code

Une fois les liens affiliés récupérés, mettre à jour dans :
- `agents/samba_agent.py` → section CTA block (3 liens outils)
- `ui/blog.html` → articles déjà publiés (remplacer les URLs)

Commande pour vérifier les liens actuels :
```
grep -n "n8n.io\|make.com\|hostinger" agents/samba_agent.py
```
