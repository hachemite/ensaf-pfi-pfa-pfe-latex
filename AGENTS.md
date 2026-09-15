# AGENTS.md — Rapport de Stage ENSAF (LaTeX)

Ce fichier est la référence unique pour tout agent (Antigravity, Claude Code, ou
autre) qui édite ce dépôt. Il consolide les consignes venant de trois sources,
**classées par priorité stricte en cas de conflit** :

1. **Notes manuscrites de Pr. Rassil** (encadrante académique) — priorité absolue.
2. **Le rapport de référence déjà rédigé** (`rapport_de_stage_Hachem...pdf`) —
   sert de modèle de structure et de ton quand Rassil ne précise rien.
3. **Guide officiel ENSAF** (`GUIDE_REDACTION.md`) et **Instructions Générales**
   — règles de forme par défaut, applicables sauf contradiction avec 1 ou 2.

Si une consigne des guides contredit une note de Rassil, **la note de Rassil
gagne toujours**. Ne jamais "arbitrer" en silence — signaler le conflit à
l'utilisateur si un cas nouveau apparaît qui n'est pas déjà tranché ci-dessous.

---

## 1. Contexte du projet

- Rapport de stage PFA, ENSAF, filière Ingénierie Logicielle et IA (ou GSEEII
  selon le contexte du dépôt).
- Compilation LaTeX, structure multi-fichiers, classe custom `ensaf.cls`.
- Cible : usage en local (Antigravity / VS Code) **et** sur Overleaf sans
  adaptation — ne jamais introduire de dépendance qui casse l'un des deux.
- Le stage traite **UNE SEULE problématique**. Ne jamais élargir le sujet ou
  en injecter une seconde, même si un chapitre semble "manquer de matière".

---

## 2. Structure du dépôt (ne pas dévier sans raison)

```
main.tex                    # point d'entrée, \input uniquement, pas de logique
ensaf.cls                   # TOUTES les règles de forme vivent ici, jamais ailleurs
front/                      # pages liminaires
  titlepage.tex
  dedicace.tex
  remerciements.tex
  resume-fr.tex / resume-en.tex / resume-ar.tex
  abreviations.tex
chapters/
  00-introduction-generale.tex
  01-cadre-general.tex
  02-etat-art.tex
  03-realisation.tex
  04-conclusion-perspectives.tex
back/
  bibliographie.bib
  annexes.tex
figures/ch1/ ch2/ ch3/
logos/
compile.bat / preview.py / zip_for_overleaf.py / zip_overleaf.bat
```

**Règle stricte** : un fait/paragraphe technique va dans le chapitre qui lui
correspond, jamais "là où il y a de la place". Si un chapitre déborde en
volume par rapport aux autres, c'est un signal pour réorganiser le contenu,
pas pour l'y laisser (cf. équilibre des chapitres, section 5).

Toute nouvelle règle de forme (marge, police, espacement, en-tête) se code
**dans `ensaf.cls`**, jamais en dur dans un chapitre. Un `\vspace{}` ou
`\fontsize{}` isolé dans un fichier de `chapters/` est un anti-pattern à
corriger dès qu'il est repéré.

---

## 3. Hiérarchie de contenu imposée (ordre non négociable)

1. Couverture (page de garde)
2. Feuille blanche
3. Dédicace — texte **personnel**, jamais une formule générique copiée d'un
   autre rapport
4. Remerciements
5. Résumés FR / EN / AR + mots-clés (mots techniques uniquement, jamais de
   phrases complètes en guise de mot-clé)
6. Liste des abréviations
7. Liste des tableaux / liste des figures
8. Sommaire
9. Introduction générale
10. **Chapitre 1 — Cadre général du projet**
11. **Chapitre 2 — État de l'art / description des technologies**
12. **Chapitre 3 — Réalisation et résultats**
13. Conclusion et perspectives
14. Bibliographie & Sitographie (min. 10 références hors sitographie)
15. Annexes (glossaire, specs techniques)

