"""
Génère le PDF "Automatise 5 tâches en 1 weekend" — Guide WULIX 9€
"""
from fpdf import FPDF
from pathlib import Path
import zipfile

OUTPUT_DIR = Path("C:/Users/USER/.claude/projects/projet jarvis/agents/content/gumroad_pack")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PDF_PATH = OUTPUT_DIR / "Guide_Automatise_5_Taches_WULIX.pdf"
ZIP_PATH = OUTPUT_DIR / "produit3_guide_automatisation_9eur.zip"

PURPLE = (124, 58, 237)
DARK = (15, 15, 15)
CYAN = (0, 200, 220)
WHITE = (255, 255, 255)
GRAY = (156, 163, 175)
LIGHT_BG = (245, 243, 255)

def s(text):
    """Sanitise les caractères Unicode non supportés par Helvetica (latin-1)"""
    return (text
        .replace('\u2014', '-').replace('\u2013', '-')   # tirets longs
        .replace('\u2192', '->').replace('\u2190', '<-') # flèches
        .replace('\u2019', "'").replace('\u2018', "'")   # apostrophes courbes
        .replace('\u201c', '"').replace('\u201d', '"')   # guillemets courbes
        .replace('\u2026', '...').replace('\u00a9', '(c)')
        .replace('\u2705', 'v').replace('\u2714', 'v')   # coches
    )

class GuidePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 20, 20)

    def cell(self, w=0, h=0, txt='', border=0, ln=0, align='', fill=False, link=''):
        return super().cell(w, h, s(str(txt)), border, ln, align, fill, link)

    def multi_cell(self, w, h, txt='', border=0, align='J', fill=False, split_only=False, link='', ln=3, max_line_height=None, markdown=False, print_sh=False):
        return super().multi_cell(w, h, s(str(txt)), border, align, fill, split_only, link, ln, max_line_height, markdown, print_sh)

    def header(self):
        if self.page_no() > 1:
            self.set_fill_color(*PURPLE)
            self.rect(0, 0, 210, 8, 'F')
            self.set_font('Helvetica', 'B', 8)
            self.set_text_color(*WHITE)
            self.set_xy(0, 1)
            self.cell(0, 6, '  WULIX - Automatise 5 taches en 1 weekend', align='L')
            self.set_xy(0, 1)
            self.cell(0, 6, f'Page {self.page_no()}  ', align='R')
            self.set_text_color(0, 0, 0)
            self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, 'wulix.fr  |  contact@wulix.fr  |  (c) 2026 WULIX Agency', align='C')

    def cover_page(self):
        # Fond sombre
        self.set_fill_color(10, 0, 21)
        self.rect(0, 0, 210, 297, 'F')

        # Bande violette haute
        self.set_fill_color(*PURPLE)
        self.rect(0, 0, 210, 4, 'F')

        # Logo WULIX
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(*WHITE)
        self.set_xy(20, 20)
        self.set_text_color(*PURPLE)
        self.cell(0, 10, 'WULIX', align='L')

        # Badge "Guide PDF"
        self.set_fill_color(30, 0, 60)
        self.set_xy(20, 38)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(200, 180, 255)
        self.cell(40, 8, '  GUIDE PDF  ', fill=True)

        # Titre principal
        self.set_xy(20, 58)
        self.set_font('Helvetica', 'B', 34)
        self.set_text_color(0, 220, 255)
        self.multi_cell(170, 14, 'Automatise 5 tâches\nen 1 weekend', align='L')

        # Sous-titre
        self.set_xy(20, 110)
        self.set_font('Helvetica', '', 18)
        self.set_text_color(*WHITE)
        self.cell(0, 10, 'Sans écrire une seule ligne de code', align='L')

        # 5 points
        tasks = ['Relances email automatiques', 'Tableau de bord en temps réel',
                 'Posts réseaux planifiés', 'Alertes intelligentes', 'Fichiers organisés auto']
        y = 135
        for task in tasks:
            self.set_fill_color(*PURPLE)
            self.set_xy(20, y)
            self.set_font('Helvetica', 'B', 11)
            self.set_text_color(0, 220, 255)
            self.cell(8, 7, 'v', align='C')
            self.set_font('Helvetica', '', 11)
            self.set_text_color(*WHITE)
            self.cell(0, 7, f'  {task}', align='L')
            y += 10

        # Badge prix
        self.set_fill_color(*PURPLE)
        self.rect(20, 200, 50, 22, 'F')
        self.set_xy(20, 205)
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(*WHITE)
        self.cell(50, 12, '9 EUR', align='C')

        self.set_xy(20, 224)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(180, 180, 180)
        self.cell(0, 6, 'Guide PDF - Telechargement immediat', align='L')

        # Auteur
        self.set_xy(20, 265)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, 'Par Omar Sylla - WULIX Agency  |  wulix.fr', align='L')

        # Bande basse
        self.set_fill_color(*PURPLE)
        self.rect(0, 293, 210, 4, 'F')

    def section_title(self, num, title, desc=""):
        self.set_fill_color(*PURPLE)
        self.rect(20, self.get_y(), 4, 14, 'F')
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(*PURPLE)
        self.set_x(27)
        self.cell(0, 8, s(f'Chapitre {num} - {title}'), ln=True)
        if desc:
            self.set_font('Helvetica', 'I', 11)
            self.set_text_color(*GRAY)
            self.set_x(27)
            self.cell(0, 6, s(desc), ln=True)
        self.ln(4)

    def body_text(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, s(text))
        self.ln(2)

    def bullet(self, text, color=PURPLE):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*color)
        self.set_x(22)
        self.cell(6, 7, 'v')
        self.set_font('Helvetica', '', 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 7, s(text))

    def info_box(self, title, content):
        self.set_fill_color(*LIGHT_BG)
        self.set_draw_color(*PURPLE)
        x, y = self.get_x(), self.get_y()
        self.rect(20, y, 170, 4, 'F')
        self.set_fill_color(*LIGHT_BG)
        self.rect(20, y+4, 170, 30, 'F')
        self.set_fill_color(*PURPLE)
        self.rect(20, y, 4, 34, 'F')
        self.set_xy(26, y + 2)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*PURPLE)
        self.cell(0, 5, s(title))
        self.set_xy(26, y + 9)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(160, 5, s(content))
        self.ln(6)

    def code_block(self, code):
        self.set_fill_color(30, 30, 40)
        lines = code.strip().split('\n')
        h = len(lines) * 5 + 8
        y = self.get_y()
        self.rect(20, y, 170, h, 'F')
        self.set_xy(24, y + 4)
        self.set_font('Courier', '', 8)
        self.set_text_color(0, 220, 180)
        for line in lines:
            self.set_x(24)
            self.cell(0, 5, line, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def result_badge(self, text):
        self.set_fill_color(220, 252, 231)
        y = self.get_y()
        self.rect(20, y, 170, 12, 'F')
        self.set_fill_color(34, 197, 94)
        self.rect(20, y, 4, 12, 'F')
        self.set_xy(26, y + 2)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(21, 128, 61)
        self.cell(0, 8, s(f'Resultat : {text}'))
        self.ln(10)

def generate():
    pdf = GuidePDF()

    # Page de couverture
    pdf.add_page()
    pdf.cover_page()

    # ─── Page 2 : Introduction ───
    pdf.add_page()
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(*PURPLE)
    pdf.cell(0, 10, 'Introduction', ln=True)
    pdf.ln(3)
    pdf.body_text(
        "Tu passes des heures chaque semaine sur des tâches que tu pourrais automatiser ?\n\n"
        "Ce guide est fait pour toi. Pas de code complexe, pas d'abonnement coûteux. "
        "Juste 5 automatisations concrètes que tu peux mettre en place ce weekend avec des outils gratuits.\n\n"
        "Chaque chapitre suit le même format :\n"
        "  - L'objectif clair\n"
        "  - Les outils nécessaires (tous gratuits)\n"
        "  - Les étapes pas à pas\n"
        "  - Le résultat attendu en temps économisé"
    )
    pdf.info_box("Pour qui est ce guide ?",
        "Freelances, consultants, solopreneurs, créateurs de contenu, gérants de TPE.\n"
        "Aucune compétence technique requise. Si tu utilises Gmail et Google Sheets, tu peux tout faire.")
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, 'Ce que tu vas accomplir :', ln=True)
    pdf.ln(2)
    chapters = [
        'Automatiser tes relances email (Gmail + Google Sheets)',
        'Créer un tableau de bord qui se met à jour tout seul',
        'Programmer tes posts réseaux sociaux à l\'avance',
        'Recevoir des alertes intelligentes automatiques',
        'Organiser tes fichiers automatiquement'
    ]
    for i, ch in enumerate(chapters, 1):
        pdf.bullet(f'Chapitre {i} : {ch}')

    # ─── Chapitre 1 ───
    pdf.add_page()
    pdf.ln(5)
    pdf.section_title(1, "Relances Email Automatiques", "Objectif : 0 prospect oublié, 30 min/semaine économisées")
    pdf.body_text(
        "Combien de fois as-tu oublié de relancer un prospect ? Ou envoyé une relance trop tard ?\n\n"
        "Avec Google Sheets + Google Apps Script, tu configures une fois et le système relance automatiquement."
    )
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 7, 'Outils requis (100% gratuits) :', ln=True)
    pdf.bullet('Google Sheets (gratuit avec compte Google)')
    pdf.bullet('Google Apps Script (intégré dans Google Sheets)')
    pdf.bullet('Gmail (ton adresse email Google)')
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 7, 'Étapes :', ln=True)
    pdf.ln(2)
    steps = [
        "Crée un Google Sheet avec ces colonnes : Prénom | Email | Date contact | Statut | Nb relances",
        "Remplis avec tes prospects actuels. Statut = 'À relancer' par défaut.",
        "Dans Google Sheets : Extensions → Apps Script → Nouveau script",
        "Colle le code ci-dessous et personnalise l'objet et le message.",
        "Lance une fois manuellement pour tester. Puis configure le déclencheur quotidien.",
    ]
    for i, step in enumerate(steps, 1):
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(*PURPLE)
        pdf.set_x(20)
        pdf.cell(8, 7, f'{i}.')
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 7, s(step))
    pdf.ln(3)
    pdf.code_block(
        "function relancerContacts() {\n"
        "  var sheet = SpreadsheetApp.getActiveSheet();\n"
        "  var data = sheet.getDataRange().getValues();\n"
        "  var today = new Date();\n"
        "  for (var i = 1; i < data.length; i++) {\n"
        "    var email = data[i][1];\n"
        "    var dateContact = new Date(data[i][2]);\n"
        "    var statut = data[i][3];\n"
        "    var jours = (today - dateContact) / (1000*60*60*24);\n"
        "    if (statut == 'À relancer' && jours >= 7) {\n"
        "      GmailApp.sendEmail(email,\n"
        "        'Suivi de notre échange',\n"
        "        'Bonjour, je voulais faire un point...');\n"
        "      sheet.getRange(i+1, 4).setValue('Relancé');\n"
        "    }\n"
        "  }\n"
        "}"
    )
    pdf.result_badge("30 min/semaine économisées, 0 prospect oublié")

    # ─── Chapitre 2 ───
    pdf.add_page()
    pdf.ln(5)
    pdf.section_title(2, "Tableau de Bord Automatique", "Objectif : vision claire de ton activité en 30 secondes")
    pdf.body_text(
        "Fini de chercher tes chiffres dans 5 fichiers différents. Un tableau de bord Google Sheets "
        "consolidé te donne une vue complète de ton activité sans saisie manuelle."
    )
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 7, 'Formules clés à connaître :', ln=True)
    pdf.ln(2)
    formulas = [
        ("IMPORTRANGE", "Importe des données depuis un autre Google Sheet"),
        ("QUERY", "Filtre et trie tes données comme une base de données"),
        ("ARRAYFORMULA", "Applique une formule à toute une colonne en 1 ligne"),
        ("SPARKLINE", "Crée des mini-graphiques dans une cellule"),
    ]
    for name, desc in formulas:
        pdf.set_fill_color(*LIGHT_BG)
        pdf.set_x(20)
        pdf.set_font('Courier', 'B', 10)
        pdf.set_text_color(*PURPLE)
        pdf.cell(32, 7, f'={name}', fill=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 7, f'  {desc}', ln=True)
    pdf.ln(4)
    pdf.info_box("Template inclus",
        "Ce guide inclut un lien vers un template Google Sheets prêt à copier :\n"
        "Revenus mensuels | Clients actifs | Projets en cours | Objectifs vs réel\n"
        "Accès : wulix.fr/template-dashboard")
    pdf.result_badge("1h/semaine économisée, vision claire en 30 secondes")

    # ─── Chapitre 3 ───
    pdf.add_page()
    pdf.ln(5)
    pdf.section_title(3, "Posts Réseaux Automatiques", "Objectif : 3 posts/semaine sans y passer du temps")
    pdf.body_text(
        "LinkedIn, Twitter, Instagram — maintenir une présence régulière prend du temps. "
        "Make.com te permet de préparer un mois de contenu en 1h et de le publier automatiquement."
    )
    steps3 = [
        "Crée un compte gratuit sur make.com (1 000 opérations/mois offertes)",
        "Crée un Google Sheet avec les colonnes : Date | Texte du post | Statut",
        "Dans Make.com : créer un scénario → ajouter module Google Sheets (Lire une ligne)",
        "Ajouter module LinkedIn ou Twitter → Créer un post",
        "Configurer le planificateur : tous les lundis, mercredis et vendredis à 9h",
        "Remplis le Sheet le dimanche soir → 3 posts partent automatiquement"
    ]
    for i, step in enumerate(steps3, 1):
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(*PURPLE)
        pdf.set_x(20)
        pdf.cell(8, 7, f'{i}.')
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 7, s(step))
    pdf.ln(3)
    pdf.info_box("Astuce WULIX",
        "Prépare 12 posts d'un coup (4 semaines) chaque mois.\n"
        "Thèmes alternés : conseil, cas client, présentation produit, question à l'audience.\n"
        "Notre pack LinkedIn inclut 4 semaines de posts prêts à copier-coller.")
    pdf.result_badge("2h/semaine récupérées, présence continue sur les réseaux")

    # ─── Chapitre 4 ───
    pdf.add_page()
    pdf.ln(5)
    pdf.section_title(4, "Alertes Intelligentes", "Objectif : être notifié en temps réel, 0 surveillance manuelle")
    pdf.body_text(
        "Tu rates des opportunités parce que tu n'es pas toujours à l'affût ?\n"
        "Configure ces 4 alertes automatiques et ne rate plus rien."
    )
    alerts = [
        ("Nouveau contact formulaire", "Typeform/Tally → Make.com → Email + Notion"),
        ("Vente Gumroad réalisée", "Gumroad webhook → Make.com → Email de confirmation"),
        ("Mention de ta marque", "Google Alerts → Email quotidien avec les mentions"),
        ("Résumé quotidien", "Make.com → Email récap 8h : ventes, contacts, tâches"),
    ]
    for alert, flow in alerts:
        pdf.set_fill_color(*LIGHT_BG)
        y = pdf.get_y()
        pdf.rect(20, y, 170, 14, 'F')
        pdf.set_fill_color(*PURPLE)
        pdf.rect(20, y, 4, 14, 'F')
        pdf.set_xy(26, y + 2)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(*PURPLE)
        pdf.cell(0, 5, s(alert))
        pdf.set_xy(26, y + 7)
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(*GRAY)
        pdf.cell(0, 5, s(f'Workflow : {flow}'))
        pdf.ln(16)
    pdf.result_badge("Réactivité maximale, 0 opportunité manquée")

    # ─── Chapitre 5 ───
    pdf.add_page()
    pdf.ln(5)
    pdf.section_title(5, "Organiser ses Fichiers Automatiquement", "Objectif : dossiers propres en 10 secondes")
    pdf.body_text(
        "Bureau encombré, dossier Téléchargements ingérable ?\n"
        "Ce script Python copier-coller (commenté en français) trie tout automatiquement."
    )
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 7, 'Script Python — copier-coller complet :', ln=True)
    pdf.ln(2)
    pdf.code_block(
        "import os, shutil\n"
        "from pathlib import Path\n\n"
        "# Modifie ce chemin\n"
        "DOSSIER = Path.home() / 'Downloads'\n\n"
        "CATEGORIES = {\n"
        "    'PDF':      ['.pdf'],\n"
        "    'Images':   ['.jpg','.png','.gif','.webp'],\n"
        "    'Videos':   ['.mp4','.mov','.avi'],\n"
        "    'Docs':     ['.doc','.docx','.xls','.xlsx'],\n"
        "    'Archives': ['.zip','.rar'],\n"
        "    'Code':     ['.py','.js','.html','.css'],\n"
        "}\n\n"
        "for fichier in Path(DOSSIER).iterdir():\n"
        "    if fichier.is_file():\n"
        "        ext = fichier.suffix.lower()\n"
        "        for cat, exts in CATEGORIES.items():\n"
        "            if ext in exts:\n"
        "                dest = Path(DOSSIER) / cat\n"
        "                dest.mkdir(exist_ok=True)\n"
        "                shutil.move(str(fichier), dest)\n"
        "print('Terminé !')"
    )
    pdf.body_text(
        "Pour lancer ce script automatiquement au démarrage :\n"
        "  Windows : Ajoute un raccourci dans C:\\Users\\USER\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\n"
        "  Mac : Utilise Automator → Application → Run Shell Script"
    )
    pdf.result_badge("15 min/semaine économisées, bureau propre en permanence")

    # ─── Conclusion ───
    pdf.add_page()
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(*PURPLE)
    pdf.cell(0, 10, 'Et maintenant ?', ln=True)
    pdf.ln(3)
    pdf.body_text(
        "Tu as maintenant tout ce qu'il faut pour récupérer 3 à 5 heures par semaine.\n\n"
        "La clé : commence par UNE seule automatisation ce weekend. Celle qui te coûte le plus de temps.\n\n"
        "Une fois que tu verras le résultat, tu voudras tout automatiser."
    )
    pdf.info_box("Aller plus loin avec WULIX",
        "Tu veux qu'on configure tout ça pour toi ?\n"
        "WULIX propose des missions sur mesure : Python, n8n, Make.com, APIs.\n"
        "Délai moyen : 3 à 5 jours. Prix à partir de 150 EUR HT.\n"
        "Contact : wulix.fr  |  contact@wulix.fr")
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, 'Nos autres ressources :', ln=True)
    pdf.bullet('Pack Scripts Python (29 EUR) — 5 scripts prêts à l\'emploi sur Gumroad')
    pdf.bullet('Pipeline LinkedIn n8n (19 EUR) — workflow complet sur Gumroad')
    pdf.bullet('Consulting 2h (200 EUR HT) — audit de tes processus + feuille de route')
    pdf.ln(6)
    pdf.set_fill_color(*PURPLE)
    pdf.set_text_color(*WHITE)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.rect(20, pdf.get_y(), 170, 14, 'F')
    pdf.set_xy(20, pdf.get_y() + 3)
    pdf.cell(170, 8, 'wulix.fr  |  contact@wulix.fr', align='C')

    # Sauvegarde
    pdf.output(str(PDF_PATH))
    print(f"PDF généré : {PDF_PATH}")

    # Création du ZIP
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(PDF_PATH, PDF_PATH.name)
        # Readme
        readme = (
            "WULIX — Guide Automatise 5 tâches en 1 weekend\n"
            "================================================\n\n"
            "Contenu :\n"
            "- Guide_Automatise_5_Taches_WULIX.pdf (guide principal)\n\n"
            "Support : contact@wulix.fr\n"
            "Site : wulix.fr\n"
        )
        zf.writestr("README.txt", readme)

    print(f"ZIP créé : {ZIP_PATH}")
    print("Prêt à uploader sur Gumroad !")

if __name__ == "__main__":
    generate()
