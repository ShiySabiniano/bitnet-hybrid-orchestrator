---
nav_order: 3
title: Architecture
---

# Architecture

The **BitNet Hybrid Orchestrator** blends **hierarchical planning**, **parallel fan-out**, and **sequential chains** in one compact runtime.  
Safety is enforced by a **TinyBERT Guard** at input and output, with optional node-level gates.

---

## High-level view

- **Control plane — Orchestrator**
  - Builds and executes a **mixed DAG** (directed acyclic graph) from `pipeline.yml`.
  - Applies **budgets** (latency, memory, concurrency) and **policies** (guard thresholds).
- **Data plane — Agents**
  - Small, swappable functions (e.g., `bitnet.summarizer`, `bitnet.claimcheck`, `bitnet.synthesis`).
  - Plug a real **BitNet** backend later; placeholders run in the demo.
- **Safety plane — Guard**
  - **Pre-guard** filters inputs; **post-guard** moderates outputs (PII redaction, toxicity/jailbreak).
  - Optional **per-node guard** wraps risky stages.
- **Observability**
  - Minimal JSON **traces** with redaction; **moderation card** attached to outputs.
- **Storage & RAG (optional)**
  - DuckDB + FAISS for small local knowledge bases.

---

## Data flow (overview)

```mermaid
flowchart TD
    U[User Input / Source] --> G1[Guard: Input Filter]
    G1 --> O[Orchestrator - Plan DAG]
    O --> P[Parse / Summarize]
    P -->|parallel| C1[Claim Check 1]
    P -->|parallel| C2[Claim Check 2]
    C1 --> R[Reduce / Synthesis]
    C2 --> R
    R --> G2[Guard: Output Moderation]
    G2 --> X[Response + Moderation Card]
````

* **Parallelism** speeds independent checks (`C1`, `C2`), while dependencies remain **sequential**.
* **Guard** executes **before** orchestration and **after** final synthesis; enable **per-node** gates where risk justifies it.

---

## Config-as-data (pipeline.yml → runtime)

```yaml
name: summarize_and_verify
budgets: { latency_ms: 1800, deadline_ms: 4000, max_concurrency: 2, memory_mb: 1200 }
models:  { reasoner: bitnet-s-1.58b, guard: tinybert-onnx-int8 }
policies:
  thresholds: { toxicity_block: 0.50, pii_redact: 0.70, jailbreak_block: 0.60 }
nodes:
  - { id: parse,  agent: bitnet.summarizer, guard_pre: true,  guard_post: true }
  - { id: claim1, agent: bitnet.claimcheck, deps: [parse],    guard_post: true, params: { claim: "..." } }
  - { id: claim2, agent: bitnet.claimcheck, deps: [parse],    guard_post: true, params: { claim: "..." } }
  - { id: reduce, agent: bitnet.synthesis,  deps: [claim1, claim2], guard_post: true }
```

**Mapping**

* `nodes[*].deps` → edges in the DAG.
* `budgets.max_concurrency` → scheduler semaphore.
* `policies.thresholds.*` → guard thresholds (block/redact).
* `io.inputs/outputs` (optional) → explicit data binding between nodes.

---

## Orchestrator internals

### Core components

* **`AgentRegistry`** — name → callable adapter
* **`Scheduler`** — executes nodes when dependencies are satisfied; respects budgets
* **`Node`** — metadata (deps, guard flags, params, timeouts)

### Execution model

1. Build `id → Node`, `id → deps`.
2. Start **ready** nodes (no unmet deps), limited by `max_concurrency`.
3. On completion, **fan-out** results to children; queue next ready nodes.
4. Apply **pre/post guard** where configured.
5. Enforce **timeouts** and **retries** (node-level).

### Planner hints

```yaml
planner:
  prefer_parallel_for_independent_leaves: true
  serialize_when_memory_low: true
  critical_path_bias: true
  degrade_model_tiers_if_needed: true
