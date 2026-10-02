# PROTOCOL — how every session boots, works and closes

> The operational form of LAW-004 ("never skip a microstep"). Each procedure is a numbered
> checklist. Agents (human or AI) follow it literally. Commands assume the repository root.

### PRO-001 · Boot sequence (start of every session)
- **status:** active
- **cites:** LAW-004, INT-005

1. `python -m mnemosyne boot`: read the intention, laws, state, last checkpoint and next steps.
2. `python -m mnemosyne check`: the memory must be valid. A W01 drift warning means work happened
   after the last checkpoint. Read JOURNAL to learn what.
3. `git log --oneline -10` and `git status`: confirm the working tree matches CURRENT_STATE.
4. For the task at hand, run `python -m mnemosyne query "<topic>"` and read the cited LAW, DEC and
   MAP entries before touching code.
5. If the task conflicts with a law or an accepted decision, stop and raise it with the Commander
   (PRO-005).

### PRO-002 · Work loop (every change)
- **status:** active
- **cites:** LAW-002, LAW-001, LAW-013

1. Locate the component in ATLAS. Read its files, tests and evidence.
2. Change behaviour without deleting capability. Keep the old path as an explicit option
   (LAW-001).
3. Add or adjust tests. Never skip or weaken a test to obtain green (LAW-013).
4. Run `ruff check .`, `python -m pytest -W error` and `shellcheck scripts/*.sh` if scripts changed.
5. Update the documents the change touches, together with the memory entries that describe them
   (LAW-003).

### PRO-003 · Close sequence (end of every session)
- **status:** active
- **cites:** LAW-004, LAW-003, LAW-012

1. All gates in LAW-002 are green.
2. Update CURRENT_STATE. Every changed fact must be a measure, or be anchored to the new checkpoint.
3. Record new decisions in DECISIONS (PRO-004), and new or changed files in ATLAS (PRO-007).
4. Append the session to JOURNAL: what was done, the commits and open questions.
5. `python -m mnemosyne check` reports zero errors.
6. Commit everything except the checkpoint.
7. `python -m mnemosyne checkpoint "<title>" --gates "<evidence>" --agent "<who>"`.
8. `python -m mnemosyne check --strict` reports zero errors. Commit the checkpoint and push.

### PRO-004 · Recording a decision
- **status:** active
- **cites:** LAW-005, DEC-014

1. Take the next free `DEC-NNN`. Record status (`accepted`, or `open` if the Commander must rule),
   date, `cites` (at least one INT or LAW) and evidence.
2. Write the body as context → decision → alternatives → consequences.
3. A decision that replaces an earlier one sets `supersedes`. The old entry is marked
   `superseded` and is never deleted.

### PRO-005 · Changing intention or laws, and breaking changes
- **status:** active
- **cites:** LAW-005, ONT-017

1. The agent writes the proposal as an `open` decision with its consequences.
2. Only the Commander approves. The approval is recorded in the decision, with date and words.
3. The change is then applied, and the decision status becomes `accepted`.

### PRO-006 · Retraining Λ-Logos
- **status:** active
- **cites:** LAW-014, DEC-017

1. `python -m logos train --force`. A new fingerprint means a new model ID.
2. Re-run the benchmark. The new model must not be worse than the recorded MRR (STATE-004).
3. Re-index every vault: `SpartanVault.reindex()`.
4. Update STATE-004 and record the reason in DECISIONS.

### PRO-007 · Adding a file or component
- **status:** active
- **cites:** LAW-012

1. Map the file in ATLAS, either by extending an existing pattern or adding a `MAP-NNN` entry.
2. A new component cites the intention or decision that justifies it.
3. `python -m mnemosyne check` must not report M08.

### PRO-008 · When memory and code disagree
- **status:** active
- **cites:** IDN-003, LAW-003

1. The code and its measured behaviour are the evidence.
2. Correct the memory entry. If the disagreement revealed a defect, fix the code under PRO-002.
3. Record the discrepancy in JOURNAL so the drift has a history.
