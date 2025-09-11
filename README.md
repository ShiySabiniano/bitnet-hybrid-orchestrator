# BitNet Hybrid Orchestrator  
_Hierarchical + Parallel + Sequential orchestration with **BitNet** as the core reasoner and **TinyBERT** as dual-layer safeguards (edge-ready)._

<div align="center">

  <!-- Hero / Goal badges (GitHub-safe) -->
  <a href="#what-is-this">
    <img src="https://img.shields.io/badge/%F0%9F%9A%80_Goal-Innovation-ff6a00?labelColor=ee0979&logo=target&logoColor=white&style=for-the-badge" alt="Goal: Innovation">
  </a>
  &nbsp;
  <a href="#architecture-at-a-glance">
    <img src="https://img.shields.io/badge/Hybrid-Orchestration-1E90FF?logo=matrix&logoColor=white&style=for-the-badge" alt="Hybrid Orchestration">
  </a>
  &nbsp;
  <a href="#quickstart">
    <img src="https://img.shields.io/badge/Edge--Ready-BitNet%20%2B%20TinyBERT-0A8754?style=for-the-badge" alt="Edge-Ready">
  </a>

  <br/><br/>

  <!-- Row 1: Primary badges -->
  <a href="https://colab.research.google.com/gist/ShiySabiniano/a34e01bcfc227cddc55a6634f1823539/bitnet_tinybert_orchestrator_colab.ipynb">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Run in Colab" height="28">
  </a>
  &nbsp;
  <a href="https://ShiySabiniano.github.io/bitnet-hybrid-orchestrator/">
    <img src="https://img.shields.io/badge/Docs-GitHub%20Pages-black?logo=readthedocs" alt="Docs" height="28">
  </a>
  &nbsp;
  <a href="https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/actions">
    <img src="https://img.shields.io/badge/CI-GitHub%20Actions-blue?logo=githubactions" alt="CI" height="28">
  </a>
  &nbsp;
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-AGPL--3.0--or--later-2ea44f?logo=gnu" alt="License" height="28">
  </a>
  &nbsp;
  <a href="https://img.shields.io/badge/status-alpha-orange">
    <img src="https://img.shields.io/badge/status-alpha-orange" alt="Status" height="28">
  </a>

  <br/><br/>

  <!-- Row 2: Security & Governance -->
  <a href="SECURITY.md">
    <img src="https://img.shields.io/badge/Security-Policy-444?logo=datadog&logoColor=white" alt="Security Policy" height="22">
  </a>
  &nbsp;
  <a href="COMPLIANCE.md">
    <img src="https://img.shields.io/badge/AGPL-%C2%A713%20Compliance-444?logo=shield&logoColor=white" alt="AGPL §13 Compliance" height="22">
  </a>
  &nbsp;
  <a href="security/pgp/ShiySabiniano.asc">
    <img src="https://img.shields.io/badge/PGP-Public%20Key-444?logo=protonmail&logoColor=white" alt="PGP Public Key" height="22">
  </a>
  &nbsp;
  <a href="https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/security/advisories/new">
    <img src="https://img.shields.io/badge/Report-Vulnerability-8B0000?logo=github&logoColor=white" alt="Report a Vulnerability" height="22">
  </a>

  <br/><br/>

  <!-- Row 3: Quick links -->
  <a href="https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator"><b>🏠 Repo</b></a>
  &nbsp;•&nbsp;
  <a href="https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/issues"><b>🐞 Issues</b></a>
  &nbsp;•&nbsp;
  <a href="https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/discussions"><b>💬 Discussions</b></a>
  &nbsp;•&nbsp;
  <a href="https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/releases"><b>📦 Releases</b></a>
  &nbsp;•&nbsp;
  <a href="docs/roadmap.md"><b>🗺️ Roadmap</b></a>
  &nbsp;•&nbsp;
  <a href="docs/api.md"><b>🧩 Pipeline API</b></a>
  &nbsp;•&nbsp;
  <a href="docs/chat.md"><b>💬 Chat mode</b></a>
  &nbsp;•&nbsp;
  <a href="orchestrator/pipeline.yml"><b>🧪 Example pipeline.yml</b></a>
  &nbsp;•&nbsp;
  <a href="CHANGELOG.md"><b>📝 Changelog</b></a>
  &nbsp;•&nbsp;
  <a href="https://www.linkedin.com/in/shiy-sabiniano/"><b>🔗 LinkedIn</b></a>

