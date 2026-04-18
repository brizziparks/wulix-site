# -*- coding: utf-8 -*-
"""
WULIX - Generateur PDF Produit 3
Guide : Automatise 5 taches en 1 weekend
"""
from fpdf import FPDF
import os

OUTPUT = r"C:\Users\USER\.claude\projects\projet jarvis\agents\content\gumroad_pack\guide_automatisation_wulix.pdf"
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

CYAN   = (0, 229, 255)
PURPLE = (124, 58, 237)
DARK   = (10, 0, 21)
WHITE  = (255, 255, 255)
LIGHT  = (220, 220, 220)
GREEN  = (100, 220, 120)

class PDF(FPDF):
    def header(self):
        self.set_fill_color(*DARK)
        self.rect(0, 0, 210, 15, 'F')
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*CYAN)
        self.set_xy(10, 4)
        self.cell(0, 6, 'WULIX  |  wulix.fr  |  contact@wulix.fr', ln=False)
        self.set_xy(0, 4)
        self.cell(200, 6, 'Guide : Automatise 5 taches en 1 weekend', align='R')
        self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_fill_color(*DARK)
        self.rect(0, 285, 210, 15, 'F')
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*LIGHT)
        self.cell(0, 8, f'Page {self.page_no()} | (c) WULIX 2026 | Licence personnelle non commerciale', align='C')

    def chapter_title(self, num, title):
        self.set_fill_color(*PURPLE)
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 14)
        self.set_x(10)
        self.cell(190, 12, f'  Chapitre {num} : {title}', ln=True, fill=True)
        self.ln(4)

    def section(self, title):
        self.set_text_color(*CYAN)
        self.set_font('Helvetica', 'B', 11)
        self.set_x(10)
        self.cell(0, 8, title, ln=True)
        self.set_draw_color(*CYAN)
        self.set_x(10)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(3)

    def body(self, text):
        self.set_text_color(200, 200, 200)
        self.set_font('Helvetica', '', 10)
        self.set_x(10)
        self.multi_cell(190, 6, text)
        self.ln(2)

    def tip(self, text):
        self.set_fill_color(20, 0, 40)
        self.set_text_color(*GREEN)
        self.set_font('Helvetica', 'I', 10)
        self.set_x(10)
        self.multi_cell(190, 6, '  -> ' + text, fill=True)
        self.ln(2)

    def step(self, n, text):
        self.set_text_color(*CYAN)
        self.set_font('Helvetica', 'B', 10)
        self.set_x(10)
        self.cell(8, 7, str(n) + '.', ln=False)
        self.set_text_color(210, 210, 210)
        self.set_font('Helvetica', '', 10)
        self.multi_cell(182, 7, text)

    def code_block(self, code):
        self.set_fill_color(15, 0, 30)
        self.set_text_color(*CYAN)
        self.set_font('Courier', '', 8)
        self.set_x(10)
        self.multi_cell(190, 5, code, fill=True, border=1)
        self.ln(2)

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.set_margins(10, 18, 10)

# ===================== PAGE DE GARDE =====================
pdf.add_page()
pdf.set_fill_color(*DARK)
pdf.rect(0, 0, 210, 297, 'F')

pdf.set_y(40)
pdf.set_text_color(*CYAN)
pdf.set_font('Helvetica', 'B', 32)
pdf.cell(0, 14, 'WULIX', align='C', ln=True)

pdf.set_draw_color(*CYAN)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(8)

pdf.set_font('Helvetica', 'B', 22)
pdf.set_text_color(*WHITE)
pdf.cell(0, 12, 'Automatise 5 taches', align='C', ln=True)
pdf.cell(0, 12, 'en 1 weekend', align='C', ln=True)
pdf.ln(4)

pdf.set_font('Helvetica', '', 14)
pdf.set_text_color(*LIGHT)
pdf.cell(0, 8, 'Sans coder - Guide PDF complet', align='C', ln=True)
pdf.ln(12)

# Badge prix
pdf.set_fill_color(*PURPLE)
pdf.set_text_color(*WHITE)
pdf.set_font('Helvetica', 'B', 20)
pdf.set_x(80)
pdf.cell(50, 12, '  9 EUR  ', align='C', fill=True, ln=True)
pdf.ln(20)

