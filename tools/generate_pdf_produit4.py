"""
Génère le PDF Produit 4 — Pack 50 Prompts IA WULIX
"""
from fpdf import FPDF
from pathlib import Path

OUTPUT_PDF = Path("C:/Users/USER/.claude/projects/projet jarvis/agents/content/gumroad_pack/Pack_50_Prompts_IA_WULIX.pdf")
OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)

def s(text):
    return (text
        .replace('\u2014', '-').replace('\u2013', '-')
        .replace('\u2192', '->').replace('\u2190', '<-')
        .replace('\u2019', "'").replace('\u2018', "'")
        .replace('\u201c', '"').replace('\u201d', '"')
        .replace('\u2026', '...').replace('\u00a9', '(c)')
        .replace('\u2705', 'v').replace('\u2714', 'v')
        .replace('\u2713', 'v').replace('\u00e9', 'e')
        .replace('\u00e8', 'e').replace('\u00ea', 'e')
        .replace('\u00e0', 'a').replace('\u00f4', 'o')
        .replace('\u00ee', 'i').replace('\u00fb', 'u')
        .replace('\u00e2', 'a').replace('\u00e7', 'c')
        .replace('\u00f9', 'u').replace('\u00ef', 'i')
        .replace('\u00eb', 'e').replace('\u00ef', 'i')
    )

class PromptsPDF(FPDF):
    def cell(self, w=0, h=0, txt='', border=0, ln=0, align='', fill=False, link=''):
        return super().cell(w, h, s(str(txt)), border, ln, align, fill, link)
    def multi_cell(self, w, h, txt='', border=0, align='J', fill=False, split_only=False, link='', ln=3, max_line_height=None, markdown=False, print_sh=False):
        return super().multi_cell(w, h, s(str(txt)), border, align, fill, split_only, link, ln, max_line_height, markdown, print_sh)

pdf = PromptsPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# PAGE DE COUVERTURE
pdf.set_fill_color(0, 16, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.set_text_color(0, 220, 130)
pdf.set_font("Helvetica", "B", 36)
pdf.set_y(60)
pdf.cell(0, 15, "PACK 50 PROMPTS IA", ln=True, align='C')
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, "Prets a l'emploi", ln=True, align='C')
pdf.set_font("Helvetica", "", 16)
pdf.set_text_color(148, 163, 184)
pdf.ln(5)
pdf.cell(0, 8, "ChatGPT / Claude / Gemini", ln=True, align='C')
pdf.ln(15)
pdf.set_font("Helvetica", "", 14)
pdf.set_text_color(0, 220, 130)
pdf.cell(0, 8, "v Redaction    v Automatisation    v Analyse", ln=True, align='C')
pdf.cell(0, 8, "v Business    v Productivite", ln=True, align='C')
pdf.ln(20)
pdf.set_font("Helvetica", "B", 48)
pdf.set_text_color(0, 220, 130)
pdf.cell(0, 20, "5 EUR", ln=True, align='C')
pdf.set_font("Helvetica", "", 12)
pdf.set_text_color(148, 163, 184)
pdf.cell(0, 8, "wulix.fr  |  contact@wulix.fr", ln=True, align='C')

