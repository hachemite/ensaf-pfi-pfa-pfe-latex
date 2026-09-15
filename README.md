# 🎓 Modèle de Rapport de Projet de Fin d'Année (PFA) / PFE — ENSAF

Modèle LaTeX officiel et standardisé pour la rédaction des rapports de stage, PFA et PFE à l'**École Nationale des Sciences Appliquées de Fès (ENSAF)**.

---

## ⚡ Démarrage Rapide (4 Étapes)

### 0. Personnaliser vos informations (Formulaire & IA)
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

### 1. Compiler localement
- **Option A (Double-clic) :** Double-cliquez sur [`compile.bat`](compile.bat).
- **Option B (Python) :** Lancez dans votre terminal :
  ```bash
  python preview.py
  ```
  *(Compile le document avec Tectonic et ouvre directement `main.pdf`)*

### 2. Vérifier la conformité académique (Linter)
Avant de soumettre votre rapport, vérifiez automatiquement le respect des règles ENSAF (pas de "je", pas de soulignage, captions obligatoires, etc.) :
```bash
python lint.py
```

### 3. Exporter pour Overleaf
Pour rédiger en ligne sur Overleaf avec vos binômes :
- Double-cliquez sur [`zip_overleaf.bat`](zip_overleaf.bat) (ou lancez `python zip_for_overleaf.py`).
- Déposez l'archive générée **`overleaf_ensaf_template.zip`** sur [Overleaf](https://www.overleaf.com) (*New Project -> Upload Project*).
- **Moteur vérifié :** Compile directement avec le compilateur standard **pdfLaTeX** d'Overleaf (avec intégration des composants pré-générés ou repli natif automatique).

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
