# Guide de Rédaction et de Mise en Forme du Rapport PFA / PFE (ENSAF)

Ce guide récapitule les règles officielles de présentation, de typographie et de structuration du rapport de stage / projet de fin d'année et de fin d'études à l'**ENSAF (École Nationale des Sciences Appliquées de Fès)**, telles qu'établies dans le *Guide officiel de rédaction*.

---

## 1. Respect des Règles de Présentation (Section 2.2 du Guide)

| Règle Officielle | Spécification ENSAF | Implémentation dans la classe `ensaf.cls` |
| :--- | :--- | :--- |
| **2.2.1 Taille du mémoire** | • **30 à 40 pages** pour 4ème année (PFA)<br>• **50 à 70 pages** pour 5ème année (PFE)<br>*(hors annexes)* | Structure dimensionnée pour 4 chapitres de développement équilibrés. |
| **2.2.2 Mise en page** | • Format papier **A4**<br>• Rendu sobre en **Noir & Blanc / Niveaux de gris**<br>• Marges uniformes : Gauche/Droite = **2.5 cm**, Haut/Bas = **2.0 cm** | Configuré via `\usepackage[left=2.5cm,right=2.5cm,top=2cm,bottom=2cm]{geometry}` et palette `grisfonce` / `grisclair`. |
| **2.2.3 Familles de polices** | • Police proportionnelle **« Times »** obligatoire.<br>• Polices Courier et fantaisistes **strictement prohibées**. | Configuré via le package standard `\usepackage{mathptmx}` (Times pour texte et mathématiques). |
| **2.2.4 Tailles et styles** | • Corps du texte en **12 pt** (romain).<br>• Titres hiérarchisés en polices plus grandes.<br>• **Soulignage proscrit** (utiliser gras ou italique). | Corps fixé à `12pt`, titres via `titlesec` en gras sans aucun soulignage. |
| **2.2.5 Espacements & Alignement** | • Texte **justifié** au fer à droite avec césures françaises.<br>• Interligne aéré (**1.5**).<br>• Espacements : **2 lignes** avant `\section`, **1.5 ligne** avant `\subsection`, **1 ligne** avant `\subsubsection`. | `\setstretch{1.5}` et espacements `\titlespacing*` configurés exactement selon la règle. |
| **2.2.6 Pagination** | • Pagination **numérique arabe (1, 2, 3...)** obligatoire.<br>• Positionnée dans le **pied de page**.<br>• Commence dès l'en-tête (Dédicaces) et s'achève aux Annexes. | `\pagenumbering{arabic}` avec `\fancyfoot[R]{\thepage}` et `\fancyfoot[L]{ENSA de Fès}`. |

---

## 2. Règles des En-têtes (*Headers*) et Pieds de Page (*Footers*)

Conformément à la **Section 2.2.2** et à la charte visuelle ENSAF :

1. **En-tête haut (*Header*) :**
   - **Gauche :** Intitulé du chapitre courant (`\leftmark`).
   - **Droite :** Nom de l'école (**ENSAF** en gras).
   - **Ligne de séparation :** Ligne fine discrète de `0.4pt`.
2. **Pied de page (*Footer*) :**
   - **Gauche :** `ENSA de Fès`.
   - **Droite :** Numéro de page en chiffres arabes (`\thepage`).
3. **Premières pages de chapitres (*Style Plain*) :**
   - L'en-tête haut est automatiquement masqué pour ne pas surcharger le titre du chapitre, seul le pied de page avec la pagination et la mention `ENSA de Fès` est affiché.

---

## 3. Règles pour les Flottants, Équations et Bibliographie

### A. Tableaux et Figures (Section 2.4)
- **Numérotation indépendante :** Format `Nc.No` (ex : *Figure 2.1* = première figure du Chapitre 2).
- **Légendes :** Centrées, en italique, police 12pt (`\captionsetup{font={it,small},labelfont={bf,it}}`).
- **Tableaux :** Titre sobre sous le tableau (ou au-dessus).
- **Figures :** Fichiers numériques insérés avec légende descriptive en dessous.

### B. Équations Mathématiques (Section 2.4.4)
- **Symboles scalaires :** En *italique* ($m$, $E$, $c$).
- **Vecteurs et matrices :** En **gras** ($\mathbf{V}$, $\mathbf{M}$).
- **Mise en évidence :** Équation centrée avec numéro `(Nc.No)` tabulé à droite :
  ```latex
  \begin{equation}
      E = m c^2
  \end{equation}
  ```

### C. Références Bibliographiques (Section 2.5)
- **Dans le texte :** `Nom [Numéro]` ou simplement `[Numéro]`. Pour plus de deux auteurs : `Nom et al. [Numéro]`.
- **En fin de document :** Liste classée par **ordre alphabétique** du nom du premier auteur.
- **Documents électroniques :** Indiquer l'URL sans point terminal pour éviter toute confusion.

---

## 4. Guide d'Utilisation et Commandes Pratiques

### A. Compilation Locale
- **Via le script Batch :** Double-cliquez sur `compile.bat` ou lancez :
  ```cmd
  .\compile.bat
  ```
- **Via Python (compilation et ouverture automatique du PDF) :**
  ```bash
  python preview.py
  ```

### B. Exportation vers Overleaf
Pour éditer votre rapport en ligne sur Overleaf en équipe :
1. Lancez le script de packaging :
   ```bash
   python zip_for_overleaf.py
   ```
   *(ou double-cliquez sur `zip_overleaf.bat`)*
2. Le fichier **`overleaf_ensaf_template.zip`** est généré automatiquement.
3. Rendez-vous sur [Overleaf](https://www.overleaf.com) $\rightarrow$ **New Project** $\rightarrow$ **Upload Project** et sélectionnez le fichier zip.

---

## 5. Ce Qu'il Faut Éviter (Recommandations du Jury)

- ❌ **Pas de "je" personnel** dans le corps technique (utiliser la tournure impersonnelle *"Il apparaît que..."* ou le *"nous"* collectif). Le "je" est toléré uniquement dans les remerciements et la conclusion personnelle.
- ❌ **Éviter la rédaction chronologique type journal de bord :** Privilégier une structure logique (*Contexte $\rightarrow$ Analyse $\rightarrow$ Conception $\rightarrow$ Réalisation $\rightarrow$ Résultats*).
- ❌ **Pas de soulignage :** Remplacer par du gras ou de l'italique.
- ❌ **Équilibrer les chapitres :** Veiller à ce que les chapitres de développement aient des volumes comparables.
- ❌ **Respecter les sous-sections :** Toute sous-section `x.1.1` impose l'existence d'une sous-section `x.1.2`.
