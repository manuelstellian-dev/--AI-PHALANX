"""
Mnemosyne Checkpoints - a hash chain of verified repository states.

Each checkpoint records:
- tree:   SHA-256 over every repository file (path + content hash), excluding
          CHECKPOINT.md itself, so the checkpoint can live inside the tree
- commit: the git commit the work was based on
- prev:   the previous checkpoint's hash ("GENESIS" for the first)
- hash:   SHA-256 of the checkpoint's own canonical fields

Changing any recorded field, or any earlier checkpoint, breaks the chain.
Changing any repository file makes the latest checkpoint's tree "drift",
which `mnemosyne check --strict` reports, so a session cannot close without
a new save point.
"""

import hashlib
import os
import subprocess
from datetime import datetime, timezone
from typing import Dict, List, Optional

from mnemosyne.graph import Entry, MEMORY_DIR, REPO_ROOT, load_graph
from mnemosyne.measures import tracked_files

CHECKPOINT_FILE = ".memory/CHECKPOINT.md"
GENESIS = "GENESIS"
HASH_FIELDS = ("date", "agent", "commit", "tree", "prev", "gates")


def tree_hash(root: str = REPO_ROOT) -> str:
    """SHA-256 over all repository files except the checkpoint file."""
    tracked_files.cache_clear()
    h = hashlib.sha256()
    for rel in tracked_files(root):
        if rel == CHECKPOINT_FILE:
            continue
        with open(os.path.join(root, rel), "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        h.update(f"{rel}\0{digest}\n".encode("utf-8"))
    return h.hexdigest()


def entry_hash(entry_id: str, title: str, fields: Dict[str, str]) -> str:
    """Canonical hash of a checkpoint entry."""
    parts = [entry_id, title] + [f"{k}={fields.get(k, '')}" for k in HASH_FIELDS]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _field(entry: Entry, name: str) -> str:
    values = entry.get(name)
    return values[0] if values else ""


def chain(memory_dir: str = MEMORY_DIR) -> List[Entry]:
    """Checkpoint entries in file order."""
    graph = load_graph(memory_dir)
    return sorted(graph.by_kind("checkpoint"), key=lambda e: e.line)


def verify_chain(memory_dir: str = MEMORY_DIR) -> List[str]:
    """
    Verify every checkpoint's hash and link.

    Returns:
        Error messages (empty = chain intact)
    """
    errors = []
    prev = GENESIS
    for entry in chain(memory_dir):
        fields = {k: _field(entry, k) for k in HASH_FIELDS}
        if fields["prev"] != prev:
            errors.append(f"{entry.id}: prev={fields['prev'][:12]} does not link to {prev[:12]}")
        expected = entry_hash(entry.id, entry.title, fields)
        if _field(entry, "hash") != expected:
            errors.append(f"{entry.id}: hash mismatch (entry was altered)")
        prev = _field(entry, "hash")
    return errors


def latest(memory_dir: str = MEMORY_DIR) -> Optional[Entry]:
    entries = chain(memory_dir)
    return entries[-1] if entries else None


def drift(root: str = REPO_ROOT, memory_dir: str = MEMORY_DIR) -> Optional[str]:
    """
    Compare the current tree with the latest checkpoint.

    Returns:
        None if they match, otherwise a description of the drift
    """
    last = latest(memory_dir)
    if last is None:
        return "no checkpoint recorded"
    current = tree_hash(root)
    if _field(last, "tree") != current:
        return f"tree changed since {last.id} ({_field(last, 'tree')[:12]} -> {current[:12]})"
    return None


def create(title: str, gates: str, agent: str, root: str = REPO_ROOT,
           memory_dir: str = MEMORY_DIR) -> str:
    """
    Append a new checkpoint to CHECKPOINT.md.

    Args:
        title: One-line description of the verified state
        gates: Evidence that the state is good (tests, lint, checks)
        agent: Who verified it (human or AI identifier)

    Returns:
        The new checkpoint ID
    """
    entries = chain(memory_dir)
    errors = verify_chain(memory_dir)
    if errors:
        raise RuntimeError("Refusing to extend a broken chain: " + "; ".join(errors))

    number = len(entries) + 1
    entry_id = f"CHK-{number:03d}"
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                                text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "unknown"
    fields = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "agent": agent,
        "commit": commit,
        "tree": tree_hash(root),
        "prev": _field(entries[-1], "hash") if entries else GENESIS,
        "gates": gates,
    }
    digest = entry_hash(entry_id, title, fields)
    block = [f"\n### {entry_id} · {title}", "- **status:** verified"]
    block += [f"- **{k}:** {fields[k]}" for k in HASH_FIELDS]
    block.append(f"- **hash:** {digest}")
    path = os.path.join(memory_dir, "CHECKPOINT.md")
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n".join(block) + "\n")
    return entry_id
