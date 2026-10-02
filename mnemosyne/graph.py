"""
Mnemosyne Graph - parse .memory/ into a typed knowledge graph.

Entry syntax (human-readable Markdown, machine-parseable):

    ### LAW-003 · No capability is ever deleted
    - **status:** active
    - **cites:** INT-001, IDN-002
    - **enforced_by:** tests/test_system_integrity.py
    Free Markdown body. Mentions of other IDs (DEC-012) become edges too.

Nodes: every entry (by ID) and every repository path an entry points at.
Edges: typed by the field that declares them, plus `mentions` from the body.
"""

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MEMORY_DIR = os.path.join(REPO_ROOT, '.memory')

# File → (ID prefix, node kind). Order = boot sequence (read top to bottom).
MEMORY_FILES: Dict[str, Tuple[str, str]] = {
    "INTENTION.md": ("INT", "intention"),
    "IDENTITY.md": ("IDN", "identity"),
    "LAWS.md": ("LAW", "law"),
    "ONTOLOGY.md": ("ONT", "term"),
    "DECISIONS.md": ("DEC", "decision"),
    "ATLAS.md": ("MAP", "component"),
    "CURRENT_STATE.md": ("STATE", "state"),
    "CHECKPOINT.md": ("CHK", "checkpoint"),
    "JOURNAL.md": ("EVT", "event"),
    "EXTENSIONS.md": ("EXT", "extension"),
    "PROTOCOL.md": ("PRO", "procedure"),
}
PREFIX_TO_FILE = {prefix: name for name, (prefix, _) in MEMORY_FILES.items()}

ID_PATTERN = r"(?:INT|IDN|LAW|ONT|DEC|MAP|STATE|CHK|EVT|EXT|PRO)-\d{3}"
ID_RE = re.compile(rf"\b({ID_PATTERN})\b")
HEADING_RE = re.compile(rf"^###\s+({ID_PATTERN})\s+·\s+(.+?)\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"^-\s+\*\*([a-z_]+):\*\*\s*(.*?)\s*$")

# Fields whose values are entry IDs
ID_FIELDS = ("cites", "supersedes", "implements", "depends_on", "refines")
# Fields whose values are repository paths (path or path::test_name; globs in `files`)
PATH_FIELDS = ("evidence", "enforced_by", "files")
# Comma-separated list fields. Other fields (e.g. `measure`) accumulate one value per line.
LIST_FIELDS = ID_FIELDS + PATH_FIELDS

STATUSES = {"active", "superseded", "planned", "in_progress", "done", "blocked",
            "open", "accepted", "verified", "rejected"}


@dataclass
class Entry:
    """One addressable node of the memory graph."""
    id: str
    title: str
    file: str
    kind: str
    line: int
    fields: Dict[str, List[str]] = field(default_factory=dict)
    body: str = ""

    def get(self, name: str) -> List[str]:
        return self.fields.get(name, [])

    @property
    def status(self) -> Optional[str]:
        values = self.get("status")
        return values[0] if values else None

    @property
    def text(self) -> str:
        """Title + body: the text used for semantic retrieval."""
        return f"{self.title}\n{self.body}"


@dataclass
class Edge:
    source: str
    target: str
    kind: str


@dataclass
class MemoryGraph:
    """Parsed .memory/ directory."""
    root: str
    entries: Dict[str, Entry] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)
    duplicates: List[Tuple[str, str, str]] = field(default_factory=list)
    missing_files: List[str] = field(default_factory=list)

    def neighbors(self, entry_id: str) -> List[Edge]:
        """Edges touching an entry (both directions)."""
        return [e for e in self.edges if e.source == entry_id or e.target == entry_id]

    def by_kind(self, kind: str) -> List[Entry]:
        return [e for e in self.entries.values() if e.kind == kind]


def _split_values(raw: str) -> List[str]:
    return [v.strip().strip("`") for v in raw.split(",") if v.strip()]


def parse_file(path: str, prefix: str, kind: str) -> List[Entry]:
    """
    Parse one memory file into entries.

    Args:
        path: Markdown file
        prefix: Expected ID prefix
        kind: Node kind for its entries

    Returns:
        Entries in file order
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()
    name = os.path.basename(path)
    headings = list(HEADING_RE.finditer(text))
    entries = []
    for i, match in enumerate(headings):
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        # A level-2 heading ends the entry (section boundary)
        section_break = re.search(r"^##\s", text[match.end():end], re.MULTILINE)
        if section_break:
            end = match.end() + section_break.start()
        block = text[match.end():end].strip("\n")
        fields: Dict[str, List[str]] = {}
        body_lines = []
        in_fields = True
        for line in block.splitlines():
            m = FIELD_RE.match(line) if in_fields else None
            if m:
                key, value = m.group(1), m.group(2)
                fields.setdefault(key, []).extend(
                    _split_values(value) if key in LIST_FIELDS else [value])
                continue
            if line.strip():
                in_fields = False
            body_lines.append(line)
        entries.append(Entry(
            id=match.group(1), title=match.group(2), file=name, kind=kind,
            line=text[:match.start()].count("\n") + 1,
            fields=fields, body="\n".join(body_lines).strip(),
        ))
    return entries


def load_graph(memory_dir: str = MEMORY_DIR) -> MemoryGraph:
    """
    Load every memory file and build typed edges.

    Args:
        memory_dir: Path of the .memory directory

    Returns:
        MemoryGraph
    """
    graph = MemoryGraph(root=memory_dir)
    for name, (prefix, kind) in MEMORY_FILES.items():
        path = os.path.join(memory_dir, name)
        if not os.path.exists(path):
            graph.missing_files.append(name)
            continue
        for entry in parse_file(path, prefix, kind):
            if entry.id in graph.entries:
                graph.duplicates.append((entry.id, graph.entries[entry.id].file, entry.file))
                continue
            graph.entries[entry.id] = entry

    for entry in graph.entries.values():
        for kind in ID_FIELDS:
            for target in entry.get(kind):
                graph.edges.append(Edge(entry.id, target, kind))
        for kind in PATH_FIELDS:
            for target in entry.get(kind):
                graph.edges.append(Edge(entry.id, target, kind))
        declared = {t for k in ID_FIELDS for t in entry.get(k)}
        for target in sorted(set(ID_RE.findall(entry.body)) - declared - {entry.id}):
            graph.edges.append(Edge(entry.id, target, "mentions"))
    return graph
