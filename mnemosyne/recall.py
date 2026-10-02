"""
Mnemosyne Recall - semantic retrieval over the memory graph with Λ-Logos,
and the boot context pack for a new session.
"""

from typing import Dict, List, Tuple

import numpy as np

from mnemosyne import checkpoint as chk
from mnemosyne.graph import MEMORY_DIR, MemoryGraph, load_graph


# Weight of the latent (semantic) channel; the rest is the lexical channel.
# 0.5 measured MRR 0.78 vs 0.70 for pure latent on the memory recall set
# (tests/test_mnemosyne.py::test_recall_benchmark).
DEFAULT_ALPHA = 0.5


def query(text: str, top_k: int = 5, memory_dir: str = MEMORY_DIR,
          alpha: float = DEFAULT_ALPHA) -> List[Dict]:
    """
    Find the memory entries most relevant to a question.

    Ranking blends two channels of Λ-Logos (the project's own model): the
    trained latent space (meaning) and the untrained hashed projection
    (exact terms, e.g. "CPU spike"). Each hit includes its graph
    neighbourhood, so the answer comes with its reasons.

    Args:
        text: Natural-language question
        top_k: Number of entries to return
        alpha: Latent-channel weight in [0, 1] (1 = purely semantic)

    Returns:
        Hits: id, title, file, score, neighbors [(edge kind, other id)]
    """
    from logos import LogosEmbedder, get_model
    graph = load_graph(memory_dir)
    entries = [e for e in graph.entries.values() if e.kind != "checkpoint"]
    if not entries:
        return []
    semantic = get_model()
    lexical = LogosEmbedder(n_features=semantic.n_features, dim=semantic.dim, seed=semantic.seed)
    texts = [e.text for e in entries]
    scores = (alpha * (semantic.embed_batch(texts) @ semantic.embed(text))
              + (1 - alpha) * (lexical.embed_batch(texts) @ lexical.embed(text)))
    hits = []
    for idx in np.argsort(-scores, kind="stable")[:top_k]:
        entry = entries[int(idx)]
        neighbors: List[Tuple[str, str]] = []
        for edge in graph.neighbors(entry.id):
            other = edge.target if edge.source == entry.id else edge.source
            direction = edge.kind if edge.source == entry.id else f"{edge.kind}←"
            neighbors.append((direction, other))
        hits.append({"id": entry.id, "title": entry.title, "file": entry.file,
                     "score": float(scores[idx]), "neighbors": neighbors})
    return hits


def boot_pack(memory_dir: str = MEMORY_DIR) -> str:
    """
    Compact context for starting a session: intention, laws, state, last
    checkpoint, open next steps. Read this first; follow IDs for depth.

    Returns:
        Markdown text
    """
    graph: MemoryGraph = load_graph(memory_dir)

    def section(kind: str, title: str, statuses=None) -> List[str]:
        lines = [f"## {title}"]
        for entry in sorted(graph.by_kind(kind), key=lambda e: e.id):
            if statuses is None or entry.status in statuses:
                lines.append(f"- {entry.id} · {entry.title}")
        return lines + [""]

    last = chk.latest(memory_dir)
    lines = ["# ΛΕΩΝΙΔΑΣ-AI PHALANX — Boot Pack", ""]
    lines += section("intention", "Intention")
    lines += section("law", "Laws (never violate)", {"active"})
    lines += section("state", "Current state")
    lines += ["## Last checkpoint",
              f"- {last.id} · {last.title}" if last else "- none", ""]
    lines += section("extension", "Next (planned / in progress)", {"planned", "in_progress", "open"})
    lines += ["Protocol: .memory/PROTOCOL.md · Query: python -m mnemosyne query \"...\""]
    return "\n".join(lines)
