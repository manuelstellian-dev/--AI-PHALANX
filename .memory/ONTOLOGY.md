# ONTOLOGY — shared vocabulary and the schema of this memory

> Defines the terms used everywhere else, so humans and agents mean the same thing by the same word.
> The last entries define the memory graph itself (node kinds, edge kinds, entry syntax).

## Domain terms

### ONT-001 · Λ-Core
- **status:** active
- **cites:** INT-001
- **evidence:** core/leonidasbrain.py, core/commandprocessor.py

The decision nucleus. `LeondasBrain` runs the homeostasis loop and the FFP. `CommandProcessor`
(the "Λ-Möbius Engine" router) interprets the Commander's commands and routes them to modules.

### ONT-002 · Phalanx
- **status:** active
- **cites:** INT-003
- **evidence:** phalanx/helot.py, phalanx/agoge.py, phalanx/krypteia.py, phalanx/thermopylae.py

The internal-control modules:
- **Helot:** resources, the P factor (ONT-005), survival probability (ONT-007).
- **Agoge:** adaptation factor.
- **Krypteia:** silent threat watch.
- **Thermopylae:** controlled self-destruction.

### ONT-003 · Hoplites
- **status:** active
- **cites:** INT-001
- **evidence:** hoplites/spartanguard.py, hoplites/shieldbearer.py

The action modules:
- **Spartan Guard:** AES-256-GCM.
- **Shield Bearer:** air-gap and firewall.
- **Battle Oracle:** risk analysis.
- **Weapon Master:** controlled external access.
- **Messenger:** encrypted messages.

### ONT-004 · Λ-TAS (Autonomous Spartan Time)
- **status:** active
- **cites:** INT-003, DEC-011
- **evidence:** core/leonidasbrain.py

`Λ-TAS = T₁·ln(U+1) / (1 − 1/(k·P))` in seconds, with T₁ = 1 s and k = 100, clamped to [0.1, 10].
It is the period of the homeostasis loop. The fallback when k·P ≤ 1 is P/(1+U).

### ONT-005 · P — Parallelism Factor
- **status:** active
- **cites:** ONT-004

`P = 1 + cores·(1 − CPU%/100) + 5·GPU load`, measured by Helot (`last_resources`). GPU load is
simulated for now (EXT-018).

### ONT-006 · U — Universe Expansion Factor
- **status:** active
- **cites:** ONT-004

`U = (1 + active tasks + ln(max(1, vault MB))) · Agoge adaptation`, computed by the CommandProcessor.

### ONT-007 · Survival probability
- **status:** active
- **cites:** INT-003

Helot computes it as 1.0 minus penalties for critical CPU (0.10), memory (0.15) and disk (0.10).
Below the Thermopylae threshold (0.95) it counts as a breach (LAW-011).

### ONT-008 · SPARTA
- **status:** active
- **cites:** INT-002
- **evidence:** sparta/semantic_foundation.py, sparta/reflexive_generator.py, sparta/foundation_bridge.py, sparta/runtime.py

*Semantic Phalanx Architecture for Reasoning with Truth and Accountability.* Its layers are the
Foundation (verified concepts), the Bridge (validation) and the Reflexive Generator (logical
answers that carry sources). It is served at `/api/v1/sparta/*` and through the `sparta_query`
command.

### ONT-009 · Concept (16-field schema)
- **status:** active
- **cites:** ONT-008
- **evidence:** sparta/semantic_memory.jsonl

The 16 fields are:
- id, domain, subdomain, topic
- definition, formal_statement
- relations, prerequisites
- confidence, source, reflex_tag
- examples, counterexamples, applications
- verification, uncertainty

One JSON object per line.

### ONT-010 · Placeholder and quarantine
- **status:** active
- **cites:** LAW-007, DEC-013

A **placeholder** is a concept in a family of numbered IDs (`epistemic_01` … `epistemic_40`)
whose definitions are identical once digits are normalized. **Quarantine** moves placeholders out
of the active Foundation when it loads. They stay in the file and in `foundation.quarantined`,
but are never used to answer queries.

