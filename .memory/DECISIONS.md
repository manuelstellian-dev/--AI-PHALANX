# DECISIONS — the rationale ledger

> Why each significant path was chosen and the others rejected, so settled questions are not
> re-litigated. Format: context → decision → alternatives → consequences. Decisions are never
> deleted; a replaced decision is marked `superseded` and names its successor.
> Every decision cites at least one intention or law (validator rule M07).

## Founding decisions (November 2025)

### DEC-001 · Spartan modular architecture: Λ-Core → Phalanx → Hoplites
- **status:** accepted
- **date:** 2025-11-02
- **cites:** INT-001, IDN-001
- **evidence:** core/leonidasbrain.py, ARCHITECTURE.md

**Context.** A decision core for high-stakes use needs clear separation of command, internal
control and action.
**Decision.** Use three tiers with one military role per module, wired by the brain and the
command router.
**Alternatives.** A monolithic agent, or a generic plugin bus. Both were rejected: they blur
responsibility and make audit harder.
**Consequences.** Every file maps to a role (ATLAS), and modules are tested in isolation.

### DEC-002 · Extract and transform Omega-AIOS concepts; never combine systems
- **status:** accepted
- **date:** 2025-11-02
- **cites:** INT-001, IDN-001
- **evidence:** TEMPORAL_COMPRESSION_MASTER_PLAN.md, control/kronos_arbiter.py

**Context.** Temporal compression and parallel execution existed in another system (Omega-AIOS).
**Decision.** Understand each concept and re-implement it under Spartan names: Kronos-Arbiter,
Phalanx-Executor and Λ-Möbius (ONT-018).
**Alternatives.** Importing or merging the other system. Rejected: it would bring foreign
dependencies and dilute identity.
**Consequences.** Projected speedups (714×) are a planning model that was never measured
(EXT-017).

### DEC-003 · SPARTA reasons logically over verified concepts, not by token prediction
- **status:** accepted
- **date:** 2025-11-02
- **cites:** INT-002, LAW-007
- **evidence:** docs/sparta/SPARTA_OVERVIEW.md, sparta/reflexive_generator.py

**Context.** LLM hallucination is unacceptable in critical operations.
**Decision.** Answers are composed from Foundation concepts and carry confidence, sources and a
reasoning chain. Unknown topics produce an honest "unknown".
**Alternatives.** An LLM with retrieval augmentation. Rejected: it can still fabricate.
**Consequences.** Answer quality is bounded by the quality of the Foundation (DEC-013, EXT-002).

### DEC-004 · A 16-field concept schema with confidence and uncertainty
- **status:** accepted
- **date:** 2025-11-03
- **cites:** INT-002
- **evidence:** sparta/semantic_memory.jsonl, docs/sparta/SPARTA_FOUNDATION.md

**Decision.** Each concept carries its definition, formal statement, relations, prerequisites,
confidence, source, examples, counterexamples, applications, verification method and uncertainty
(ONT-009).
**Consequences.** Confidence is self-assigned at authoring time. It lacks calibration (EXT-003).

### DEC-005 · FastAPI on port 7300 with bearer-token authentication
- **status:** accepted
- **date:** 2025-11-02
- **cites:** INT-001, LAW-010
- **evidence:** api/server.py

**Decision.** Use a single REST surface. Health is public; everything else requires the token.
**Consequences.** Hardening (expiry, rate limits, CORS) is still open (EXT-006).

## Integrity remediation (2026-10-02)

### DEC-006 · PROJECT_STATUS.md is authoritative; superseded reports are kept as historical records
- **status:** accepted
- **date:** 2026-10-02
- **cites:** LAW-003, IDN-002
- **evidence:** PROJECT_STATUS.md, BACKLOG.md

**Context.** Twelve overlapping audit reports contradicted each other and the code. They were
produced by a heuristic that counted any file over 50 lines as done.
**Decision.** Keep one measured status document. Old reports keep their content under a
historical banner.
**Alternatives.** Deleting the old reports. Rejected under LAW-001.

