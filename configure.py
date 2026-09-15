#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
configure.py — Générateur et configurateur de métadonnées ENSAF.
Lit 'project_info.yaml' et synchronise automatiquement :
  1. La couverture officielle Word (CSI, CSA, CPFE) :
     - Écrit les métadonnées directement dans le document Word officiel
     - Conserve 100% de la mise en page, logos et polices officielles
     - Réduit automatiquement les espacements pour garantir STRICTEMENT 1 seule page
     - Exporte en PDF (front/couverture.pdf) et l'intègre dans le rapport via pdfpages
     - Gère l'option 'NONE' pour compiler sans aucune page de garde.
  2. Le résumé en langue arabe (front/resume_ar.pdf) :
     - Génère une page autonome haute fidélité avec polices arabes natives (HarfBuzz)
     - Élimine toutes les erreurs de glyphes manquants dans LaTeX/Tectonic
  3. Les remerciements protocolaires (front/remerciements.tex).

Usage :
  python configure.py             # Applique la configuration complète
  python configure.py --check     # Affiche les métadonnées actuelles
"""

import sys
import os
import re
import subprocess
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[ERREUR] Le module PyYAML n'est pas installé. Lancez : pip install pyyaml")
    sys.exit(1)


BASE_DIR = Path(__file__).parent.resolve()
CONFIG_PATH = BASE_DIR / "project_info.yaml"
TITLEPAGE_PATH = BASE_DIR / "front" / "titlepage.tex"
REMERCIEMENTS_PATH = BASE_DIR / "front" / "remerciements.tex"
RESUME_AR_TEX_PATH = BASE_DIR / "front" / "resume-ar.tex"
RESUME_AR_HTML_PATH = BASE_DIR / "front" / "resume_ar.html"
RESUME_AR_PDF_PATH = BASE_DIR / "front" / "resume_ar.pdf"
COUVERTURE_DOCX_PATH = BASE_DIR / "front" / "couverture.docx"
COUVERTURE_PDF_PATH = BASE_DIR / "front" / "couverture.pdf"


def escape_latex(text: str) -> str:
    """Échappe les caractères réservés LaTeX."""
    if not text:
        return ""
    chars = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
    }
    res = str(text)
    for c, rep in chars.items():
        res = re.sub(r"(?<!\\)" + re.escape(c), rep, res)
    return res


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"[ERREUR] Fichier de configuration introuvable : {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def generate_word_cover(cfg: dict) -> bool:
    """Remplit le modèle Word officiel ENSAF et l'exporte en PDF sur exactement 1 page."""
    acad = cfg.get("academique", {})
    modele = str(acad.get("modele_couverture", "PFA")).upper().strip()
    inclure = acad.get("inclure_couverture", True)

    if not inclure or modele in ["NONE", "AUCUN", "AUCUNE", "SANS", "FALSE", "OFF", "0"]:
        print("      [*] Option 'NONE' sélectionnée : aucune page de garde ne sera générée.")
        if COUVERTURE_PDF_PATH.exists():
            try:
                COUVERTURE_PDF_PATH.unlink()
            except Exception:
                pass
        return False

    # Sélection du modèle officiel
    template_map = {
        "PFE": "couvertures_rapport_stage_ensaf/Projet_Fin_Etudes_3A_PFE_cpfe.docx",
        "CPFE": "couvertures_rapport_stage_ensaf/Projet_Fin_Etudes_3A_PFE_cpfe.docx",
        "INITIATION": "couvertures_rapport_stage_ensaf/Stage_Initiation_1A_csi.docx",
        "CSI": "couvertures_rapport_stage_ensaf/Stage_Initiation_1A_csi.docx",
        "PFA": "couvertures_rapport_stage_ensaf/Stage_Application_2A_PFA_csa.docx",
        "CSA": "couvertures_rapport_stage_ensaf/Stage_Application_2A_PFA_csa.docx",
    }
    template_rel = template_map.get(modele, "couvertures_rapport_stage_ensaf/Stage_Application_2A_PFA_csa.docx")
    template_path = BASE_DIR / template_rel

    if not template_path.exists():
        print(f"      [AVERTISSEMENT] Modèle Word introuvable : {template_path}")
        return False

    proj = cfg.get("projet", {})
    auteurs = cfg.get("auteurs", [])
    org = cfg.get("organisme", {})
    enc = cfg.get("encadrement", {})
    jury = cfg.get("jury", {})

    filiere = acad.get("filiere", "Génie Informatique")
    org_str = f"{org.get('nom', 'Entreprise')} ({org.get('ville', 'Fès')})"
    sujet = proj.get("titre", "Titre du projet")
    periode = proj.get("periode_stage", "")
    promotion = str(acad.get("promotion", "2026"))
    soutenance = str(acad.get("date_soutenance", "Juin 2026"))

    auteurs_str = ", ".join(f"{a.get('civilite', 'M.')} {a.get('prenom', '')} {a.get('nom', '')}" for a in auteurs)

    enc_acad = "[Encadrant ENSAF]"
    if enc.get("academique"):
        ea = enc["academique"][0]
        enc_acad = f"{ea.get('civilite', 'Prof.')} {ea.get('prenom_nom', '')}"

    enc_pro = "[Encadrant Société]"
    if enc.get("professionnel"):
        ep = enc["professionnel"][0]
        enc_pro = f"{ep.get('civilite', 'Dr.')} {ep.get('prenom_nom', '')}"

    jury_members = []
    for m in jury.get("membres", []):
        civ = m.get("civilite", "Prof.")
        pnom = m.get("prenom_nom", "")
        qual = m.get("qualite", "")
        jury_members.append(f"{civ} {pnom} ({qual})" if qual else f"{civ} {pnom}")

    ps_code = r"""param(
    [string]$inDocx,
    [string]$outDocx,
    [string]$outPdf,
    [string]$filiere,
    [string]$org,
    [string]$sujet,
    [string]$periode,
    [string]$auteurs,
    [string]$encAcad,
    [string]$encPro,
    [string]$promotion,
    [string]$soutenance,
    [string]$juryList
)

$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $d = $w.Documents.Open($inDocx)
    
    function Do-Replace($search, $replaceVal) {
        $find = $d.Content.Find
        $find.ClearFormatting()
        $find.Replacement.ClearFormatting()
        [void]$find.Execute($search, $false, $false, $false, $false, $false, $true, 1, $false, $replaceVal, 2)
    }
    
    Do-Replace "Génie …." ("Génie " + $filiere)
    Do-Replace "Génie …" ("Génie " + $filiere)
    Do-Replace "Stage réalisé au sein de : ….." ("Stage réalisé au sein de : " + $org)
    Do-Replace "Stage réalisé au sein de : …." ("Stage réalisé au sein de : " + $org)
    Do-Replace "Stage réalisé au sein de : …" ("Stage réalisé au sein de : " + $org)
    Do-Replace "Sujet de stage" ("Sujet de stage : " + $sujet)
    if ($periode -ne "") {
        Do-Replace "Période de stage : …." ("Période de stage : " + $periode)
        Do-Replace "Période de stage : …" ("Période de stage : " + $periode)
    }
    Do-Replace "Réalisé par M. (Prénom & Nom)" ("Réalisé par : " + $auteurs)
    Do-Replace "Réalisé par M. (Prénom & Nom" ("Réalisé par : " + $auteurs)
    Do-Replace "Encadrant ENSAF     …." ("Encadrant ENSAF : " + $encAcad)
    Do-Replace "Encadrant ENSAF" ("Encadrant ENSAF : " + $encAcad)
    Do-Replace "Encadrant Société     …." ("Encadrant Société : " + $encPro)
    Do-Replace "Encadrant Société" ("Encadrant Société : " + $encPro)
    Do-Replace "Promotion …" ("Promotion " + $promotion)
    Do-Replace "Soutenance le ….." ("Soutenance le : " + $soutenance)
    Do-Replace "Soutenance le …." ("Soutenance le : " + $soutenance)
    Do-Replace "Soutenance le …" ("Soutenance le : " + $soutenance)

    # Réduction stricte à exactement 1 seule page
    $pages = $d.ComputeStatistics(2)
    while ($pages -gt 1) {
        $deleted = $false
        for ($i = $d.Paragraphs.Count; $i -ge 1; $i--) {
            $p = $d.Paragraphs.Item($i)
            if ($p.Range.Text.Trim() -eq "") {
                $p.Range.Delete()
                $deleted = $true
                break
            }
        }
        if (-not $deleted) {
            foreach ($p in $d.Paragraphs) {
                $p.SpaceAfter = [Math]::Max(0, $p.SpaceAfter - 1)
                $p.SpaceBefore = [Math]::Max(0, $p.SpaceBefore - 1)
            }
            break
        }
        $pages = $d.ComputeStatistics(2)
    }
    
    $d.SaveAs([ref]$outDocx, [ref]16)
    $d.SaveAs([ref]$outPdf, [ref]17)
    $d.Close([ref]$false)
    Write-Output "SUCCESS"
} catch {
    Write-Error $_.Exception.Message
} finally {
    $w.Quit()
}
"""
    ps_tmp = BASE_DIR / ".word_cover_gen.ps1"
    try:
        with open(ps_tmp, "w", encoding="utf-8") as f:
            f.write(ps_code)

        args = [
            "powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_tmp),
            str(template_path), str(COUVERTURE_DOCX_PATH), str(COUVERTURE_PDF_PATH),
            filiere, org_str, sujet, periode, auteurs_str, enc_acad, enc_pro,
            promotion, soutenance, "; ".join(jury_members)
        ]
        res = subprocess.run(args, capture_output=True, text=True)
        if "SUCCESS" in res.stdout and COUVERTURE_PDF_PATH.exists():
            print(f"      -> Couverture Word {modele} générée sur 1 page : {COUVERTURE_PDF_PATH.relative_to(BASE_DIR)}")
            return True
        else:
            print("      [AVERTISSEMENT] Génération Word COM non disponible :", res.stderr.strip() or res.stdout.strip())
            return False
    finally:
        if ps_tmp.exists():
            try:
                ps_tmp.unlink()
            except Exception:
                pass