```

---

## Agent interface

Agents are small async functions with a stable signature. You can wrap BitNet/ONNX/CPP backends behind them.

```python
async def agent_name(text: str, **params) -> dict:
    """
    Returns:
      { "text": "...", ... }  # primary payload under "text"
    """
```

**Examples**

* `bitnet.summarizer(text, max_sentences=3)`
* `bitnet.claimcheck(text, claim="...")`
* `bitnet.synthesis(text, pieces=[...])`

Keep outputs **JSON-serializable**, deterministic where possible (for tests), and small.

---

## Guard design

* **PII redaction** (regex + model): email, phone by default; extend with custom patterns.
* **Toxicity/Jailbreak**: thresholds decide *allow / redact / block*.
* **Moderation card** attaches to outputs:

```json
{
  "guard_version": "v0.1",
  "decisions": [
    {
      "node": "output",
      "allowed": true,
      "labels": {"toxicity": 0.03, "jailbreak": 0.04, "pii": 0.81},
      "actions": ["redact"],
      "redactions": [{"span":[18,36],"type":"PII.email"}],
      "why": "PII redacted; scores below thresholds"
    }
  ]
}
```

**Placement**

* Always **pre-guard** user inputs.
* Always **post-guard** final outputs.
* Use **per-node guard** for risky tools (code exec, network calls).

---

## Budgets & device profiles

```yaml
device_profile:
  mode: auto        # phone | sbc | vps
budgets:
  latency_ms: 1800
  deadline_ms: 4000
  max_concurrency: 2
  memory_mb: 1200
```

* The scheduler enforces **concurrency caps** and may serialize under pressure.
* The planner biases the **critical path** to improve p50/p95 latency.

**Latency budgeting (example)**

* Parse: 300–500 ms
* Claim checks (parallel): \~2 × 400–600 ms (critical path uses the slower leaf)
* Reduce: 200–300 ms
* Guard overhang: 50–120 ms
  → Target `latency_ms ≈ 1.8s` on CPU-only edge profile.

---

## Observability

* **Traces**: per-node timings, decisions, provenance.
* **Redaction**: `tracing.redact_pii_in_traces: true`.
* **Provenance**: reducer includes which leaves fed the output.

```yaml
tracing:
  enabled: true
  redact_pii_in_traces: true
  save_provenance: true
```

---

## Failure modes & mitigations

| Failure             | Symptom                  | Mitigation                                                               |
| ------------------- | ------------------------ | ------------------------------------------------------------------------ |
| Guard blocks input  | Request rejected         | Safe refusal template; allow user to reframe                             |
| Guard blocks output | No final response        | `on_error.node.blocked_post: regenerate_safe` (fallback template)        |
| OOM / slow on edge  | Crashes or large p95     | Lower `max_concurrency`, shorten inputs; enable serialize-under-pressure |
| Model not found     | Agent fails to load      | Use placeholders; document `models.*_path` overrides                     |
| RAG misses          | “uncertain” claim checks | Add small KB (DuckDB+FAISS), improve chunking, add aliases/synonyms      |
| Threshold mismatch  | Over-/under-blocking     | Tune `toxicity_block`, `jailbreak_block`, expand PII patterns            |

---

## Packaging & deployment

* **Colab / Notebook** — fast demo path (no install).
* **Local** — `pip install -r orchestrator/requirements.txt`.
* **Edge** — prefer CPU paths first; later, enable ONNX Runtime EPs or native BitNet builds.

**AGPL §13 Compliance**

* Expose `/source` endpoint or UI footer with **exact commit**.
* Add `X-AGPL-Source` header (see `COMPLIANCE.md`).

---

## Security notes

* Never commit real PII in examples. Use `test@example.com` and reserved numbers.
* Keep **PII redaction before logging**.
* See **[SECURITY](../SECURITY.md)** for reporting and the PGP contact.

---

## Next

* Read the **[Quickstart](./quickstart.md)** to run the demo.
* Tune thresholds in **[Safety](./safety.md)**.
* Explore the **[Pipeline API](./api.md)** to define your own DAGs.

```
::contentReference[oaicite:0]{index=0}
```
