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

## 2. Intégration du Modèle dans Vos Projets

### 🔹 Option A : Utilisation en Dépôt Autonome (Nouveau Rapport)
Pour créer votre propre dépôt de rapport à partir de ce template :
- Cliquez sur **Use this template** en haut du dépôt GitHub, ou clonez-le directement :
  ```bash
  git clone https://github.com/hachemite/ensaf-pfi-pfa-pfe-latex.git mon-rapport
  cd mon-rapport
  ```

### 🔹 Option B : Intégration dans un Projet Logiciel Existant
Pour documenter un projet existant (par exemple dans un dossier `docs/` ou `rapport/`) :
```bash
# À la racine de votre projet de code :
git submodule add https://github.com/hachemite/ensaf-pfi-pfa-pfe-latex.git docs/rapport
```

### 🔹 Option C : Importation Directe sur Overleaf
- Exécutez `python zip_for_overleaf.py` (ou téléchargez le ZIP depuis GitHub).
- Importez l'archive sur Overleaf via **New Project $\rightarrow$ Upload Project**.

---

## 3. Rédaction Assistée par IA (`PROMPT_START.md`)

Le modèle a été optimisé pour être piloté par des assistants IA de pointe (**Cursor**, **Claude Code**, **Google Antigravity**, **GitHub Copilot**, **ChatGPT**) :

1. Ouvrez le projet dans votre IDE IA.
2. Copiez le prompt contenu dans **[`PROMPT_START.md`](PROMPT_START.md)** et collez-le dans la discussion de votre agent.
3. L'assistant exécutera automatiquement le cycle en 6 étapes :
   - Ingestion de vos notes et analyse de votre code source.
   - Questions ciblées pour compléter [`project_info.yaml`](project_info.yaml) et synchronisation via `python configure.py`.
   - Proposition d'un plan de sous-sections chapitre par chapitre pour validation.
   - Rédaction rigoureuse sous les directives académiques de [`AGENTS.md`](AGENTS.md).
   - **Boucle d'auto-correction automatique** : l'agent lance `python lint.py`, corrige immédiatement dans les fichiers `.tex` les alertes soulevées, et répète jusqu'à validation sans erreur.
   - Vérification des listes transversales (`abreviations.tex`, `annexes.tex`, `bibliographie.bib`).

---

## 4. Comment Démarrer et Remplir le Rapport Manuellement

### Étape 1 : Renseigner vos métadonnées (`project_info.yaml`)
La méthode recommandée consiste à modifier le fichier central **[`project_info.yaml`](project_info.yaml)** :

| Option `modele_couverture` | Usage / Niveau ENSAF | Fichier source Word officiel |
| :--- | :--- | :--- |
| **`"PFA"`** *(défaut)* | Stage d'Application (2ème année / 4A) | `couvertures_rapport_stage_ensaf/Stage_Application_2A_PFA_csa.docx` |
| **`"PFE"`** | Projet de Fin d'Études (3ème année / 5A) | `couvertures_rapport_stage_ensaf/Projet_Fin_Etudes_3A_PFE_cpfe.docx` |
| **`"INITIATION"`** | Stage d'Initiation (1ère année / 3A) | `couvertures_rapport_stage_ensaf/Stage_Initiation_1A_csi.docx` |
| **`"NONE"`** | **Sans couverture** (démarre direct aux dédicaces) | *(Aucune page de garde insérée)* |

Renseignez également :
- **Auteurs :** 1 étudiant (solo), binôme ou trinôme (il suffit de décommenter les blocs dans `project_info.yaml`).
- **Entreprise & Sujet :** Nom de l'organisme, ville, titre et période de stage.
- **Encadrement :** Encadrant pédagogique ENSAF et encadrant professionnel en société.
- **Jury :** Noms et qualités des membres du jury.
- **Résumé en arabe :** Section `resume_arabe` (titre `ملخص`, texte et mots-clés).

Puis appliquez la configuration automatique :
```bash
python configure.py
```
Ce script :
1. Remplit automatiquement le document Word officiel correspondant dans [`couvertures_rapport_stage_ensaf/`](couvertures_rapport_stage_ensaf/).
2. Compacte le texte pour garantir **strictement 1 seule page** (`front/couverture.pdf`) avec un encodage UTF-8 parfait.
3. Génère le résumé arabe haute fidélité (`front/resume_ar.pdf`) avec polices natives Windows sans bordure artificielle.
4. Rédige les remerciements protocolaires personnalisés dans `front/remerciements.tex`.

---

### Étape 2 : Personnaliser les pages d'en-tête (`front/`)

1. **Dédicaces (`front/dedicace.tex`) :**
   - Le texte est **automatiquement centré** et en italique Times.
   - Remplacez simplement `[Votre Prénom]` à la fin.

2. **Remerciements (`front/remerciements.tex`) :**
   - Générés automatiquement par `configure.py` avec le protocole officiel ENSAF.
   - Si vous souhaitez ajouter un mot personnel, utilisez le champ `remerciements.mot_personnel` dans `project_info.yaml`.

