"""
Tests for Mnemosyne, the project memory graph (.memory/).

The repository's own memory must validate with zero errors (LAW-003, LAW-012),
and every validator rule is exercised on small synthetic memories.
"""

import os
import shutil
import subprocess
import sys

import pytest

from mnemosyne import checkpoint as chk
from mnemosyne.graph import MEMORY_FILES, load_graph
from mnemosyne.recall import boot_pack, query
from mnemosyne.validate import validate

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MEMORY_DIR = os.path.join(REPO_ROOT, '.memory')


# ---------------------------------------------------------------- repository

def test_repository_memory_is_valid():
    """The real .memory/ has no errors: references, enforcers, ATLAS, measures, chain."""
    report = validate(MEMORY_DIR, REPO_ROOT)
    assert report.errors == []


def test_repository_memory_has_every_file_kind():
    graph = load_graph(MEMORY_DIR)
    assert graph.missing_files == []
    kinds = {e.kind for e in graph.entries.values()}
    for _, kind in MEMORY_FILES.values():
        if kind != "checkpoint":
            assert kind in kinds, kind


def test_every_law_names_an_existing_enforcer():
    graph = load_graph(MEMORY_DIR)
    laws = graph.by_kind("law")
    assert len(laws) >= 10
    assert all(law.get("enforced_by") for law in laws)


def test_boot_pack_contains_the_essentials():
    pack = boot_pack(MEMORY_DIR)
    assert "INT-001" in pack
    assert "LAW-001" in pack
    assert "Last checkpoint" in pack


def test_query_recalls_the_relevant_decision():
    hits = query("why do we not use external embedding models", top_k=5, memory_dir=MEMORY_DIR)
    ids = [h["id"] for h in hits]
    assert {"DEC-012", "LAW-006", "INT-004"} & set(ids)
    assert all(isinstance(h["neighbors"], list) for h in hits)


# Memory recall benchmark: question -> acceptable entries (any in top 3 counts)
RECALL_SET = {
    "what happens if the CPU spikes once": {"DEC-009", "LAW-011"},
    "why do we not use external embedding models": {"LAW-006", "DEC-012", "INT-004"},
    "how do I start a session": {"PRO-001"},
    "where is the vault key stored": {"DEC-008", "MAP-006", "EXT-004"},
    "who decides breaking changes": {"LAW-005", "PRO-005", "ONT-017"},
    "what are the fake placeholder concepts": {"DEC-013", "ONT-010", "EXT-028"},
    "how is the repository state verified at the end of work": {"PRO-003"},
    "which components are still simulated": {"STATE-007"},
    "how do we retrain the model": {"PRO-006", "DEC-017"},
    "why are settings ignored": {"DEC-007", "EXT-007"},
}


def test_recall_benchmark():
    """Hybrid recall finds the right entry in the top 3 for most questions."""
    hits = 0
    for question, acceptable in RECALL_SET.items():
        ids = [h["id"] for h in query(question, top_k=3, memory_dir=MEMORY_DIR)]
        hits += bool(acceptable & set(ids))
    # Measured at introduction: 8/10 with alpha 0.5 (pure latent: 7/10)
    assert hits >= 7, hits


