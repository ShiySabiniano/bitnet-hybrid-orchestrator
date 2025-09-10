---
name: Feature request
about: Propose an enhancement for BitNet Hybrid Orchestrator
title: "[feat] <short summary>"
labels: enhancement
assignees: ""
---

<!--
Please check existing issues first. For security-sensitive ideas (e.g., new tool exec, network access),
do NOT file publicly—see SECURITY.md.

Be as specific as possible; small, focused requests ship faster.
-->

## Summary
A clear, concise description of the feature and the problem it solves.

## Motivation / Use Case
- Who benefits (operator, developer, end user)?
- What is painful today?
- Why is this important on **edge** devices?

## Proposal
Describe the solution at a high level. Include diagrams or pseudo-code if helpful.

### API / Schema Changes (if any)
- Orchestrator public API:
- New/changed agents:
- `orchestrator/pipeline.yml` schema deltas:
  ```yaml
  # example
  nodes:
    - id: new_node
      agent: tools.retriever
      deps: [parse]
      guard_pre: true
      params: { k: 4 }
````

### UX / CLI (if any)

New commands, flags, or configuration. Example usage:

```bash
orchestrator run --pipeline orchestrator/pipeline.yml --input file.txt
```

## Alternatives Considered

* Option A:
* Option B:
* Why the proposal is preferable:

## Scope

* **In scope:** …
* **Out of scope:** …

## Risks & Mitigations

| Risk                  | Impact | Likelihood | Mitigation                                      |
| --------------------- | ------ | ---------- | ----------------------------------------------- |
| Threshold regressions | Medium | Medium     | Add guard eval set to CI                        |
| Memory use on SBCs    | High   | Medium     | Serialize under pressure; cap `max_concurrency` |

## Security / Safety / Privacy

* Guard implications (PII redaction, jailbreak/toxicity thresholds):
* Per-node `guard_pre/guard_post` needed?
* Any new external calls / tool exec?
* Telemetry/logging changes (ensure `tracing.redact_pii_in_traces: true`)

## Performance / Resource Targets

* Expected latency impact (p50/p95):
* Memory footprint (MB):
* Concurrency considerations:

## Compatibility

* Backward compatible?
* Migration steps (docs needed? deprecation period?):

## Dependencies & Licensing

* New packages or model weights?
* Add entries to `THIRD_PARTY_LICENSES.md` with license and source URL.
* AGPL considerations for network-served use (see `COMPLIANCE.md`).

## Acceptance Criteria

* [ ] Feature flag or config toggle (default safe)
* [ ] Unit tests / golden tests
* [ ] Docs updated (`docs/*` and README Quick Links if applicable)
* [ ] Example in Colab or a minimal script
* [ ] CI passes

## Additional Context

Links to prior discussions, benchmarks, mockups, related issues/PRs, or external references.

```
::contentReference[oaicite:0]{index=0}
```
