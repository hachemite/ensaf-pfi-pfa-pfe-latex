#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
configure.py — Générateur et configurateur de métadonnées ENSAF.
Lit 'project_info.yaml' et met à jour automatiquement :
  - front/titlepage.tex (Page de garde officielle, gestion solo/binôme/trinôme & jury)
  - front/remerciements.tex (Texte de remerciements protocolaire personnalisé)

Usage :
  python configure.py             # Applique la configuration depuis project_info.yaml
  python configure.py --check     # Affiche les métadonnées actuelles
"""

import sys
import os
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[ERREUR] Le module PyYAML n'est pas installé. Lancez : pip install pyyaml")
    sys.exit(1)


BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "project_info.yaml"
TITLEPAGE_PATH = BASE_DIR / "front" / "titlepage.tex"
REMERCIEMENTS_PATH = BASE_DIR / "front" / "remerciements.tex"


def escape_latex(text: str) -> str:
    """Échappe les caractères réservés LaTeX tout en préservant les macros éventuelles."""
    if not text:
        return ""
    # Si le texte contient déjà des chevrons ou crochets bruts
    # On n'échappe pas les barres obliques déjà présentes
    chars = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
    }
    # Remplacement simple sans casser les commandes existantes
    res = str(text)
    for c, rep in chars.items():
        # Éviter de ré-échapper si précédé d'un backslash
        res = re.sub(r"(?<!\\)" + re.escape(c), rep, res)
    return res


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"[ERREUR] Fichier de configuration introuvable : {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def build_titlepage(cfg: dict) -> str:
    acad = cfg.get("academique", {})
    proj = cfg.get("projet", {})
    auteurs = cfg.get("auteurs", [])
    org = cfg.get("organisme", {})
    enc = cfg.get("encadrement", {})
    jury = cfg.get("jury", {})

    univ = escape_latex(acad.get("universite", "UNIVERSITÉ SIDI MOHAMED BEN ABDELLAH"))
    inst = escape_latex(acad.get("institution", "ÉCOLE NATIONALE DES SCIENCES APPLIQUÉES DE FÈS"))
    dept = escape_latex(acad.get("departement", "Génie Informatique"))
    type_rapport = escape_latex(acad.get("type_rapport", "RAPPORT DE PROJET DE FIN D'ANNÉE"))
    diplome = escape_latex(acad.get("diplome_vise", "Diplôme d'Ingénieur d'État en Génie Informatique"))

    titre = escape_latex(proj.get("titre", "[TITRE DU PROJET]"))
    sous_titre = escape_latex(proj.get("sous_titre", ""))
    periode = escape_latex(proj.get("periode_stage", ""))
    annee = escape_latex(acad.get("annee_universitaire", "2025 -- 2026"))

    org_nom = escape_latex(org.get("nom", "[Organisme d'accueil]"))
    org_ville = escape_latex(org.get("ville", "Fès"))

    # Section Auteurs (1, 2 ou 3)
    auteurs_lines = []
    for a in auteurs:
        civ = a.get("civilite", "M.")
        prenom = a.get("prenom", "")
        nom = a.get("nom", "")
        auteurs_lines.append(f"\\textbf{{{civ} {prenom} {nom}}}")

    if len(auteurs_lines) == 1:
        bloc_auteurs = f"\\textbf{{R\\'ealis\\'e par :}}\\\\[0.2cm]\n    {auteurs_lines[0]}"
    elif len(auteurs_lines) == 2:
        bloc_auteurs = f"\\textbf{{R\\'ealis\\'e par (Bin\\^ome) :}}\\\\[0.2cm]\n    " + "\\\\\n    ".join(auteurs_lines)
    else:
        bloc_auteurs = f"\\textbf{{R\\'ealis\\'e par (Trin\\^ome) :}}\\\\[0.2cm]\n    " + "\\\\\n    ".join(auteurs_lines)

    # Section Encadrement
    enc_lines = []
    # Encadrants académiques
    for acad_enc in enc.get("academique", []):
        civ = acad_enc.get("civilite", "M./Mme")
        nom = acad_enc.get("prenom_nom", "[Encadrant ENSAF]")
        enc_lines.append(f"\\textbf{{{civ} {nom}}} \\textit{{(Encadrant Acad\\'emique ENSAF)}}")
    # Encadrants professionnels
    for pro_enc in enc.get("professionnel", []):
        civ = pro_enc.get("civilite", "M./Mme")
        nom = pro_enc.get("prenom_nom", "[Encadrant Société]")
        enc_lines.append(f"\\textbf{{{civ} {nom}}} \\textit{{(Encadrant Professionnel)}}")

    bloc_encadrement = "\\textbf{Sous la direction de :}\\\\[0.2cm]\n    " + "\\\\\n    ".join(enc_lines)

    # Section Jury (optionnelle sur page de garde)
    bloc_jury = ""
    if jury.get("afficher_sur_garde", False) and jury.get("membres"):
        membres_str = []
        for m in jury["membres"]:
            civ = m.get("civilite", "M.")
            nom = m.get("prenom_nom", "")
            qualite = m.get("qualite", "Membre")
            etab = m.get("etablissement", "ENSAF")
            membres_str.append(f"\\textbf{{{civ} {nom}}}, {qualite} ({etab})")
        bloc_jury = "\n\\vspace{0.4cm}\n\\begin{center}\n\\small \\textbf{Membres du Jury :}\\\\[0.1cm]\n" + " \\quad | \\quad ".join(membres_str) + "\n\\end{center}\n"

    modele = str(acad.get("modele_couverture", "PFA")).upper().strip()
    inclure = acad.get("inclure_couverture", True)
    promotion = escape_latex(acad.get("promotion", "2026"))
    date_soutenance = escape_latex(acad.get("date_soutenance", "Juin 2026"))

    # CAS 0 : AUCUNE COUVERTURE (NONE / SANS / inclure_couverture: false)
    if not inclure or modele in ["NONE", "AUCUN", "AUCUNE", "SANS", "FALSE", "OFF", "0"]:
        return "% ============================================================\n" \
               "% PAGE DE GARDE DÉSACTIVÉE (modele_couverture: NONE)\n" \
               "% Le rapport est compilé sans page de garde (pour impression\n" \
               "% séparée ou insertion d'une couverture externe).\n" \
               "% ============================================================\n"

    # CAS 1 : PROJET DE FIN D'ÉTUDES (PFE / cpfe.docx)
    if "PFE" in modele or "FIN D" in type_rapport.upper():
        jury_items = []
        for pro in enc.get("professionnel", []):
            civ = pro.get("civilite", "M.")
            pnom = pro.get("prenom_nom", "[Encadrant Société]")
            jury_items.append(f"\\textbf{{{civ} {pnom}}} & Encadrant(e) Soci\\'et\\'e \\\\")
        for aca in enc.get("academique", []):
            civ = aca.get("civilite", "Prof.")
            pnom = aca.get("prenom_nom", "[Encadrant ENSAF]")
            jury_items.append(f"\\textbf{{{civ} {pnom}}} & Encadrant ENSAF \\\\")
        for j in jury.get("membres", []):
            civ = j.get("civilite", "Prof.")
            pnom = j.get("prenom_nom", "[Enseignant ENSAF]")
            role = j.get("qualite", "Enseignant ENSAF")
            jury_items.append(f"\\textbf{{{civ} {pnom}}} & {role} \\\\")

        jury_block = ""
        if jury_items:
            jury_block = f"""\\vspace{{0.5cm}}