### ONT-011 · Λ-Möbius states
- **status:** active
- **cites:** DEC-002
- **evidence:** control/lambda_mobius.py

The engine computes T_Wrap, T_Mult, T_Hybrid = (a·b)/(a+b) (half the harmonic mean, DEC-015),
T_Balance (geometric mean) and T_Supreme. The arbiter chooses WRAP (+1), STEADY (0) or UNWRAP (−1).

### ONT-012 · Kronos-Arbiter
- **status:** active
- **cites:** DEC-002
- **evidence:** control/kronos_arbiter.py

`T_parallel = T_sequential / (N·Θ·Λ·η)`, bounded by Amdahl's law when `amdahl_fraction < 1`.

### ONT-013 · FFP (Fractal Flux Pipeline)
- **status:** active
- **cites:** INT-003
- **evidence:** control/fractal_pipeline.py

The self-repair cycle Scan → Detect → Quarantine → Heal → Improve → Reinvest, paced by T_Supreme.
HEAL and REINVEST currently only log (EXT-015).

### ONT-014 · Λ-Logos
- **status:** active
- **cites:** INT-004, DEC-012
- **evidence:** logos/model.py, logos/tokenizer.py

The project's own embedding model. The pipeline is: signed feature hashing over normalized words,
bigrams and character n-grams → TF-IDF → randomized SVD (latent semantic axes) → 384-dimensional
unit vectors. It is trained on the project corpus (SPARTA, `.memory/`, docs).

### ONT-015 · Model ID and fingerprint
- **status:** active
- **cites:** LAW-014
- **evidence:** logos/model.py

The model ID has the form `logos-v1:<first 12 hex of SHA-256(parameters + corpus)>`. Every vector
store records the ID of the model that produced its vectors.

### ONT-016 · Vault redaction
- **status:** active
- **cites:** DEC-008
- **evidence:** vault/spartan_vault.py

For encrypted entries, the semantic index stores only `[ENCRYPTED]`. The plaintext lives only in
the Fernet ciphertext and is returned only with `decrypt=true`.

### ONT-017 · Commander
- **status:** active
- **cites:** INT-001, IDN-004

The project owner: the final authority on intention, laws and breaking changes (LAW-005).

### ONT-018 · Spartanization
- **status:** active
- **cites:** DEC-002, IDN-001

Concepts adopted from elsewhere are extracted, understood and renamed into the Spartan
vocabulary. They are never combined wholesale with another system.

### ONT-019 · Λ-Modules
- **status:** active
- **cites:** INT-006
- **evidence:** docs/sparta/SPARTA_LAMBDA_MODULES.md

These are the seven specified extensions of SPARTA:
- Identity
- Pattern
- Meta
- Guide
- Affect
- Reflect
- Zero (logic/creativity balance; critical)

They are not implemented yet (EXT-011).

## Memory schema

### ONT-020 · Node kinds
- **status:** active
- **cites:** DEC-014
- **evidence:** mnemosyne/graph.py

| Prefix | File | Kind |
|---|---|---|
| INT | INTENTION.md | intention |
| IDN | IDENTITY.md | identity |
| LAW | LAWS.md | law |
| ONT | ONTOLOGY.md | term |
| DEC | DECISIONS.md | decision |
| MAP | ATLAS.md | component |
| STATE | CURRENT_STATE.md | state |
| CHK | CHECKPOINT.md | checkpoint |
| EVT | JOURNAL.md | event |
| EXT | EXTENSIONS.md | extension |
| PRO | PROTOCOL.md | procedure |

Repository paths named in entries are file nodes.

### ONT-021 · Edge kinds and entry syntax
- **status:** active
- **cites:** DEC-014, ONT-020

Edge kinds:
- **ID edges:** `cites`, `supersedes`, `implements`, `depends_on`, `refines`
- **path edges:** `evidence`, `enforced_by` (`path::symbol` allowed), `files` (glob patterns, ATLAS only)
- **implicit:** `mentions`, from any entry ID written in a body

Entry syntax: `### PREFIX-NNN · Title`, then `- **field:** value` lines, then the Markdown body.
Statuses: active, superseded, planned, in_progress, done, blocked, open, accepted, verified, rejected.