---

## 4. Règles de contenu par section (issues de Rassil + Instructions Générales)

### Titre du rapport
Doit être **attractif** et mettre en valeur la contribution réelle du
stagiaire — jamais un intitulé plat type "Stage chez [Entreprise]". Vérifier
systématiquement qu'un titre proposé répond à "qu'est-ce que ce travail a
apporté", pas juste "où ça s'est passé".

### Page de garde
- Encadrant académique : nom seul, **sans "Pr."** devant.
- Jury : toujours listé **après** les encadrants, jamais avant.

### Introduction générale
- 2 à 3 paragraphes, **style technique** (résumé technique détaillé, pas une
  intro littéraire).
- Structure imposée : contexte/secteur d'activité → problématique unique →
  méthodologie choisie (justifier la cohérence de chaque étape) → annonce du
  plan ("ce rapport est réparti en N chapitres : le chapitre 1 ... le
  chapitre 2 ...").
- Longueur : 2 pages minimum, jamais plus de 4-5 pages (Instructions
  Générales) — Rassil valide la fourchette basse (2-3 paragraphes réels).
- **Jamais de romain pour la numérotation** des sous-parties, même ici.

### Chapitre 1 — Cadre général du projet
- Tient sur **une seule page sans texte** pour la page de titre du chapitre
  (via `\finPageTitre`), le contenu démarre après.
- Contenu : contexte entreprise → analyse de l'existant → mission confiée →
  contraintes.
- **Diagramme de Gantt obligatoire en fin de chapitre** (via `pgfgantt`,
  jamais une image externe si évitable — le Gantt doit rester éditable en
  LaTeX pur).
- Termine par `\sectionTransition{}` qui annonce explicitement le chapitre 2.

### Chapitre 2 — État de l'art
- Doit être une **description réelle des technologies**, pas une liste à
  puces creuse. Chaque techno mentionnée mérite une sous-section avec un
  minimum de profondeur (rôle dans le projet, alternative envisagée si
  pertinent).
- Termine par `\sectionTransition{}` qui annonce le chapitre 3.

### Chapitre 3 — Réalisation et résultats
- Structure : méthodologie adoptée → résultats obtenus → discussion
  critique.
- Chaque résultat chiffré doit être accompagné d'un commentaire — **ne
  jamais laisser un tableau ou une figure sans texte d'analyse autour**
  (règle explicite des Instructions Générales).
- Termine par `\sectionTransition{}` qui prépare la conclusion générale.

### Conclusion générale et perspectives
- Structure imposée : rappel de la problématique → résultats principaux →
  limites du travail → perspectives / pistes futures.
- 2 pages minimum, 4 pages maximum.
- C'est le **seul autre endroit** (avec les remerciements) où une tournure
  personnelle légère est tolérée pour un bilan, mais toujours mesurée.

---

## 5. Style de rédaction — à faire respecter sur CHAQUE paragraphe généré

**Interdits stricts, dans tout le corps du rapport (hors remerciements et
dédicace) :**
- ❌ "je", "j'ai effectué", "mon rapport", "ce stage m'a permis", "pendant mon
  stage" — reformuler systématiquement en tournure impersonnelle ("il
  apparaît que...", "cette étape a consisté à...", "on a procédé à...").
- ❌ Structure chronologique type journal de bord ("Semaine 1 j'ai fait X,
  semaine 2 j'ai fait Y"). La structure doit être **logique** :
  Contexte → Analyse → Conception → Réalisation → Résultats.
- ❌ Soulignage pour la mise en valeur — gras ou italique uniquement.
- ❌ Titres de section terminés par un point ou deux-points.
- ❌ Couleurs autres que noir / blanc / gris dans tout élément visuel
  (tableaux, figures, diagrammes).
- ❌ Romain pour la pagination ou la numérotation des sections — chiffres
  arabes uniquement, y compris pour les sous-sections (`1.1.2`, pas `I.1.2`).
- ❌ Sous-section orpheline : toute `x.1.1` impose l'existence d'une `x.1.2`.
  Vérifier systématiquement après ajout d'une sous-section.
- ❌ Schéma, tableau ou résultat numérique sans commentaire d'analyse
  immédiatement avant ou après.
- ❌ Objet en annexe qui n'apporte aucune valeur ajoutée, ou annexe jamais
  référencée depuis le corps du texte (une annexe sans renvoi explicite doit
  être supprimée, pas laissée "au cas où").

**Équilibre des chapitres** : avant de considérer un chapitre "terminé",
comparer son volume aux autres chapitres de développement. Un écart de plus
d'environ 30% doit déclencher soit un enrichissement du chapitre le plus
court, soit un allègement (déplacement vers annexe) du plus long.

---

## 6. Conventions LaTeX à respecter systématiquement

### Figures
```latex
\begin{figure}[H]
\centering
\IfFileExists{figures/chX/nom.png}{%
    \includegraphics[width=0.85\textwidth]{figures/chX/nom.png}%
}{%
    \fbox{\parbox[c][5cm][c]{0.85\textwidth}{\centering \textit{[Image en attente]}}}%
}
\caption{Titre descriptif de la figure}
\label{fig:nom-court}
\end{figure}
```
Toujours utiliser `\IfFileExists` pour ne jamais casser la compilation si une
image n'a pas encore été fournie par l'utilisateur.

### Tableaux
`tabularx` avec `\toprule`/`\midrule`/`\bottomrule` (booktabs), jamais de
grille type Excel avec tous les traits verticaux — contraire au style sobre
imposé par les guides.

### Équations
- Symboles scalaires en italique, vecteurs/matrices en gras.
- Toute équation mise en évidence est numérotée `(Nc.No)`, référencée via
  `\eqref{}`.

### Citations bibliographiques
- Ajout systématique dans `back/bibliographie.bib`, jamais de bibliographie
  tapée à la main dans un chapitre.
- Citation dans le texte : `\cite{clé}` → rendu `Nom [Numéro]` automatique
  via biblatex, jamais recopié en dur.
- Minimum 10 références hors sitographie — vérifier ce compte avant de
  considérer le rapport "complet".
- Sitographie : jamais un moteur de recherche ou une encyclopédie collaborative
  comme source ; toujours accompagnée de la date de consultation.

### Chapitres
Chaque `\chapter{}` est immédiatement suivi de `\finPageTitre`, puis le
contenu démarre. Chaque chapitre de développement se termine par
`\sectionTransition{...}` qui annonce explicitement le chapitre suivant —
ne jamais terminer un chapitre sans cette transition.

---

## 7. Maintenance continue des listes transversales (abréviations, glossaire, références)

Ces trois éléments ne sont **jamais une tâche de fin de projet**. Ils
doivent être mis à jour **à chaque fois** qu'un chapitre est édité — ajouté,
modifié ou étendu — pas seulement lors d'une passe dédiée en fin de
rédaction. Un sigle, un terme technique ou une affirmation citée qui
apparaît dans un chapitre et n'est pas répercuté immédiatement dans ces
trois emplacements est considéré comme une régression, au même titre qu'un
test qui casse.

### 7.1 Liste des abréviations (`front/abreviations.tex`)

- Après **toute** édition d'un chapitre (nouveau contenu, reformulation,
  passe de correction section 11), relire le texte modifié et vérifier que
  chaque sigle introduit (API, MVC, SGBD, REST, CI/CD, JSON, UML, ORM,
  HTTP, etc.) est présent dans le tableau `tabularx` avec sa définition
  complète.
- Ne jamais ajouter un sigle qui n'apparaît pas réellement dans le corps du
  texte — la liste doit refléter exactement ce qui est utilisé, ni plus ni
  moins.
- Un sigle retiré d'un chapitre (suite à reformulation) doit être retiré de
  la liste s'il n'apparaît plus nulle part ailleurs dans le document.

### 7.2 Annexe A : Glossaire des termes techniques (`back/annexes.tex`)

- Même règle que 7.1, appliquée aux termes techniques non-sigles (ex :
  "patron de conception", "injection de dépendances", "conteneurisation") introduits ou reformulés dans un chapitre.
- Chaque terme du glossaire doit être **référencé au moins une fois** depuis
  le corps du texte (renvoi explicite ou simplement l'usage du terme lui-même
  dans un chapitre) — un terme du glossaire jamais utilisé ailleurs est à
  supprimer, conformément à l'interdiction des annexes non référencées
  (section 5).

### 7.3 Références bibliographiques (`back/bibliographie.bib`)

- Toute affirmation nouvellement ajoutée à un chapitre qui s'appuie sur une
  source externe (norme, étude, statistique, définition établie) reçoit son
  `\cite{}` **au moment où la phrase est écrite**, pas différé à une passe
  ultérieure. Si la source réelle n'est pas encore trouvée, marquer
  `[CITATION MANQUANTE : description de l'affirmation à sourcer]` en
  commentaire LaTeX plutôt que de laisser l'affirmation sans trace.
- Ne jamais inventer une entrée BibTeX pour combler un `\cite{}` manquant —
  cf. section 6, aucune référence n'est ajoutée sans être une source réelle
  vérifiable.
- Avant de considérer un chapitre "terminé" (même provisoirement), vérifier
  qu'aucun `[CITATION MANQUANTE]` ni `[À compléter]` ne subsiste sans être
  explicitement signalé dans le suivi de tâches (`TODO.md`).

### 7.4 Vérification obligatoire après chaque prompt d'édition de chapitre

À la fin de **chaque** prompt qui modifie un chapitre (contenu, correction
grammaticale, passe de naturel), l'agent doit répondre explicitement à ces
trois questions avant de considérer la tâche terminée :
1. Un nouveau sigle a-t-il été introduit ou retiré ? → `front/abreviations.tex`
   mis à jour ou non concerné.
2. Un nouveau terme technique a-t-il été introduit ou retiré ? →
   `back/annexes.tex` (glossaire) mis à jour ou non concerné.
3. Une nouvelle affirmation sourcée a-t-elle été ajoutée ? →
   `back/bibliographie.bib` mis à jour, `\cite{}` inséré, ou
   `[CITATION MANQUANTE]` marqué explicitement.

Si la réponse à l'une de ces trois questions est ambiguë, l'agent doit le
signaler plutôt que de supposer qu'aucune mise à jour n'est nécessaire.

---

## 8. Recherche de sources externes (recherche web obligatoire, jamais inventée)

Chaque fois qu'un chapitre introduit un concept, un outil, une norme, un
algorithme ou une affirmation qui bénéficierait d'une source (cf. section
7.3), l'agent effectue une **recherche web réelle** avant d'ajouter quoi que
ce soit à `back/bibliographie.bib`. Ceci s'applique en continu pendant la
rédaction, pas comme une passe unique en fin de projet.

