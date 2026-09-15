# 🎓 Modèle de Rapport de Projet de Fin d'Année (PFA) / PFE — ENSAF

Modèle LaTeX officiel et standardisé pour la rédaction des rapports de stage, PFA et PFE à l'**École Nationale des Sciences Appliquées de Fès (ENSAF)**.

---

## ⚡ Démarrage Rapide (4 Étapes)

### 0. Personnaliser vos informations (Formulaire & IA)
Renseignez vos informations dans **[`project_info.yaml`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/project_info.yaml)** (titre, solo/binôme/trinôme, entreprise, encadrants ENSAF et société, période de stage, jury), puis appliquez-les automatiquement :
```bash
python configure.py
```
*(Génère automatiquement `front/titlepage.tex` et `front/remerciements.tex` sur mesure).*

### 1. Compiler localement
- **Option A (Double-clic) :** Double-cliquez sur [`compile.bat`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/compile.bat).
- **Option B (Python) :** Lancez dans votre terminal :
  ```bash
  python preview.py
  ```
  *(Compile le document et ouvre directement `main.pdf`)*

### 2. Vérifier la conformité académique (Linter)
Avant de soumettre votre rapport, vérifiez automatiquement le respect des règles ENSAF (pas de "je", pas de soulignage, captions obligatoires, etc.) :
```bash
python lint.py
```

### 3. Exporter pour Overleaf
Pour rédiger en ligne sur Overleaf avec vos binômes :
- Double-cliquez sur [`zip_overleaf.bat`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/zip_overleaf.bat) (ou exécutez `python zip_for_overleaf.py`).
- Glissez-déposez le fichier généré **`overleaf_ensaf_template.zip`** sur [Overleaf](https://www.overleaf.com) (*New Project -> Upload Project*).

---

## 📁 Organisation des Fichiers

| Dossier / Fichier | Description |
| :--- | :--- |
| [`project_info.yaml`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/project_info.yaml) | Formulaire de métadonnées (auteurs, entreprise, encadrants, jury) |
| [`configure.py`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/configure.py) | Script de synchronisation automatique des pages liminaires |
| [`main.tex`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/main.tex) | Fichier racine du projet |
| [`ensaf.cls`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/ensaf.cls) | Classe de style (police Times 12pt, marges 2.5cm/2cm, en-têtes) |
| [`front/`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/front) | Dédicaces, Remerciements, Résumés (FR/EN/AR), Abréviations |
| [`chapters/`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/chapters) | Chapitres 0 à 4 (Introduction, Cadre, État de l'art, Réalisation, Conclusion) |
| [`back/`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/back) | Annexes, glossaire et bibliographie (`bibliographie.bib`) |
| [`figures/`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/figures) | Vos captures d'écran et schémas (`ch1/`, `ch2/`, `ch3/`) |
| [`TODO.md`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/TODO.md) | Suivi d'avancement chapitre par chapitre |
| [`GUIDE_UTILISATION_TEMPLATE.md`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/GUIDE_UTILISATION_TEMPLATE.md) | Guide détaillé des commandes et syntaxes LaTeX |

---

## 📋 Normes ENSAF Principales
- **Volume cible :** 30 à 40 pages (PFA 4ème année) / 50 à 70 pages (PFE 5ème année).
- **Style :** Forme impersonnelle (proscrire le "je" sauf en dédicaces/remerciements).
- **Titres :** Grande lettre, centrés sur page dédiée (`\finPageTitre`), sans deux-points.
- **Figures / Tableaux :** Numérotation `Nc.No` avec légende (`\caption`) systématique.
