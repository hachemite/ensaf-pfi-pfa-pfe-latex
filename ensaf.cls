\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ensaf}[2026/08/29 Classe Rapport ENSAF - Conforme Guide Officiel]
\LoadClass[12pt,a4paper]{report}

% ============================================================
% 1. LANGUES ET ENCODAGES
% ============================================================
\RequirePackage[LAE,T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[arabic,french]{babel}

% ============================================================
% 2. MISE EN PAGE ET MARGES (Section 2.2.2)
% ============================================================
% Marges : Gauche/Droite = 2.5cm, Haut/Bas = 2cm
\RequirePackage[left=2.5cm,right=2.5cm,top=2cm,bottom=2cm,headheight=15pt]{geometry}
\RequirePackage{setspace}
\setstretch{1.5} % Interligne aéré (Section 2.2.5)

% ============================================================
% 3. POLICE TIMES (Section 2.2.3 & 2.2.4)
% ============================================================
% Police proportionnelle Times obligatoire (corps en 12pt)
\RequirePackage{mathptmx}

% ============================================================
% 4. PAGINATION EN CHIFFRES ARABES (Section 2.2.6)
% ============================================================
\pagenumbering{arabic}

% ============================================================
% 5. PALETTE NOIR & BLANC / GRIS (Section 2.2.2)
% ============================================================
\RequirePackage[table]{xcolor}
\definecolor{grisfonce}{gray}{0.3}
\definecolor{grisclair}{gray}{0.85}

% ============================================================
% 6. PACKAGES COMPLÉMENTAIRES (Flottants, Tableaux, Graphiques)
% ============================================================
\RequirePackage{graphicx}
\RequirePackage{float}
\RequirePackage{caption}
% Légendes de figures et tableaux : centrées, italique, 12pt (Section 2.4)
\captionsetup{font={it,small},labelfont={bf,it},justification=centering}
\RequirePackage{booktabs}
\RequirePackage{tabularx}
\RequirePackage{amsmath,amssymb} % Équations mathématiques (Section 2.4.4)
\RequirePackage{hyperref}
\hypersetup{
    hidelinks,
    colorlinks=false,
    pdfborder={0 0 0}
}
\RequirePackage{titlesec}
\RequirePackage{fancyhdr}
\RequirePackage{pgfgantt}
\RequirePackage[toc,page]{appendix}
\RequirePackage[backend=bibtex,style=numeric,sorting=nyt]{biblatex}

% ============================================================
% 7. FORMAT DES TITRES ET ESPACEMENTS (Sections 2.2.4 & 2.2.5)
% ============================================================
% Titre de chapitre : deux lignes horizontales (haut et bas), centré verticalement au milieu de la page
\titleformat{\chapter}[block]%
  {\filcenter\normalfont\huge\bfseries}%
  {\titleline{\titlerule[1.5pt]}\vspace{20pt}\thechapter.\quad}%
  {0pt}%
  {}%
  [\vspace{20pt}\titleline{\titlerule[1.5pt]}]
\titlespacing*{\chapter}{0pt}{0.30\textheight}{0pt}

% Format spécifique pour chapitres non numérotés (\chapter*{...})
\titleformat{name=\chapter,numberless}[display]
  {\centering\normalfont\bfseries}
  {}
  {0pt}
  {\Huge\MakeUppercase}
\titlespacing*{name=\chapter,numberless}{0pt}{0pt}{20pt}

% Espacements conformes au guide (2 lignes avant section, 1.5 avant sous-section, 1 avant sous-sous-section)
\titleformat{\section}
  {\normalfont\Large\bfseries}{\thesection}{1em}{}
\titlespacing*{\section}{0pt}{24pt}{12pt}

\titleformat{\subsection}
  {\normalfont\large\bfseries}{\thesubsection}{1em}{}
\titlespacing*{\subsection}{0pt}{18pt}{8pt}

\titleformat{\subsubsection}
  {\normalfont\normalsize\bfseries}{\thesubsubsection}{1em}{}
\titlespacing*{\subsubsection}{0pt}{12pt}{6pt}

% Commande pour page de titre de chapitre seule
\newcommand{\finPageTitre}{\clearpage}

% Numérotation arabe classique à 3 niveaux (ex: 1.1.2)
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{3}

% ============================================================
% 8. EN-TÊTES ET PIEDS DE PAGE
% ============================================================
\pagestyle{fancy}
\fancyhf{}
% En-tête : supprimé
\renewcommand{\headrulewidth}{0pt}

% Pied de page : numéro de page centré uniquement
\fancyfoot[C]{\thepage}
\renewcommand{\footrulewidth}{0pt}

% Style 'plain' pour les premières pages de chapitre
\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyfoot[C]{\thepage}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\footrulewidth}{0pt}%
}

% Compatibilité report class
\providecommand{\mainmatter}{}
\providecommand{\backmatter}{}

% ============================================================
% 9. SECTION DE TRANSITION ENTRE CHAPITRES (Section 1.1.2)
% ============================================================
\newcommand{\sectionTransition}[1]{%
  \section*{Conclusion}
  \addcontentsline{toc}{section}{Conclusion}
  #1
}