# Features liste
features = [
    'Relances email automatiques (Gmail + Sheets)',
    'Tableau de bord auto-mis a jour (Google Sheets)',
    'Publier sur les reseaux automatiquement (Make.com)',
    'Alertes intelligentes en temps reel',
    'Trier ses fichiers automatiquement (Python)',
]
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(*GREEN)
for f in features:
    pdf.set_x(45)
    pdf.cell(0, 8, '->  ' + f, ln=True)

pdf.ln(15)
pdf.set_font('Helvetica', '', 9)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 6, 'wulix.fr  |  contact@wulix.fr  |  (c) 2026 WULIX', align='C', ln=True)
pdf.cell(0, 6, 'Licence personnelle - Usage non commercial - Non redistribuable', align='C', ln=True)

# ===================== SOMMAIRE =====================
pdf.add_page()
pdf.set_text_color(*CYAN)
pdf.set_font('Helvetica', 'B', 18)
pdf.ln(2)
pdf.cell(0, 12, 'Sommaire', ln=True)
pdf.set_draw_color(*CYAN)
pdf.line(10, pdf.get_y(), 80, pdf.get_y())
pdf.ln(6)

sommaire = [
    ('Introduction', 'Pourquoi automatiser ?', 3),
    ('Chapitre 1', 'Relances email automatiques (Gmail + Sheets)', 4),
    ('Chapitre 2', 'Tableau de bord automatique (Google Sheets)', 6),
    ('Chapitre 3', 'Poster sur les reseaux automatiquement (Make.com)', 9),
    ('Chapitre 4', 'Recevoir des alertes intelligentes', 12),
    ('Chapitre 5', 'Organiser ses fichiers avec Python', 15),
    ('Conclusion', 'Et apres ? Les prochaines etapes', 18),
    ('Ressources', 'Liens et outils utiles', 19),
]
pdf.set_font('Helvetica', '', 11)
for cat, titre, page in sommaire:
    pdf.set_text_color(*CYAN)
    pdf.set_x(10)
    pdf.cell(35, 8, cat, ln=False)
    pdf.set_text_color(*WHITE)
    pdf.cell(140, 8, titre, ln=False)
    pdf.set_text_color(120,120,120)
    pdf.cell(15, 8, str(page), align='R', ln=True)
    pdf.set_draw_color(30, 0, 60)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

# ===================== INTRODUCTION =====================
pdf.add_page()
pdf.set_text_color(*WHITE)
pdf.set_font('Helvetica', 'B', 16)
pdf.cell(0, 10, 'Introduction : Pourquoi automatiser ?', ln=True)
pdf.set_draw_color(*PURPLE)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(4)

pdf.body(
    "Tu passes combien d'heures par semaine sur des taches repetitives ?\n\n"
    "Envoyer des relances. Copier des donnees d'un tableau a l'autre. Publier sur les "
    "reseaux sociaux. Trier des fichiers. Recevoir des alertes.\n\n"
    "Selon une etude McKinsey, 45% des activites professionnelles peuvent etre automatisees "
    "avec les outils actuels. Pourtant, la majorite des freelances et solopreneurs continuent "
    "a les faire manuellement - faute de temps pour apprendre, ou parce qu'ils pensent que "
    "ca demande de savoir coder.\n\n"
    "Ce guide prouve le contraire. En 5 chapitres pratiques, tu vas automatiser 5 taches "
    "concretes - avec des outils gratuits, sans ecrire une seule ligne de code (sauf au "
    "chapitre 5 ou on copie-colle un script tout pret).\n\n"
    "Temps estime : 1 weekend. Gain estime : 3 a 5 heures par semaine."
)
pdf.tip("Chaque chapitre est independant. Commence par la tache qui t'enerve le plus !")

# ===================== CHAPITRE 1 =====================
pdf.add_page()
pdf.chapter_title(1, "Relances email automatiques")
pdf.section("Objectif")
pdf.body("Ne plus jamais oublier de relancer un prospect ou un client. Gain : 30 min/semaine.")

pdf.section("Outils necessaires")
pdf.body("- Gmail (gratuit)\n- Google Sheets (gratuit)\n- Google Apps Script (integre a Sheets, gratuit)")

pdf.section("Etape 1 - Creer ton Google Sheet de suivi")
pdf.body("Ouvre Google Sheets et cree un nouveau fichier avec ces colonnes :")
pdf.code_block("A: Nom      B: Email              C: Dernier contact  D: Statut      E: Notes\nMartin D.  martin@ex.com         2026-04-01          A relancer     Devis envoye")

