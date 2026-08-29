"""
Script de compilation et prévisualisation automatique du rapport LaTeX (ENSAF)
Usage : python preview.py [--open]
"""

import os
import sys
import subprocess
import webbrowser

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
TECTONIC_EXE = os.path.join(os.environ.get('USERPROFILE', ''), '.tectonic_bin', 'tectonic.exe')

def compile_pdf():
    print("[1/2] Compilation du document main.tex...")
    if os.path.exists(TECTONIC_EXE):
        cmd = [TECTONIC_EXE, "main.tex"]
    else:
        cmd = ["pdflatex", "-interaction=nonstopmode", "main.tex"]
    
    res = subprocess.run(cmd, cwd=WORKSPACE)
    if res.returncode == 0 and os.path.exists(os.path.join(WORKSPACE, "main.pdf")):
        print("\n[SUCCÈS] 'main.pdf' a été généré avec succès !")
        return True
    else:
        print("\n[ERREUR] La compilation a échoué.")
        return False

def open_pdf():
    pdf_path = os.path.join(WORKSPACE, "main.pdf")
    if os.path.exists(pdf_path):
        print(f"[2/2] Ouverture de '{pdf_path}'...")
        os.startfile(pdf_path)

if __name__ == "__main__":
    success = compile_pdf()
    if success:
        open_pdf()
