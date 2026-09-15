# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **AI Self-Correction Loop** in `PROMPT_START.md`: Explicit instruction after step 5 to automatically execute `python lint.py`, fix reported issues directly in-file, re-run `lint.py`, and repeat until clean before reporting a chapter complete.
- Version history tracking via `CHANGELOG.md` linked from `README.md`.

---

## [0.5.0] - 2026-09-15

### Added
- **GitHub Actions CI Workflow** (`.github/workflows/check.yml`): Runs automatically on every push and pull request to `main`.
- **Automated Validation**: Runs `python lint.py` and compiles `main.tex` via `xu-cheng/latex-action` (full `pdflatex → biber/bibtex → pdflatex → pdflatex` cycle).
- **Automated Artifact Upload**: Generates and uploads downloadable `main.pdf` directly to the Actions tab.

### Changed
- Refined Arabic abstract heading in `configure.py` and `front/resume-ar.tex` to a standalone, prominent 26pt title **ملخص**, removing the redundant French subtitle.
- Whitelisted standalone `front/couverture.pdf` and `front/resume_ar.pdf` in `.gitignore` to guarantee immediate, standalone compilation in CI and Overleaf without local dependencies.

### Fixed
- Fixed Word cover template vertical spacing in `configure.py`: dynamically pruned empty spacer paragraphs so *"Période de stage"* sits cleanly above the green background box border.
- Corrected `lint.py` exit-code handling so that critical compliance errors properly trigger a non-zero exit code in CI pipelines.

---

## [0.4.0] - 2026-09-15

### Added
- **AI Agent Onboarding Prompt** (`PROMPT_START.md`): Single copy-paste prompt guiding AI assistants through note ingestion, metadata collection, chapter planning, and drafted output.
- **IDE Assistant Pointers**: Added configuration pointers for Claude (`CLAUDE.md`), Cursor (`.cursorrules`), and GitHub Copilot (`.github/copilot-instructions.md`).
- **Open-Source Licensing**: Added standard MIT `LICENSE` with academic provenance and supervisor acknowledgments (Pr. Amina Rassil).
- **Demo Reference Branch**: Created `example-filled-report` branch showcasing a complete, filled report and compiled `example.pdf`.

### Fixed
- Stripped all hardcoded absolute local machine paths from documentation and template files.
- Validated Overleaf export archive (`zip_for_overleaf.py`) with clean relative paths.

---

## [0.3.0] - 2026-09-15

### Added
- **YAML Configuration System** (`project_info.yaml`): Centralized metadata schema for student authors, host company, dates, academic supervisors, and jury members.
- **Automated Synchronization Script** (`configure.py`): Ingests `project_info.yaml` and updates LaTeX front-matter files automatically.
- **Official ENSAF Word Cover Templates**: Integrated official docx models for Initiation, Application (PFA), and PFE stages.
- **Strict 1-Page Cover Generation**: Automated Word COM pipeline generating `front/couverture.pdf`.
- **High-Fidelity Arabic Abstract Pipeline**: Headless browser rendering generating `front/resume_ar.pdf` with native typographic ligatures.
- Added cover style selection support (`"PFA"`, `"PFE"`, `"INITIATION"`, or `"NONE"` for unfronted reports).

### Fixed
- Eliminated UTF-8 mojibake (`rÃ©alisÃ©`) in generated Word cover documents using UTF-8-SIG encoding and explicit unicode constants.
- Robust Word placeholder substitution using regular expressions.
- Comprehensive LaTeX special character escaping and accent macros in `configure.py`.

---

## [0.2.0] - 2026-09-15

### Added
- **AI Agent Rulebook** (`AGENTS.md`): Consolidated academic guidelines from Pr. Rassil, reference reports, and official ENSAF guide into a prioritized source of truth.
- Strict writing conventions: impersonal phrasing, mandatory `\sectionTransition{}` chapter transitions, and analysis text around all floats.

### Changed
- Hardened `.gitignore` to prevent committing build artifacts, secret keys, scratch notes, and temporary files.
- Standardized appendix layout and expanded bibliography citations.

### Fixed
- Enforced strict impersonal academic tone in conclusion and technical chapters (removed 1st person pronouns *"je"*, *"mon"*).

---

## [0.1.0] - 2026-08-29

### Added
- **Custom LaTeX Class** (`ensaf.cls`): Strict compliance with ENSAF standards (Times 12pt, 1.5 line spacing, 2.5cm/2cm margins, Arabic numbering).
- **Modular Report Architecture**: `main.tex`, `front/` matter, `chapters/` (00 to 04), `back/`, `figures/`, `logos/`.
- **Automated Academic Linter** (`lint.py`): Verification of banned pronouns, underlines, missing captions, and orphan subsections.
- **Trilingual Abstracts**: Dedicated templates for French, English, and Arabic summaries.
- **Build Tooling**: `compile.bat` and `preview.py` (with automatic Tectonic compiler integration).
- **Overleaf Exporter** (`zip_for_overleaf.py`): 1-click generation of clean zip archive for Overleaf import.
- Human user guide (`GUIDE_UTILISATION_TEMPLATE.md`) and initial `README.md`.
