---
nav_order: 5
title: Pipeline API (YAML Schema)
---

# Pipeline API

Define hybrid workflows as **config-as-data**. The orchestrator reads a single YAML file and builds a mixed **DAG** (hierarchical plan with sequential and parallel nodes), applies **guards**, and enforces **budgets**.

This page documents the schema used by `orchestrator/pipeline.yml`.

---

## File header

```yaml
version: 0.1.0                 # ← pipeline file version (project-specific)
schema: pipeline.v1            # ← schema id (for future migrations)
name: summarize_and_verify
description: |
  Summarize an input, check claims in parallel, then synthesize a brief.
owners:
  - Shiy Sabiniano
````

---

## Top-level keys

### `device_profile` (optional)

Hints the planner uses to size models and concurrency on edge devices.

```yaml
device_profile:
  mode: auto        # one of: auto | phone | sbc | vps
  caps:
    cpu_threads: auto
    memory_mb: auto
```

### `budgets`

Runtime limits enforced by the scheduler.

```yaml
budgets:
  latency_ms: 1800        # soft target
  deadline_ms: 4000       # hard kill deadline
  max_concurrency: 2      # upper bound on concurrent nodes
  memory_mb: 1200         # soft memory budget (advisory)
```

### `models`

Logical model names used by agents and guard. (You can also pin paths.)

```yaml
models:
  reasoner: bitnet-s-1.58b
  guard: tinybert-onnx-int8
  embedder: mini-embed-small        # optional, for RAG
  # reasoner_path: /models/bitnet/bitnet-s-1.58b.onnx
  # guard_path:    /models/tinybert/tinybert-int8.onnx
```

### `storage` (optional)

Built-ins for KV cache and a tiny local RAG setup.

```yaml
storage:
  kv_cache:
    enabled: true
    max_items: 64
  rag_index:
    enabled: false
    db_path: ./data/rag.duckdb
    vector_index: ./data/faiss.index
```

### `policies`

Guard thresholds and output behavior.

```yaml
policies:
  thresholds:
    toxicity_block: 0.50
    pii_redact: 0.70
    jailbreak_block: 0.60
  redactions:
    email: true
    phone: true
  output:
    append_moderation_card: true
    safe_templates:
      fallback_enabled: true
```

### `tracing`

Minimal observability with privacy in mind.

```yaml
tracing:
  enabled: true
  redact_pii_in_traces: true
  save_provenance: true
```

---

## Nodes (the DAG)

Each node declares its **agent**, **dependencies**, guard flags, and parameters.

```yaml
nodes:
  - id: parse
    agent: bitnet.summarizer
    deps: []                    # no deps → root
    guard_pre: true             # input filter (TinyBERT)
    guard_post: true            # output moderation
    timeout_ms: 900
    max_retries: 0
    params:
      max_sentences: 3
    io:                         # optional explicit bindings
      inputs:
        text: ${source.text}
      outputs:
        text: ${result.text}

  - id: claim1
    agent: bitnet.claimcheck
    deps: [parse]
    guard_pre: false
    guard_post: true
    timeout_ms: 600
    max_retries: 1
    params:
      claim: "BitNet uses 1.58-bit weights"
      kb: []                    # if empty, use default agent KB
    io:
      inputs:
        text: ${nodes.parse.text}
      outputs:
        text: ${result.text}

  - id: claim2
    agent: bitnet.claimcheck
    deps: [parse]
    guard_pre: false
    guard_post: true
    timeout_ms: 600
    max_retries: 1
    params:
      claim: "TinyBERT is effective for classification"
      kb: []
    io:
      inputs:
        text: ${nodes.parse.text}
      outputs:
        text: ${result.text}

  - id: reduce
    agent: bitnet.synthesis
    deps: [claim1, claim2]      # ← parallel fan-in
    guard_pre: false
    guard_post: true
    timeout_ms: 800
    max_retries: 0
    params: {}
    io:
      inputs:
        text: ${nodes.parse.text}
        pieces:
          - ${nodes.claim1.text}
          - ${nodes.claim2.text}
      outputs:
        text: ${result.text}
