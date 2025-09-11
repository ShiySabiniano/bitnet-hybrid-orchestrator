#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
ui/chat_gradio.py

Multi-turn chat UI for the BitNet Hybrid Orchestrator.
- Keeps a rolling transcript (User/Assistant) and feeds it into the same hybrid DAG:
    parse → [claim1, claim2] (parallel) → reduce
- Runs the TinyBERT-style guard on input and output each turn.
- Reuses the tiny orchestrator pieces from `orchestrator/cli.py`.

Usage:
  pip install -r orchestrator/requirements.txt
  pip install -r ui/requirements.txt
  python ui/chat_gradio.py
"""

import os
import json
import asyncio
from typing import List, Tuple

import gradio as gr

# Allow run_until_complete inside notebooks/Gradio
try:
    import nest_asyncio  # type: ignore
    nest_asyncio.apply()
except Exception:
    pass

# --- Import orchestrator primitives (Registry, Scheduler, Node, guard, agents) ---
try:
    # These should exist in your repo per README layout
    from orchestrator.cli import (
        Registry,
        Scheduler,
        Node,
        guard,          # TinyBERT-style guard instance
        summarizer,     # demo agent
        claimcheck,     # demo agent
        synthesis,      # demo agent
    )
except ImportError as e:
    # Helpful error if the orchestrator file isn't present
    raise SystemExit(
        "ERROR: Could not import orchestrator primitives from 'orchestrator/cli.py'.\n"
        "Make sure your repo includes that file (see README layout) and your PYTHONPATH "
        "includes the repo root. Original error:\n" + repr(e)
    )


# ---------------------------
# Helpers
# ---------------------------
def _format_transcript(history: List[Tuple[str, str]], user_msg: str) -> str:
    """
    Convert chat history + new user message to a transcript string consumed by the pipeline.
    History is a list of [user, assistant] pairs from gr.Chatbot.
    """
    lines: List[str] = []
    for u, a in history:
        if u:
            lines.append(f"User: {u}")
        if a:
            lines.append(f"Assistant: {a}")
    lines.append(f"User: {user_msg}")
    return "\n".join(lines).strip()


def _build_nodes(claim1: str, claim2: str, max_sentences: int) -> List[Node]:
    """
    Construct the DAG used by the demo:
      parse → [claim1, claim2] → reduce
    """
    return [
        Node(
            id="parse",
            agent="bitnet.summarizer",
            deps=[],
            guard_pre=True,
            guard_post=True,
            timeout_ms=900,
            max_retries=0,
            params={"max_sentences": int(max_sentences)},
        ),
        Node(
            id="claim1",
            agent="bitnet.claimcheck",
            deps=["parse"],
            guard_pre=False,
            guard_post=True,
            timeout_ms=600,
            max_retries=1,
            params={"claim": claim1, "kb": []},
        ),
        Node(
            id="claim2",
            agent="bitnet.claimcheck",
            deps=["parse"],
            guard_pre=False,
            guard_post=True,
            timeout_ms=600,
            max_retries=1,
            params={"claim": claim2, "kb": []},
        ),
        Node(
            id="reduce",
            agent="bitnet.synthesis",
            deps=["claim1", "claim2"],
            guard_pre=False,
            guard_post=True,
            timeout_ms=800,
            max_retries=0,
            params={},
        ),
    ]


def _run(transcript: str, claim1: str, claim2: str, max_sentences: int) -> dict:
    """
    Register demo agents, build nodes, and execute the DAG.
    Returns the full results map {node_id: result_dict}.
    """
    reg = Registry()
    reg.register("bitnet.summarizer", summarizer)
    reg.register("bitnet.claimcheck", claimcheck)
    reg.register("bitnet.synthesis", synthesis)

    nodes = _build_nodes(claim1, claim2, max_sentences)
    sched = Scheduler(registry=reg, guard=guard, max_concurrency=2)

    async def _go():
        return await sched.run_dag(nodes, {"text": transcript})

    # Use the current loop (nest_asyncio makes this safe in Gradio)
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_go())


def chat_predict(history, user_msg, max_sentences, claim1, claim2, show_mod):
    """
    Gradio event handler for sending a chat turn.
    """
    # Build transcript from history + this user message
    transcript = _format_transcript(history, user_msg)

    # Execute DAG
    results = _run(transcript, claim1, claim2, max_sentences)

    # Compose assistant reply from the reducer
    reply = (results.get("reduce", {}) or {}).get("text", "").strip() or "(no response)"

    # Optional: moderation JSON + guard mode
    if show_mod:
        modcards = {}
        for nid, r in results.items():
            if "_moderation" in r:
                modcards[nid] = [
                    {
                        "node": m.get("node"),
                        "actions": m.get("actions"),
                        "labels": {k: round(float(v), 2) for k, v in m.get("labels", {}).items()},
                        "why": m.get("why"),
                    }
                    for m in r["_moderation"]
                ]
        debug = json.dumps(
            {"guard_mode": getattr(guard, "mode", "n/a"), "modcards": modcards},
            indent=2,
        )
    else:
        debug = ""

    # Update chat history (clear input box)
    history = history + [[user_msg, reply]]
    guard_mode = getattr(guard, "mode", "n/a")
    return history, "", debug, guard_mode


def main():
    repo = "https://github.com/ShiySabiniano/bitnet-hybrid-orchestrator"
    commit = os.getenv("APP_COMMIT_SHA", "HEAD")

    with gr.Blocks() as app:
        gr.Markdown("## BitNet Hybrid Orchestrator — Chat")
        gr.Markdown(
            "Multi-turn chat that runs the hybrid pipeline each turn.\n\n"
            "**Flow:** `parse → [claim1, claim2] (parallel) → reduce` with guard on input & output."
        )

        with gr.Row():
            maxs = gr.Slider(1, 8, value=3, step=1, label="Summary sentences")
            c1 = gr.Textbox(label="Claim 1", value="BitNet uses 1.58-bit weights")
            c2 = gr.Textbox(label="Claim 2", value="TinyBERT is effective for classification")
            show_mod = gr.Checkbox(label="Show moderation JSON", value=False)

        chat = gr.Chatbot(height=460, label="Chat with the orchestrator")
        user_in = gr.Textbox(placeholder="Type your message…", label="Message")

        with gr.Row():
            send = gr.Button("Send", variant="primary")
            clear = gr.Button("Clear")

        dbg = gr.JSON(label="Debug (moderation + guard mode)")
        mode_out = gr.Textbox(label="Guard mode", interactive=False)

        # Wire interactions
        send.click(
            chat_predict,
            inputs=[chat, user_in, maxs, c1, c2, show_mod],
            outputs=[chat, user_in, dbg, mode_out],
        )
        user_in.submit(
            chat_predict,
            inputs=[chat, user_in, maxs, c1, c2, show_mod],
            outputs=[chat, user_in, dbg, mode_out],
        )

        def _clear():
            return [], "", "", getattr(guard, "mode", "n/a")

        clear.click(_clear, outputs=[chat, user_in, dbg, mode_out])

        # AGPL §13 hint in footer
        try:
            app.footer = f"Source: [{commit[:7]}]({repo}/tree/{commit}) • License: AGPL-3.0-or-later"
        except Exception:
            pass

    # modest queue; tune as needed
    app.queue(concurrency_count=1, max_size=16).launch()


if __name__ == "__main__":
    main()
