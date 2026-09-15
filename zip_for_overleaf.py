"""
Script pour archiver et exporter le projet LaTeX vers Overleaf.
Crée une archive .zip propre contenant uniquement les fichiers sources nécessaires.
Usage : python zip_for_overleaf.py [nom_archive.zip]
"""

import os
import sys
import zipfile

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_ZIP = "overleaf_ensaf_template.zip"

# Extensions et dossiers à inclure
ALLOWED_EXTENSIONS = {'.tex', '.cls', '.bib', '.png', '.jpg', '.jpeg', '.pdf', '.gitkeep', '.eps'}
ALLOWED_ROOT_FILES = {'main.tex', 'ensaf.cls'}
INCLUDE_DIRS = {'front', 'chapters', 'back', 'figures', 'logos'}

# Fichiers et motifs à exclure
EXCLUDE_FILENAMES = {'main.pdf', '.gitignore', '.gitattributes', '.DS_Store', 'Thumbs.db'}
EXCLUDE_DIR_NAMES = {'.git', '__pycache__', '.vscode', '.idea'}
EXCLUDE_EXTENSIONS = {
    '.aux', '.bbl', '.blg', '.toc', '.lof', '.lot', '.out', '.fls',
    '.fdb_latexmk', '.synctex.gz', '.zip', '.log', '.bcf', '.run.xml'
}

def create_overleaf_zip(output_filename=DEFAULT_OUTPUT_ZIP):
    output_path = os.path.join(WORKSPACE, output_filename)
    
    # Supprimer l'ancienne archive si elle existe
    if os.path.exists(output_path):
        os.remove(output_path)
    
    files_added = []
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 1. Fichiers à la racine
        for root_file in ALLOWED_ROOT_FILES:
            full_path = os.path.join(WORKSPACE, root_file)
            if os.path.exists(full_path):
                zipf.write(full_path, arcname=root_file)
                files_added.append(root_file)
        
        # 2. Dossiers inclus
        for directory in INCLUDE_DIRS:
            dir_path = os.path.join(WORKSPACE, directory)
            if not os.path.exists(dir_path):
                continue
            for root, dirs, files in os.walk(dir_path):
                # Filtrer les dossiers internes à exclure
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIR_NAMES]
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if file in EXCLUDE_FILENAMES or ext in EXCLUDE_EXTENSIONS:
                        continue
                    if ext in ALLOWED_EXTENSIONS or file == '.gitkeep':
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, WORKSPACE).replace('\\', '/')
                        zipf.write(full_path, arcname=rel_path)
                        files_added.append(rel_path)

    has_cover = any(f.endswith('couverture.pdf') for f in files_added)
    has_ar = any(f.endswith('resume_ar.pdf') for f in files_added)

    print("=" * 60)
    print("  EXPORTATION DU PROJET POUR OVERLEAF")
    print("=" * 60)
    print(f"\n[OK] Archive generee avec succes : {output_filename}")
    print(f"[+] Total fichiers inclus : {len(files_added)}")
    print(f"[+] Emplacement : {output_path}")
    print("\nEtat des composants pre-generes :")
    if has_cover:
        print("  [OK] Page de garde officielle Word incluse (front/couverture.pdf)")
    else:
        print("  [--] Page de garde Word non incluse (repli LaTeX natif actif)")
        print("       Astuce : lancez d'abord 'python configure.py' pour l'integrer au zip.")
    if has_ar:
        print("  [OK] Resume en langue arabe inclus (front/resume_ar.pdf)")
    else:
        print("  [--] Resume arabe PDF non inclus (repli LaTeX natif actif)")
    
    print("\nInstructions d'importation Overleaf :")
    print("  1. Connectez-vous sur https://www.overleaf.com")
    print("  2. Cliquez sur 'New Project' -> 'Upload Project'")
    print(f"  3. Deposez l'archive '{output_filename}'")
    print("  4. Le projet compile avec le compilateur standard pdfLaTeX.")
    print("=" * 60)
    return output_path

if __name__ == "__main__":
    out_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT_ZIP
    create_overleaf_zip(out_name)
