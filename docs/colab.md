---
nav_order: 7
title: Colab Demo
---

# Colab Demo

Run the **BitNet Hybrid Orchestrator** end-to-end in Google Colab—no local setup required.

---

## ▶ Launch

**Open the notebook:**  
<https://colab.research.google.com/gist/ShiySabiniano/a34e01bcfc227cddc55a6634f1823539/bitnet_tinybert_orchestrator_colab.ipynb>

> Tip: Click **Runtime → Run all** to execute every cell top-to-bottom.

---

## What the demo does

- Builds a **mixed DAG** (sequential + parallel) with:
  - `parse` → `[claim1, claim2]` (parallel) → `reduce`
- Wraps the flow with a **TinyBERT Guard**:
  - **pre-guard:** input filtering + PII redaction
  - **post-guard:** output moderation + moderation card
- Uses **placeholder BitNet agents** you can swap for your backend.

Expected output highlights:
- Emails/phones like `test@example.com` are **redacted** in results and traces.
- A compact **moderation card** (JSON) is attached to outputs.
- Parallel claim checks run concurrently.

---

## Notebook map (cells)

1. **Install deps** – `onnxruntime`, `transformers`, `huggingface_hub`, etc.  
2. **TinyBERT Guard** – loads tokenizer and tries an ONNX model; falls back to regex PII if none available.  
3. **Orchestrator core** – `Node`, `AgentRegistry`, `Scheduler` (DAG executor).  
4. **Agents (placeholders)** – summarizer, claimcheck, synthesis.  
5. **Demo run** – executes the pipeline and prints results + moderation info.

---

## Swapping real backends

### Use your own TinyBERT ONNX (optional)
Choose **one** of the following in a new cell **above** the guard load:

**A) Upload directly**
```python
from google.colab import files, drive
uploaded = files.upload()  # choose your tinybert.onnx
TINYBERT_ONNX_PATH = next(iter(uploaded.keys()))
````

**B) Google Drive path**

```python
from google.colab import drive
drive.mount('/content/drive')
TINYBERT_ONNX_PATH = "/content/drive/MyDrive/models/tinybert/tinybert-int8.onnx"
```

Then, in the guard init cell, point the loader to `TINYBERT_ONNX_PATH`.

### Wire a BitNet runtime (later)

The demo agents are stubs. Replace the summarizer/claimcheck/synthesis calls with your BitNet adapter (e.g., `bitnet.cpp` or ONNX EP). Keep the function signatures the same to avoid touching the scheduler.

---

## Config knobs (match `pipeline.yml`)

* **Concurrency:** `max_concurrency=2` (Scheduler)
* **Thresholds:** `toxicity_block`, `pii_redact`, `jailbreak_block` (Guard)
* **Timeouts/retries:** per-node `timeout_ms`, `max_retries`
* **Tracing:** enable/disable PII redaction in traces

> See **[Pipeline API](./api.md)** for the YAML schema and **[Safety](./safety.md)** for policy tuning.

---

## Troubleshooting

* **ONNX model didn’t load**
  The guard prints a warning and falls back to **regex PII only**. You can still run the DAG; moderation scores will be zeros.

* **Slow or OOM**
  Reduce input size, set `max_concurrency=1`, and keep `latency_ms` budgets conservative.

* **Colab runtime reset**
  Colab VMs are ephemeral. Re-run cells or save artifacts to Google Drive.

* **Windows-style paths**
  In Colab, use POSIX paths (`/content/...`). Mount Drive for persistent files.

---

## Privacy tips

* Don’t paste real PII into the demo. Use `test@example.com` and reserved numbers like `202-555-0142`.
* Keep `tracing.redact_pii_in_traces: true` if you export logs.

---

## Next steps

* **Quickstart:** [Run locally or in Colab](./quickstart.md)
* **Architecture:** [Flow & diagrams](./architecture.md)
* **Safety:** [Guardrails & policies](./safety.md)
* **Roadmap:** [Phases & exit criteria](./roadmap.md)

---

## Owner

**Shiy Sabiniano** · [https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator](https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator)

```
::contentReference[oaicite:0]{index=0}
```
