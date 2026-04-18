# WULIX — Produit 3 Gumroad
## Guide PDF 9€ — "Automatise 5 tâches en 1 weekend"
**Rédigé par l'Agent Produit WULIX | 18 avril 2026**

---

## Fiche Produit

| Champ | Valeur |
|-------|--------|
| **Titre** | Automatise 5 tâches en 1 weekend — Sans coder |
| **Prix** | 9€ |
| **Format** | PDF 15-20 pages |
| **URL Gumroad** | wulix.gumroad.com/l/guide-automatisation |
| **Public cible** | Freelances, solopreneurs, non-développeurs |

---

## Description Gumroad

### Titre accrocheur
**"Automatise 5 tâches en 1 weekend — Sans coder (Guide PDF)"**

### Description courte (50 mots — preview)
```
Tu passes des heures sur des tâches répétitives chaque semaine ?
Ce guide te montre comment les automatiser en 1 weekend — sans toucher à du code.
5 automatisations concrètes, outils gratuits, résultats immédiats.
9€. Téléchargement immédiat.
```

### Description longue (200 mots — page produit)
```
Tu passes combien d'heures par semaine à faire des choses que tu pourrais automatiser ?

Envoyer des relances. Trier des fichiers. Copier des données d'un tableau à l'autre.
Publier sur les réseaux. Recevoir des alertes.

Ce guide de 20 pages te montre exactement comment automatiser ces 5 tâches — sans écrire une seule ligne de code.

✅ Des outils 100% gratuits (Gmail, Google Sheets, Make.com, Zapier)
✅ Des instructions étape par étape avec captures d'écran
✅ Applicable dès ce weekend
✅ Résultats mesurables : 3 à 5h récupérées chaque semaine

Ce n'est pas un cours théorique. C'est un guide opérationnel avec des cas concrets tirés de vraies missions WULIX.

Idéal pour : freelances, consultants, solopreneurs, créateurs de contenu, gérants de TPE.

Aucune compétence technique requise. Si tu sais utiliser Gmail et Google Sheets, tu peux suivre ce guide.

Prix de lancement : 9€. Accès immédiat après paiement.
```

### 5 Bullet points "Ce que tu vas apprendre"
```
✅ Automatiser tes relances email sans effort (Gmail + Google Sheets)
✅ Créer un tableau de bord qui se met à jour tout seul
✅ Programmer tes posts sur les réseaux sociaux à l'avance
✅ Recevoir des alertes intelligentes quand quelque chose change
✅ Trier et organiser tes fichiers automatiquement chaque semaine
```

---

## Sommaire du Guide (contenu réel)

### Chapitre 1 — Automatiser ses relances email (Gmail + Google Sheets)
**Objectif :** ne plus jamais oublier de relancer un prospect ou un client

**Contenu :**
- Créer un Google Sheet de suivi des contacts (Nom, Email, Date dernier contact, Statut)
- Utiliser Google Apps Script (copier-coller, pas de code à écrire) pour envoyer des relances automatiques
- Paramétrer les conditions : "si pas de réponse depuis 7 jours → envoyer email de relance"
- Template email de relance professionnel à personnaliser

**Résultat attendu :** 0 prospect oublié, 30 min/semaine économisées

---

### Chapitre 2 — Tableau de bord automatique (Google Sheets)
**Objectif :** avoir une vue claire de son activité sans saisie manuelle

**Contenu :**
- Fonctions Google Sheets avancées : IMPORTRANGE, QUERY, ARRAYFORMULA
- Créer un tableau de bord consolidé depuis plusieurs feuilles
- Graphiques automatiques mis à jour en temps réel
- Template tableau de bord freelance (revenus, clients, projets)

**Résultat attendu :** vision claire de son activité en 30 secondes, 1h/semaine économisée

---

### Chapitre 3 — Poster sur les réseaux automatiquement (Make.com gratuit)
**Objectif :** maintenir une présence sur les réseaux sans y passer du temps

**Contenu :**
- Créer un compte Make.com gratuit (1000 opérations/mois)
- Connecter LinkedIn ou Twitter à Make.com
- Créer un scénario "lire depuis Google Sheets → publier le post"
- Planifier les publications sur 4 semaines en 1h de travail

**Résultat attendu :** 3 posts/semaine publiés automatiquement, 2h/semaine récupérées

---