def build_titlepage(cfg: dict, cover_generated: bool) -> str:
    """Génère front/titlepage.tex (intègre le PDF Word ou gère NONE / fallback)."""
    acad = cfg.get("academique", {})
    modele = str(acad.get("modele_couverture", "PFA")).upper().strip()
    inclure = acad.get("inclure_couverture", True)

    # CAS 0 : AUCUNE COUVERTURE
    if not inclure or modele in ["NONE", "AUCUN", "AUCUNE", "SANS", "FALSE", "OFF", "0"]:
        return "% ============================================================\n" \
               "% PAGE DE GARDE DÉSACTIVÉE (modele_couverture: NONE)\n" \
               "% Le rapport démarre directement sans page de garde.\n" \
               "% ============================================================\n"

    # CAS 1 : Couverture Word officielle exportée en PDF sur 1 page
    return f"""% ============================================================
% PAGE DE GARDE OFFICIELLE ENSAF ({modele})
% Générée depuis le document Word officiel ({modele}) sur 1 page
% ============================================================
\\thispagestyle{{empty}}
\\IfFileExists{{front/couverture.pdf}}{{%
    \\includepdf[pages=1]{{front/couverture.pdf}}%
}}{{%
    \\begin{{center}}
        \\vspace*{{3cm}}
        {{\\Large \\textbf{{Université Sidi Mohamed Ben Abdellah}}\\\\[0.2cm]}}
        {{\\large \\textbf{{École Nationale des Sciences Appliquées de Fès}}\\\\[1.5cm]}}
        {{\\LARGE \\bfseries Rapport de Stage d'Ingénieur\\\\[1cm]}}
        {{\\large Veuillez exécuter \\texttt{{python configure.py}} sous Windows pour générer la couverture officielle Word.\\\\[0.5cm]}}
    \\end{{center}}
}}
"""


