# WULIX — Tableau de Suivi des Revenus
**Agente financière : FATOU | Mis à jour : 2026-04-18 (v2 — Malt ajouté)**

---

## 1. Tableau de Suivi Mensuel

> Remplace `AAAA-MM-JJ` par la date réelle de chaque transaction.

| Date | Canal | Produit | Montant Brut | Frais Plateforme | Net |
|------|-------|---------|-------------|-----------------|-----|
| 2026-04-__ | Fiverr | AI Agent – Basic (50€) | 50,00 € | 10,00 € (20%) | 40,00 € |
| 2026-04-__ | Fiverr | AI Agent – Standard (150€) | 150,00 € | 30,00 € (20%) | 120,00 € |
| 2026-04-__ | Fiverr | AI Agent – Premium (400€) | 400,00 € | 80,00 € (20%) | 320,00 € |
| 2026-04-__ | Fiverr | Workflow – Basic (50€) | 50,00 € | 10,00 € (20%) | 40,00 € |
| 2026-04-__ | Fiverr | Workflow – Standard (150€) | 150,00 € | 30,00 € (20%) | 120,00 € |
| 2026-04-__ | Fiverr | Workflow – Premium (400€) | 400,00 € | 80,00 € (20%) | 320,00 € |
| 2026-04-__ | Gumroad | Pack 5 Scripts Python (29€) | 29,00 € | ~4,47 € (15,4%) | ~24,53 € |
| 2026-04-__ | Gumroad | Template n8n LinkedIn (19€) | 19,00 € | ~3,18 € (16,7%) | ~15,82 € |
| 2026-04-__ | Direct | Mission audit → conversion | — | 0,00 € | — |
| 2026-04-__ | Malt | Mission jour (350€/j) | 350,00 € | 35,00 € (10%) | 315,00 € |

**Note frais Gumroad détaillée :**
- Commission fixe : 10% du montant brut
- Frais Stripe : 2,9% + 0,30$
- Frais fixe Gumroad : 0,50$
- Formule approx. : Frais = (Montant × 0,129) + 0,73€
- Exemple 29€ : 3,74 + 0,73 = **4,47€ de frais → net ≈ 24,53€**
- Exemple 19€ : 2,45 + 0,73 = **3,18€ de frais → net ≈ 15,82€**
- Attention : si trafic Gumroad Discover → commission 30%

---

## 2. Récapitulatif Mensuel

| Mois | Fiverr Net | Gumroad Net | Malt Net | Direct Net | **Total Net** |
|------|-----------|------------|---------|-----------|--------------|
| Avril 2026 | — | — | — | — | — |
| Mai 2026 | — | — | — | — | — |
| Juin 2026 | — | — | — | — | — |
| Juillet 2026 | — | — | — | — | — |
| Août 2026 | — | — | — | — | — |
| Septembre 2026 | — | — | — | — | — |

---

## 3. Objectifs Mensuels

| Mois | Objectif Net | Statut | Écart |
|------|-------------|--------|-------|
| M+1 (Mai 2026) | 500 € | En cours | — |
| M+2 (Juin 2026) | 1 200 € | À venir | — |
| M+3 (Juillet 2026) | 2 100 € | À venir | — |

**Progression cible :**
- M+1 → M+2 : +140% (×2,4)
- M+2 → M+3 : +75% (×1,75)
- Croissance mensuelle implicite : ~+60% en moyenne

---

## 4. KPIs à Suivre

### Ventes Gumroad
| KPI | Cible M+1 | Cible M+2 | Cible M+3 |
|-----|----------|----------|----------|
| Nb ventes Pack Scripts (29€) | 8 ventes | 20 ventes | 35 ventes |
| Nb ventes Template n8n (19€) | 5 ventes | 12 ventes | 20 ventes |
| Revenu Gumroad brut | 307 € | 808 € | 1 395 € |
| Revenu Gumroad net estimé | ~265 € | ~698 € | ~1 205 € |

