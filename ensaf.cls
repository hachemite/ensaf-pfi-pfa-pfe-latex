\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ensaf}[2026/08/27 Rapport de stage ENSAF - regles Rassil]
\LoadClass[12pt,a4paper]{report}

% ---------- Langue ----------
\RequirePackage[LAE,T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[arabic,french]{babel}

% ---------- Mise en page (Instructions Generales) ----------
\RequirePackage[left=2.5cm,right=2.5cm,top=2cm,bottom=2cm]{geometry}
\RequirePackage{setspace}
\setstretch{1.5}

% ---------- Police Times ----------
\RequirePackage{mathptmx}

% ---------- Pagination : arabe uniquement, jamais de romain ----------
\pagenumbering{arabic}

% ---------- Palette : noir/blanc/gris uniquement ----------
\RequirePackage[table]{xcolor}
\definecolor{grisfonce}{gray}{0.3}
\definecolor{grisclair}{gray}{0.85}

% ---------- Outils ----------
\RequirePackage{graphicx}
\RequirePackage{float}
\RequirePackage{caption}
\captionsetup{font=it,labelfont={bf,it}} % legendes centrees, italique 12pt
\RequirePackage{booktabs}
\RequirePackage{tabularx}
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
% REGLE RASSIL n°1 : titre de chapitre = grande lettre, centre,
% SANS texte de contenu sur la meme page. Pas de deux-points.
% ============================================================
\titleformat{\chapter}[display]
  {\centering\normalfont\bfseries}
  {\Large\MakeUppercase{\chaptertitlename}~\thechapter}
  {30pt}
  {\vspace{40pt}\Huge\MakeUppercase}
\titlespacing*{\chapter}{0pt}{0pt}{0pt}

% Format specifique pour les chapitres non numerotes (\chapter*{...})
\titleformat{name=\chapter,numberless}[display]
  {\centering\normalfont\bfseries}
  {}
  {0pt}
  {\Huge\MakeUppercase}
\titlespacing*{name=\chapter,numberless}{0pt}{0pt}{20pt}

% Commande pour forcer "page de titre seule" : a utiliser juste
% apres \chapter{...} et avant la premiere \section.
\newcommand{\finPageTitre}{\clearpage}

% ---------- Numerotation sections classique (1.1.2, pas de romain) ----------
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{3}

% ---------- En-tete / pied de page ----------
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0pt}

% Assurer le meme pied de page sur les pages de debut de chapitre (style plain)
\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyfoot[C]{\thepage}%
  \renewcommand{\headrulewidth}{0pt}%
}

% Compatibilite report class pour \mainmatter et \backmatter
\providecommand{\mainmatter}{}
\providecommand{\backmatter}{}

% ---------- Commande conclusion de chapitre qui reference le suivant ----------
% Usage : \sectionTransition{texte annoncant le chapitre suivant}
\newcommand{\sectionTransition}[1]{%
  \section*{Conclusion}
  \addcontentsline{toc}{section}{Conclusion}
  #1
}