# CATEGORIES ET PROMPTS
CATEGORIES = [
    ("REDACTION", [
        ("1", "Email de relance client", "Redige un email de relance client professionnel pour [NOM] qui n'a pas repondu depuis [X] jours. Ton : direct mais bienveillant. Max 100 mots."),
        ("2", "Accroches LinkedIn", "Genere 5 accroches LinkedIn percutantes sur le theme [SUJET]. Chaque accroche doit tenir en 1 phrase et donner envie de lire la suite."),
        ("3", "Réécriture texte", "Recris ce texte [TEXTE] en version plus courte, plus directe, pour un public de [CIBLE]."),
        ("4", "Proposition commerciale", "Cree une proposition commerciale pour [SERVICE] destinee a [TYPE CLIENT]. Budget : [BUDGET]. Inclure : probleme, solution, ROI, prix, delai."),
        ("5", "Objet d'email", "Redige 3 versions d'un objet d'email pour [SUJET] : une urgente, une curiosite, une benefice direct."),
        ("6", "Paragraphe fluide", "Transforme cette liste de points [LISTE] en un paragraphe fluide et convaincant de 150 mots."),
        ("7", "Profil freelance", "Redige la section 'A propos' de mon profil Malt/Fiverr. Je suis [METIER], je fais [SERVICES], pour [CLIENTS]."),
        ("8", "Post LinkedIn storytelling", "Genere un post LinkedIn storytelling a partir de : [SITUATION]. Structure : accroche -> histoire -> lecon -> CTA."),
        ("9", "FAQ service", "Redige une FAQ de 5 questions/reponses pour mon service [SERVICE]. Anticipe les objections principales."),
        ("10", "Email bienvenue", "Cree un template d'email de bienvenue pour un nouveau client. Ton chaleureux. Inclure : prochaines etapes, contact, ressources."),
    ]),
    ("AUTOMATISATION & TECH", [
        ("11", "Script Python", "Genere un script Python qui [ACTION]. Utilise uniquement les bibliotheques standard. Ajoute des commentaires en francais."),
        ("12", "Workflow n8n", "Explique comment automatiser [TACHE] avec n8n. Donne la structure du workflow etape par etape."),
        ("13", "Workflow Make.com", "Cree un workflow Make.com pour : quand [DECLENCHEUR], faire [ACTION 1], puis [ACTION 2]. Quels modules utiliser ?"),
        ("14", "Debug Python", "Debogue ce code Python : [CODE]. Explique l'erreur et propose la correction."),
        ("15", "Prompt chatbot", "Cree un prompt systeme pour un chatbot de support client en [DOMAINE]. Repondre en francais, etre poli, escalader si incertain."),
        ("16", "Regex", "Cree une regex pour extraire [PATTERN] depuis ce texte [EXEMPLE]. Explique-la."),
        ("17", "Architecture automatisation", "Propose une architecture simple pour automatiser [PROCESSUS]. Outils recommandes, cout mensuel, temps de setup."),
        ("18", "Email avec pièce jointe Python", "Genere le code pour envoyer un email via Python smtplib avec piece jointe. Variables : destinataire, objet, corps, fichier."),
        ("19", "Comparaison outils", "Explique les differences entre [OUTIL A] et [OUTIL B] pour [USE CASE]. Meilleure option pour [CONTEXTE] ?"),
        ("20", "Tableau comparatif", "Cree un tableau comparatif des meilleures solutions pour [BESOIN] : prix, facilite, fonctionnalites, support."),
    ]),
    ("ANALYSE & STRATEGIE", [
        ("21", "Analyse avis client", "Analyse ce texte [AVIS CLIENT] : sentiment general, points positifs, points negatifs, action recommandee."),
        ("22", "Tendances données", "A partir de ces donnees [DONNEES], identifie les 3 tendances principales et propose 2 actions concretes."),
        ("23", "SWOT", "Fais une analyse SWOT de mon activite : [DESCRIPTION]. Sois precis et actionnable."),
        ("24", "Stratégie pricing", "Propose une strategie de pricing pour [SERVICE/PRODUIT]. Je vise [CIBLE]. Mes couts sont [COUTS]."),
        ("25", "Réponses aux objections", "Identifie les 5 objections principales de [TYPE CLIENT] face a [OFFRE]. Pour chaque objection, propose une reponse."),
        ("26", "Analyse concurrent", "Analyse ce profil concurrent [DESCRIPTION] : forces, faiblesses, opportunites pour me differencier."),
        ("27", "Idées contenu LinkedIn", "Genere 10 idees de contenu LinkedIn pour un [METIER] ciblant [AUDIENCE]. Format : titre + angle."),
        ("28", "Plan 30 jours", "Cree un plan d'action sur 30 jours pour atteindre [OBJECTIF]. Semaine par semaine, actions concretes."),
        ("29", "Analyse brief client", "A partir de ce brief [BRIEF], identifie les besoins explicites, implicites, et les risques du projet."),
        ("30", "Upsells", "Propose 3 upsells pertinents pour un client qui achete [PRODUIT/SERVICE]. Justifie chaque suggestion."),
    ]),
    ("PRODUCTIVITE PERSONNELLE", [
        ("31", "Planning Eisenhower", "Transforme cette liste de taches [LISTE] en planning journalier. Priorise selon la matrice Eisenhower."),
        ("32", "Planning realiste", "J'ai [X] heures et ces taches [LISTE]. Cree un planning realiste avec pauses."),
        ("33", "Compte-rendu reunion", "Redige un compte-rendu de reunion a partir de ces notes [NOTES]. Format : decisions, actions, responsables, delais."),
        ("34", "Questions discovery", "Genere 5 questions percutantes pour un entretien decouverte client sur [TYPE MISSION]."),
        ("35", "Suivi hebdomadaire", "Cree un template de suivi hebdomadaire pour [ACTIVITE]. Colonnes : realise, en cours, bloque, prochain."),
        ("36", "Resume executif", "Transforme ce rapport [TEXTE] en resume executif de 200 mots maximum."),
        ("37", "Checklist processus", "Genere une checklist complete pour [PROCESSUS]. Par phases, rien ne doit etre oublie."),
        ("38", "Message delegation", "Redige un message de delegation pour confier [TACHE] a [PERSONNE]. Contexte, attendu, deadline, ressources."),
        ("39", "Templates situations difficiles", "Cree 3 templates de reponse pour : client mecontent, retard de livraison, demande hors scope."),
        ("40", "Categorisation emails", "Genere un systeme de categorisation pour mes emails entrants. 5-7 categories max, regles claires."),
    ]),
    ("BUSINESS & VENTE", [
        ("41", "Offre irresistible", "Cree une offre irresistible pour [SERVICE] a [PRIX]. Benefices chiffres, garanties, bonus, urgence."),
        ("42", "Script 2 minutes", "Redige un script de presentation de 2 minutes pour [OFFRE]. Pour networking ou appel decouverte."),
        ("43", "Temoignages clients", "Genere 5 temoignages clients realistes pour [SERVICE]. Differents profils, differents benefices."),
        ("44", "Lancement zero budget", "Propose une strategie de lancement pour [PRODUIT] avec zero budget. Canaux : LinkedIn, Reddit, forums."),
        ("45", "Email nurturing", "Cree un email de nurturing pour des prospects pas encore prets. Objectif : maintenir le contact."),
        ("46", "Analyse page de vente", "Analyse cette page de vente [TEXTE] et propose 3 ameliorations pour augmenter la conversion."),
        ("47", "Titres accrocheurs", "Genere 10 titres accrocheurs pour un guide sur [SUJET]. Direct, benefice clair, curiosite."),
        ("48", "Programme fidelite", "Cree un programme de fidelite simple pour [ACTIVITE]. Recompenses, paliers, communication."),
        ("49", "Pitch investisseur", "Redige un pitch investisseur 5 slides pour [PROJET]. Probleme, solution, marche, traction, equipe."),
        ("50", "Prix psychologiques", "Genere une strategie de prix psychologiques pour [GAMME]. Explique le rationnel derriere chaque prix."),
    ]),
]