3. **Résumés (`front/resume-fr.tex`, `resume-en.tex`, `resume-ar.tex`) :**
   - Remplissez les résumés en français (`resume-fr.tex`) et en anglais (`resume-en.tex`) d'une dizaine de lignes chacun avec 3 à 5 mots-clés.
   - Le résumé en arabe est généré automatiquement par `configure.py` via la section `resume_arabe` de `project_info.yaml`.

4. **Abréviations (`front/abreviations.tex`) :**
   - Ajoutez ou modifiez vos sigles techniques dans le tableau `tabularx` :
     ```latex
     \textbf{AWS} & Amazon Web Services (Plateforme cloud) \\
     \textbf{API} & Application Programming Interface \\
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

---

## 5. Commandes Utiles & Exemples Prêts à l'Emploi

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

## 6. Compilation, Prévisualisation & CI/CD

### 🔹 Méthode 1 : Double-clic Windows (Recommandé)
- Double-cliquez sur `compile.bat`.
- Le script compile le document avec Tectonic (ou pdflatex) et génère `main.pdf`.

### 🔹 Méthode 2 : Via Python
- Ouvrez un terminal dans le dossier du projet et tapez :
  ```bash
  python preview.py
  ```
- Le script compile et **ouvre directement le fichier PDF** dans votre lecteur par défaut.

### 🔹 Méthode 3 : Compilation Automatique GitHub Actions (CI/CD)
- À chaque `git push` ou pull request sur la branche `main`, le workflow [`.github/workflows/check.yml`](.github/workflows/check.yml) s'exécute automatiquement.
- Il valide la conformité académique via `lint.py` et compile `main.pdf`.
- Vous pouvez télécharger le PDF généré directement depuis l'onglet **Actions** de votre dépôt GitHub sans compiler sur votre machine.

---

## 7. Exportation vers Overleaf

Pour collaborer en ligne sur Overleaf avec vos binômes :

1. Exécutez `python zip_for_overleaf.py` (ou double-cliquez sur `zip_overleaf.bat`).
2. Le fichier **`overleaf_ensaf_template.zip`** est créé à la racine du projet, contenant l'ensemble des sources TeX, figures, logos et composants pré-générés.
3. Sur votre compte [Overleaf](https://www.overleaf.com) :
   - Cliquez sur **New Project** $\rightarrow$ **Upload Project**.
   - Déposez le fichier **`overleaf_ensaf_template.zip`**.
4. **Compilation vérifiée :** Le projet utilise le moteur standard **pdfLaTeX** d'Overleaf.
   - Si vous avez exécuté `python configure.py` au préalable, la couverture officielle Word (`couverture.pdf`) et le résumé arabe (`resume_ar.pdf`) sont automatiquement intégrés.
   - Si ces fichiers ne sont pas présents, le code bascule automatiquement sur des pages liminaires de repli en pur LaTeX (`\IfFileExists`), garantissant une compilation immédiate sans erreur.

---

## 8. Foire Aux Questions (FAQ) & Dépannage

### Q1 : Comment remplacer le logo de mon entreprise ?
Déposez simplement votre logo au format PNG dans le dossier `logos/` sous le nom **`logo-entreprise.png`**. Il sera automatiquement pris en compte sur toutes les pages.

### Q2 : Comment vérifier que mon rapport respecte toutes les règles ENSAF ?
Lancez simplement la commande :
```bash
python lint.py
```
Le linter vérifie :
- L'absence de tournures personnelles ("je", "mon", "nous" dans le corps technique).
- La présence systématique de légendes (`\caption`) et de labels sur toutes les figures et tableaux.
- L'absence de texte souligné (`\underline`) prohibé par le guide officiel.
- L'équilibre des volumes de chapitres.

### Q3 : Puis-je modifier directement la couverture Word manuellement ?
Oui ! Vous pouvez ouvrir directement le fichier Word généré dans `front/couverture.docx` (ou le modèle dans `couvertures_rapport_stage_ensaf/`), faire vos ajustements, puis l'enregistrer sous `front/couverture.pdf`. LaTeX inclura automatiquement votre PDF personnalisé.

### Q4 : Comment fonctionne le résumé en langue arabe ?
Le résumé en arabe est généré au format autonome haute fidélité (`front/resume_ar.pdf`) pour bénéficier du moteur de rendu natif Windows (polices avec ligatures et diacritiques arabes complètes). Il est ensuite fusionné dans le rapport avec son titre de chapitre et sa pagination sans provoquer d'erreur de police LaTeX.

### Q5 : Que faire si je travaille sous Linux ou macOS ?
Si Microsoft Word n'est pas installé sur votre machine :
- Définissez `modele_couverture: "NONE"` dans `project_info.yaml` pour compiler directement sans page de garde.
- Ou convertissez le document Word officiel en PDF avec LibreOffice (`libreoffice --headless --convert-to pdf front/couverture.docx`) et placez le résultat dans `front/couverture.pdf`.
- Vous pouvez également utiliser directement Overleaf via `python zip_for_overleaf.py`.
