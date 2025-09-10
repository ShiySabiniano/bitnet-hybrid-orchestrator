# BitNet Hybrid Orchestrator  
_Hierarchical + Parallel + Sequential orchestration with **BitNet** as the core reasoner and **TinyBERT** as dual-layer safeguards (edge-ready)._

<div align="center">

<!-- Goal badge (GitHub-safe, no inline CSS) -->
<a href="#what-is-this">
  <img src="https://img.shields.io/badge/%F0%9F%9A%80_Goal-Innovation-ff6a00?labelColor=ee0979&logo=target&logoColor=white&style=for-the-badge" alt="Goal: Innovation">
</a>

<br/><br/>

<!-- Row 1: Badges -->
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

<!-- Row 2: Quick links -->
<a href="https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator"><b>🏠 Repo</b></a>
&nbsp;•&nbsp;
<a href="https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/issues"><b>🐞 Issues</b></a>
&nbsp;•&nbsp;
<a href="https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/discussions"><b>💬 Discussions</b></a>
&nbsp;•&nbsp;
<a href="https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/releases"><b>📦 Releases</b></a>

</div>

> **Status:** alpha • **License:** AGPL-3.0-or-later • **Owner:** **Shiy Sabiniano**

---

## What is this?

A compact orchestration engine that mixes **hierarchical**, **parallel**, and **sequential** patterns in a single execution DAG:

- **BitNet agents** handle reasoning (summarize, verify, synthesize, tool calls).  
- **TinyBERT Guard** enforces safety at **input**, optional **per-node gates**, and **output**—PII redaction + moderation.  
- Designed for **on-device / edge**: phones, SBCs, lean VPS.

This repo includes a **Colab demo**, a **YAML→DAG** pipeline config, and a **Docs site** (GitHub Pages).

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
- **E. Section 4 MVP (User Interface) — ⏳**  
  CLI now; GUI/docs site; future web dashboard.

---

## Architecture (at a glance)

```mermaid
flowchart TD
A[User Input] --> G1[ TinyBERT: Input Filter ]
G1 --> O[Hierarchical Orchestrator • plan DAG]
O --> P[Parse/Intent]
P --> C1[Claim Check 1]
P --> C2[Claim Check 2]
C1 --> R[Reduce/Synthesis]
C2 --> R
R --> G2[ TinyBERT: Output Moderation ]
G2 --> X[Response]
````

* **Mixed orchestration:** parallel branches for independent checks; sequential where dependencies exist.
* **Safety as functions:** guards can wrap the whole flow or selected nodes.

---

## Quickstart

### Option 1 — Colab (zero setup)

Open the notebook:
`/notebooks/BitNet_TinyBERT_Orchestrator_Colab.ipynb`
[▶ Launch in Colab](https://colab.research.google.com/gist/ShiySabiniano/a34e01bcfc227cddc55a6634f1823539/bitnet_tinybert_orchestrator_colab.ipynb)

### Option 2 — Local (Python 3.10+)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r orchestrator/requirements.txt
# run notebook or import the orchestrator skeleton from the docs
```

> The Colab demo executes a full DAG with TinyBERT guard (ONNX if available; regex fallback) and placeholder BitNet agents. Swap in your BitNet runtime where marked.

---

## Repository layout

```
.
├─ docs/                         # GitHub Pages (Just-the-Docs)
│  ├─ index.md                   # Overview
│  ├─ quickstart.md              # How to run
│  ├─ architecture.md            # Diagrams & flow
│  ├─ safety.md                  # Guard thresholds & policy
│  ├─ api.md                     # pipeline.yml schema
│  ├─ roadmap.md                 # Phases
│  └─ colab.md                   # Notebook link
├─ orchestrator/
│  ├─ pipeline.yml               # Example pipeline (YAML→DAG)
│  └─ requirements.txt
├─ notebooks/
│  └─ BitNet_TinyBERT_Orchestrator_Colab.ipynb
├─ .github/ISSUE_TEMPLATE/
│  ├─ bug_report.md
│  └─ feature_request.md
├─ LICENSE                       # AGPL-3.0-or-later
├─ COMPLIANCE.md                 # AGPL §13 (network use) guidance
├─ THIRD_PARTY_LICENSES.md       # Dependencies + model weights licenses
├─ SECURITY.md                   # Vulnerability reporting
├─ CONTRIBUTING.md               # DCO/CLA, workflow
└─ README.md
```

---

## Pipeline as data (example)

```yaml
# orchestrator/pipeline.yml
name: summarize_and_verify
budgets: { latency_ms: 1800, max_concurrency: 2, memory_mb: 1200 }
models: { reasoner: bitnet-s-1.58b, guard: tinybert-onnx-int8 }
policies: { toxicity_block: 0.5, pii_redact: 0.7, jailbreak_block: 0.6 }
nodes:
  - { id: parse,  agent: bitnet.summarizer,  guard_pre: true, guard_post: true }
  - { id: claim1, agent: bitnet.claimcheck, deps: [parse], params: { claim: "C1" } }
  - { id: claim2, agent: bitnet.claimcheck, deps: [parse], params: { claim: "C2" } }
  - { id: reduce, agent: bitnet.synthesis,  deps: [claim1, claim2] }
```

---

## Swapping the real backends

* **BitNet reasoner:** connect your BitNet runtime (e.g., bitnet.cpp / ONNX EP).
* **TinyBERT guard:** keep ONNX INT8; tune thresholds; optionally fine-tune to your taxonomy.
* **RAG:** replace the toy list with DuckDB + FAISS (or your vector DB).

---

## AGPL-3.0-or-later (network use) — what you must do

If you host a modified version over a network, **AGPL §13** requires offering users the **Corresponding Source** of your modifications:

* Add a **“Source”** link (or `/source` endpoint) that points to the exact commit running.
* Include an HTTP header like:
  `X-AGPL-Source: https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/tree/main`
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

```
::contentReference[oaicite:0]{index=0}
```
