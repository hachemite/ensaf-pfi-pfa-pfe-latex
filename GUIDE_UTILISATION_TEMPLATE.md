# Guide Pratique : Utilisation du Modèle LaTeX ENSAF

Ce guide est le **manuel d'utilisation pratique** du modèle LaTeX qui vous a été préparé. Il vous explique pas à pas comment personnaliser chaque section, insérer vos images, gérer la bibliographie et compiler votre rapport.

---

## 1. Structure du Projet

```text
cmrpi/
├── main.tex                    # Fichier racine (point d'entrée principal)
├── ensaf.cls                   # Classe LaTeX (styles, marges, polices, en-têtes)
├── compile.bat                 # Script de compilation rapide Windows
├── preview.py                  # Script Python : compile et ouvre le PDF automatiquement
├── zip_overleaf.bat            # Script 1-clic pour créer l'archive Overleaf
├── zip_for_overleaf.py         # Script Python de compression Overleaf
│
├── front/                      # Pages liminaires (avant-corps)
│   ├── titlepage.tex           # Page de garde officielle ENSAF
│   ├── dedicace.tex            # Dédicaces (centrées)
│   ├── remerciements.tex       # Remerciements
│   ├── resume-fr.tex           # Résumé en français + mots-clés
│   ├── resume-en.tex           # Abstract en anglais + keywords
│   ├── resume-ar.tex           # Résumé en arabe + mots-clés
│   └── abreviations.tex        # Tableau des abréviations & sigles
│
├── chapters/                   # Chapitres du rapport
│   ├── 00-introduction-generale.tex
│   ├── 01-cadre-general.tex
│   ├── 02-etat-art.tex
│   ├── 03-realisation.tex
│   └── 04-conclusion-perspectives.tex
│
├── back/                       # Fin du document
│   ├── annexes.tex             # Glossaire et spécifications techniques
│   └── bibliographie.bib       # Fichier BibTeX des références
│
├── figures/                    # Dossier contenant vos images et diagrammes
│   ├── ch1/                    # Images du Chapitre 1
│   ├── ch2/                    # Images du Chapitre 2
│   └── ch3/                    # Images du Chapitre 3
│
└── logos/                      # Logos
    ├── logo-ensaf.png          # Logo ENSAF
    └── logo-entreprise.png     # Logo de votre entreprise d'accueil
```

---

## 2. Comment Démarrer et Remplir le Rapport