### Commandes Fiverr
| KPI | Cible M+1 | Cible M+2 | Cible M+3 |
|-----|----------|----------|----------|
| Nb commandes Basic (50€) | 2 | 5 | 8 |
| Nb commandes Standard (150€) | 1 | 3 | 5 |
| Nb commandes Premium (400€) | 0 | 1 | 2 |
| Revenu Fiverr brut | 350 € | 1 000 € | 1 800 € |
| Revenu Fiverr net (80%) | 280 € | 800 € | 1 440 € |

### Conversion Direct (wulix.fr)
| KPI | Cible M+1 | Cible M+2 | Cible M+3 |
|-----|----------|----------|----------|
| Audits gratuits réalisés | 5 | 10 | 15 |
| Conversions en mission | 0 | 1 | 2 |
| Taux de conversion | 0% | 10% | 13% |
| Valeur moyenne mission | — | 500 € | 750 € |
| Revenu direct net | — | 500 € | 1 500 € |

### KPIs Globaux
| KPI | Définition |
|-----|-----------|
| ARR (Annual Run Rate) | Total Net Mois × 12 |
| Revenu par canal (%) | Part de chaque canal sur le total net |
| Panier moyen Fiverr | Revenu Fiverr brut / Nb commandes |
| Panier moyen Gumroad | Revenu Gumroad brut / Nb ventes |
| Taux conversion audit | Nb missions signées / Nb audits réalisés |
| Délai moyen livraison | Jours entre commande et livraison |

---

## 5. Calcul des Frais par Plateforme

### Fiverr
```
Frais = 20% du montant brut
Net   = Montant brut × 0,80

  Basic  50€  →  frais 10,00€  →  net  40,00€
  Std   150€  →  frais 30,00€  →  net 120,00€
  Prem  400€  →  frais 80,00€  →  net 320,00€
```

### Gumroad
```
Frais = 10% (commission) + 2,9% (Stripe) + 0,30$ (Stripe fixe) + 0,50$ (Gumroad fixe)
      ≈ 12,9% + 0,80$ fixe (~0,73€ au taux actuel)

Formule : Frais = (Montant × 0,129) + 0,73
          Net   = Montant - Frais

  19€  →  frais ≈ 3,18€  →  net ≈ 15,82€
  29€  →  frais ≈ 4,47€  →  net ≈ 24,53€

Cas Gumroad Discover (trafic apporté par Gumroad) : commission = 30%
  29€  →  frais ≈ 9,44€  →  net ≈ 19,56€
```

### Malt
```
Frais = 10% de commission
Net   = Montant brut × 0,90

  350€/jour  →  frais 35€  →  net 315€/jour
  700€ (2j)  →  frais 70€  →  net 630€
  1750€ (5j) →  frais 175€ →  net 1 575€

⚠️ Profil créé le 18/04/2026 — pas encore de photo → invisible dans les recherches
⚠️ Ajouter une photo de profil pour activer la visibilité
```

### Direct (wulix.fr)
```
Frais = 0%
Net   = Montant brut intégral
```

---

## 6. Projections sur 6 Mois

### Hypothèses

| Canal | Basse | Moyenne | Haute |
|-------|-------|---------|-------|
| Fiverr — croissance commandes | +1/mois | +2-3/mois | +4-5/mois |
| Gumroad — croissance ventes | +5/mois | +10-15/mois | +20-30/mois |
| Direct — missions | 0 | 1/trimestre | 1/mois dès M+2 |

---

### Scénario BAS (visibilité faible, peu d'actions marketing)

| Mois | Fiverr Net | Gumroad Net | Direct Net | **Total Net** | Objectif | Delta |
|------|-----------|------------|-----------|--------------|---------|-------|
| Avril 2026 | 80 € | 50 € | 0 € | **130 €** | — | — |
| Mai 2026 | 160 € | 120 € | 0 € | **280 €** | 500 € | -220 € |
| Juin 2026 | 240 € | 200 € | 0 € | **440 €** | 1 200 € | -760 € |
| Juillet 2026 | 320 € | 300 € | 0 € | **620 €** | 2 100 € | -1 480 € |
| Août 2026 | 400 € | 400 € | 500 € | **1 300 €** | — | — |
| Septembre 2026 | 480 € | 500 € | 500 € | **1 480 €** | — | — |
| **Cumul 6 mois** | **1 680 €** | **1 570 €** | **1 000 €** | **4 250 €** | — | — |

