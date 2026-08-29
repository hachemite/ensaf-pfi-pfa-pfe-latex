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

# Fichiers / motifs à exclure
EXCLUDE_PATTERNS = {
    'main.pdf', '.zip', '.git', '__pycache__', '.vscode', '.idea',
    '.aux', '.bbl', '.blg', '.toc', '.lof', '.lot', '.out', '.fls', '.fdb_latexmk', '.synctex.gz'
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
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in ALLOWED_EXTENSIONS or file == '.gitkeep':
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, WORKSPACE)
                        
                        # Vérifier exclusion
                        if any(exc in file for exc in EXCLUDE_PATTERNS):
                            continue
                        
                        zipf.write(full_path, arcname=rel_path)
                        files_added.append(rel_path)

    print("=" * 60)
    print("  EXPORTATION DU PROJET POUR OVERLEAF")
    print("=" * 60)
    print(f"\n[OK] Archive générée avec succès : {output_filename}")
    print(f"[+] Total fichiers inclus : {len(files_added)}")
    print(f"[+] Emplacement : {output_path}")
    print("\nComment l'utiliser sur Overleaf :")
    print("  1. Allez sur https://www.overleaf.com")
    print("  2. Cliquez sur 'New Project' -> 'Upload Project'")
    print(f"  3. Sélectionnez le fichier '{output_filename}'")
    print("  4. Overleaf compilera automatiquement votre rapport !")
    print("=" * 60)
    return output_path

if __name__ == "__main__":
    out_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT_ZIP
    create_overleaf_zip(out_name)
