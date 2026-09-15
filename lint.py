r"""
Script de lint et verification de conformite academique pour rapport LaTeX (ENSAF).
Verifie automatiquement les regles du guide officiel de redaction :
- Proscription du "je" / "mon" / "j'ai" dans le corps technique
- Proscription du soulignage (\underline)
- Presence obligatoire de \caption et \label pour les figures et tableaux
- Regle hierarchique : au moins deux sous-sections (x.y.1 implique x.y.2)
- Absence de deux-points dans les titres de chapitres
- Detection des placeholders non completes [TEXTE...]
Usage : python lint.py [--strict]
"""

import os
import re
import sys

# Support pour terminaux Windows cp1252
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

WORKSPACE = os.path.dirname(os.path.abspath(__file__))

# Fichiers où le "je" / style personnel est toléré
ALLOWED_PERSONAL_PRONOUNS_FILES = {
    'dedicace.tex',
    'remerciements.tex',
}

# Fichiers à analyser
TARGET_DIRS = ['front', 'chapters', 'back']
ROOT_FILES = ['main.tex']

# Patterns regex
RE_JE = re.compile(r"\b(je|j'ai|j'avais|j'étais|j'estime|j'ai\s+pu|mon|ma|mes|moi)\b", re.IGNORECASE)
RE_UNDERLINE = re.compile(r"\\underline\s*\{", re.IGNORECASE)
RE_COLON_IN_CHAPTER = re.compile(r"\\chapter\{[^}]*:[^}]*\}", re.IGNORECASE)
RE_PLACEHOLDER = re.compile(r"\[(Nom|Titre|Prénom|Technologie|ex\.|Description|Valeur|Insérer|Votre)[^\]]*\]", re.IGNORECASE)

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def get_tex_files():
    files_list = []
    for root_f in ROOT_FILES:
        p = os.path.join(WORKSPACE, root_f)
        if os.path.exists(p):
            files_list.append(p)
    
    for d in TARGET_DIRS:
        dp = os.path.join(WORKSPACE, d)
        if os.path.exists(dp):
            for root, _, files in os.walk(dp):
                for f in files:
                    if f.endswith('.tex'):
                        files_list.append(os.path.join(root, f))
    return sorted(files_list)