### DEC-007 · Each module receives its own configuration section
- **status:** accepted
- **date:** 2026-10-02
- **cites:** LAW-003, IDN-006
- **evidence:** api/server.py, tests/test_system_integrity.py::TestConfigWiring

**Context.** Every module received the root configuration, so every per-module setting (including
`thermopylae_armed`) was silently ignored.
**Decision.** `get_section(config, ...)` resolves each module's section and falls back to the root
for flat legacy configurations (LAW-001).

### DEC-008 · Vault redaction: encrypted plaintext never enters the index or the disk
- **status:** accepted
- **date:** 2026-10-02
- **cites:** LAW-011, INT-003
- **evidence:** vault/spartan_vault.py, tests/test_vector_store.py::test_no_plaintext_written_to_disk

**Context.** Plaintext was returned and persisted regardless of `decrypt`, and the key was never
reloaded.
**Decision.**
- The index stores `[ENCRYPTED]` for encrypted entries.
- The key is resolved as `SPARTA_VAULT_KEY` → `encryption.key` → newly generated.
- `index_plaintext=True` keeps the legacy behaviour as an explicit opt-in.

**Consequences.** Re-indexing needs decryption (DEC-017).

### DEC-009 · Thermopylae requires a sustained breach
- **status:** accepted
- **date:** 2026-10-02
- **cites:** LAW-011, INT-003
- **evidence:** phalanx/thermopylae.py, tests/test_system_integrity.py::TestThermopylaeSafety

**Context.** A single CPU spike lowers survival to 0.90, below 0.95. Once armed and wired, the
protocol would destroy everything on one transient.
**Decision.** Add `consecutive_breaches_required` (3 in settings; the default of 1 preserves the
old behaviour). The protocol destroys every configured vault path and resolves paths from the
repository root.

### DEC-010 · JSON is the primary persistence format; pickle is only a fallback
- **status:** accepted
- **date:** 2026-10-02
- **cites:** LAW-010
- **evidence:** vault/vector_store.py

**Decision.** Vectors are persisted in JSON with their embeddings. A tampered pickle is never
loaded when the JSON exists.

### DEC-011 · Λ-TAS is a period in seconds, driven by measured P and U
- **status:** accepted
- **date:** 2026-10-02
- **cites:** INT-003, LAW-003
- **evidence:** core/leonidasbrain.py, ADVANCED_CAPABILITIES.md

**Context.** The specification defines T_new in seconds, but the loop slept for `1/Λ-TAS` and used
the configured core count instead of Helot's P.
**Decision.** The loop sleeps Λ-TAS seconds, takes P from Helot and U from the CommandProcessor
(ONT-004).

## Sovereignty and memory (2026-10-02)

### DEC-012 · Λ-Logos, our own embedding model, replaces the external model
- **status:** accepted
- **date:** 2026-10-02
- **cites:** INT-004, LAW-006, LAW-009
- **evidence:** logos/model.py, logos/benchmark.py, tests/test_logos.py

**Context.** The Commander ruled that the project will no longer use external models or APIs. The
vault depended on `sentence-transformers` (pretrained weights downloaded from HuggingFace, torch
runtime, 5.9 GB environment), which also contradicted the air-gap.

**Decision.** Build Λ-Logos (ONT-014): a latent semantic embedder written with NumPy and SciPy
only. It is trained on the project's own corpus and is deterministic and fingerprinted.

**Alternatives.**
1. Keep the external model. Rejected by the Commander's ruling.
2. Train a transformer from scratch. Rejected: it needs a GPU and a large corpus, and an
   opaque network is not appropriate for an auditable fortress.
3. A plain TF-IDF without training. Kept as the untrained fallback, but it measures lower.

**Measured result** (fixed benchmark, 28 paraphrase queries against 420 concepts):

| | Trained Λ-Logos | Lexical baseline |
|---|---|---|
| MRR | 0.68–0.69 | 0.53 |
| Recall@5 | 82–86% | 61% |
| Mean rank | 14–16 | 40 |

