# 📋 Suivi de Rédaction du Rapport (TODO)

Ce fichier permet de suivre l'état d'avancement de la rédaction du rapport, chapitre par chapitre. 
- `[ ]` : À rédiger
- `[-]` : En cours / Placeholder à compléter
- `[x]` : Rédigé et validé par le linter

---

## 📌 1. Pages Liminaires (Front Matter)
- [x] **Configuration générale (`project_info.yaml` & `python configure.py`)** :
  - [x] Infrastructure de synchronisation automatique (solo/binôme/trinôme, filières, encadrement, jury)
  - [x] Support multi-modèles de couverture : PFA (2A), PFE (3A), INITIATION (1A) ou NONE
- [x] **Page de garde (`front/titlepage.tex`)** :
  - [x] Remplissage automatisé du document Word officiel avec conservation 100% du style
  - [x] Algorithme de compactage garantissant strictement 1 seule page (`front/couverture.pdf`)
  - [x] Inclusion propre via `\includepdf`
- [-] **Dédicaces (`front/dedicace.tex`)** :
  - [x] Alignement centré et mise en page Times
  - [-] Remplacer `[Votre Prénom]`
- [x] **Remerciements (`front/remerciements.tex`)** :
  - [x] Formule officielle personnalisée avec direction, encadrants pro/académiques et jury
- [-] **Résumés et Mots-Clés (`front/resume-*.tex`)** :
  - [-] Résumé en français (10 lignes) + 3 à 5 mots-clés
  - [-] Abstract en anglais (10 lines) + keywords
  - [x] Résumé en arabe haute fidélité (`front/resume_ar.pdf`) avec titre sobre « ملخص » sans cadre artificiel
- [-] **Liste des abréviations (`front/abreviations.tex`)** :
  - [-] Ajouter les sigles et acronymes propres au projet

---

## 📖 2. Corps du Rapport (Chapitres)

### Chapitre 0 : Introduction Générale (`chapters/00-introduction-generale.tex`)
- [-] Contexte général et motivation du stage
- [-] Définition claire de la problématique
- [-] Objectifs assignés au travail d'ingénieur
- [x] Présentation de la structure du rapport (4 chapitres)

### Chapitre 1 : Cadre Général du Projet (`chapters/01-cadre-general.tex`)
- [-] Présentation de l'organisme d'accueil (secteur, expertises, solutions)
- [-] Analyse de l'existant (architecture, acteurs, schéma fonctionnel)
- [-] Problématique et identification des limitations
- [-] Périmètre de la mission (tâches incluses / exclues)
- [-] Planning prévisionnel et diagramme de Gantt (`pgfgantt`)

### Chapitre 2 : État de l'Art et Choix Technologiques (`chapters/02-etat-art.tex`)
- [-] Démarche méthodologique (Agile / Cycle itératif / Gestion de projet)
- [-] Étude comparative des technologies Front-End, Back-End et Base de données
- [-] Justification des choix retenus
- [-] Architecture globale et modélisation conceptuelle (diagramme d'architecture)
- [-] Assurance qualité et stratégie de tests

### Chapitre 3 : Réalisation et Analyse Critique (`chapters/03-realisation.tex`)
- [-] Environnement de développement et configuration
- [-] Présentation des modules développés (avec captures d'écran réelles)
- [-] Extraits de code / algorithmes représentatifs
- [-] Résultats quantitatifs et tableau des métriques avant/après
- [-] Discussion critique (respect du cahier des charges, limites et difficultés)

### Chapitre 4 : Conclusion et Perspectives (`chapters/04-conclusion-perspectives.tex`)
- [-] Bilan synthétique des réalisations
- [-] Acquis méthodologiques et compétences d'ingénierie développées
- [-] Perspectives d'évolution à court, moyen et long terme
- [-] Conclusion personnelle et perspectives professionnelles

---

## 📚 3. Fin du Document (Back Matter)
- [-] **Annexes (`back/annexes.tex`)** :
  - [-] Glossaire des termes techniques
  - [-] Documentation des endpoints d'API / schémas complémentaires
- [-] **Bibliographie (`back/bibliographie.bib`)** :
  - [-] Ajouter les articles, livres et documentations officielles cités dans le texte

---

## 🎯 4. Checklist Avant Dépôt Final
- [ ] **Nombre de pages :** 30 à 40 pages (PFA 4A) / 50 à 70 pages (PFE 5A) hors annexes.
- [ ] **Lint automatique :** Exécuter `python lint.py` et obtenir 0 erreur critique.
- [ ] **Zéro "je" :** Vérifier l'absence de tournures personnelles dans le corps technique.
- [ ] **Flottants :** Chaque figure et tableau a une légende (`\caption`) et un label (`\label`).
- [ ] **Citations :** Chaque document de la bibliographie est cité au moins une fois dans le texte avec `\cite{...}`.
- [ ] **Compilation :** Le PDF compile sans erreur via `compile.bat` ou `python preview.py`.
