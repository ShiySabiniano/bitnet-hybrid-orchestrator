---
title: Quickstart
nav_order: 2
---

# Quickstart

This guide shows you how to run the **BitNet Hybrid Orchestrator** in **Colab** (zero setup) or **locally** with Python. It also covers the optional **Web UIs** (single-turn and multi-turn chat) and how to use the optional **TinyBERT ONNX** guard.

---

## TL;DR

- **Colab (recommended first run):**  
  👉 https://colab.research.google.com/gist/ShiySabiniano/a34e01bcfc227cddc55a6634f1823539/bitnet_tinybert_orchestrator_colab.ipynb  
  Run Cells **1 → 5**.  
  - **Cell 6:** single-turn web form.  
  - **Cell 6B:** **chat mode** (multi-turn, history-preserving).

- **Local (Python 3.10+):**
  ```bash
  git clone https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator.git
  cd bitnet-hybrid-orchestrator
  python -m venv .venv && source .venv/bin/activate    # Windows: .\.venv\Scripts\Activate.ps1
  pip install -r orchestrator/requirements.txt
```

**Optional Web UIs (local):**

```bash
pip install -r ui/requirements.txt
python ui/chat_gradio.py     # multi-turn chat UI
# or create ui/gradio_demo.py from Colab Cell 6 and:
# python ui/gradio_demo.py
```

---

## 1) What you’re running

The demo executes a compact **hybrid DAG**:

```
parse → [claim1, claim2] (parallel) → reduce
```

* **BitNet agents (placeholders)**: `summarizer`, `claimcheck`, `synthesis`
  (These are CPU-cheap, deterministic stubs you can swap with real BitNet backends.)
* **TinyBERT Guard**: input/output moderation + **PII redaction**.

  * Runs with **heuristics + regex** by default.
  * If you provide a **TinyBERT ONNX** model + tokenizer, it adds learned signals.

---

## 2) Run in Google Colab (zero setup)