\\noindent
\\textbf{{Membres de jury :}}\\\\[0.15cm]
\\begin{{tabularx}}{{\\textwidth}}{{@{{}}p{{7.5cm}} X@{{}}}}
{chr(10).join(jury_items)}
\\end{{tabularx}}
"""

        content = f"""\\begin{{titlepage}}
\\thispagestyle{{empty}}

% ============================================================
% LOGOS ENSAF ET ORGANISME D'ACCUEIL
% ============================================================
\\begin{{minipage}}{{0.45\\textwidth}}
    \\flushleft
    \\IfFileExists{{logos/logo-ensaf.png}}{{%
        \\includegraphics[height=2.2cm]{{logos/logo-ensaf.png}}%
    }}{{%
        \\fbox{{\\parbox[c][2cm][c]{{3.5cm}}{{\\centering \\textbf{{Logo ENSAF}}}}}}%
    }}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}{{0.45\\textwidth}}
    \\flushright
    \\IfFileExists{{logos/logo-entreprise.png}}{{%
        \\includegraphics[height=2.2cm]{{logos/logo-entreprise.png}}%
    }}{{%
        \\fbox{{\\parbox[c][2cm][c]{{3.5cm}}{{\\centering \\textbf{{Logo Entreprise}}}}}}%
    }}