pdf.section("Etape 2 - Ouvrir Apps Script")
pdf.body("Dans Google Sheets : Extensions > Apps Script > colle ce code :")
pdf.code_block(
    "function envoyerRelances() {\n"
    "  var sheet = SpreadsheetApp.getActiveSheet();\n"
    "  var data = sheet.getDataRange().getValues();\n"
    "  var today = new Date();\n\n"
    "  for (var i = 1; i < data.length; i++) {\n"
    "    var email = data[i][1];\n"
    "    var statut = data[i][3];\n"
    "    var lastContact = new Date(data[i][2]);\n"
    "    var daysDiff = (today - lastContact) / (1000*60*60*24);\n\n"
    "    if (statut === 'A relancer' && daysDiff >= 7) {\n"
    "      GmailApp.sendEmail(email,\n"
    "        'Suivi de notre echange',\n"
    "        'Bonjour, je voulais faire suite a notre echange...');\n"
    "      sheet.getRange(i+1, 4).setValue('Relance envoyee');\n"
    "      sheet.getRange(i+1, 3).setValue(today.toISOString().split('T')[0]);\n"
    "    }\n"
    "  }\n"
    "}"
)

pdf.section("Etape 3 - Planifier l'execution automatique")
pdf.step(1, "Dans Apps Script : Icone horloge (Triggers) > Ajouter un declencheur")
pdf.step(2, "Fonction : envoyerRelances | Evenement : Temporel | Chaque jour | 8h00")
pdf.step(3, "Enregistrer")
pdf.tip("Resultat : chaque matin a 8h, le script verifie tes contacts et envoie les relances automatiquement !")

# ===================== CHAPITRE 2 =====================
pdf.add_page()
pdf.chapter_title(2, "Tableau de bord automatique")
pdf.section("Objectif")
pdf.body("Avoir une vue claire de ton activite (revenus, clients, projets) sans saisie manuelle. Gain : 1h/semaine.")

pdf.section("Outils necessaires")
pdf.body("- Google Sheets (gratuit)\n- Formules avancees : IMPORTRANGE, QUERY, SPARKLINE")

pdf.section("Structure recommandee")
pdf.body("Cree 3 feuilles dans ton Google Sheets :")
pdf.code_block("Feuille 1 : Ventes     (saisie manuelle des transactions)\nFeuille 2 : Clients    (liste des clients et statuts)\nFeuille 3 : Dashboard  (agregation automatique - ne pas modifier)")

pdf.section("Formules essentielles pour le Dashboard")
pdf.body("Revenu total du mois en cours :")
pdf.code_block('=SUMPRODUCT((MONTH(Ventes!A2:A100)=MONTH(TODAY()))*(YEAR(Ventes!A2:A100)=YEAR(TODAY()))*Ventes!C2:C100)')

pdf.body("Nombre de clients actifs :")
pdf.code_block('=COUNTIF(Clients!D2:D100,"Actif")')

pdf.body("Graphique sparkline de tes revenus des 6 derniers mois :")
pdf.code_block('=SPARKLINE(Revenus_Mensuels!B2:B7,{"charttype","bar";"color1","#00e5ff"})')

pdf.section("Mise a jour automatique")
pdf.body(
    "Google Sheets recalcule toutes les formules automatiquement. "
    "Tu n'as qu'a saisir tes ventes dans la Feuille 1 - le Dashboard se met a jour seul.\n\n"
    "Astuce : installe l'app Google Sheets sur ton telephone pour saisir une vente "
    "en 10 secondes, meme depuis un cafe."
)
pdf.tip("Partage le Dashboard en lecture seule avec ton comptable pour lui eviter de te demander des rapports !")

# ===================== CHAPITRE 3 =====================
pdf.add_page()
pdf.chapter_title(3, "Poster sur les reseaux automatiquement")
pdf.section("Objectif")
pdf.body("Maintenir une presence sur LinkedIn/Twitter sans y passer du temps. Gain : 2h/semaine.")

pdf.section("Outils necessaires")
pdf.body("- Make.com (gratuit : 1000 operations/mois)\n- Google Sheets (pour stocker tes posts)\n- Compte LinkedIn ou Twitter connecte")

pdf.section("Etape 1 - Preparer tes posts dans Google Sheets")
pdf.code_block("A: Date de publication  B: Heure  C: Reseau    D: Contenu du post            E: Statut\n2026-04-28              08:30     LinkedIn     Voici 3 conseils pour...       pending\n2026-04-30              18:00     Twitter      L'automatisation c'est...      pending")