def check_file(filepath):
    rel_path = os.path.relpath(filepath, WORKSPACE)
    filename = os.path.basename(filepath)
    issues = []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    in_figure = False
    in_table = False
    fig_has_caption = False
    fig_has_label = False
    fig_start_line = 0
    tab_has_caption = False
    tab_has_label = False
    tab_start_line = 0

    section_counts = {}
    current_section = None

    for i, line in enumerate(lines, start=1):
        clean_line = line.strip()
        # Ignorer les lignes commentées
        if clean_line.startswith('%'):
            continue

        # 1. Vérification du "je" / possessif
        if filename not in ALLOWED_PERSONAL_PRONOUNS_FILES:
            is_conclusion_perso = "Perspectives professionnelles" in clean_line or "bilan personnel" in clean_line or "Conclusion personnelle" in clean_line
            if not is_conclusion_perso:
                matches = RE_JE.findall(clean_line)
                if matches:
                    issues.append((i, 'WARNING', 'Section 1.1.3 (Style)', f"Pronom personnel proscrit detecte : {', '.join(set(matches))} (privilegiez la forme impersonnelle ou 'nous')"))

        # 2. Vérification du soulignage (\underline)
        if RE_UNDERLINE.search(clean_line):
            issues.append((i, 'ERROR', 'Section 2.2.4 (Typographie)', "Soulignage (\\underline) proscrit. Utilisez le gras (\\textbf) ou l'italique (\\textit)"))

        # 3. Vérification des deux-points dans les titres de chapitres
        if RE_COLON_IN_CHAPTER.search(clean_line):
            issues.append((i, 'WARNING', 'Regle Titres ENSAF', "Deux-points (':') detecte dans un titre de chapitre (deconseille)"))

        # 4. Détection des placeholders non remplis
        placeholders = RE_PLACEHOLDER.findall(clean_line)
        if placeholders:
            issues.append((i, 'INFO', 'Redaction', f"Placeholder(s) a completer : {', '.join(placeholders[:2])}"))

        # 5. Vérification des flottants (Figures & Tableaux)
        if '\\begin{figure}' in clean_line:
            in_figure = True
            fig_has_caption = False
            fig_has_label = False
            fig_start_line = i
        elif '\\end{figure}' in clean_line and in_figure:
            in_figure = False
            if not fig_has_caption:
                issues.append((fig_start_line, 'ERROR', 'Section 2.4.2 (Figures)', "Figure sans \\caption detectee"))
            if not fig_has_label:
                issues.append((fig_start_line, 'WARNING', 'Section 2.4 (Flottants)', "Figure sans \\label pour references croisees"))

        if '\\begin{table}' in clean_line:
            in_table = True
            tab_has_caption = False
            tab_has_label = False
            tab_start_line = i
        elif '\\end{table}' in clean_line and in_table:
            in_table = False
            if not tab_has_caption:
                issues.append((tab_start_line, 'ERROR', 'Section 2.4.1 (Tableaux)', "Tableau sans \\caption detecte"))
            if not tab_has_label:
                issues.append((tab_start_line, 'WARNING', 'Section 2.4 (Flottants)', "Tableau sans \\label pour references croisees"))

        if in_figure:
            if '\\caption' in clean_line:
                fig_has_caption = True
            if '\\label' in clean_line:
                fig_has_label = True

        if in_table:
            if '\\caption' in clean_line:
                tab_has_caption = True
            if '\\label' in clean_line:
                tab_has_label = True

        # 6. Suivi des sections / sous-sections pour règles hiérarchiques (Section 1.2.4)
        sec_match = re.search(r"\\section\{([^}]+)\}", clean_line)
        subsec_match = re.search(r"\\subsection\{([^}]+)\}", clean_line)
        if sec_match:
            current_section = sec_match.group(1)
            section_counts[current_section] = []
        elif subsec_match and current_section:
            section_counts[current_section].append((i, subsec_match.group(1)))

    for sec, subsecs in section_counts.items():
        if len(subsecs) == 1:
            line_no = subsecs[0][0]
            name = subsecs[0][1]
            issues.append((line_no, 'WARNING', 'Section 1.2.4 (Structure)', f"Sous-section orpheline '{name}' sous la section '{sec}' (le guide exige au moins 2 sous-sections)"))

    return rel_path, issues

def run_lint(strict_mode=False):
    print("=" * 65)
    print("  LINT AUTOMATIQUE & VERIFICATION DE CONFORMITE ENSAF")
    print("=" * 65)

    files = get_tex_files()
    total_errors = 0
    total_warnings = 0
    total_placeholders = 0

    for filepath in files:
        rel_path, issues = check_file(filepath)
        if not issues:
            print(f"{Colors.GREEN}[OK] {rel_path}{Colors.RESET}")
            continue

        print(f"\n{Colors.BOLD}Fichier : {rel_path}{Colors.RESET}")
        for line_num, severity, rule, msg in issues:
            if severity == 'ERROR':
                total_errors += 1
                color = Colors.RED
                tag = "[ERREUR]"
            elif severity == 'WARNING':
                total_warnings += 1
                color = Colors.YELLOW
                tag = "[AVERTISSEMENT]"
            else:
                total_placeholders += 1
                color = Colors.BLUE
                tag = "[A COMPLETER]"

            print(f"  {color}{tag} Ligne {line_num:3d} [{rule}]{Colors.RESET} : {msg}")

    print("\n" + "=" * 65)
    print("  BILAN DU LINT")
    print("=" * 65)
    print(f"  * Erreurs critiques    : {total_errors}")
    print(f"  * Avertissements       : {total_warnings}")
    print(f"  * Placeholders restants: {total_placeholders}")
    
    if total_errors == 0 and total_warnings == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCES] Votre rapport est 100% conforme aux regles du guide ENSAF.{Colors.RESET}\n")
        return 0
    elif total_errors == 0:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}[INFO] Rapport valide pour compilation. Des avertissements ou placeholders subsistent.{Colors.RESET}\n")
        return 1 if strict_mode else 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}[ECHEC] Des erreurs de conformite bloquantes ont ete detectees.{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    strict_mode = "--strict" in sys.argv
    code = run_lint(strict_mode=strict_mode)
    sys.exit(code)