\\end{{minipage}}

\\vspace{{0.6cm}}

\\begin{{center}}
    {{\\large \\textbf{{{univ}}}}}\\\\[0.15cm]
    {{\\large \\textbf{{{inst}}}}}\\\\[0.6cm]

    {{\\LARGE \\textbf{{Projet de Fin d'\\'Etudes}}}}\\\\[0.25cm]
    {{\\large \\textbf{{Pour l'obtention du dipl\\^ome}}}}\\\\[0.15cm]
    {{\\Large \\textbf{{D'Ing\\'enieur d'\\'Etat}}}}\\\\[0.25cm]
    {{\\large \\textbf{{G\\'enie {dept}}}}}\\\\[0.2cm]
    {{\\normalsize \\textbf{{Promotion {promotion}}}}}\\\\[0.6cm]

    \\rule{{\\linewidth}}{{0.5mm}}\\\\[0.35cm]
    {{\\Large \\bfseries Sujet de stage :}}\\\\[0.2cm]
    {{\\large {titre}}}\\\\[0.15cm]
    {{\\normalsize \\textit{{{sous_titre}}}}}\\\\[0.2cm]
    \\rule{{\\linewidth}}{{0.5mm}}\\\\[0.5cm]

    {{\\large \\textbf{{Stage r\\'ealis\\'e au sein de :}} {org_nom} ({org_ville})}}\\\\[0.4cm]
\\end{{center}}

\\vfill

% IDENTIFICATION DES ÉTUDIANTS ET DATE DE SOUTENANCE
\\noindent
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    {bloc_auteurs}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    \\raggedleft
    \\textbf{{Soutenance le :}}\\\\[0.2cm]
    {date_soutenance}
\\end{{minipage}}

{jury_block}
\\vfill

\\begin{{center}}
    \\small \\textbf{{Ann\\'ee Universitaire :}} {annee}
\\end{{center}}

\\end{{titlepage}}
"""
        return content

    # CAS 2 : STAGE D'INITIATION (1ère année / csi.docx)
    elif "INIT" in modele or "1" in modele:
        titre_stage = "Stage d'Initiation"
        statut_etudiant = "\\'El\\`eve Ing\\'enieur en 1\\textsuperscript{\\grave{{e}}re} ann\\'ee"
    # CAS 3 : STAGE D'APPLICATION (2ème année / PFA / csa.docx)
    else:
        titre_stage = "Stage d'Application"
        statut_etudiant = "\\'El\\`eve Ing\\'enieur en 2\\textsuperscript{\\grave{{e}}me} ann\\'ee"

    # Jury pour stage d'application / initiation
    bloc_jury_stage = ""
    if jury.get("membres"):
        j_l = []
        for m in jury["membres"]:
            civ = m.get("civilite", "M.")
            nom = m.get("prenom_nom", "")
            j_l.append(f"-- {civ} {nom}")
        bloc_jury_stage = f"""\\vspace{{0.5cm}}
\\noindent
\\textbf{{Membres de jury :}}\\\\[0.15cm]
\\begin{{tabular}}{{@{{}}l}}
    {" \\\\\\\\ " + chr(10) + "    ".join(j_l)}
\\end{{tabular}}
"""

    content = f"""\\begin{{titlepage}}
\\thispagestyle{{empty}}

% ============================================================
% LOGOS ENSAF ET ORGANISME D'ACCUEIL
% ============================================================
\\begin{{minipage}}{{0.45\\textwidth}}
    \\flushleft
    \\IfFileExists{{logos/logo-ensaf.png}}{{%
        \\includegraphics[height=2.2cm]{{logos/logo-ensaf.png}}%
    }}{{%
        \\fbox{{\\parbox[c][2cm][c]{{3.5cm}}{{\\centering \\textbf{{Logo ENSAF}}}}}}%
    }}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}{{0.45\\textwidth}}
    \\flushright
    \\IfFileExists{{logos/logo-entreprise.png}}{{%
        \\includegraphics[height=2.2cm]{{logos/logo-entreprise.png}}%
    }}{{%
        \\fbox{{\\parbox[c][2cm][c]{{3.5cm}}{{\\centering \\textbf{{Logo Entreprise}}}}}}%
    }}
\\end{{minipage}}

\\vspace{{0.6cm}}

\\begin{{center}}
    {{\\large \\textbf{{{univ}}}}}\\\\[0.15cm]
    {{\\large \\textbf{{{inst}}}}}\\\\[0.6cm]

    {{\\LARGE \\textbf{{{titre_stage}}}}}\\\\[0.3cm]
    {{\\large \\textbf{{{statut_etudiant}}}}}\\\\[0.15cm]
    {{\\large \\textbf{{G\\'enie {dept}}}}}\\\\[0.8cm]

    {{\\large \\textbf{{Stage r\\'ealis\\'e au sein de :}} {org_nom} ({org_ville})}}\\\\[0.5cm]

    \\rule{{\\linewidth}}{{0.5mm}}\\\\[0.35cm]
    {{\\Large \\bfseries Sujet de stage :}}\\\\[0.2cm]
    {{\\large {titre}}}\\\\[0.15cm]
    {{\\normalsize \\textit{{{sous_titre}}}}}\\\\[0.2cm]
    \\rule{{\\linewidth}}{{0.5mm}}\\\\[0.5cm]

    {periode_str}
\\end{{center}}

\\vfill

% IDENTIFICATION DES ÉTUDIANTS ET DE L'ENCADREMENT
\\noindent
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    {bloc_auteurs}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    \\raggedleft
    {bloc_encadrement}
\\end{{minipage}}

{bloc_jury_stage}
\\vfill

\\begin{{center}}
    \\small \\textbf{{Ann\\'ee Universitaire :}} {annee}
\\end{{center}}

\\end{{titlepage}}
"""
    return content


def build_remerciements(cfg: dict) -> str:
    org = cfg.get("organisme", {})
    enc = cfg.get("encadrement", {})
    jury = cfg.get("jury", {})
    acad = cfg.get("academique", {})
    rem = cfg.get("remerciements", {})

    org_nom = escape_latex(org.get("nom", "[Nom de l'organisme d'accueil]"))
    org_part = escape_latex(org.get("partenaire", ""))
    dir_info = org.get("directeur", {})
    dir_civ = escape_latex(dir_info.get("civilite", "M."))
    dir_nom = escape_latex(dir_info.get("nom", "[Nom du Directeur]"))
    dir_titre = escape_latex(dir_info.get("titre", "Directeur"))

    dept = escape_latex(acad.get("departement", "Génie Informatique"))
    equipe_collabs = escape_latex(rem.get("equipe_collaborateurs", "l'équipe des ingénieurs, techniciens et stagiaires de l'organisme"))

    # Formule organisme & partenaire
    if org_part:
        org_mention = f"au \\textbf{{{org_nom}}} ainsi qu'\\`a \\textbf{{{org_part}}}"
    else:
        org_mention = f"\\`a l'organisme d'accueil \\textbf{{{org_nom}}}"

    # Directeur
    dir_mention = ""
    if dir_nom and not dir_nom.startswith("["):
        dir_mention = f"""\\vspace{{0.4cm}}

\\noindent
J'adresse mes remerciements les plus distingu\\'es \\`a {dir_civ} {dir_nom}, \\textit{{{dir_titre}}}, pour son accueil bienveillant, ses orientations strat\\'egiques, sa vision et pour les moyens mis \\`a disposition tout au long de cette mission d'ing\\'enierie.
"""

    # Encadrants professionnels
    pro_encs = enc.get("professionnel", [])
    if pro_encs:
        items_pro = []
        for p in pro_encs:
            civ = escape_latex(p.get("civilite", "M."))
            pnom = escape_latex(p.get("prenom_nom", "[Encadrant]"))
            role = escape_latex(p.get("specialite") or p.get("fonction", "Encadrant professionnel"))
            mention = escape_latex(p.get("mention_remerciement", "pour sa disponibilité constante et ses conseils avisés"))
            items_pro.append(f"    \\item \\textbf{{{civ} {pnom}}}, \\textit{{{role}}}, {mention} ;")
        bloc_pro = f"""\\vspace{{0.4cm}}

\\noindent
Je tiens \\`a t\\'emoigner ma vive et profonde reconnaissance \\`a mes encadrants professionnels au sein de \\textbf{{{org_nom}}} :
\\begin{{itemize}}
{chr(10).join(items_pro)}
\\end{{itemize}}
"""
    else:
        bloc_pro = ""

    # Encadrant académique
    acad_encs = enc.get("academique", [])
    if acad_encs:
        items_acad = []
        for a in acad_encs:
            civ = escape_latex(a.get("civilite", "M."))
            pnom = escape_latex(a.get("prenom_nom", "[Encadrant Académique]"))
            mention = escape_latex(a.get("mention_remerciement", "pour son suivi pédagogique rigoureux, ses remarques constructives et ses précieux conseils méthodologiques"))
            items_acad.append(f"\\textbf{{{civ} {pnom}}} {mention}")
        bloc_acad = f"""\\vspace{{0.4cm}}

\\noindent
Mes sinc\\`eres remerciements vont \\'egalement \\`a mon encadrant acad\\'emique \\`a l'\\textbf{{\\'Ecole Nationale des Sciences Appliqu\\'ees de F\\`es (ENSAF)}}, {', '.join(items_acad)}.
"""
    else:
        bloc_acad = ""

    # Jury
    membres_jury = jury.get("membres", [])
    bloc_jury_list = ""
    if membres_jury:
        j_lines = []
        for j in membres_jury:
            civ = escape_latex(j.get("civilite", "M."))
            nom = escape_latex(j.get("prenom_nom", "[Membre]"))
            qualite = escape_latex(j.get("qualite", "Membre"))
            etab = escape_latex(j.get("etablissement", "ENSAF"))
            j_lines.append(f"    \\item \\textbf{{{civ} {nom}}} --- \\textit{{{qualite} ({etab})}} ;")
        bloc_jury_list = f"""
\\vspace{{0.4cm}}
\\noindent
\\textbf{{Membres du jury :}}
\\begin{{itemize}}
{chr(10).join(j_lines)}
\\end{{itemize}}
"""

    content = f"""\\chapter*{{Remerciements}}
\\addcontentsline{{toc}}{{chapter}}{{Remerciements}}

\\noindent
Avant d'entamer le d\\'eveloppement technique de ce rapport, il m'appara\\^it essentiel d'exprimer mes sinc\\`eres remerciements \\`a l'ensemble des personnes et des institutions dont la disponibilit\\'e, les conseils et la confiance ont permis la bonne r\\'ealisation et l'aboutissement de ce projet de fin d'ann\\'ee.

\\vspace{{0.4cm}}

\\noindent
J'exprime tout d'abord ma profonde gratitude {org_mention} pour m'avoir ouvert ses portes, accueilli au sein de ses structures et permis d'effectuer ce stage dans un cadre professionnel stimulant et propice \\`a l'apprentissage.
{dir_mention}{bloc_pro}{bloc_acad}
\\vspace{{0.4cm}}

\\noindent
Je remercie chaleureusement {equipe_collabs} pour leur coop\\'eration bienveillante, la richesse des \\'echanges techniques et l'esprit de partage qui ont anim\\'e cette exp\\'erience professionnelle.

\\vspace{{0.4cm}}

\\noindent
Mes remerciements s'adressent \\'egalement au corps professoral et administratif du d\\'epartement \\textbf{{{dept}}} de l'ENSAF pour la qualit\\'e de la formation d'ing\\'enieur d'\\'Etat dispens\\'ee tout au long du cursus.

\\vspace{{0.4cm}}

\\noindent
Enfin, j'adresse mes vifs remerciements aux honorables membres du jury pour l'honneur qu'ils me font en acceptant d'\\'evaluer ce travail d'ing\\'enierie et d'enrichir ce rapport par leurs observations avis\\'ees.
{bloc_jury_list}
"""
    return content


def print_check(cfg: dict):
    print("=" * 65)
    print("  MÉTADONNÉES DU PROJET ENSAF (project_info.yaml)")
    print("=" * 65)
    acad = cfg.get("academique", {})
    proj = cfg.get("projet", {})
    auteurs = cfg.get("auteurs", [])
    org = cfg.get("organisme", {})
    enc = cfg.get("encadrement", {})
    jury = cfg.get("jury", {})

    print(f"[*] Titre       : {proj.get('titre')}")
    print(f"[*] Sous-titre  : {proj.get('sous_titre')}")
    print(f"[*] Type        : {acad.get('type_rapport')}")
    print(f"[*] Filière     : {acad.get('filiere')}")
    print(f"[*] Période     : {proj.get('periode_stage')}")
    print(f"[*] Organisme   : {org.get('nom')} ({org.get('ville')})")
    print(f"[*] Auteur(s)   :")
    for a in auteurs:
        print(f"    - {a.get('civilite')} {a.get('prenom')} {a.get('nom')}")
    print(f"[*] Encadrement Académique :")
    for ea in enc.get("academique", []):
        print(f"    - {ea.get('civilite')} {ea.get('prenom_nom')}")
    print(f"[*] Encadrement Société    :")
    for ep in enc.get("professionnel", []):
        print(f"    - {ep.get('civilite')} {ep.get('prenom_nom')} ({ep.get('specialite') or ep.get('fonction')})")
    print(f"[*] Jury :")
    for j in jury.get("membres", []):
        print(f"    - {j.get('civilite')} {j.get('prenom_nom')} [{j.get('qualite')}]")
    print("=" * 65)


def main():
    if "--check" in sys.argv:
        cfg = load_config()
        print_check(cfg)
        return

    print("=" * 65)
    print("  CONFIGURATION AUTOMATIQUE DU RAPPORT ENSAF")
    print("=" * 65)
    cfg = load_config()

    print("[1/2] Génération de la page de garde (front/titlepage.tex)...")
    titlepage_tex = build_titlepage(cfg)
    with open(TITLEPAGE_PATH, "w", encoding="utf-8") as f:
        f.write(titlepage_tex)
    print(f"      -> Mis à jour avec succès : {TITLEPAGE_PATH.relative_to(BASE_DIR)}")

    print("[2/2] Génération des remerciements (front/remerciements.tex)...")
    rem_tex = build_remerciements(cfg)
    with open(REMERCIEMENTS_PATH, "w", encoding="utf-8") as f:
        f.write(rem_tex)
    print(f"      -> Mis à jour avec succès : {REMERCIEMENTS_PATH.relative_to(BASE_DIR)}")

    print("-" * 65)
    print("[SUCCÈS] Vos pages liminaires sont synchronisées avec 'project_info.yaml'.")
    print("         Pour recompiler : python preview.py")
    print("=" * 65)


if __name__ == "__main__":
    main()