pdf.section("Etape 2 - Creer le scenario Make.com")
pdf.step(1, "Va sur make.com > Create a new scenario")
pdf.step(2, "Module 1 : Schedule (trigger) - toutes les heures")
pdf.step(3, "Module 2 : Google Sheets - Search Rows (filtre : Date = aujourd'hui, Heure = maintenant, Statut = pending)")
pdf.step(4, "Module 3 : LinkedIn/Twitter - Create Post (contenu = colonne D)")
pdf.step(5, "Module 4 : Google Sheets - Update Row (Statut = posted)")
pdf.step(6, "Save > Activer le toggle ON")

pdf.section("Resultat")
pdf.body(
    "Tu prepares tous tes posts du mois en 1h le dimanche soir. "
    "Make.com les publie automatiquement aux bons jours et heures. "
    "Tu n'as plus a te connecter aux reseaux pour publier."
)
pdf.tip("Avec 1000 operations gratuites/mois, tu peux faire 33 posts/mois - largement suffisant !")

# ===================== CHAPITRE 4 =====================
pdf.add_page()
pdf.chapter_title(4, "Alertes intelligentes en temps reel")
pdf.section("Objectif")
pdf.body("Etre notifie instantanement quand quelque chose d'important se passe. Gain : 30 min/semaine.")

pdf.section("Alerte 1 : Nouveau formulaire de contact")
pdf.body("Quand quelqu'un remplit ton formulaire wulix.fr, recois un email/SMS immediatement.")
pdf.step(1, "Make.com > nouveau scenario")
pdf.step(2, "Trigger : Webhooks (copie l'URL webhook dans ton formulaire)")
pdf.step(3, "Action : Gmail - Send Email (a toi-meme avec les infos du contact)")
pdf.tip("Temps de reponse < 5 minutes = taux de conversion x3 !")

pdf.section("Alerte 2 : Nouvelle vente Gumroad")
pdf.body("Recois une notification a chaque vente sur Gumroad.")
pdf.step(1, "Make.com > nouveau scenario")
pdf.step(2, "Trigger : Gumroad - Watch Sales")
pdf.step(3, "Action : Gmail - Send Email OU Telegram - Send Message")

pdf.section("Alerte 3 : Veille concurrentielle")
pdf.body("Recois un email quand un concurrent publie du nouveau contenu.")
pdf.step(1, "Make.com ou Zapier (gratuit)")
pdf.step(2, "Trigger : RSS - New Item (entre le flux RSS du blog concurrent)")
pdf.step(3, "Action : Gmail - Send Email avec le titre et lien de l'article")
pdf.tip("Google Alerts (gratuit) fait aussi ca tres bien pour la veille sur des mots-cles !")

# ===================== CHAPITRE 5 =====================
pdf.add_page()
pdf.chapter_title(5, "Organiser ses fichiers avec Python")
pdf.section("Objectif")
pdf.body("Ne plus jamais avoir un dossier Telechargements en chaos. Gain : 15 min/semaine.")

pdf.section("Prerequis")
pdf.body("Python doit etre installe sur ton ordinateur. Verifie avec : python --version\nSi besoin : telecharge Python sur python.org (gratuit, 5 min)")

pdf.section("Le script - copier-coller integralement")
pdf.code_block(
    "import os, shutil\n"
    "from pathlib import Path\n\n"
    "DOSSIER = Path.home() / 'Downloads'\n\n"
    "CATEGORIES = {\n"
    "    'PDF':       ['.pdf'],\n"
    "    'Images':    ['.jpg','.jpeg','.png','.gif','.webp'],\n"
    "    'Videos':    ['.mp4','.mov','.avi','.mkv'],\n"
    "    'Documents': ['.doc','.docx','.xls','.xlsx','.ppt','.pptx'],\n"
    "    'Archives':  ['.zip','.rar','.7z'],\n"
    "    'Code':      ['.py','.js','.html','.css','.json'],\n"
    "}\n\n"
    "for fichier in Path(DOSSIER).iterdir():\n"
    "    if fichier.is_file():\n"
    "        ext = fichier.suffix.lower()\n"
    "        for cat, exts in CATEGORIES.items():\n"
    "            if ext in exts:\n"
    "                dest = Path(DOSSIER) / cat\n"
    "                dest.mkdir(exist_ok=True)\n"
    "                shutil.move(str(fichier), str(dest / fichier.name))\n"
    "                print(f'[OK] {fichier.name} -> {cat}/')\n"
    "                break\n\n"
    "print('Organisation terminee !')"
)

