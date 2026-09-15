# 📑 Modèles Officiels des Couvertures de Rapport de Stage — ENSAF

Ce dossier rassemble les **modèles officiels de pages de garde** de l'École Nationale des Sciences Appliquées de Fès (ENSAF), disponibles en format **Word (.docx)** et en format **LaTeX (.tex)**.

---

## 📂 Contenu du Dossier

| Niveau / Stage | Fichier Word Officiel (.docx) | Fichier LaTeX Équivalent (.tex) | Description |
| :--- | :--- | :--- | :--- |
| **1ère Année Ingénieur (3A)** | [`Stage_Initiation_1A_csi.docx`](Stage_Initiation_1A_csi.docx) | [`couverture_csi.tex`](couverture_csi.tex) | **Stage d'Initiation** (découverte du milieu professionnel, ouvrier / technicien) |
| **2ème Année Ingénieur (4A)** | [`Stage_Application_2A_PFA_csa.docx`](Stage_Application_2A_PFA_csa.docx) | [`couverture_csa.tex`](couverture_csa.tex) | **Stage d'Application / PFA** (projet technique et ingénierie) |
| **3ème Année Ingénieur (5A)** | [`Projet_Fin_Etudes_3A_PFE_cpfe.docx`](Projet_Fin_Etudes_3A_PFE_cpfe.docx) | [`couverture_cpfe.tex`](couverture_cpfe.tex) | **Projet de Fin d'Études (PFE)** (obtention du diplôme d'Ingénieur d'État) |

---

## 🎯 Spécificités de chaque couverture

### 1. Stage d'Initiation (`csi`)
- **Titre principal :** *Stage d'Initiation*
- **Sous-titre de statut :** *Élève Ingénieur en 1ère année Génie [Filière]*
- **Champs requis :**
  - Organisme d'accueil
  - Sujet de stage
  - Période de stage
  - Réalisé par (M. / Mme Prénom & Nom)
  - Encadrement (Encadrant ENSAF & Encadrant Société)
  - Membres de jury (3 membres)

### 2. Stage d'Application / PFA (`csa`)
- **Titre principal :** *Stage d'Application*
- **Sous-titre de statut :** *Élève Ingénieur en 2ème année Génie [Filière]*
- **Champs requis :**
  - Organisme d'accueil
  - Sujet de stage
  - Période de stage
  - Réalisé par (solo ou binôme)
  - Encadrement (Encadrant ENSAF & Encadrant Société)
  - Membres de jury (3 membres)

### 3. Projet de Fin d'Études (`cpfe`)
- **Titre principal :** *Projet de Fin d'Études*
- **Mention de diplôme :** *Pour l'obtention du diplôme D'Ingénieur d'État Génie [Filière]*
- **Promotion :** *Promotion [Année]*
- **Champs requis :**
  - Sujet de stage
  - Stage réalisé au sein de [Organisme]
  - Réalisé par (M. / Mme Prénom & Nom)
  - Date de soutenance (*Soutenance le : ...*)
  - Membres de jury détaillés :
    - Encadrant(e) Société
    - Encadrant ENSAF
    - Enseignants ENSAF (Rapporteurs / Examinateurs)

---

## ⚡ Utilisation automatique avec `configure.py`

Vous pouvez sélectionner directement le modèle de couverture souhaité dans [`project_info.yaml`](../project_info.yaml) :

```yaml
academique:
  # Valeurs possibles :
  #   - "PFA"        : Stage d'Application (2A / 4ème année)
  #   - "PFE"        : Projet de Fin d'Études (3A / 5ème année)
  #   - "INITIATION" : Stage d'Initiation (1A / 3ème année)
  #   - "NONE"       : SANS couverture (démarre directement aux dédicaces)
  modele_couverture: "PFA"
```

Puis exécutez simplement :
```bash
python configure.py
```
Le script remplit directement le document Word officiel avec vos métadonnées en pur UTF-8, le compacte automatiquement pour garantir **strictement 1 seule page**, génère `front/couverture.pdf`, et l'intègre dans votre rapport LaTeX via `front/titlepage.tex`.
