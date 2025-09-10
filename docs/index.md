---
nav_order: 1
title: BitNet Hybrid Orchestrator
---

# BitNet Hybrid Orchestrator
_Compact, edge-ready orchestration that blends **hierarchical**, **parallel**, and **sequential** patterns with **BitNet** as the core reasoner and **TinyBERT** as dual-layer safeguards._

<div align="center">

<a href="./quickstart.html"><img src="https://img.shields.io/badge/%F0%9F%9A%80_Get_Started-Quickstart-1E90FF?style=for-the-badge" alt="Quickstart"></a>
&nbsp;
<a href="../LICENSE"><img src="https://img.shields.io/badge/License-AGPL--3.0--or--later-2ea44f?logo=gnu&style=for-the-badge" alt="AGPL"></a>
&nbsp;
<a href="../SECURITY.md"><img src="https://img.shields.io/badge/Security-Policy-444?style=for-the-badge" alt="Security Policy"></a>
&nbsp;
<a href="https://colab.research.google.com/gist/ShiySabiniano/a34e01bcfc227cddc55a6634f1823539/bitnet_tinybert_orchestrator_colab.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Run in Colab" height="28"></a>

</div>

---

## What is this?
A production-minded blueprint and runnable skeleton for a **hybrid orchestration** system:

- **BitNet agents** for summarization, verification, and synthesis (swap in your real BitNet backend).  
- **TinyBERT Guard** at **input**, optional **per-node**, and **output** for PII redaction + moderation.  
- **Mixed DAG** execution (sequential + parallel) with timeouts, retries, and budget-aware routing.  
- **Config-as-data** via `orchestrator/pipeline.yml`.

> Designed for **on-device / edge** targets: phones, SBCs, and lean VPS.

---

## Quick Links
- 🚀 **Quickstart:** [Run the demo](./quickstart.html)  
- 🧭 **Architecture:** [Flow & diagrams](./architecture.html)  
- 🛡️ **Safety:** [Guardrails & policies](./safety.html)  
- 🧩 **Pipeline API:** [YAML schema & examples](./api.html)  
- 🗺️ **Roadmap:** [Phases & exit criteria](./roadmap.html)  
- 🎒 **Colab:** <https://colab.research.google.com/gist/ShiySabiniano/a34e01bcfc227cddc55a6634f1823539/bitnet_tinybert_orchestrator_colab.ipynb>

---

## Sections (project map)

| Section | Status | What it covers |
|---|---|---|
| **A. Blueprint Foundation** | ✅ Complete | Architecture, guard model, scheduler, pipeline config, docs, legal/compliance |
| **B. MVP 1 — Core Intelligence** | 🟨 Partial | Runnable DAG with BitNet adapter swap points, device profiles, basic tests |
| **C. MVP 2 — Learning Loop** | ⏳ Planned | Local eval harness, threshold tuning, optional TinyBERT fine-tune hooks |
| **D. MVP 3 — Autonomous Logic** | 🟨 Partial | Planner heuristics, fallbacks, budget-aware routing |
| **E. MVP 4 — User Interface** | ⏳ Planned | Minimal dashboard/TUI for traces & moderation cards |

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
