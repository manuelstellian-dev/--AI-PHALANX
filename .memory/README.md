# `.memory/` — the persistent memory of ΛΕΩΝΙΔΑΣ-AI PHALANX

> **Start here, every session.** `python -m mnemosyne boot` prints the essentials;
> `python -m mnemosyne check` proves they are still true.

This directory is the project's **canonical, executable memory**. It is a knowledge graph:
- every entry has a stable ID (`LAW-006`, `DEC-012`, …);
- fields declare typed edges to other entries and to repository files;
- **Mnemosyne** (`mnemosyne/`) parses, validates, checkpoints and searches it with **Λ-Logos**,
  the project's own model.

It exists so that no session, human or AI, starts by asking *"what is this?"*. Every session
starts from *"how do we advance from here, within what we know and what we have decided?"*

## The graph — read in this order

| # | File | Prefix | Role in the graph |
|---|------|--------|-------------------|
| 1 | INTENTION.md | INT | **Root node.** What is built, and why. Every entry must trace back here |
| 2 | IDENTITY.md | IDN | **Self-model.** Ethos, character, human–AI relationship, conventions |
| 3 | LAWS.md | LAW | **Constraint layer.** Inviolable rules, each with an executable enforcer |
| 4 | ONTOLOGY.md | ONT | **Vocabulary and schema.** Domain terms; node and edge kinds of this graph |
| 5 | DECISIONS.md | DEC | **Causal edges.** Why each path was chosen (context → decision → alternatives → consequences) |
| 6 | ATLAS.md | MAP | **Territory.** Every repository file mapped to a component, compressed |
| 7 | CURRENT_STATE.md | STATE | **Present reality.** Facts are *measures*, recomputed from the code |
| 8 | CHECKPOINT.md | CHK | **Temporal anchors.** A hash chain of verified repository states |
| 9 | JOURNAL.md | EVT | **History.** Append-only events, what happened and when |
| 10 | EXTENSIONS.md | EXT | **Forward edges.** The road to the end-state (mirrors BACKLOG.md) |
| 11 | PROTOCOL.md | PRO | **Procedures.** Boot, work and close microsteps |

## What makes it more than documentation

- **Typed edges.**
  - ID edges: `cites`, `supersedes`, `implements`, `depends_on`, `refines`.
  - Path edges: `evidence`, `enforced_by`, `files`.
  - Body mentions of IDs are `mentions` edges.
- **Executable laws.** Every law names its enforcer (a test, a CI gate or a tool), and the
  validator checks that the enforcer exists.
- **Measured state.** `- **measure:** sparta.concepts_active = 420` is recomputed on every check,
  and drift is an error.
- **Verifiable checkpoints.** Each checkpoint hashes the whole repository tree and the previous
  checkpoint. Tampering or unrecorded work is detected.
- **Total coverage.** ATLAS must map every file in the repository, so nothing exists outside the
  memory.
- **Lineage.** Every entry must connect to INTENTION; orphans are errors.
- **Recall.** `python -m mnemosyne query "..."` ranks entries with Λ-Logos and returns each hit
  with its graph neighbourhood, so the answer comes with its reasons.

## Commands

```bash
python -m mnemosyne boot                         # session context pack
python -m mnemosyne check [--strict]             # validate (strict: no drift since checkpoint)
python -m mnemosyne query "why no external models?"
python -m mnemosyne checkpoint "title" --gates "evidence" --agent "who"
python -m mnemosyne graph --format mermaid       # visualize entry-to-entry edges
python -m mnemosyne stats
```

## Entry syntax

```markdown
### LAW-006 · No external models and no external APIs at runtime
- **status:** active
- **cites:** INT-004
- **enforced_by:** tests/test_logos.py::test_no_external_ml_runtime_is_imported

Free Markdown body. Mentioning DEC-012 here creates a `mentions` edge.
```

Validator rules: M01–M13 and W01 (see `mnemosyne/validate.py`). The full schema is ONT-020 and
ONT-021.