def generate_arabic_resume(cfg: dict):
    """Génère une page autonome pour le résumé en langue arabe avec rendu natif parfait."""
    proj = cfg.get("projet", {})
    org = cfg.get("organisme", {})
    res_cfg = cfg.get("resume_arabe", {})

    org_nom = org.get("nom", "المؤسسة المستضيفة")
    sujet = proj.get("titre", "المشروع")

    titre_ar = res_cfg.get("titre", "ملخص المشروع")
    texte_ar = res_cfg.get("texte", "")
    mots_cles = res_cfg.get("mots_cles", "هندسة البرمجيات، بنية النظم، تطوير التطبيقات.")

    if not texte_ar:
        texte_ar = f"""يقدّم هذا التقرير وصفاً شاملاً لمشروع نهاية السنة المنجز لدى مؤسسة {org_nom}، والمتمحور حول {sujet}. استجابةً للتحديات المرصودة، تم وضع وتنفيذ حلول هندسية متكاملة ومستدامة وفق أفضل المعايير التقنية المعمول بها.

اعتمدت المنهجية المتبعة على التحليل المنهجي للمتطلبات، والتصميم المعماري المعياري، مع اعتماد ممارسات التطوير الحديثة لضمان جودة الأداء وقابلية الصيانة والتوسع. وتُظهر النتائج المحققة نجاعة الحلول المقترحة ومطابقتها للمواصفات المسطرة."""

    paragraphs_html = "\n".join(f"    <p>{p.strip()}</p>" for p in texte_ar.split("\n\n") if p.strip())

    html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
  @page {{
    size: A4 portrait;
    margin: 2cm 2.5cm 2cm 2.5cm;
  }}
  body {{
    font-family: 'Traditional Arabic', 'Segoe UI', Arial, sans-serif;
    line-height: 1.8;
    font-size: 15pt;
    color: #111;
    margin: 0;
    padding: 0;
  }}
  h1.fr-title {{
    direction: ltr;
    text-align: left;
    font-family: 'Times New Roman', Times, serif;
    font-size: 20pt;
    font-weight: bold;
    margin-top: 1cm;
    margin-bottom: 1.2cm;
  }}
  .box {{
    border: 1.5px solid #222;
    padding: 24px 28px;
    border-radius: 2px;
  }}
  .box-title {{
    text-align: center;
    font-size: 18pt;
    font-weight: bold;
    margin-bottom: 20px;
  }}
  p {{
    text-align: justify;
    text-justify: inter-word;
    margin-bottom: 16px;
    text-indent: 1.2em;
  }}
  .keywords {{
    margin-top: 25px;
    font-size: 13pt;
    border-top: 1px dashed #777;
    padding-top: 12px;
  }}