for cat_name, prompts in CATEGORIES:
    pdf.add_page()
    pdf.set_fill_color(0, 16, 10)
    pdf.rect(0, 0, 210, 297, 'F')

    # En-tête catégorie
    pdf.set_fill_color(0, 220, 130)
    pdf.rect(0, 0, 210, 18, 'F')
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 16, 10)
    pdf.set_y(4)
    pdf.cell(0, 10, f"  CATEGORIE : {cat_name}", ln=True)

    pdf.ln(5)
    for num, titre, prompt in prompts:
        # Numéro + titre
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 220, 130)
        pdf.cell(12, 7, f"#{num}", ln=0)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 7, titre, ln=True)

        # Prompt
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(148, 163, 184)
        pdf.set_x(15)
        pdf.multi_cell(180, 5, prompt, align='L')
        pdf.ln(2)

# PAGE FINALE
pdf.add_page()
pdf.set_fill_color(0, 16, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.set_y(80)
pdf.set_font("Helvetica", "B", 22)
pdf.set_text_color(0, 220, 130)
pdf.cell(0, 12, "Merci d'avoir achete ce pack !", ln=True, align='C')
pdf.ln(10)
pdf.set_font("Helvetica", "", 14)
pdf.set_text_color(255, 255, 255)
pdf.multi_cell(0, 8, "Ces 50 prompts sont conçus pour vous faire gagner du temps immediatement. Copiez, adaptez, et utilisez-les dans ChatGPT, Claude ou Gemini.", align='C')
pdf.ln(15)
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(0, 220, 130)
pdf.cell(0, 8, "Nos autres produits :", ln=True, align='C')
pdf.set_font("Helvetica", "", 12)
pdf.set_text_color(148, 163, 184)
pdf.ln(5)
pdf.cell(0, 8, "Pack Scripts Python WULIX (29EUR) -> wulix.gumroad.com", ln=True, align='C')
pdf.cell(0, 8, "Pipeline LinkedIn Automatise (19EUR) -> wulix.gumroad.com", ln=True, align='C')
pdf.cell(0, 8, "Guide 5 taches en 1 weekend (9EUR) -> wulix.gumroad.com", ln=True, align='C')
pdf.ln(15)
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(0, 220, 130)
pdf.cell(0, 8, "contact@wulix.fr  |  wulix.fr", ln=True, align='C')

pdf.output(str(OUTPUT_PDF))
print(f"PDF genere : {OUTPUT_PDF}")