The ranges cover the first training and the retraining with `.memory/` included (STATE-004). The
installed environment is 350 MB instead of 5.9 GB.

Memory recall blends the latent and lexical channels of the model. Exact terms such as "CPU spike"
survive, while meaning still generalizes.

**Consequences.**
- Semantic quality is below large pretrained transformers; improving it is EXT-027.
- The external backend remains as a lazy, non-default opt-in (LAW-001).

### DEC-013 · Quarantine template placeholders in the SPARTA Foundation
- **status:** accepted
- **date:** 2026-10-02
- **cites:** LAW-007, INT-002, LAW-001
- **evidence:** sparta/semantic_foundation.py, tests/test_system_integrity.py::test_placeholders_never_answer_as_verified

**Context.** 80 of 500 concepts (`epistemic_NN`, `universal_principle_NN`, `knowledge_mode_NN`)
are numbered templates such as "Epistemic concept N concerning…". They carry confidence 0.97 and
were served as `[VERIFIED]` answers.

**Decision.** Detect and quarantine them on load (ONT-010). The data file is untouched and
`quarantine_placeholders=False` restores the raw load.

**Consequences.**
- 420 active concepts and 22 active domains.
- Dangling references among active concepts drop from 544 to 224.
- Replacing the placeholders with real concepts is EXT-028.

### DEC-014 · `.memory/` is the project's canonical, executable memory graph
- **status:** accepted
- **date:** 2026-10-02
- **cites:** INT-005, LAW-003, LAW-012
- **evidence:** mnemosyne/graph.py, mnemosyne/validate.py, .memory/README.md

**Context.** Work across many sessions and agents suffered context collapse: rediscovered vision,
re-derived decisions, assumed state.

**Decision.** `.memory/` holds 11 typed files. Entries have stable IDs and typed edges (ONT-020,
ONT-021). Mnemosyne enforces the memory's laws:
- references resolve;
- enforcers exist;
- ATLAS covers every file;
- measured facts match reality;
- checkpoints form a hash chain;
- every entry traces to INTENTION.

**Alternatives.**
1. Free-form notes. Rejected: unverifiable.
2. An external graph database. Rejected under LAW-006 and LAW-009, and it would not be
   reviewable in git.

**Consequences.** The memory must be updated in the same change as the code (PRO-003), and CI
checks it.

### DEC-015 · Keep the specified T_Hybrid formula; correct its name; the Commander decides intent
- **status:** open
- **date:** 2026-10-02
- **cites:** LAW-005, IDN-006
- **evidence:** control/lambda_mobius.py, docs/LAMBDA_MOBIUS.md

**Context.** `T_Λ^Hybrid = (a·b)/(a+b)` was labelled "harmonic mean", but it is half of it.
**Decision so far.** Keep the formula (changing it is a behaviour change, LAW-005) and correct
every label.
**Open.** Did the specification intend the true harmonic mean 2ab/(a+b)? Switching would double
STEADY-state timing. This awaits the Commander (EXT-017).

### DEC-016 · Tools must not overwrite authoritative documents
- **status:** accepted
- **date:** 2026-10-02
- **cites:** LAW-003, LAW-008
- **evidence:** autonomous_audit_agent.py, tests/test_autonomous_audit_agent.py

**Decision.** Documents marked `<!-- status:authoritative -->` are skipped by the audit agent unless
`--force-doc-update` is passed.

### DEC-017 · The model artifact is frozen; a retrain requires an explicit vault re-index
- **status:** accepted
- **date:** 2026-10-02
- **cites:** LAW-014, INT-004
- **evidence:** logos/runtime.py, vault/spartan_vault.py

**Context.** Λ-Logos learns from documents that keep changing. Silent retraining would make stored
vectors incomparable with new ones.
**Decision.** `models/logos-v1.npz` is loaded as-is once it exists. Retraining is explicit
(`python -m logos train --force`) and is followed by `SpartanVault.reindex()` (PRO-006). The
artifact is generated, not committed: it is about 23 MB and reproducible from the corpus and
parameters. The Docker image trains it at build time.

