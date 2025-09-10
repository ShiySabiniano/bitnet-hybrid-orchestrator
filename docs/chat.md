# Chat mode (multi-turn)

**Chat mode** lets you talk to the orchestrator over multiple turns. Each new message is appended to a rolling **transcript** (“User:/Assistant:” lines) that feeds the same hybrid pipeline:  
`parse → [claim1, claim2] (parallel) → reduce`, with **TinyBERT Guard** on **input** and **output** every turn.

- Guard can **redact PII** in the transcript before processing.
- Output is moderated again and may be redacted before display.
- Works in **Colab** (shareable link) or **locally** with Gradio.

---

## Quickstart

### A) Google Colab (recommended first run)

1. Run **Cells 1 → 5** from the notebook to load deps, guard, orchestrator, and agents.  
2. Add the **chat UI** cell (named “Cell 6B — Chat Demo”) after Cell 5 and run it.  
   - If you used our Colab from the README, scroll to **Cell 6B** and run it.
3. Click the `*.gradio.live` link and start chatting.

**What it does**  
At every turn, the chat UI builds a transcript from the chat history + your new message, then calls the DAG with `sources={"text": transcript}`.

---

### B) Local run (Gradio app)

Install core + UI deps:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r orchestrator/requirements.txt
pip install -r ui/requirements.txt
````

Launch chat:

```bash
python ui/chat_gradio.py
```

Open the printed local URL (and/or a `gradio.live` URL). Type a message; each turn runs the hybrid pipeline and returns the **Executive Brief** as the assistant reply.

---

## How it works

### Transcript assembly

The chat UI formats the rolling history like:

```
User: hello
Assistant: Hi—what can I help with?
User: verify these points about BitNet and TinyBERT
```

This **transcript** becomes the `text` input to the pipeline’s root node (`parse`). The reducer’s output becomes the assistant reply for that turn.

### Guard (safety)

* **Pre-guard** runs on the transcript (redacts PII; may block if thresholds are exceeded).
* **Post-guard** runs on the synthesized reply (may redact or block).
* If you provide a TinyBERT **ONNX** model + tokenizer, the guard adds learned signals; otherwise heuristics are used for jailbreak cues plus regex PII.

Environment knobs:

```bash
# Optional: disable ONNX path entirely
export GUARD_DISABLE_ONNX=1
# Or provide an ONNX model and tokenizer directory
export TINYBERT_ONNX_PATH=/path/to/tinybert-int8.onnx
export TINYBERT_TOKENIZER_DIR=/path/to/tokenizer
```

---

## Configuration

You can keep chat fully UI-driven, or describe it in a pipeline file.

**`orchestrator/pipeline.chat.yml`**

```yaml
version: 0.1.0
schema: pipeline.v1
name: chat_orchestrator
budgets: { latency_ms: 2000, max_concurrency: 2, memory_mb: 1200 }
models: { reasoner: bitnet-s-1.58b, guard: tinybert-onnx-int8 }
policies:
  thresholds: { toxicity_block: 0.5, pii_redact: 0.7, jailbreak_block: 0.6 }

conversation:
  kind: transcript            # transcript | none
  window_messages: 12         # keep last N user/assistant pairs
  persist: false              # set true if you add a server with storage
  redact_pii_in_history: true # store only the redacted transcript

nodes:
  - { id: parse,  agent: bitnet.summarizer, guard_pre: true, guard_post: true, params: { max_sentences: 3 } }
  - { id: claim1, agent: bitnet.claimcheck, deps: [parse], params: { claim: "BitNet uses 1.58-bit weights" } }
  - { id: claim2, agent: bitnet.claimcheck, deps: [parse], params: { claim: "TinyBERT is effective for classification" } }
  - { id: reduce, agent: bitnet.synthesis,  deps: [claim1, claim2] }
```

* The **UI** uses this policy by default (same thresholds) even if you don’t load the YAML.
* To enforce a hard window, the UI truncates history to `window_messages`.

See **[docs/api.md](./api.md)** for the full schema.

---

## Customizing the chat

* **Claims:** In the UI, edit “Claim 1/2” fields; add more branches by extending the DAG (another `Node` with `deps: ["parse"]`).
* **Summary length:** Adjust “Summary sentences” (flows into the `summarizer` agent).
* **Replace agents with BitNet:** Keep function signatures (`async def summarizer(...) -> dict`) and route to your BitNet runtime.
* **RAG evidence:** Replace dummy lists with DuckDB/FAISS in the `claimcheck` agent.

---

## Troubleshooting

* **NameError: guard/Registry/Node not defined**
  Run cells **1 → 5** first (the chat UI reuses those globals).

* **“event loop already running”** in Colab
  We install and call `nest_asyncio.apply()` in the UI cell to allow `run_until_complete`. Re-run the chat cell once after installing.

* **No public link appears**
  Some environments disable sharing; still open the local URL in the cell output. In Colab, allow pop-ups and re-run.

* **Blocked output**
  Your reply hit a guard threshold. Lower `toxicity_block`/`jailbreak_block` in config (carefully), or revise the prompt.

* **Performance**
  This demo is CPU-only and deterministic. Swap the placeholder agents for accelerated BitNet backends when ready.

---

## FAQ

**Does chat remember earlier turns?**
Yes, within the configured **window** (`conversation.window_messages`). The transcript is passed into the pipeline every turn.

**Do you store my conversation?**
Colab sessions are ephemeral. The local UI keeps state in RAM only. If you build a server, follow the `persist` flag behavior and redact stored history (`redact_pii_in_history: true`).

**Streaming replies?**
Not in the demo. You can add streaming by emitting partial reducer output and sending incremental updates to the UI.

**Multi-user?**
The demo UI is single-tenant. For servers, create per-session state keyed by client id and apply your rate limits.

---

## Compliance & Security

If you host the chat over a network (even privately), **AGPL §13** requires exposing the **Corresponding Source** for the running commit. Add a footer link and/or an HTTP header like:

```
X-AGPL-Source: https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/tree/<COMMIT_SHA>
```

See **[COMPLIANCE.md](../COMPLIANCE.md)** and **[SECURITY.md](../SECURITY.md)**.

---

## See also

* **Architecture:** high-level diagrams and execution flow — **[docs/architecture.md](./architecture.md)**
* **Pipeline schema:** nodes, policies, conversation — **[docs/api.md](./api.md)**
* **Colab guide:** notebook cells and tips — **[docs/colab.md](./colab.md)**

```
::contentReference[oaicite:0]{index=0}
```
