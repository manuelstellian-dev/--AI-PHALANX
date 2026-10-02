"""
Λ-Logos Corpus - the project's own knowledge, as training documents.

Sources (all local, all versioned in the repository):
- SPARTA Foundation concepts (sparta/semantic_memory.jsonl)
- Project memory (.memory/*.md)
- Documentation (*.md at the root and under docs/), chunked by heading

The file order is sorted, so the same repository state always yields the same
corpus and therefore the same model fingerprint.
"""

import glob
import json
import os
import re
from typing import List, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

_HEADING_RE = re.compile(r"^#{1,4}\s+", re.MULTILINE)
MIN_CHUNK_CHARS = 40


def concept_text(concept: dict) -> str:
    """Flatten a 16-field SPARTA concept into one training document."""
    parts = [concept.get("topic", ""), concept.get("definition", ""),
             concept.get("formal_statement", ""), concept.get("subdomain", "")]
    for key in ("examples", "applications", "counterexamples"):
        parts.extend(concept.get(key, []))
    return ". ".join(p for p in parts if p)


def sparta_documents(root: str = REPO_ROOT) -> List[Tuple[str, str]]:
    """(source, text) for every SPARTA concept."""
    path = os.path.join(root, "sparta", "semantic_memory.jsonl")
    docs: List[Tuple[str, str]] = []
    if not os.path.exists(path):
        return docs
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                concept = json.loads(line)
                docs.append((f"sparta:{concept['id']}", concept_text(concept)))
    return docs


def markdown_chunks(path: str, root: str = REPO_ROOT) -> List[Tuple[str, str]]:
    """Split a Markdown file into heading-delimited chunks."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    rel = os.path.relpath(path, root)
    starts = [m.start() for m in _HEADING_RE.finditer(text)] or [0]
    if starts[0] != 0:
        starts.insert(0, 0)
    chunks = []
    for i, start in enumerate(starts):
        chunk = text[start:starts[i + 1] if i + 1 < len(starts) else len(text)].strip()
        if len(chunk) >= MIN_CHUNK_CHARS:
            title = chunk.splitlines()[0].lstrip("#").strip()[:80]
            chunks.append((f"{rel}#{title}", chunk))
    return chunks


def markdown_files(root: str = REPO_ROOT) -> List[str]:
    """Sorted Markdown sources: root, docs/ and .memory/."""
    patterns = ["*.md", os.path.join("docs", "**", "*.md"), os.path.join(".memory", "*.md")]
    files = set()
    for pattern in patterns:
        files.update(glob.glob(os.path.join(root, pattern), recursive=True))
    return sorted(files)


def build_corpus(root: str = REPO_ROOT) -> List[Tuple[str, str]]:
    """
    Build the default training corpus.

    Returns:
        List of (source id, text), deterministic for a given repository state
    """
    docs = sparta_documents(root)
    for path in markdown_files(root):
        docs.extend(markdown_chunks(path, root))
    return docs