```

### Node fields (reference)

| Field         | Type      | Default | Notes                                               |
| ------------- | --------- | ------- | --------------------------------------------------- |
| `id`          | string    | —       | Unique within file; becomes DAG node id             |
| `agent`       | string    | —       | Name in `AgentRegistry` (e.g., `bitnet.summarizer`) |
| `deps`        | string\[] | `[]`    | Parents that must complete before this node runs    |
| `guard_pre`   | bool      | `true`  | Run TinyBERT guard on input                         |
| `guard_post`  | bool      | `true`  | Run guard on output (recommended)                   |
| `timeout_ms`  | int       | `1000`  | Node-level timeout                                  |
| `max_retries` | int       | `0`     | Retries on failure/timeout                          |
| `params`      | object    | `{}`    | Freeform kwargs passed to agent                     |
| `io.inputs`   | object    | —       | Explicit input bindings (see **Bindings**)          |
| `io.outputs`  | object    | —       | Map agent result → named outputs                    |

---

## Bindings (data wiring)

Use **templated references** to pass values between nodes:

* **Source input:** `${source.text}` — the initial payload provided by the runner.
* **From another node:** `${nodes.<id>.<field>}` — e.g., `${nodes.parse.text}`.
* **From current result:** `${result.text}` — the agent’s returned payload.

> The orchestrator injects the agent’s returned dict under `result`. By convention, agents put their main payload under `text`.

---

## Planner & error handling (optional)

```yaml
planner:
  prefer_parallel_for_independent_leaves: true
  serialize_when_memory_low: true
  critical_path_bias: true
  degrade_model_tiers_if_needed: true

on_error:
  strategy: partial_ok              # partial_ok | abort | best_effort
  node:
    blocked_pre: safe_refusal       # pre-guard blocks → return safe refusal
    blocked_post: regenerate_safe   # post-guard blocks → regenerate using safe template
  synthesis:
    missing_inputs: skip_and_label  # reducer notes missing leaves in summary
```

---

## Validation rules

* `nodes[*].id` **must be unique**.
* The graph formed by `deps` **must be acyclic**.
* All `deps` must reference existing node ids.
* Guards: enabling `guard_post: false` on the final node is allowed but **not recommended**.
* Template references in `io` must resolve to known sources: `source`, `nodes.<id>`, or `result`.

---

## Minimal example

```yaml
version: 0.1.0
schema: pipeline.v1
name: tiny_demo
budgets: { latency_ms: 1200, max_concurrency: 1, memory_mb: 512 }
models:  { reasoner: bitnet-s-1.58b, guard: tinybert-onnx-int8 }
policies:
  thresholds: { toxicity_block: 0.5, pii_redact: 0.7, jailbreak_block: 0.6 }
nodes:
  - { id: parse,  agent: bitnet.summarizer, guard_pre: true, guard_post: true }
  - { id: reduce, agent: bitnet.synthesis,  deps: [parse], guard_post: true }
```

---

## Advanced example (with RAG and explicit I/O)

```yaml
storage:
  rag_index:
    enabled: true
    db_path: ./data/rag.duckdb
    vector_index: ./data/faiss.index

nodes:
  - id: parse
    agent: bitnet.summarizer
    deps: []
    guard_pre: true
    guard_post: true
    params: { max_sentences: 4 }
    io:
      inputs:  { text: ${source.text} }
      outputs: { text: ${result.text}, key_phrases: ${result.key_phrases} }

  - id: retrieve
    agent: tools.retriever
    deps: [parse]
    guard_pre: false
    guard_post: false
    params:
      k: 4
    io:
      inputs:  { query: ${nodes.parse.key_phrases} }
      outputs: { chunks: ${result.chunks} }

  - id: verify
    agent: bitnet.claimcheck
    deps: [parse, retrieve]
    guard_post: true
    params:
      claim: "BitNet uses 1.58-bit weights"
    io:
      inputs:
        text: ${nodes.parse.text}
        kb:   ${nodes.retrieve.chunks}
      outputs:
        text: ${result.text}

  - id: reduce
    agent: bitnet.synthesis
    deps: [verify]
    guard_post: true
    io:
      inputs:
        text: ${nodes.parse.text}
        pieces:
          - ${nodes.verify.text}
      outputs:
        text: ${result.text}
```

---

## Agent contract (for implementers)

Agents are simple async callables registered under a **name**:

```python
async def my_agent(text: str, **params) -> dict:
    """
    Return a JSON-serializable dict.
    The primary payload should be under 'text' for consistency.
    """
    return {"text": "...", "extra": {...}}
```

* Use **typed dicts / pydantic** if you want schema validation at the boundaries.
* Keep outputs small and deterministic where possible (simplifies tests).

---

## Security notes (schema-level)

* Keep `guard_pre: true` on user-facing roots and `guard_post: true` on the last node.
* Redact PII **before** traces: `tracing.redact_pii_in_traces: true`.
* If any node calls tools/exec/network, consider setting `guard_pre: true` for that node.

---

## Runner input (example)

The pipeline expects the runner to pass a **source** object (e.g., via CLI/SDK):

```json
{
  "source": {
    "text": "Contact me at test@example.com. BitNet b1.58 is efficient..."
  }
}
```

Your runner binds `${source.text}` to the root node’s input when executing.

---

## Tips

* Start with **`max_concurrency: 1–2`** on CPU-only devices.
* Place heavier work on **parallel leaves**; keep reducers light.
* Prefer **file-level** changes in YAML over hard-coding logic in agents: easier to test and review.

---

```
::contentReference[oaicite:0]{index=0}
```
