# Changelog
All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.0.0/)**  
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]
### Added
- BitNet runtime adapter (bitnet.cpp / ONNX EP) — **planned**
- TinyBERT ONNX guard fine-tuning hooks + policy pack — **planned**
- DuckDB + FAISS RAG backend with ingest CLI — **planned**
- Unit tests for scheduler, guard, and agents; GitHub Actions matrix — **planned**
- Web dashboard (minimal) for DAG traces and moderation cards — **planned**

### Changed
- YAML → DAG loader to support node-level timeouts, retries, and cost/mem hints — **planned**

### Security
- Optional HW-backed subkeys (YubiKey/Nitrokey) how-to in SECURITY.md — **planned**

---

## [0.1.0] — 2025-09-10
### Added
- **Project scaffolding**:
  - `README.md` with badge deck, quick links, Colab integration, and architecture overview
  - `docs/` site (Just-the-Docs): quickstart, architecture, safety, API/pipeline schema, roadmap, Colab page
  - `orchestrator/pipeline.yml` (example) and `requirements.txt`
  - `notebooks/BitNet_TinyBERT_Orchestrator_Colab.ipynb` (demo DAG with TinyBERT guard + placeholder BitNet agents)
- **Governance & legal**:
  - `LICENSE` (**AGPL-3.0-or-later**)
  - `COMPLIANCE.md` with AGPL §13 network-use guidance (`/source` endpoint, `X-AGPL-Source` header, OCI labels)
  - `SECURITY.md` with PGP contact, coordinated disclosure, scope, and safe-harbor guidelines
  - `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1)
  - `CONTRIBUTING.md` (DCO workflow, conventional commits, SPDX headers)
  - `THIRD_PARTY_LICENSES.md` template
- **Community**:
  - Issue templates (bug report, feature request)
  - Status/Docs/License/CI badges and repo quick links in README

### Changed
- README hero block updated with **owner = Shiy Sabiniano**, security & compliance badges, and direct Colab gist link.

### Security
- Added **PGP card** details and public key path (`security/pgp/ShiySabiniano.asc`) to facilitate encrypted vulnerability reports.

---

## How we version
- **MAJOR**: incompatible API changes to the orchestrator or pipeline schema  
- **MINOR**: backward-compatible features, new agents, new policies  
- **PATCH**: backward-compatible bug fixes, docs-only changes

---

[Unreleased]: https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/releases/tag/v0.1.0