### 8.1 Ce qui compte comme une source valide

- Livres académiques ou techniques réels (vérifiables via l'éditeur, WorldCat,
  ou Google Books — pas seulement "connus de mémoire").
- Normes officielles (ISO, NIST, DGSSI/DNSSI) — lien vers la page officielle
  de la norme ou de l'organisme.
- Documentation officielle d'outils/API réellement utilisés dans le projet
  (URLhaus, AbuseIPDB, Streamlit, Pydantic, scikit-learn, pandas) — lien
  direct vers la page de documentation, avec date de consultation.
- Articles de blog ou billets techniques **uniquement** s'ils proviennent
  d'une source reconnue dans le domaine (éditeurs des outils eux-mêmes,
  publications CTI établies) — jamais un forum, un contenu SEO générique,
  ou un site dont la fiabilité n'est pas évidente.

### 8.2 Procédure de vérification (obligatoire, pas optionnelle)

1. **Rechercher réellement** la source sur le web — jamais citer de mémoire
   un livre, une norme ou une URL sans l'avoir consultée dans cette session.
2. **Récupérer la page réelle** (fetch, pas seulement un résultat de
   recherche) pour confirmer titre exact, auteur(s), année, éditeur, ou
   URL/DOI stable.
3. Ajouter l'entrée BibTeX **avec la preuve** (URL consultée en commentaire
   au-dessus de l'entrée, ou champ `note`/`urldate` pour les sources web) —
   pas seulement l'entrée finale sans trace de vérification.