---

### Scénario MOYEN (exécution régulière, présence active sur LinkedIn + Malt)

| Mois | Fiverr Net | Gumroad Net | Malt Net | Direct Net | **Total Net** | Objectif | Delta |
|------|-----------|------------|---------|-----------|--------------|---------|-------|
| Avril 2026 | 120 € | 100 € | 0 € | 0 € | **220 €** | — | — |
| Mai 2026 | 280 € | 265 € | 630 € | 0 € | **1 175 €** | 500 € | +675 € OK |
| Juin 2026 | 640 € | 700 € | 945 € | 500 € | **2 785 €** | 1 200 € | +1 585 € OK |
| Juillet 2026 | 960 € | 1 000 € | 1 575 € | 500 € | **4 035 €** | 2 100 € | +1 935 € OK |
| Août 2026 | 1 120 € | 1 200 € | 2 205 € | 1 000 € | **5 525 €** | — | — |
| Septembre 2026 | 1 440 € | 1 500 € | 2 520 € | 1 000 € | **6 460 €** | — | — |
| **Cumul 6 mois** | **4 560 €** | **4 765 €** | **7 875 €** | **3 000 €** | **20 200 €** | — | — |

---

### Scénario HAUT (forte traction, contenu viral, bouche-à-oreille)

| Mois | Fiverr Net | Gumroad Net | Direct Net | **Total Net** | Objectif | Delta |
|------|-----------|------------|-----------|--------------|---------|-------|
| Avril 2026 | 200 € | 200 € | 0 € | **400 €** | — | — |
| Mai 2026 | 560 € | 500 € | 500 € | **1 560 €** | 500 € | +1 060 € OK |
| Juin 2026 | 1 280 € | 1 200 € | 1 500 € | **3 980 €** | 1 200 € | +2 780 € OK |
| Juillet 2026 | 2 400 € | 2 000 € | 2 000 € | **6 400 €** | 2 100 € | +4 300 € OK |
| Août 2026 | 3 200 € | 2 500 € | 3 000 € | **8 700 €** | — | — |
| Septembre 2026 | 4 000 € | 3 000 € | 3 000 € | **10 000 €** | — | — |
| **Cumul 6 mois** | **11 640 €** | **9 400 €** | **10 000 €** | **31 040 €** | — | — |

---

## 7. Leviers de Croissance Prioritaires

| Priorité | Action | Impact estimé | Délai |
|----------|--------|--------------|-------|
| #1 CRITIQUE | Ajouter 2 nouveaux produits Gumroad (template, mini-cours) | +30% rev. passif | 2 semaines |
| #2 CRITIQUE | Publier 3 posts/semaine LinkedIn avec CTA wulix.fr | +trafic audit | Immédiat |
| #3 IMPORTANT | Optimiser titre et description gigs Fiverr (SEO interne) | +impressions gigs | 1 semaine |
| #4 IMPORTANT | Séquence email post-achat Gumroad vers upsell | +LTV client | 2 semaines |
| #5 MOYEN | Page de vente dédiée sur wulix.fr par offre | +taux conversion directe | 3 semaines |
| #6 MOYEN | Demander avis 5 étoiles à chaque client Fiverr livré | +ranking algorithme | Permanent |

---

## 8. Template de Saisie Rapide

Pour ajouter une vente, copier cette ligne dans le tableau §1 :

```
| 2026-MM-JJ | [Fiverr/Gumroad/Direct] | [Nom du produit] | XX,XX € | XX,XX € (X%) | XX,XX € |
```

**Calcul rapide du net :**
- Fiverr  : `Net = Brut × 0,80`
- Gumroad : `Net = Brut × 0,871 - 0,73`
- Direct  : `Net = Brut`

---

*Fichier généré par FATOU, agente financière WULIX — 2026-04-18*
*Prochaine révision recommandée : 2026-05-01*