</div>

> **Status:** alpha • **License:** AGPL-3.0-or-later • **Owner:** **Shiy Sabiniano**

---

## What is this?

A compact orchestration engine that mixes **hierarchical**, **parallel**, and **sequential** patterns in a single execution DAG:

- **BitNet agents** handle reasoning (summarize, verify, synthesize, tool calls).  
- **TinyBERT Guard** enforces safety at **input**, optional **per-node gates**, and **output**—PII redaction + moderation.  
- Designed for **on-device / edge**: phones, SBCs, lean VPS.

This repo includes a **Colab demo**, a **YAML→DAG** pipeline config, a **Docs site**, and **multi-turn chat** UI.

---

## Feature map (your sections)

- **A. Blueprint Foundation — ✅**  
  Architecture, DAG scheduler, safety layer, config-as-data, test/metrics, and roadmap.
- **B. Section 1 MVP (Core Intelligence) — 🟨**  
  Working skeleton agents (summarize/claim-check/synthesis) with swap points for real BitNet backends.
- **C. Section 2 MVP (Learning Loop) — ⏳**  
  Hooks reserved for data curation, eval harness, fine-tuning loops.
- **D. Section 3 MVP (Autonomous Logic) — 🟨**  
  Planning heuristics, retries/fallbacks, budget-aware routing; extend to multi-episode planning.
- **E. Section 4 MVP (User Interface) — 🟨**  
  CLI + single-turn **Web UI** + **Chat mode** (multi-turn) + docs site.

---

## Architecture (at a glance)

```mermaid
flowchart TD
  A["User Input"] --> G1["TinyBERT: Input Filter"]
  G1 --> O["Hierarchical Orchestrator • plan DAG"]
  O --> P["Parse/Intent"]
  P --> C1["Claim Check 1"]
  P --> C2["Claim Check 2"]
  C1 --> R["Reduce/Synthesis"]
  C2 --> R
  R --> G2["TinyBERT: Output Moderation"]
  G2 --> X["Response"]
````

* **Mixed orchestration:** parallel branches for independent checks; sequential where dependencies exist.
* **Safety as functions:** guards can wrap the whole flow or selected nodes.

---

## Quickstart

### Option 1 — Colab (zero setup)

Open the notebook:
`/notebooks/BitNet_TinyBERT_Orchestrator_Colab.ipynb`
[▶ Launch in Colab](https://colab.research.google.com/gist/ShiySabiniano/a34e01bcfc227cddc55a6634f1823539/bitnet_tinybert_orchestrator_colab.ipynb)

* **Single-turn UI:** run **Cell 6** to get a form that runs the pipeline once.
* **Chat mode (multi-turn):** run **Cell 6B** for a chat that preserves history across turns. See **[docs/chat.md](docs/chat.md)**.

### Option 2 — Local (Python 3.10+)

```bash
git clone https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator.git
cd bitnet-hybrid-orchestrator

# macOS/Linux
python -m venv .venv && source .venv/bin/activate
# Windows (PowerShell)
# python -m venv .venv; . .\.venv\Scripts\Activate.ps1