### Chapitre 4 — Alertes intelligentes (Make.com / Zapier)
**Objectif :** être notifié en temps réel sans surveiller manuellement

**Contenu :**
- Alerte quand un nouveau client remplit ton formulaire de contact
- Alerte quand une vente Gumroad/Fiverr est réalisée
- Alerte quand un concurrent publie un nouveau contenu
- Résumé quotidien par email de toutes tes activités

**Résultat attendu :** réactivité maximale, 0 opportunité manquée

---

### Chapitre 5 — Organiser ses fichiers automatiquement (script Python simple)
**Objectif :** ne plus avoir un bureau ou un dossier Téléchargements en chaos

**Contenu :**
- Script Python copier-coller (commenté ligne par ligne en français)
- Tri automatique par type de fichier (PDF, images, vidéos, docs)
- Tri par date (créer des dossiers par mois automatiquement)
- Lancer le script automatiquement au démarrage de l'ordinateur

**Script Python inclus :**
```python
import os
import shutil
from pathlib import Path
from datetime import datetime

# Dossier à organiser (modifie ce chemin)
DOSSIER = Path.home() / "Downloads"

# Types de fichiers et leurs dossiers de destination
CATEGORIES = {
    "PDF": [".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Vidéos": [".mp4", ".mov", ".avi", ".mkv"],
    "Documents": [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Archives": [".zip", ".rar", ".7z"],
    "Code": [".py", ".js", ".html", ".css", ".json"],
}

def organiser_fichiers(dossier):
    for fichier in Path(dossier).iterdir():
        if fichier.is_file():
            extension = fichier.suffix.lower()
            for categorie, extensions in CATEGORIES.items():
                if extension in extensions:
                    destination = Path(dossier) / categorie
                    destination.mkdir(exist_ok=True)
                    shutil.move(str(fichier), str(destination / fichier.name))
                    print(f"✅ {fichier.name} → {categorie}/")
                    break

organiser_fichiers(DOSSIER)
print("🎉 Organisation terminée !")
```

**Résultat attendu :** dossiers propres en 10 secondes, 15 min/semaine économisées

---

## Brief Cover Canva

### Dimensions
**1280 × 720 px** (format 16:9, compatible Gumroad)

### Palette couleurs WULIX
- Fond : `#0a0015` (violet très sombre / quasi noir)
- Titre principal : `#00e5ff` (cyan électrique)
- Sous-titre : `#ffffff` (blanc)
- Prix / accent : `#7c3aed` (violet)
- Éléments déco : `#1a0030` (violet foncé)

### Contenu de la cover

**Zone haute (logo) :**
- "WULIX" en haut à gauche — police bold, couleur blanche, taille petite

**Zone centrale (titre) :**
- Ligne 1 : "Automatise 5 tâches" — très grand, couleur cyan `#00e5ff`
- Ligne 2 : "en 1 weekend" — très grand, couleur cyan
- Ligne 3 : "Sans coder" — moyen, couleur blanche, style italique ou léger

**Zone droite (éléments visuels) :**
- Icônes simples : ✅ × 5 (représentant les 5 tâches)
- Ou 5 petites bulles/badges avec les mots : Email • Sheets • Réseaux • Alertes • Fichiers

**Zone basse (prix et CTA) :**
- Badge arrondi couleur violet `#7c3aed` avec "9€" en blanc bold
- Texte sous le badge : "Guide PDF — Téléchargement immédiat"
- Petite ligne : "wulix.fr"

### Style général
- Fond avec légère texture ou dégradé (de `#0a0015` vers `#0d001f`)
- Quelques points lumineux / particules pour l'ambiance tech
- Police recommandée : Inter Bold ou Space Grotesk

---

## Checklist de Lancement

- [ ] Rédiger le PDF complet (15-20 pages) depuis ce sommaire
- [ ] Créer la cover sur Canva selon le brief ci-dessus
- [ ] Créer le produit sur Gumroad (wulix.gumroad.com/l/guide-automatisation)
- [ ] Ajouter la description longue + bullet points
- [ ] Uploader le PDF + la cover
- [ ] Fixer le prix à 9€
- [ ] Ajouter le snippet CGV (voir cgv_gumroad_snippet.md)
- [ ] Publier
- [ ] Poster l'annonce sur Twitter + LinkedIn (demander à MARIAMA)
- [ ] Ajouter au portfolio Malt

---

*Agent Produit WULIX | 18 avril 2026 | contact@wulix.fr*
