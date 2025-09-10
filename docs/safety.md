---
nav_order: 4
title: Safety & Guardrails
---

# Safety & Guardrails

This project uses a **TinyBERT Guard** to protect both inputs and outputs. It detects and mitigates **PII**, **toxicity/abuse**, and **jailbreak attempts**, and can optionally gate high-risk nodes (e.g., code exec, external tools).

- **Input Filter (pre-guard):** cleans and blocks unsafe prompts before orchestration.
- **Per-Node Gate (optional):** wraps risky nodes in the DAG.
- **Output Moderation (post-guard):** redacts PII and enforces policy before returning a response.
- **Moderation Card:** attaches a compact JSON record of decisions to outputs.

See also: [SECURITY](../SECURITY.md) and [COMPLIANCE](../COMPLIANCE.md).

---

## Configuration

The guard is configured via `policies.thresholds` and `policies.redactions` in your pipeline:

```yaml
# orchestrator/pipeline.yml (excerpt)
policies:
  thresholds:
    toxicity_block: 0.50      # block > 0.50
    pii_redact: 0.70          # redact if score/prob >= 0.70
    jailbreak_block: 0.60     # block > 0.60
  redactions:
    email: true
    phone: true
  output:
    append_moderation_card: true
    safe_templates:
      fallback_enabled: true