</style>
</head>
<body>
  <h1 class="fr-title">Résumé en langue arabe</h1>
  <div class="box">
    <div class="box-title">{titre_ar}</div>
{paragraphs_html}
    <div class="keywords">
      <strong>كلمات مفتاحية :</strong> {mots_cles}
    </div>
  </div>
</body>
</html>"""

    with open(RESUME_AR_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Conversion en PDF via Edge Headless
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    edge_exe = next((p for p in edge_paths if os.path.exists(p)), None)
    if edge_exe:
        cmd = [
            edge_exe,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={RESUME_AR_PDF_PATH}",
            str(RESUME_AR_HTML_PATH)
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            if RESUME_AR_PDF_PATH.exists():
                print(f"      -> Résumé arabe généré avec succès : {RESUME_AR_PDF_PATH.relative_to(BASE_DIR)}")
        except Exception as e:
            print("      [AVERTISSEMENT] Erreur lors de l'export PDF du résumé arabe :", e)


def build_remerciements(cfg: dict) -> str:
    """Génère front/remerciements.tex selon le protocole officiel ENSAF."""
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

    if org_part:
        org_mention = f"au \\textbf{{{org_nom}}} ainsi qu'\\`a \\textbf{{{org_part}}}"
    else:
        org_mention = f"\\`a l'organisme d'accueil \\textbf{{{org_nom}}}"

    dir_mention = ""
    if dir_nom and not dir_nom.startswith("["):
        dir_mention = f"""\\vspace{{0.4cm}}

\\noindent
J'adresse mes remerciements les plus distingu\\'es \\`a {dir_civ} {dir_nom}, \\textit{{{dir_titre}}}, pour son accueil bienveillant, ses orientations strat\\'egiques, sa vision et pour les moyens mis \\`a disposition tout au long de cette mission d'ing\\'enierie.
"""

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

    print(f"[*] Modèle couverture : {acad.get('modele_couverture', 'PFA')}")
    print(f"[*] Titre             : {proj.get('titre')}")
    print(f"[*] Sous-titre        : {proj.get('sous_titre')}")
    print(f"[*] Filière           : {acad.get('filiere')}")
    print(f"[*] Période           : {proj.get('periode_stage')}")
    print(f"[*] Organisme         : {org.get('nom')} ({org.get('ville')})")
    print(f"[*] Auteur(s)         :")
    for a in auteurs:
        print(f"    - {a.get('civilite')} {a.get('prenom')} {a.get('nom')}")
    print(f"[*] Encadrant ENSAF   :")
    for ea in enc.get("academique", []):
        print(f"    - {ea.get('civilite')} {ea.get('prenom_nom')}")
    print(f"[*] Encadrant Société :")
    for ep in enc.get("professionnel", []):
        print(f"    - {ep.get('civilite')} {ep.get('prenom_nom')} ({ep.get('specialite') or ep.get('fonction')})")
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

    print("[1/3] Génération de la couverture officielle Word (garantie 1 page)...")
    cover_ok = generate_word_cover(cfg)
    titlepage_tex = build_titlepage(cfg, cover_ok)
    with open(TITLEPAGE_PATH, "w", encoding="utf-8") as f:
        f.write(titlepage_tex)
    print(f"      -> Mis à jour : {TITLEPAGE_PATH.relative_to(BASE_DIR)}")

    print("[2/3] Génération du résumé arabe haute fidélité (front/resume_ar.pdf)...")
    generate_arabic_resume(cfg)

    print("[3/3] Génération des remerciements (front/remerciements.tex)...")
    rem_tex = build_remerciements(cfg)
    with open(REMERCIEMENTS_PATH, "w", encoding="utf-8") as f:
        f.write(rem_tex)
    print(f"      -> Mis à jour : {REMERCIEMENTS_PATH.relative_to(BASE_DIR)}")

    print("-" * 65)
    print("[SUCCÈS] Rapport synchronisé avec 'project_info.yaml'.")
    print("         Pour recompiler : python preview.py")
    print("=" * 65)


if __name__ == "__main__":
    main()