### DEC-018 · Placeholder detection is structural, not semantic
- **status:** accepted
- **date:** 2026-10-02
- **cites:** LAW-007, IDN-003
- **refines:** DEC-013
- **evidence:** sparta/semantic_foundation.py

**Decision.** An entry is a placeholder only when two things hold together: it belongs to a
numbered-ID family, and the family shares one template definition (three or more members).
Distinct numbered concepts, such as `law_01` and `law_02` with different definitions, are kept.
**Rationale.** Zero false positives on real knowledge matters more than catching subtler filler.
Subtler filler is a curation task (EXT-028).

## Supreme specification (2026-10-02)

### DEC-019 · Single-sampler rule: one periodic loop feeds every observation to Thermopylae
- **status:** accepted
- **date:** 2026-10-02
- **cites:** LAW-011, INT-003
- **refines:** DEC-009
- **evidence:** core/leonidasbrain.py, control/fractal_pipeline.py, tests/test_system_integrity.py::TestThermopylaeSingleSampler

**Context.** The brain fed Thermopylae only on breach ticks, so recoveries never reset the counter,
and the FFP fed the same counter a second time. On the pre-fix code, four *non-consecutive* breaches
activated destruction. That violated DEC-009 and LAW-011.

**Decision.** The homeostasis loop observes every tick, breach and recovery alike. The FFP defers
breach counting while the brain runs, and keeps the capability in standalone mode (LAW-001).

**Rationale.** A consecutive-run counter is well-defined only over a single, complete, periodic
sequence of observations.

### DEC-020 · The Supreme Specification is the architecture reference
- **status:** accepted
- **date:** 2026-10-02
- **cites:** INT-006, LAW-003, LAW-005
- **evidence:** docs/SUPREME_SPECIFICATION.md

**Decision.** `docs/SUPREME_SPECIFICATION.md` derives the complete architecture from eight axioms
(A1–A8). The axioms are extracted from INTENTION and LAWS. The specification covers strata, flows,
equations E1–E25, invariants, the gap register G-01 to G-22, and derived requirements DR-1 to DR-14.

**Admission rule.** A new module or mechanism is admitted only if it is logically, mathematically
*and* necessarily required. Rejected candidates are recorded with their reasons.

**Consequences.**
- Derived requirements become EXT entries.
- Behaviour-changing derivations wait for ratification (DEC-021).

### DEC-021 · Ratify the derived forms CD-1 to CD-6
- **status:** open
- **date:** 2026-10-02
- **cites:** LAW-005, DEC-020, DEC-015
- **evidence:** docs/SUPREME_SPECIFICATION.md

Each derivation fixes the *form*. The Commander chooses the constant or approves the behaviour
change.

| CD | Change | Constant to choose |
|---|---|---|
| CD-1 | Λ-TAS constant k = r/(r−1); today P changes Λ-TAS by ≤ 1.01% | r |
| CD-2 | Thermopylae persistence as a duration τ, N = ⌈τ/T⌉, chosen from a false-activation budget α | α (today: 11.6%/day at p = 0.01) |
| CD-3 | Λ-Möbius threshold κ = k·P_ref·(1 + ln U_ref); today the arbiter is always WRAP and ≈ 1 s | reference point; plus the T_Hybrid intent (DEC-015) |
| CD-4 | SPARTA answer confidence becomes the Fréchet lower bound max(0, 1 − Σ(1 − cᵢ)), instead of min cᵢ (an upper bound) | approval of the behaviour change |
| CD-5 | Λ-Zero signs: Λ₀ = tanh(k₁ℓ − k₂χ + k₃\|θ̇\|), with k₂ > 0.549 | k₂ |
| CD-6 | API perimeter: refuse the default token in strict mode, CORS origins, token expiry | approval of the behaviour change |
