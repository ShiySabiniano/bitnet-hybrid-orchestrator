---
nav_order: 2
title: Quickstart
---

# Quickstart

Two fast ways to try the **BitNet Hybrid Orchestrator**.

---

## 🚀 TL;DR

- **Run in Colab (no setup):**  
  👉 <a href="https://colab.research.google.com/gist/ShiySabiniano/a34e01bcfc227cddc55a6634f1823539/bitnet_tinybert_orchestrator_colab.ipynb"><b>Open the Colab demo</b></a>

- **Read the docs site:**  
  👉 <a href="https://ShiySabiniano.github.io/bitnet-hybrid-orchestrator/"><b>GitHub Pages</b></a>

---

## Option 1 — Colab (zero install)

1. Open the notebook:  
   **Colab:** https://colab.research.google.com/gist/ShiySabiniano/a34e01bcfc227cddc55a6634f1823539/bitnet_tinybert_orchestrator_colab.ipynb
2. **Runtime → Run all**.
3. You should see a mixed DAG execute:

   - `parse` → `[claim1, claim2]` (parallel) → `reduce`  
   - A **moderation card** from TinyBERT Guard on outputs  
   - PII (like `test@example.com`) redacted in results/traces

> If ONNX TinyBERT can’t load, the notebook falls back to regex PII redaction. You can plug your own ONNX path later.

---

## Option 2 — Local (Python 3.10+)

### 2.1 Install

**macOS / Linux**
```bash
git clone https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator.git
cd bitnet-hybrid-orchestrator
python -m venv .venv && source .venv/bin/activate
pip install -r orchestrator/requirements.txt
