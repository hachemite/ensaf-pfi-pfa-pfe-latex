# 🎓 Modèle de Rapport de Projet de Fin d'Année (PFA) / PFE — ENSAF

[![Check & Compile](https://github.com/hachemite/ensaf-pfi-pfa-pfe-latex/actions/workflows/check.yml/badge.svg)](https://github.com/hachemite/ensaf-pfi-pfa-pfe-latex/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Changelog](https://img.shields.io/badge/Changelog-Keep%20a%20Changelog-blue)](CHANGELOG.md)

Modèle LaTeX officiel et standardisé pour la rédaction des rapports de stage, PFA et PFE à l'**École Nationale des Sciences Appliquées de Fès (ENSAF)**.

> 💡 **Exemple complet de démonstration / Fully-filled example :**  
> Vous souhaitez voir un rapport d'ingénierie 100% complété et compilé avec ce modèle ?  
> 👉 **[Consulter l'exemple complet sur la branche `example-filled-report`](https://github.com/hachemite/ensaf-pfi-pfa-pfe-latex/tree/example-filled-report)** *(avec son PDF généré [`example.pdf`](https://github.com/hachemite/ensaf-pfi-pfa-pfe-latex/blob/example-filled-report/example.pdf))*.
> 
> 📋 **Journal des modifications :** Consultez le **[`CHANGELOG.md`](CHANGELOG.md)** pour l'historique complet des versions et des évolutions du modèle.

---

## 🚀 Comment Intégrer ce Modèle dans Votre Projet

Vous pouvez utiliser ce dépôt de plusieurs manières selon votre organisation de travail :

### Option 1 : Nouveau dépôt indépendant (Recommandé)
- Cliquez sur le bouton vert **"Use this template"** en haut à droite sur GitHub pour créer votre propre dépôt de rapport.
- Ou clonez-le directement en local :
  ```bash
  git clone https://github.com/hachemite/ensaf-pfi-pfa-pfe-latex.git mon-rapport-pfa
  cd mon-rapport-pfa
  ```

### Option 2 : Dans un sous-dossier de votre projet de code
Si vous souhaitez conserver votre code et votre rapport dans le même dépôt Git :
```bash
# Dans la racine de votre projet logiciel :
git submodule add https://github.com/hachemite/ensaf-pfi-pfa-pfe-latex.git docs/rapport
# ou cloner directement comme sous-dossier :
git clone https://github.com/hachemite/ensaf-pfi-pfa-pfe-latex.git rapport
```

### Option 3 : Import 1-Clic sur Overleaf
- Téléchargez l'archive ZIP du projet ou exécutez `python zip_for_overleaf.py`.
- Sur [Overleaf](https://www.overleaf.com), cliquez sur **New Project** $\rightarrow$ **Upload Project** et déposez l'archive.

---

## 🤖 Rédiger avec un Assistant IA (Agent-Driven Workflow)

Ce dépôt est spécialement conçu pour être piloté par un assistant IA (**Cursor**, **Claude Code**, **Google Antigravity**, **GitHub Copilot**, **ChatGPT/Codex**).

### 🎯 Le Prompt de Démarrage Unique (`PROMPT_START.md`)
Dès l'ouverture du projet dans votre éditeur avec agent :
1. Ouvrez le fichier **[`PROMPT_START.md`](PROMPT_START.md)**.
2. Copiez l'intégralité du texte et collez-le dans le chat de votre assistant IA.

### 🔄 Ce que l'agent réalise pour vous automatiquement :
1. **Analyse de vos documents** : Il vous demande vos notes brutes ou analyse le code source de votre projet.
2. **Configuration ciblée** : Il déduit les informations requises, vous pose *uniquement* les questions manquantes pour [`project_info.yaml`](project_info.yaml) et exécute `python configure.py`.
3. **Plan de contenu validé** : Il propose un plan détaillé chapitre par chapitre respectant la structure officielle ENSAF et attend votre feu vert avant de rédiger.
4. **Rédaction guidée** : Il rédige les chapitres selon les règles strictes de [`AGENTS.md`](AGENTS.md) (forme impersonnelle, transitions `\sectionTransition`, diagramme de Gantt en `pgfgantt`).
5. **🔁 Boucle d'auto-correction automatique** : Après chaque chapitre, l'agent lance automatiquement `python lint.py`, corrige directement les avertissements dans le fichier LaTeX, et réitère jusqu'à obtention d'un rapport 100% conforme.

---

## ⚡ Démarrage Rapide (Workflow Local)

### 1. Personnaliser vos informations (Formulaire & IA)
Renseignez vos informations dans **[`project_info.yaml`](project_info.yaml)** :
- **`modele_couverture`** :
  - `"PFA"` : Stage d'Application (2ème année cycle ingénieur / 4A)
  - `"PFE"` : Projet de Fin d'Études (3ème année cycle ingénieur / 5A)
  - `"INITIATION"` : Stage d'Initiation (1ère année cycle ingénieur / 3A)
  - `"NONE"` : SANS couverture (le rapport démarre directement avec les dédicaces)
- **Auteurs :** supporte 1 étudiant (solo), binôme ou trinôme.
- **Entreprise & Sujet :** Nom, ville, sujet de stage, période.
- **Encadrants & Jury :** Noms et qualités des encadrants et membres du jury.

Puis appliquez la configuration automatique :
```bash
python configure.py
```
*(Génère automatiquement la couverture Word officielle garantie sur 1 page `front/couverture.pdf`, le résumé en arabe haute fidélité `front/resume_ar.pdf`, et les remerciements protocolaires `front/remerciements.tex`).*

### 2. Compiler localement
- **Option A (Double-clic) :** Double-cliquez sur [`compile.bat`](compile.bat).
- **Option B (Python) :** Lancez dans votre terminal :
  ```bash
  python preview.py
  ```
  *(Compile le document avec Tectonic et ouvre directement `main.pdf`)*

### 3. Vérifier la conformité académique (Linter)
Avant de soumettre votre rapport, vérifiez automatiquement le respect des règles ENSAF (pas de "je", pas de soulignage, captions obligatoires, sous-sections équilibrées, etc.) :
```bash
python lint.py
```

### 4. Intégration Continue (GitHub Actions CI)
À chaque `git push` ou pull request sur la branche `main` :
- Le workflow [`.github/workflows/check.yml`](.github/workflows/check.yml) s'exécute automatiquement.
- Il valide la conformité académique via `lint.py`.
- Il compile le rapport avec la chaîne complète LaTeX (`pdflatex → biber/bibtex → pdflatex → pdflatex`).
- Il publie le PDF compilé (`main.pdf`) dans les artefacts de téléchargement de GitHub Actions sans nécessiter de compilation locale.

### 5. Exporter pour Overleaf
Pour rédiger en ligne sur Overleaf avec vos binômes :
- Double-cliquez sur [`zip_overleaf.bat`](zip_overleaf.bat) (ou lancez `python zip_for_overleaf.py`).
- Déposez l'archive générée **`overleaf_ensaf_template.zip`** sur [Overleaf](https://www.overleaf.com) (*New Project -> Upload Project*).
- **Moteur vérifié :** Compile directement avec le compilateur standard **pdfLaTeX** d'Overleaf.

---

## 📁 Organisation des Fichiers

| Dossier / Fichier | Description |
| :--- | :--- |
| [`project_info.yaml`](project_info.yaml) | Formulaire de métadonnées (auteurs, entreprise, encadrants, jury) |
| [`configure.py`](configure.py) | Script de synchronisation automatique des pages liminaires |
| [`main.tex`](main.tex) | Fichier racine du projet |
| [`ensaf.cls`](ensaf.cls) | Classe de style (police Times 12pt, marges 2.5cm/2cm, en-têtes) |
| [`front/`](front/) | Dédicaces, Remerciements, Résumés (FR/EN/AR), Abréviations |
| [`chapters/`](chapters/) | Chapitres 0 à 4 (Introduction, Cadre, État de l'art, Réalisation, Conclusion) |
| [`back/`](back/) | Annexes, glossaire et bibliographie (`bibliographie.bib`) |
| [`figures/`](figures/) | Vos captures d'écran et schémas (`ch1/`, `ch2/`, `ch3/`) |
| [`TODO.md`](TODO.md) | Suivi d'avancement chapitre par chapitre |
| [`GUIDE_UTILISATION_TEMPLATE.md`](GUIDE_UTILISATION_TEMPLATE.md) | Guide détaillé des commandes et syntaxes LaTeX |

---

## 📋 Normes ENSAF Principales
- **Volume cible :** 30 à 40 pages (PFA 4ème année) / 50 à 70 pages (PFE 5ème année).
- **Style :** Forme impersonnelle (proscrire le "je" sauf en dédicaces/remerciements).
- **Titres :** Grande lettre, centrés sur page dédiée (`\finPageTitre`), sans deux-points.
- **Figures / Tableaux :** Numérotation `Nc.No` avec légende (`\caption`) systématique.

---

## 🏛️ Provenance & Remerciements (Provenance & Acknowledgments)

> **Projet indépendant & non officiel**  
> Ce modèle implémente les exigences typographiques du guide officiel de rédaction de l'**ENSAF (École Nationale des Sciences Appliquées de Fès)** et intègre les directives méthodologiques du **Pr. Rassil** (encadrante académique).  
> 
> Il s'agit d'un travail indépendant développé par **Hachem Squalli El Houssaini**, sans affiliation institutionnelle ni approbation officielle de l'administration de l'ENSAF. Les étudiants doivent s'assurer de la conformité de leur version finale auprès de leur propre encadrant.  
> 
> *This template implements the formatting requirements of ENSAF's official redaction guide and incorporates methodological guidance from Pr. Rassil (academic supervisor). It is an independent, unofficial project by Hachem Squalli El Houssaini and is not officially endorsed by ENSAF.*

---

## 📄 Licence (License)

Ce projet est distribué sous licence open-source **[MIT](LICENSE)**.  
Copyright (c) 2026 **Hachem Squalli El Houssaini and Contributors**. Vous êtes libres de l'utiliser, l'adapter et le redistribuer pour vos travaux académiques et professionnels.