def test_cli_check_succeeds():
    result = subprocess.run([sys.executable, "-m", "mnemosyne", "check"], cwd=REPO_ROOT,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK:" in result.stdout


# ------------------------------------------------------------ synthetic memory

def _write_memory(base, **files):
    """Create a minimal valid memory; keyword arguments override file contents."""
    mem = base / ".memory"
    mem.mkdir()
    defaults = {name: f"# {name}\n" for name in MEMORY_FILES}
    defaults["INTENTION.md"] = "### INT-001 · Purpose\n- **status:** active\n\nWhy.\n"
    defaults["ATLAS.md"] = ("### MAP-001 · Everything\n- **status:** active\n- **cites:** INT-001\n"
                            "- **files:** *\n")
    defaults.update(files)
    for name, text in defaults.items():
        (mem / name).write_text(text, encoding="utf-8")
    return str(mem)


def _codes(report):
    return {line.split()[0] for line in report.errors}


def test_minimal_memory_is_valid(tmp_path):
    report = validate(_write_memory(tmp_path), str(tmp_path), check_measures=False)
    assert report.errors == []
    assert any(w.startswith("W01") for w in report.warnings)  # no checkpoint yet


def test_dangling_reference_is_detected(tmp_path):
    mem = _write_memory(tmp_path, **{"LAWS.md": "### LAW-001 · L\n- **cites:** INT-404\n"
                                                "- **enforced_by:** .memory/LAWS.md\n"})
    assert "M04" in _codes(validate(mem, str(tmp_path), check_measures=False))


def test_body_mentions_are_edges(tmp_path):
    mem = _write_memory(tmp_path, **{"IDENTITY.md": "### IDN-001 · I\n- **cites:** INT-001\n\nSee DEC-999.\n"})
    assert "M04" in _codes(validate(mem, str(tmp_path), check_measures=False))


def test_law_without_enforcer_and_missing_enforcer(tmp_path):
    mem = _write_memory(tmp_path, **{"LAWS.md": (
        "### LAW-001 · No enforcer\n- **cites:** INT-001\n\n"
        "### LAW-002 · Ghost enforcer\n- **cites:** INT-001\n- **enforced_by:** tests/nope.py::test_x\n")})
    codes = _codes(validate(mem, str(tmp_path), check_measures=False))
    assert {"M06", "M07"} <= codes


def test_enforcer_symbol_must_exist(tmp_path):
    (tmp_path / "t.py").write_text("def test_real():\n    pass\n")
    ok = _write_memory(tmp_path, **{"LAWS.md": "### LAW-001 · L\n- **cites:** INT-001\n"
                                               "- **enforced_by:** t.py::test_real\n"})
    assert validate(ok, str(tmp_path), check_measures=False).errors == []
    shutil.rmtree(ok)
    bad = _write_memory(tmp_path, **{"LAWS.md": "### LAW-001 · L\n- **cites:** INT-001\n"
                                                "- **enforced_by:** t.py::test_missing\n"})
    assert "M06" in _codes(validate(bad, str(tmp_path), check_measures=False))


def test_unmapped_file_is_detected(tmp_path):
    (tmp_path / "orphan.py").write_text("x = 1\n")
    mem = _write_memory(tmp_path, **{"ATLAS.md": ("### MAP-001 · Memory only\n- **cites:** INT-001\n"
                                                  "- **files:** .memory/*\n")})
    errors = validate(mem, str(tmp_path), check_measures=False).errors
    assert any(e.startswith("M08") and "orphan.py" in e for e in errors)


def test_disconnected_entry_is_detected(tmp_path):
    mem = _write_memory(tmp_path, **{"ONTOLOGY.md": "### ONT-001 · Island\n- **status:** active\n"})
    assert "M13" in _codes(validate(mem, str(tmp_path), check_measures=False))


def test_wrong_file_and_duplicates_and_status(tmp_path):
    mem = _write_memory(tmp_path, **{
        "IDENTITY.md": "### LAW-001 · Misplaced\n- **cites:** INT-001\n- **enforced_by:** .memory/LAWS.md\n",
        "LAWS.md": ("### LAW-001 · Twin\n- **cites:** INT-001\n- **enforced_by:** .memory/LAWS.md\n\n"
                    "### LAW-002 · Odd status\n- **status:** maybe\n- **cites:** INT-001\n"
                    "- **enforced_by:** .memory/LAWS.md\n"),
    })
    codes = _codes(validate(mem, str(tmp_path), check_measures=False))
    assert {"M02", "M11"} <= codes


def test_decision_and_extension_must_be_anchored(tmp_path):
    mem = _write_memory(tmp_path, **{
        "DECISIONS.md": "### DEC-001 · Floating\n- **cites:** MAP-001\n",
        "EXTENSIONS.md": "### EXT-001 · Adrift\n- **depends_on:** DEC-001\n",
    })
    codes = _codes(validate(mem, str(tmp_path), check_measures=False))
    assert {"M07", "M12"} <= codes


def test_measure_drift_is_detected(tmp_path):
    os.makedirs(tmp_path / "tests")
    (tmp_path / "tests" / "test_a.py").write_text("def test_one():\n    pass\n")
    good = _write_memory(tmp_path, **{"CURRENT_STATE.md": ("### STATE-001 · Tests\n- **cites:** INT-001\n"
                                                           "- **measure:** tests.functions = 1\n")})
    assert validate(good, str(tmp_path)).errors == []
    shutil.rmtree(good)
    stale = _write_memory(tmp_path, **{"CURRENT_STATE.md": ("### STATE-001 · Tests\n- **cites:** INT-001\n"
                                                            "- **measure:** tests.functions = 7\n")})
    errors = validate(stale, str(tmp_path)).errors
    assert any(e.startswith("M09") and "declared 7, measured 1" in e for e in errors)


# ----------------------------------------------------------------- checkpoints

def test_checkpoint_chain_and_drift(tmp_path):
    mem = _write_memory(tmp_path)
    first = chk.create("First save", "tests green", "pytest", str(tmp_path), mem)
    second = chk.create("Second save", "tests green", "pytest", str(tmp_path), mem)
    assert (first, second) == ("CHK-001", "CHK-002")
    assert chk.verify_chain(mem) == []
    assert chk.drift(str(tmp_path), mem) is None

    (tmp_path / "new_file.txt").write_text("work after the checkpoint")
    assert "tree changed" in chk.drift(str(tmp_path), mem)
    strict = validate(mem, str(tmp_path), strict=True, check_measures=False)
    assert "W01" in _codes(strict)


def test_tampered_checkpoint_breaks_the_chain(tmp_path):
    mem = _write_memory(tmp_path)
    chk.create("Save", "green", "pytest", str(tmp_path), mem)
    chk.create("Save again", "green", "pytest", str(tmp_path), mem)
    path = os.path.join(mem, "CHECKPOINT.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace("- **gates:** green", "- **gates:** forged", 1))
    errors = chk.verify_chain(mem)
    assert any("hash mismatch" in e for e in errors)
    assert "M10" in _codes(validate(mem, str(tmp_path), check_measures=False))
    with pytest.raises(RuntimeError):
        chk.create("On a broken chain", "green", "pytest", str(tmp_path), mem)


def test_checkpoint_refuses_invalid_memory(tmp_path, monkeypatch):
    """The CLI will not create a save point while the memory has errors."""
    mem = _write_memory(tmp_path, **{"LAWS.md": "### LAW-001 · L\n- **cites:** INT-404\n"
                                                "- **enforced_by:** .memory/LAWS.md\n"})
    from mnemosyne import __main__ as cli
    monkeypatch.setattr(cli, "validate",
                        lambda **kwargs: validate(mem, str(tmp_path), check_measures=False))
    assert cli.main(["checkpoint", "x", "--gates", "g", "--agent", "a"]) == 1
    assert chk.chain(mem) == []


def test_cli_boot_stats_graph_query(capsys):
    from mnemosyne.__main__ import main
    assert main(["boot"]) == 0
    assert "Boot Pack" in capsys.readouterr().out
    assert main(["stats"]) == 0
    assert "entries by kind" in capsys.readouterr().out
    assert main(["graph"]) == 0
    assert "INT-001" in capsys.readouterr().out
    assert main(["graph", "--format", "mermaid"]) == 0
    assert capsys.readouterr().out.startswith("graph TD")
    assert main(["query", "who decides breaking changes", "-k", "2"]) == 0
    assert "LAW-005" in capsys.readouterr().out


def test_cli_checkpoint_creates_entry(tmp_path, monkeypatch, capsys):
    mem = _write_memory(tmp_path)
    from mnemosyne import __main__ as cli
    monkeypatch.setattr(cli, "validate", lambda **kwargs: validate(mem, str(tmp_path), check_measures=False))
    original_create = chk.create
    monkeypatch.setattr(cli.chk, "create",
                        lambda title, gates, agent: original_create(title, gates, agent, str(tmp_path), mem))
    assert cli.main(["checkpoint", "Green", "--gates", "all green", "--agent", "pytest"]) == 0
    assert "Created CHK-001" in capsys.readouterr().out
