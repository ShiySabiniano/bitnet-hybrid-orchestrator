#!/usr/bin/env python
"""
Minimal CLI runner for BitNet Hybrid Orchestrator demo.
Loads sample text or a file, runs the mixed DAG with guard, prints results.
"""
import argparse, asyncio, json, sys, re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Callable

# ---- Tiny guard (regex PII; mirrors notebook fallback) ----
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?:\+?\d{1,3}[\s\-\.]?)?(?:\(?\d{3}\)?[\s\-\.]?)\d{3}[\s\-\.]?\d{4}\b")

class Guard:
    def check(self, text: str, mode="input") -> Dict[str, Any]:
        redactions = []
        out = EMAIL.sub("[REDACTED_EMAIL]", text)
        if out != text: redactions.append({"type":"PII.email"})
        out2 = PHONE.sub("[REDACTED_PHONE]", out)
        if out2 != out: redactions.append({"type":"PII.phone"})
        return {"allowed": True, "text": out2, "labels":{"pii": 1.0 if redactions else 0.0}, "actions": ["redact"] if redactions else []}

guard = Guard()

# ---- Orchestrator core (trimmed) ----
@dataclass
class Node:
    id: str
    agent: str
    deps: List[str] = field(default_factory=list)
    guard_pre: bool = True
    guard_post: bool = True
    timeout_ms: int = 1000
    max_retries: int = 0
    params: Dict[str, Any] = field(default_factory=dict)

class Registry:
    def __init__(self): self._a: Dict[str, Callable[..., Any]] = {}
    def register(self, name, fn): self._a[name]=fn
    async def run(self, name, **kw): return await self._a[name](**kw)

class Scheduler:
    def __init__(self, registry: Registry, guard: Guard, max_concurrency=2):
        import asyncio
        self.r, self.g, self.sema = registry, guard, asyncio.Semaphore(max_concurrency)
    async def _run(self, n: Node, payload: Dict[str, Any]):
        if n.guard_pre:
            g = self.g.check(payload.get("text",""), "input")
            if not g["allowed"]: raise RuntimeError("blocked_pre")
            payload = dict(payload, text=g["text"])
        res = await self.r.run(n.agent, **n.params, **payload)
        if n.guard_post:
            g2 = self.g.check(res.get("text",""), "output")
            if not g2["allowed"]: raise RuntimeError("blocked_post")
            res["text"] = g2["text"]
        res["_node"] = n.id
        return res
    async def run_dag(self, nodes: List[Node], sources: Dict[str, Any]):
        id2 = {n.id:n for n in nodes}; deps = {n.id:set(n.deps) for n in nodes}
        ready = [n.id for n in nodes if not n.deps]
        inbuf = {rid: dict(sources) for rid in ready}; running={}
        async def launch(i): running[i]=asyncio.create_task(self._run(id2[i], inbuf[i]))
        for i in ready: await launch(i)
        results={}
        while running:
            done,_ = await asyncio.wait(running.values(), return_when=asyncio.FIRST_COMPLETED)
            for i,t in list(running.items()):
                if t in done:
                    results[i]=await t; running.pop(i)
                    for c, ds in deps.items():
                        if i in ds:
                            ds.remove(i); inbuf.setdefault(c,{}).update(results[i])
                    for c, ds in list(deps.items()):
                        if not ds and c not in results and c not in running:
                            await launch(c)
        return results

# ---- Demo agents (same as notebook, trimmed) ----
import re
def _sents(x): return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", x) if s.strip()]

async def summarizer(text: str, max_sentences: int=3, **_):
    s = _sents(text); keep = s[:max(1, max_sentences)]
    return {"text": " ".join(keep)}

def _tok(s): return re.findall(r"[A-Za-z0-9]+", s.lower())
async def claimcheck(text: str, claim: str, **_):
    verdict = "supported" if all(t in _tok(text) for t in _tok(claim)) else "uncertain"
    return {"text": f"Claim: {claim} → {verdict}"}

async def synthesis(text: str, pieces: List[str]=None, **_):
    pieces = pieces or []
    return {"text": "Executive Brief:\n- " + "\n- ".join([p.splitlines()[0] for p in pieces if p.strip()])}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="Inline text or @path/to/file.txt", required=False)
    args = ap.parse_args()

    if args.input and args.input.startswith("@"):
        with open(args.input[1:], "r", encoding="utf-8") as f:
            text = f.read()
    elif args.input:
        text = args.input
    else:
        text = "Contact me at test@example.com. BitNet b1.58 enables efficient ~1.58-bit weights. TinyBERT helps safety."

    reg = Registry()
    for name, fn in [("bitnet.summarizer", summarizer), ("bitnet.claimcheck", claimcheck), ("bitnet.synthesis", synthesis)]:
        reg.register(name, fn)

    nodes = [
        Node("parse", "bitnet.summarizer", [], True, True, 900, 0, {"max_sentences": 3}),
        Node("claim1","bitnet.claimcheck",["parse"], False, True, 600, 1, {"claim":"BitNet uses 1.58-bit weights"}),
        Node("claim2","bitnet.claimcheck",["parse"], False, True, 600, 1, {"claim":"TinyBERT is effective for classification"}),
        Node("reduce","bitnet.synthesis", ["claim1","claim2"], False, True, 800, 0, {}),
    ]

    async def run():
        sched = Scheduler(reg, guard, max_concurrency=2)
        res = await sched.run_dag(nodes, {"text": text})
        for nid in ["parse","claim1","claim2","reduce"]:
            r = res.get(nid, {})
            print(f"\n=== {nid} ===\n{r.get('text','')}")
    try:
        asyncio.run(run())
    except RuntimeError:
        import nest_asyncio, asyncio as aio; nest_asyncio.apply(); aio.get_event_loop().run_until_complete(run())

if __name__ == "__main__":
    main()
