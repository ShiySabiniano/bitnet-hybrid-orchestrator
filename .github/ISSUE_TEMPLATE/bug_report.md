---
name: Bug report
about: Create a report to help us improve BitNet Hybrid Orchestrator
title: "[bug] <short summary>"
labels: bug
assignees: ""
---

<!--
⚠️ SECURITY: Do NOT report vulnerabilities here.
Use GitHub → Security → "Report a vulnerability" or email Troubleshooting@sabiniano.me (PGP in SECURITY.md).
Sanitize PII before posting (emails, phone numbers, tokens, keys).
-->

## Summary
A clear and concise description of the problem.

## Environment
- **Version / Commit SHA:** `git rev-parse HEAD` =
- **Install Type:** ☐ Colab ☐ Local
- **OS / CPU / RAM:** (e.g., Windows 11 / i7 / 16GB)
- **Python:** `python --version`
- **onnxruntime:** `python -c "import onnxruntime as ort; print(ort.__version__)"`
- **transformers:** `python -c "import transformers as t; print(t.__version__)"`
- **Other relevant packages:** (duckdb, faiss-cpu, etc.)

## Reproduction Steps
1. …
2. …
3. …

### Minimal `pipeline.yml` (sanitized)
> Include only the smallest snippet that reproduces the bug.

```yaml
version: 0.1.0
schema: pipeline.v1
name: repro
budgets: { latency_ms: 1800, max_concurrency: 2, memory_mb: 1200 }
policies:
  thresholds: { toxicity_block: 0.5, pii_redact: 0.7, jailbreak_block: 0.6 }
nodes:
  - { id: parse, agent: bitnet.summarizer, guard_pre: true, guard_post: true }
  # add any other nodes needed to reproduce
````

### Input sample (sanitized)

```text
<smallest input that triggers the issue, with PII removed>
```

## Expected Behavior

What you expected to happen.

## Actual Behavior

What actually happened (include error messages).

### Logs / Trace / Stack

\<copy relevant lines only; redact PII/tokens>

```
<stack trace or log snippet>
```

### Moderation Card (if relevant)

> If the guard blocked/redacted unexpectedly, paste the JSON decision for the affected node(s).

```json
{
  "node": "output",
  "allowed": true,
  "labels": {"toxicity": 0.03, "jailbreak": 0.04, "pii": 0.81},
  "actions": ["redact"]
}
```

### Screenshots (optional)

Attach images or GIFs showing the issue.

## Guard / Policy Settings

* `toxicity_block`: …
* `pii_redact`: …
* `jailbreak_block`: …
* Per-node `guard_pre` / `guard_post`: …

## Device Profile & Budgets

```
device_profile: { mode: auto }
budgets: { latency_ms: ..., deadline_ms: ..., max_concurrency: ..., memory_mb: ... }
```

## Reproducibility

* ☐ Always
* ☐ Intermittent
* ☐ Only under load / large inputs
* Notes:

## Severity

* ☐ P0 – crash / data loss / security bypass
* ☐ P1 – broken feature / incorrect result
* ☐ P2 – degraded performance / flaky behavior
* ☐ P3 – cosmetic / docs

## Workarounds

Any temporary steps that mitigate the issue.

## Additional Context

Links to related issues/PRs, hardware specifics, BitNet backend details, etc.

---

**AGPL §13 note (hosted instances):** if this bug occurs in a network-served deployment, please include the `X-AGPL-Source` header value and/or the exact commit link of the running service.

```
::contentReference[oaicite:0]{index=0}
```