1. Open Colab:
   [https://colab.research.google.com/gist/ShiySabiniano/a34e01bcfc227cddc55a6634f1823539/bitnet\_tinybert\_orchestrator\_colab.ipynb](https://colab.research.google.com/gist/ShiySabiniano/a34e01bcfc227cddc55a6634f1823539/bitnet_tinybert_orchestrator_colab.ipynb)
2. Run **Cells 1 → 5** in order.
3. Choose a UI:

   * **Cell 6** — single-turn UI: paste text → pipeline runs once.
   * **Cell 6B** — **chat UI**: multi-turn, keeps transcript history.

**Notes**

* The Guard reports its mode: `regex-only` or `onnx+regex`.
* Colab will show a public `*.gradio.live` URL while the session is active. Don’t use real PII.

---

## 3) Local setup (CLI + Web UI)

### 3.1 Core runtime

```bash
git clone https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator.git
cd bitnet-hybrid-orchestrator
python -m venv .venv && source .venv/bin/activate    # Windows: .\.venv\Scripts\Activate.ps1
pip install -r orchestrator/requirements.txt
```

Run the tiny CLI (optional):

```bash
python orchestrator/cli.py --input "Contact test@example.com. BitNet b1.58 ... TinyBERT ..."
# or
python orchestrator/cli.py --input @sample.txt
```

### 3.2 Optional Web UIs (local)

```bash
pip install -r ui/requirements.txt
```

* **Chat UI (multi-turn):**

  ```bash
  python ui/chat_gradio.py
  ```
* **Single-turn UI:** create `ui/gradio_demo.py` by copying **Colab Cell 6**, then:

  ```bash
  python ui/gradio_demo.py
  ```

---

## 4) Optional: enable TinyBERT ONNX guard

If you have a TinyBERT (sequence classification) **ONNX** model and tokenizer dir:

**Colab env vars (one-time per session):**

```python
import os
os.environ["TINYBERT_ONNX_PATH"] = "/content/tinybert-int8.onnx"
os.environ["TINYBERT_TOKENIZER_DIR"] = "/content/tokenizer"
# Or to force regex-only: os.environ["GUARD_DISABLE_ONNX"] = "1"
```

**Local shell (before starting the app):**

```bash
export TINYBERT_ONNX_PATH=/absolute/path/to/tinybert-int8.onnx
export TINYBERT_TOKENIZER_DIR=/absolute/path/to/tokenizer
# To disable ONNX entirely:
# export GUARD_DISABLE_ONNX=1
```

If paths are not set or model loading fails, the guard falls back to **heuristics + regex**.

---

## 5) Tweaking the pipeline

Open **`orchestrator/pipeline.yml`** and edit node params / thresholds:

```yaml
name: summarize_and_verify
budgets: { latency_ms: 1800, max_concurrency: 2, memory_mb: 1200 }
models:  { reasoner: bitnet-s-1.58b, guard: tinybert-onnx-int8 }
policies:
  thresholds: { toxicity_block: 0.5, pii_redact: 0.7, jailbreak_block: 0.6 }
nodes:
  - { id: parse,  agent: bitnet.summarizer, guard_pre: true, guard_post: true, params: { max_sentences: 3 } }
  - { id: claim1, agent: bitnet.claimcheck, deps: [parse], params: { claim: "C1" } }
  - { id: claim2, agent: bitnet.claimcheck, deps: [parse], params: { claim: "C2" } }
  - { id: reduce, agent: bitnet.synthesis,  deps: [claim1, claim2] }
```

**Chat mode config** sample: **`orchestrator/pipeline.chat.yml`**

```yaml
conversation:
  kind: transcript
  window_messages: 12
  persist: false
  redact_pii_in_history: true
```

---

## 6) Swapping in real BitNet backends

Replace placeholder agents with your runtime while keeping signatures:

```python
async def summarizer(text: str, max_sentences: int = 3, **_) -> dict:
    # call your BitNet summarization backend here
    return {"text": "..."}
```

Do the same for `claimcheck` and `synthesis`. The orchestrator and UIs don’t need changes.

---

## 7) Troubleshooting

* **NameError: guard/Registry/Node not defined**
  Run cells **1 → 5** first (the UI cells reuse those).

* **“event loop already running”** (Colab/Notebooks)
  We install `nest_asyncio` and call `nest_asyncio.apply()`. Re-run the UI cell once after install.

* **No public link appears**
  Use the **local URL** printed by Gradio. In Colab, permit pop-ups and try again.

* **Blocked content or redaction looks aggressive**
  Lower `toxicity_block` / `jailbreak_block` or increase `pii_redact` in the policy (carefully).

* **Port in use (local)**
  Set a custom port:

  ```python
  demo.launch(server_port=7861, share=True)
  ```

* **Version conflicts**
  If Colab preinstalls newer libs, pin versions in Cell 1 or restart runtime.

---

## 8) Security & compliance

* **Vulnerabilities:** see **[SECURITY.md](../SECURITY.md)** (PGP key + safe-harbor).
* **License:** AGPL-3.0-or-later. If you host a UI/API, expose the running commit’s **source** per **AGPL §13**.
  Copy-paste snippets: **[COMPLIANCE.md](../COMPLIANCE.md)**.
* **Third-party licenses:** track model weights/libs in **THIRD\_PARTY\_LICENSES.md**.

---

## 9) Next steps

* Integrate your BitNet runtime (onnx/cpp/accelerated).
* Expand the guard taxonomy (beyond PII).
* Add RAG (DuckDB + FAISS) to `claimcheck`.
* Build a server (FastAPI) and add `/source` + `X-AGPL-Source` header.

---

**Need help?** Open a thread in **Discussions** or file an **Issue** with a minimal repro.

```
::contentReference[oaicite:0]{index=0}
```