pdf.section("Lancer le script")
pdf.step(1, "Copie le code ci-dessus dans un fichier : organiser.py")
pdf.step(2, "Double-clic sur le fichier OU terminal : python organiser.py")
pdf.step(3, "Regarde ton dossier Downloads : tout est trie en sous-dossiers !")

pdf.section("Lancement automatique au demarrage")
pdf.body("Windows : touche Win + R > shell:startup > colle un raccourci vers ton script\nMac : LaunchAgents > cree un .plist pointant vers le script")
pdf.tip("Lance-le une fois par semaine le lundi matin - tes downloads seront toujours propres !")

# ===================== CONCLUSION =====================
pdf.add_page()
pdf.set_text_color(*WHITE)
pdf.set_font('Helvetica', 'B', 16)
pdf.cell(0, 10, 'Conclusion : Et apres ?', ln=True)
pdf.set_draw_color(*PURPLE)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(4)

pdf.body(
    "Felicitations ! Tu viens d'automatiser 5 taches qui te volaient du temps chaque semaine.\n\n"
    "Recapitulatif du temps recupere :\n"
    "  -> Relances email : 30 min/semaine\n"
    "  -> Tableau de bord : 1h/semaine\n"
    "  -> Posts reseaux : 2h/semaine\n"
    "  -> Alertes intelligentes : 30 min/semaine\n"
    "  -> Tri de fichiers : 15 min/semaine\n\n"
    "Total : 4h15 recuperees chaque semaine, soit 17h par mois.\n\n"
    "La prochaine etape ? Automatiser des processus encore plus complexes :\n"
    "  -> Agents IA qui repondent a tes emails\n"
    "  -> Scripts Python qui generent tes rapports clients\n"
    "  -> Workflows n8n pour integrer tous tes outils ensemble\n\n"
    "C'est exactement ce que WULIX fait pour ses clients."
)

pdf.section("Tu veux aller plus loin ?")
pdf.body(
    "Explore nos autres produits sur wulix.gumroad.com :\n"
    "  -> Pack Scripts Python (29 EUR) : 5 scripts avances prêts a l'emploi\n"
    "  -> Pipeline LinkedIn Automatise (19 EUR) : workflow n8n cle en main\n\n"
    "Ou contacte-nous pour une mission sur mesure : contact@wulix.fr"
)

# ===================== RESSOURCES =====================
pdf.add_page()
pdf.set_text_color(*WHITE)
pdf.set_font('Helvetica', 'B', 16)
pdf.cell(0, 10, 'Ressources & Liens utiles', ln=True)
pdf.set_draw_color(*PURPLE)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(4)

ressources = [
    ("Make.com", "make.com", "Automatisation no-code - 1000 operations/mois gratuit"),
    ("Google Apps Script", "script.google.com", "Scripts Google Sheets/Gmail gratuits"),
    ("Python", "python.org", "Telecharger Python (gratuit)"),
    ("Google Alerts", "google.com/alerts", "Veille gratuite sur des mots-cles"),
    ("n8n", "n8n.io", "Alternative open-source a Make.com"),
    ("WULIX Gumroad", "wulix.gumroad.com", "Nos produits numériques"),
    ("WULIX", "wulix.fr", "Solutions IA sur mesure - contact@wulix.fr"),
]

pdf.set_font('Helvetica', '', 10)
for nom, url, desc in ressources:
    pdf.set_text_color(*CYAN)
    pdf.set_x(10)
    pdf.cell(45, 8, nom, ln=False)
    pdf.set_text_color(*PURPLE)
    pdf.cell(60, 8, url, ln=False)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 8, desc, ln=True)
    pdf.set_draw_color(20, 0, 40)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

pdf.ln(10)
pdf.set_fill_color(*DARK)
pdf.set_text_color(*CYAN)
pdf.set_font('Helvetica', 'B', 11)
pdf.cell(0, 8, 'Merci d\'avoir lu ce guide !', align='C', ln=True)
pdf.set_text_color(150, 150, 150)
pdf.set_font('Helvetica', '', 9)
pdf.cell(0, 6, '(c) WULIX 2026 - Licence personnelle non commerciale - Non redistribuable', align='C', ln=True)
pdf.cell(0, 6, 'Toute reproduction ou revente est interdite (art. L.335-2 CPI)', align='C', ln=True)

pdf.output(OUTPUT)
print("[OK] PDF genere :", OUTPUT)
print("[OK] Pages :", pdf.page)