### Étape 1 : Renseigner vos métadonnées (`project_info.yaml`)
La méthode recommandée consiste à modifier le fichier central **[`project_info.yaml`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/project_info.yaml)** :
- **`modele_couverture`** : Choisissez `"PFA"` (Stage d'Application 2A), `"PFE"` (3A), `"INITIATION"` (1A), ou `"NONE"` (sans couverture).
- Vos informations : titre, auteurs (solo, binôme, trinôme), organisme d'accueil, dates de stage, encadrants et membres du jury.

Puis appliquez la configuration automatique :
```bash
python configure.py
```
Ce script :
1. Remplit automatiquement le document Word officiel correspondant dans [`couvertures_rapport_stage_ensaf/`](file:///c:/Users/squal/Documents/rapport_pfa/cmrpi/couvertures_rapport_stage_ensaf/).
2. Compacte le texte pour garantir **strictement 1 seule page** (`front/couverture.pdf`).
3. Génère le résumé arabe haute fidélité (`front/resume_ar.pdf`) avec le moteur natif sans bordure superflue.
4. Rédige les remerciements protocolaires dans `front/remerciements.tex`.

> **Note :** Si vous souhaitez afficher la page de garde dans le PDF généré, décommentez la ligne `\input{front/titlepage}` au début de `main.tex`.

---

### Étape 2 : Remplir les pages d'en-tête (`front/`)

1. **Dédicaces (`front/dedicace.tex`) :**
   - Le texte est **automatiquement centré** et en italique Times.
   - Remplacez simplement `[Votre Prénom]` à la fin.

2. **Remerciements (`front/remerciements.tex`) :**
   - Complétez les noms de l'entreprise, de vos tuteurs et des membres de votre équipe.

3. **Résumés (`front/resume-fr.tex`, `resume-en.tex`, `resume-ar.tex`) :**
   - Remplissez les 3 résumés (français, anglais, arabe) d'une dizaine de lignes chacun.
   - Indiquez 3 à 5 mots-clés pertinents par langue.

4. **Abréviations (`front/abreviations.tex`) :**
   - Ajoutez ou supprimez des lignes dans le tableau `tabularx` :
     ```latex
     \textbf{AWS} & Amazon Web Services (Plateforme cloud) \\
     ```

---

### Étape 3 : Rédiger les Chapitres (`chapters/`)

Chaque chapitre possède une commande spéciale et une section de transition :

1. **Page de titre de chapitre seule :**
   Après chaque `\chapter{...}`, la commande `\finPageTitre` est déjà placée pour isoler le titre sur sa propre page comme l'exige l'ENSAF.

2. **Section de conclusion / transition :**
   À la fin de chaque chapitre, utilisez la commande :
   ```latex
   \sectionTransition{%
   Ce chapitre a présenté... Le chapitre suivant sera consacré à...
   }
   ```

---

## 3. Commandes Utiles & Exemples Prêts à l'Emploi

### A. Insérer une Figure (Image / Capture d'écran)
Placez votre image dans le dossier `figures/ch1/`, `figures/ch2/` ou `figures/ch3/`, puis insérez :

```latex
\begin{figure}[H]
\centering
\IfFileExists{figures/ch2/mon_diagramme.png}{%
    \includegraphics[width=0.85\textwidth]{figures/ch2/mon_diagramme.png}%
}{%
    \fbox{\parbox[c][5cm][c]{0.85\textwidth}{\centering \textit{[Image en attente]}}}%
}
\caption{Diagramme de cas d'utilisation du système}
\label{fig:mon-diagramme}
\end{figure}
```
*Pour y faire référence dans votre texte :* `Comme illustré par la Figure~\ref{fig:mon-diagramme}...`

---

### B. Insérer un Tableau Propre
Utilisez l'environnement `tabularx` configuré pour occuper automatiquement la largeur de page :

```latex
\begin{table}[H]
\centering
\begin{tabularx}{\textwidth}{p{3.5cm} X c}
\toprule
\textbf{Critère} & \textbf{Description} & \textbf{Statut} \\
\midrule
Performance & Temps de réponse inférieur à 200 ms & Atteint \\
Sécurité    & Authentification par jetons JWT    & Validé \\
\bottomrule
\end{tabularx}
\caption{Synthèse des exigences non-fonctionnelles}
\label{tab:exigences}
\end{table}
```

---

### C. Insérer une Équation Mathématique
```latex
\begin{equation}
    E = m \cdot c^2
    \label{eq:energie}
\end{equation}
```
*Pour y faire référence :* `Selon l'équation~\eqref{eq:energie}...`

---

### D. Citer des Références Bibliographiques
1. Ajoutez votre référence dans `back/bibliographie.bib` :
   ```bibtex
   @book{sommerville2016,
     author    = {Ian Sommerville},
     title     = {Software Engineering},
     edition   = {10th},
     publisher = {Pearson},
     year      = {2016}
   }
   ```
2. Citez-la dans votre texte avec :
   ```latex
   Comme l'indique Sommerville~\cite{sommerville2016}, la séparation des préoccupations...
   ```

---

### E. Modifier le Diagramme de Gantt (`chapters/01-cadre-general.tex`)
Le diagramme de Gantt est codé nativement en LaTeX (`pgfgantt`). Vous pouvez modifier directement les semaines et les intitulés sans logiciel externe :

```latex
\begin{ganttchart}[...]{1}{10}
\gantttitle{Semaines}{10}\\
\gantttitlelist{1,...,10}{1}\\
\ganttbar{Analyse & Spécifications}{1}{2}\\
\ganttbar{Conception logicielle}{3}{5}\\
\ganttbar{Développement & Tests}{5}{9}\\
\ganttbar{Clôture & Rédaction}{9}{10}
\end{ganttchart}
```

---

## 4. Compilation et Prévisualisation

### 🔹 Méthode 1 : Double-clic Windows (Recommandé)
- Double-cliquez sur `compile.bat`.
- Le script compile le document avec Tectonic (ou pdflatex) et génère `main.pdf`.

### 🔹 Méthode 2 : Via Python
- Ouvrez un terminal dans le dossier du projet et tapez :
  ```bash
  python preview.py
  ```
- Le script compile et **ouvre directement le fichier PDF** dans votre lecteur par défaut.

---

## 5. Exportation vers Overleaf (En 1 Seul Clic)

Pour travailler sur Overleaf en ligne :

1. Double-cliquez sur **`zip_overleaf.bat`** (ou exécutez `python zip_for_overleaf.py`).
2. Le fichier **`overleaf_ensaf_template.zip`** est créé à la racine du projet.
3. Sur votre compte [Overleaf](https://www.overleaf.com) :
   - Cliquez sur **New Project** $\rightarrow$ **Upload Project**.
   - Déposez le fichier **`overleaf_ensaf_template.zip`**.
4. Overleaf compile immédiatement votre projet en ligne !