4. Si une source plausible ne peut pas être confirmée par une recherche
   réelle dans la session, ne pas l'ajouter — marquer
   `[CITATION NON VÉRIFIÉE : description]` dans le chapitre concerné plutôt
   que de fabriquer une entrée BibTeX à partir d'une supposition.

### 8.3 Interdiction stricte

- Ne jamais inventer un ISBN, un éditeur, une année d'édition ou une URL.
- Ne jamais présenter une liste de références comme "vérifiée" ou
  "ajoutée" dans un résumé de tâche sans avoir montré la preuve de
  recherche (sortie brute de la recherche/fetch) — cf. principe général
  "sortie brute avant de valider" déjà appliqué au code et aux tests.
- Toute entrée déjà présente dans `bibliographie.bib` dont l'origine n'est
  pas traçable (pas de recherche web documentée dans l'historique de la
  session qui l'a ajoutée) doit être re-vérifiée avant la relecture finale,
  pas supposée correcte parce qu'elle existe déjà dans le fichier.

### 8.4 Cas des sources déjà ajoutées sans preuve de recherche documentée

Toute entrée ajoutée au fichier avant l'introduction de cette règle doit
être traitée comme non vérifiée jusqu'à contrôle manuel : reprendre chaque
entrée, effectuer la recherche réelle, confirmer ou corriger les champs, et
ne cocher la checklist section 11 qu'une fois ce contrôle rétroactif fait.

---

## 9. Workflow attendu d'un agent sur ce dépôt

1. **Avant toute édition de contenu**, relire ce fichier — ne pas se fier
   uniquement à la mémoire de conversation.
2. **Ne jamais modifier `ensaf.cls`** pour un besoin ponctuel de mise en forme
   dans un seul chapitre — si une règle de forme doit changer, elle change
   dans la classe, globalement.
3. Après rédaction d'un chapitre, passer la checklist section 5 avant de
   considérer la tâche terminée.
4. Ne jamais introduire de package LaTeX qui ne compile pas nativement sur
   Overleaf (vérifier la compatibilité avant d'ajouter une dépendance).
5. En cas de doute sur une règle non couverte ici, poser la question à
   l'utilisateur plutôt que d'inventer une convention — ne pas improviser de
   style qui contredirait silencieusement Rassil.
6. Ne jamais générer de contenu factuel inventé (chiffres, noms de
   technologies, résultats) pour "remplir" un chapitre — utiliser des
   placeholders explicites (`[À compléter : ...]`) si l'information manque.

---

## 10. Compilation

```bash
# Local (Windows)
compile.bat
# ou
python preview.py       # compile + ouvre le PDF automatiquement

# Export vers Overleaf
python zip_for_overleaf.py   # génère overleaf_ensaf_template.zip
```

Chaîne de compilation standard : `pdflatex → biber → pdflatex → pdflatex`
(nécessaire pour que la bibliographie et les références croisées se
résolvent correctement).

---

## 11. Checklist finale avant remise

- [ ] Une seule problématique traitée dans tout le rapport
- [ ] Aucun "je" hors remerciements/conclusion
- [ ] Chaque figure/tableau a un commentaire d'analyse
- [ ] Chaque `\sectionTransition` annonce bien le chapitre suivant
- [ ] Pagination arabe uniquement, continue jusqu'aux annexes
- [ ] Minimum 10 références bibliographiques + sitographie datée
- [ ] Chaque entrée de `bibliographie.bib` a été confirmée par une recherche web réelle
- [ ] Aucune sous-section orpheline (x.1.1 sans x.1.2)
- [ ] Chapitres de développement équilibrés en volume
- [ ] Toutes les annexes référencées depuis le corps du texte
- [ ] Titre du rapport attractif, valorisant la contribution
- [ ] Résumés FR/EN/AR rédigés en dernier, une fois le rapport figé
- [ ] Aucun sigle utilisé dans le corps du texte absent de la liste des abréviations, et aucun sigle listé qui n'est plus utilisé
- [ ] Aucun terme du glossaire (Annexe A) non référencé depuis le corps du texte
- [ ] Aucun `\cite{}` manquant ni `[CITATION MANQUANTE]` non résolu dans la version finale

---

## 12. Contrôle linguistique et naturel du texte (avant compilation finale)

Cette étape intervient **uniquement une fois un chapitre figé** (plus
d'édition de contenu prévue dessus) — jamais en cours de rédaction, sous
peine de revérifier la même phrase à chaque itération d'Antigravity.

### 12.1 Vérification grammaticale et stylistique

- Outil de référence : **Antidote** (mode intégration LaTeX si disponible,
  sinon exporter le chapitre en `.txt`, corriger, reporter les corrections
  à la main dans le `.tex`). **LanguageTool** (mode français) en alternative
  gratuite.
- **Ne jamais laisser un correcteur toucher à la typographie déjà gérée par
  `ensaf.cls` / `babel[french]`** (espaces insécables avant `:`, `;`, `!`,
  `?`). Vérifier `ensaf.cls` avant de lancer un correcteur pour ne pas
  entrer en conflit avec les réglages du template.
- Le correcteur ne remplace pas la checklist de la section 11 (interdiction
  du "je", sous-sections orphelines, etc.) — il s'agit d'un contrôle
  purement linguistique, en complément, jamais en substitution.

### 12.2 Passe de naturel ("sonne comme rédigé par un humain")

Objectif : repérer et reformuler les tournures qui trahissent une rédaction
purement générée (cadence répétitive, ouvertures de phrase identiques d'une
section à l'autre, longueurs de paragraphe trop régulières, expressions
génériques type "Il convient de noter que...", "Dans le cadre de...").

- C'est une tâche de **relecture humaine assistée**, pas un outil de
  contournement de détection IA. Aucun outil de type "humanizer" destiné à
  déjouer un détecteur ne doit être utilisé sur ce rapport — l'établissement
  n'a communiqué aucune politique sur l'usage d'IA en rédaction, et ce type
  d'outil relève de l'intégrité académique, pas de la qualité rédactionnelle.
- Méthode acceptée : demander à l'agent de relire un chapitre et de
  signaler (sans réécrire automatiquement) chaque phrase qui sonne
  templatée ou générique, puis reformuler soi-même chaque signalement.
- Prompt type pour cette passe :

```text
Relis chapters/0N-....tex phrase par phrase. Signale uniquement les
phrases qui sonnent génériques, répétitives ou "IA-typiques"
(ouvertures identiques, cadence trop régulière, formules creuses).
Pour chaque signalement : cite la phrase, explique en une ligne
pourquoi elle sonne générique. Ne réécris rien toi-même — je
reformule chaque phrase signalée personnellement.
```

- Cette étape est obligatoire avant la checklist finale (section 11), sur
  chaque chapitre de développement (1, 2, 3) et l'introduction/conclusion.

### 12.3 Ordre d'exécution

1. Contenu figé (post-Phase 4/5 du plan de rédaction).
2. Passe 12.2 (naturel) — reformulation manuelle des signalements.
3. Passe 12.1 (grammaire/style) — correction des reformulations.
4. Checklist section 11.
5. Compilation finale.

Ne jamais inverser l'ordre 12.2 → 12.1 : corriger la grammaire d'une phrase
générique avant de l'avoir reformulée fait perdre le travail au correcteur
dès qu'elle change.