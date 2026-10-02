"""
Mnemosyne Validator - the laws of the memory graph, executed.

Errors (the memory is not trustworthy until fixed):
  M01 missing memory file            M08 repository file not mapped in ATLAS
  M02 duplicate entry ID             M09 measured fact differs from reality
  M03 ID prefix in wrong file        M10 checkpoint chain broken
  M04 reference to unknown entry     M11 invalid status value
  M05 evidence path does not exist   M12 extension not anchored (no cites)
  M06 enforcer missing (file/test)   M13 entry not connected to INTENTION
  M07 law without enforcer / decision without cited intention or law

Warnings:
  W01 repository drifted since the latest checkpoint (error with --strict)
"""

import fnmatch
import os
import re
from dataclasses import dataclass, field
from typing import List

from mnemosyne import checkpoint as chk
from mnemosyne.graph import (ID_FIELDS, MEMORY_DIR, MEMORY_FILES, REPO_ROOT, STATUSES,
                             MemoryGraph, load_graph)
from mnemosyne.measures import MEASURES, measure, tracked_files


@dataclass
class Report:
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def error(self, code: str, message: str):
        self.errors.append(f"{code} {message}")

    def warn(self, code: str, message: str):
        self.warnings.append(f"{code} {message}")


def _path_target_exists(target: str, root: str, files: tuple) -> str:
    """Return '' if a path/enforcer target exists, else the reason it does not."""
    path, _, symbol = target.partition("::")
    if any(ch in path for ch in "*?["):
        return "" if any(fnmatch.fnmatchcase(f, path) for f in files) else "glob matches nothing"
    full = os.path.join(root, path)
    if not os.path.exists(full):
        return "path does not exist"
    if symbol:
        with open(full, encoding="utf-8") as f:
            if not re.search(rf"^\s*(?:async\s+)?(?:def|class)\s+{re.escape(symbol)}\b", f.read(), re.M):
                return f"'{symbol}' not defined in {path}"
    return ""


def validate(memory_dir: str = MEMORY_DIR, root: str = REPO_ROOT, strict: bool = False,
             check_measures: bool = True) -> Report:
    """
    Validate the memory graph against itself and against the repository.

    Args:
        memory_dir: .memory directory
        root: Repository root
        strict: Treat checkpoint drift as an error
        check_measures: Recompute measured facts (M09)

    Returns:
        Report with errors and warnings
    """
    report = Report()
    graph: MemoryGraph = load_graph(memory_dir)
    tracked_files.cache_clear()  # always validate the current tree
    files = tracked_files(root)

    for name in graph.missing_files:
        report.error("M01", f"missing {name}")
    for entry_id, first, second in graph.duplicates:
        report.error("M02", f"{entry_id} defined in {first} and {second}")

    for entry in graph.entries.values():
        expected_file = next(n for n, (p, _) in MEMORY_FILES.items() if entry.id.startswith(p + "-"))
        if entry.file != expected_file:
            report.error("M03", f"{entry.id} belongs in {expected_file}, found in {entry.file}")
        if entry.status is not None and entry.status not in STATUSES:
            report.error("M11", f"{entry.id} has unknown status '{entry.status}'")

    for edge in graph.edges:
        if edge.kind in ID_FIELDS or edge.kind == "mentions":
            if edge.target not in graph.entries:
                report.error("M04", f"{edge.source} -> {edge.kind} -> {edge.target} (unknown entry)")
        elif edge.kind in ("evidence", "files"):
            reason = _path_target_exists(edge.target, root, files)
            if reason:
                report.error("M05", f"{edge.source} {edge.kind} {edge.target}: {reason}")
        elif edge.kind == "enforced_by":
            reason = _path_target_exists(edge.target, root, files)
            if reason:
                report.error("M06", f"{edge.source} enforced_by {edge.target}: {reason}")

    for entry in graph.by_kind("law"):
        if not entry.get("enforced_by"):
            report.error("M07", f"{entry.id} declares no enforcer")
    for entry in graph.by_kind("decision"):
        if not any(t.startswith(("INT-", "LAW-")) for t in entry.get("cites")):
            report.error("M07", f"{entry.id} cites no intention or law")
    for entry in graph.by_kind("extension"):
        if not entry.get("cites"):
            report.error("M12", f"{entry.id} is not anchored (no cites)")

    patterns = [p for e in graph.by_kind("component") for p in e.get("files")]
    for rel in files:
        if not any(fnmatch.fnmatchcase(rel, p) for p in patterns):
            report.error("M08", f"{rel} is not mapped by any ATLAS entry")

    if check_measures:
        for entry in graph.by_kind("state"):
            for declaration in entry.get("measure"):
                name, _, declared = (part.strip() for part in declaration.partition("="))
                if name not in MEASURES:
                    report.error("M09", f"{entry.id} unknown measure '{name}'")
                    continue
                actual = measure(name, root)
                if actual != declared:
                    report.error("M09", f"{entry.id} {name}: declared {declared}, measured {actual}")

    for message in chk.verify_chain(memory_dir):
        report.error("M10", message)

    # M13: every entry must connect (through entry-to-entry edges) to an intention
    adjacency = {eid: set() for eid in graph.entries}
    for edge in graph.edges:
        if edge.source in adjacency and edge.target in adjacency:
            adjacency[edge.source].add(edge.target)
            adjacency[edge.target].add(edge.source)
    seen = set()
    frontier = [e.id for e in graph.by_kind("intention")]
    while frontier:
        node = frontier.pop()
        if node not in seen:
            seen.add(node)
            frontier.extend(adjacency[node] - seen)
    for entry_id in sorted(set(graph.entries) - seen):
        if not entry_id.startswith("CHK-"):  # checkpoints are anchored by the hash chain
            report.error("M13", f"{entry_id} has no path to INTENTION")

    drift_message = chk.drift(root, memory_dir)
    if drift_message:
        (report.error if strict else report.warn)("W01", drift_message)

    return report