pip install -r orchestrator/requirements.txt
```

Run the tiny CLI demo (optional):

```bash
python orchestrator/cli.py --input "Contact test@example.com. BitNet b1.58 ... TinyBERT ..."
# or
python orchestrator/cli.py --input @sample.txt
```

---

## Optional Web UIs (Gradio)

We keep UI deps separate for lean edge installs.

```bash
# Only if you want the web UIs
pip install -r ui/requirements.txt
```

**Single-turn UI (local):** use the provided script:

```bash
python ui/gradio_demo.py
```

**Chat mode (multi-turn):**

* **Colab:** run **Cell 6B — Chat Demo**.
* **Local:** use the provided script:

```bash
python ui/chat_gradio.py
```

---

## Repository layout

```
.
├─ docs/                         # GitHub Pages (Just-the-Docs)
│  ├─ index.md
│  ├─ quickstart.md
│  ├─ architecture.md
│  ├─ safety.md
│  ├─ api.md
│  ├─ roadmap.md
│  ├─ colab.md
│  └─ chat.md                   # Multi-turn chat guide
│  └─ assets/
│     ├─ logo.svg
│     └─ diagram-overview.png
├─ orchestrator/
│  ├─ pipeline.yml              # Example pipeline (YAML→DAG)
│  ├─ pipeline.chat.yml         # Chat pipeline sample
│  ├─ requirements.txt
│  └─ cli.py                    # Tiny CLI runner
├─ ui/
│  ├─ requirements.txt          # gradio, nest_asyncio (optional UI deps)
│  ├─ gradio_demo.py            # Single-turn local app
│  └─ chat_gradio.py            # Multi-turn local chat app
├─ notebooks/
│  └─ BitNet_TinyBERT_Orchestrator_Colab.ipynb
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  │  ├─ bug_report.md
│  │  ├─ feature_request.md
│  │  └─ config.yml
│  └─ workflows/
│     └─ ci.yml
├─ SECURITY.md • CODE_OF_CONDUCT.md • CONTRIBUTING.md
├─ COMPLIANCE.md • THIRD_PARTY_LICENSES.md • CHANGELOG.md
├─ security/pgp/ShiySabiniano.asc
├─ LICENSE
└─ README.md
```

---

## Pipeline as data (example)

```yaml
# orchestrator/pipeline.yml
name: summarize_and_verify
budgets: { latency_ms: 1800, max_concurrency: 2, memory_mb: 1200 }
models: { reasoner: bitnet-s-1.58b, guard: tinybert-onnx-int8 }
policies:
  thresholds: { toxicity_block: 0.5, pii_redact: 0.7, jailbreak_block: 0.6 }
nodes:
  - { id: parse,  agent: bitnet.summarizer,  guard_pre: true, guard_post: true, params: { max_sentences: 3 } }
  - { id: claim1, agent: bitnet.claimcheck, deps: [parse], params: { claim: "C1" } }
  - { id: claim2, agent: bitnet.claimcheck, deps: [parse], params: { claim: "C2" } }
  - { id: reduce, agent: bitnet.synthesis,  deps: [claim1, claim2] }
```

---

## Swapping the real backends

* **BitNet reasoner:** connect your BitNet runtime (e.g., bitnet.cpp / ONNX EP) behind the existing agent signatures.
* **TinyBERT guard:** keep ONNX INT8; tune thresholds; optionally fine-tune to your taxonomy.
* **RAG:** replace the toy list with DuckDB + FAISS (or your vector DB).

---

## AGPL-3.0-or-later (network use) — what you must do

If you host a modified version over a network, **AGPL §13** requires offering users the **Corresponding Source** of your modifications:

* Add a **“Source”** link (or `/source` endpoint) that points to the exact commit running.
* Include an HTTP header:

  ```
  X-AGPL-Source: https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/tree/<COMMIT_SHA>
  ```
* See **COMPLIANCE.md** for drop-in examples (UI footer, API headers, Docker labels).

---

## Models & third-party licenses

This repo’s code is AGPL-3.0-or-later. **Model weights and some libraries may have different licenses** (Apache-2.0, MIT, OpenRAIL, etc.). Track them in **THIRD\_PARTY\_LICENSES.md** and respect each model’s terms.

---

## Contributing

Pull requests welcome! Please read **CONTRIBUTING.md** and follow the DCO/CLA guidance. Keep SPDX headers in source files:

```
SPDX-License-Identifier: AGPL-3.0-or-later
```

---

## Security

See **SECURITY.md** for how to report vulnerabilities. Do **not** file sensitive issues publicly.

---

## License

This project is licensed under **GNU AGPL-3.0-or-later** — see [LICENSE](LICENSE).
If you interact with it over a network, you must provide users access to the Corresponding Source (AGPL §13).

---

## Owner

**Shiy Sabiniano** — [LinkedIn](https://www.linkedin.com/in/shiy-sabiniano/)

```
::contentReference[oaicite:0]{index=0}
```
