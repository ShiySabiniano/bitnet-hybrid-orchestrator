---
name: "🐞 Bug report"
about: "Report a reproducible problem in BitNet Hybrid Orchestrator"
title: "Bug: <short summary>"
labels: ["bug", "triage"]
assignees: []
---

<!--
⚠️ If this is a QUESTION or IDEA, please use Discussions instead:
https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator/discussions

⚠️ If this report involves a SECURITY vulnerability, do NOT open a public issue.
Please follow SECURITY.md:
- GitHub: Security → Report a vulnerability
- PGP: security/pgp/ShiySabiniano.asc
-->

## Summary
A clear, concise description of the problem and its impact.

## Environment
- **Repo commit** (paste `git rev-parse HEAD` or link the commit):  
- **OS**: [Linux/macOS/Windows] (+ version)  
- **Python**: `python --version`  
- **Install method**: [pip / venv / conda / Colab]  
- **Guard mode** (from output): [`regex-only` | `onnx+regex`]  
- **Orchestrator deps** (`pip freeze | grep -E 'onnxruntime|transformers|huggingface|duckdb|faiss|pydantic|rich|typer'`):  
- **UI deps** if used (`pip freeze | grep -E 'gradio|nest_asyncio'`):  

## Area(s) affected
- [ ] Orchestrator (Scheduler / DAG / merge semantics)
- [ ] Guard (TinyBERT / ONNX / regex PII / thresholds)
- [ ] Agents (summarizer / claimcheck / synthesis)
- [ ] UI (Gradio single-turn / Chat mode)
- [ ] Colab notebook
- [ ] Docs (README / docs/)
- [ ] Pipeline schema / YAML
- [ ] CI / Packaging

## Version / Config context
- `orchestrator/pipeline.yml` or `orchestrator/pipeline.chat.yml` used (paste or attach minimal relevant excerpt):
  ```yaml
  # minimal snippet here (redact secrets/PII)
