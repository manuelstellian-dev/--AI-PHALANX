# EXTENSIONS — where the project goes next

> Forward edges from the current state to the intended end-state (INT-006). Numbering mirrors
> BACKLOG.md one-to-one (EXT-010 = B-10), which holds full acceptance criteria. Every extension
> is anchored to the laws and intentions it serves (validator rule M12); `depends_on` gives order.
> Priority: P0 integrity/security · P1 make simulated parts real · P2 tooling · P3 advanced.

## P0 — integrity and security

### EXT-001 · Audit agent measures behaviour, not file length (P0)
- **status:** planned
- **cites:** LAW-003, DEC-016
- **evidence:** autonomous_audit_agent.py

Derive completion from passing tests and the ATLAS maturity values, write reports instead of
editing documents, and raise coverage from 25% to at least 90%.

### EXT-002 · Repair the SPARTA knowledge graph (P0)
- **status:** planned
- **cites:** LAW-007, LAW-012, DEC-013
- **evidence:** sparta/semantic_foundation.py

There are 224 dangling references among the 420 active concepts. Most point at domain names used
as concept IDs (`philosophy`, `epistemology`, `logic`). Fix them with domain hub concepts or by
remapping. Done when `/api/v1/sparta/integrity` reports `healthy: true` (STATE-003).

### EXT-003 · Calibrate concept confidence (P0)
- **status:** planned
- **cites:** LAW-007, DEC-004
- **depends_on:** EXT-002

Every confidence lies in [0.95, 1.0], so the 0.70/0.80/0.95 thresholds cannot discriminate. Write
a rubric that maps source and verification to confidence bands, then re-score.

### EXT-004 · Key management and vault cryptography (P0)
- **status:** planned
- **cites:** LAW-011, DEC-008, DEC-020

- Derive the vault key from the master key (HKDF) or a secrets mount.
- Move the vault to AES-256-GCM through Spartan Guard.
- Add key rotation that re-encrypts stored data.
- Document embedding leakage.

Specification DR-13 makes two further requirements necessary:
- **Crypto-erasure:** every secret is wrapped by the master key, so Thermopylae is guaranteed by
  destroying one key. Overwriting files does not erase them on SSD or copy-on-write media.
- **A per-key AES-GCM invocation counter**, with rotation before 2³² random-nonce encryptions
  (NIST SP 800-38D).

### EXT-005 · Thermopylae reaches its targets inside Docker (P0)
- **status:** planned
- **cites:** LAW-011
- **evidence:** docker-compose.yml

`./config` is mounted read-only, so destroying the keys fails in the container. Move the keys to a
writable secrets volume and add an integration test.

### EXT-006 · Harden the API perimeter (P0)
- **status:** planned
- **cites:** LAW-010, DEC-005

Tasks:
- configurable CORS origins (the current setting is `*` with credentials);
- refuse the default token in strict mode;
- token expiry;
- rate limiting of failed authentication.

### EXT-007 · Close the configuration gap (P0)
- **status:** planned
- **cites:** LAW-003, DEC-007
- **evidence:** config/settings.yaml

At least 60 of the settings' leaf keys are read by no code. For each one, wire it in and test it,
or move it under a `declarative:` or `planned:` section. Add a test that fails on unread keys.

### EXT-008 · Container hardening (P0)
- **status:** planned
- **cites:** LAW-010, LAW-009

Run as a non-root user. The Prometheus token should come from the same secret
(`credentials_file`).

### EXT-009 · Reproducible dependencies and a wider CI matrix (P0)
- **status:** planned
- **cites:** LAW-002

Add a lock file, a CI matrix for Python 3.10–3.12, and a scheduled run that catches upstream
breakage.

## P1 — make the simulated parts real

### EXT-010 · Claim-level anti-hallucination for SPARTA (P1)
- **status:** planned
- **cites:** LAW-007, INT-002
- **depends_on:** EXT-002, EXT-003
- **evidence:** sparta/reflexive_generator.py

Check statements against `formal_statement` and `counterexamples`, not just for mentions. Use
Λ-Logos for concept retrieval, with Λ-Logos ranking feeding extraction. Add a true/false/unknown
benchmark to CI.

### EXT-011 · Implement the seven Λ-Modules (P1)
- **status:** planned
- **cites:** INT-006, ONT-019
- **depends_on:** EXT-010, EXT-019
- **evidence:** docs/sparta/SPARTA_LAMBDA_MODULES.md

Order:
1. Identity, Guide and Meta.
2. Pattern (needs EXT-010).
3. Zero (needs θ̇ from Kronos).
4. Affect and Reflect (needs EXT-019).

The single integration point is `SpartaRuntime.query`.

Specification DR-11: Λ-Guide is *necessary*. Under the Fréchet lower bound (CD-4), a verified
answer needs Σ(1 − cᵢ) ≤ 0.05, so the minimal sufficient concept set must be selected. Build
Λ-Guide first.

### EXT-012 · Real learning signal for Agoge (P1)
- **status:** planned
- **cites:** INT-003, IDN-003
- **evidence:** phalanx/agoge.py

Replace `random.uniform` with observed outcomes: Oracle accuracy, SPARTA verification rates and
Λ-Reflect errors.

Specification DR-9: today log a is a driftless random walk (gap G-17). The learning signal must
be π = 1 − e_t.

### EXT-013 · Model-based Battle Oracle (P1)
- **status:** planned
- **cites:** IDN-003, INT-001
- **evidence:** hoplites/battleoracle.py

Run Monte Carlo from scenario parameters and report empirical confidence intervals. Honour the
configured iterations and threshold.

### EXT-014 · Real Krypteia detectors (P1)
- **status:** planned
- **cites:** INT-003, LAW-011
- **evidence:** phalanx/krypteia.py

Add a file-hash baseline, socket checks and process anomaly checks. Detected threats feed survival
probability and the FFP quarantine phase.

### EXT-015 · Bounded healing and reinvestment in FFP (P1)
- **status:** planned
- **cites:** LAW-008, INT-003
- **evidence:** control/fractal_pipeline.py

Each anomaly type maps to a bounded, reversible and audited action, with no self-modification of
the core.

Specification DR-8: without actuators, the "homeostasis" loop is open-loop monitoring (gap G-16).
The actuators close the loop.

### EXT-016 · Real Weapon Master client, deny-by-default (P1)
- **status:** planned
- **cites:** LAW-009, LAW-006
- **evidence:** hoplites/weaponmaster.py

An empty allowlist must deny everything when access is enabled. Requests time out and every
outbound request is logged.

### EXT-017 · Validate temporal-compression models; settle T_Hybrid (P1)
- **status:** planned
- **cites:** DEC-002, DEC-015, IDN-003
- **evidence:** control/lambda_mobius.py

Benchmark Kronos predictions against measured Phalanx-Executor runs. Calibrate the arbiter (WRAP
is always selected at k = 100). Get the Commander's ruling on T_Hybrid.

### EXT-018 · Hardware truth for Helot (P1)
- **status:** planned
- **cites:** INT-003, ONT-005
- **evidence:** phalanx/helot.py

Use real GPU and NPU telemetry, and calibrate the survival model against recorded traces.

### EXT-019 · Persistence layer (P1)
- **status:** planned
- **cites:** INT-005, INT-003
- **evidence:** docker-compose.yml

Persist threats, messages, Oracle history and Kronos history (Redis/Postgres or SQLite).
Λ-Reflect needs this.

## P2 — tooling and documentation

### EXT-020 · Decide the fate of the roadmap executor (P2)
- **status:** open
- **cites:** DEC-002, LAW-005
- **evidence:** TEMPORAL_COMPRESSION_MASTER_PLAN.md

Master-plan Phases 2–4 were never built. Either implement them or record that they are dropped
(Commander).

### EXT-021 · Windows support scripts (P2)
- **status:** planned
- **cites:** INT-001
- **evidence:** COMPATIBILITY_MATRIX.md

Add PowerShell install and activate scripts, plus a Windows CI job.

### EXT-022 · Documentation consolidation (P2)
- **status:** planned
- **cites:** IDN-005, DEC-006

Move the historical reports to `docs/history/`, keeping their content and git history. Record a
language convention.

## P3 — advanced capabilities

### EXT-023 · Post-quantum cryptography (P3)
- **status:** planned
- **cites:** INT-006, LAW-011
- **depends_on:** EXT-004
- **evidence:** ADVANCED_CAPABILITIES.md

Use a hybrid ML-KEM-1024 (FIPS 203) key wrap over AES-256-GCM, with ML-DSA (FIPS 204) signatures.

### EXT-024 · eBPF monitoring for Krypteia (P3)
- **status:** planned
- **cites:** INT-003
- **depends_on:** EXT-014

Kernel-level syscall and network visibility on Linux. This would be the project's first C (or
Rust) component, with its own toolchain gates.

### EXT-025 · Federated Phalanx mesh (P3)
- **status:** planned
- **cites:** INT-006
- **depends_on:** EXT-012, EXT-004

Share gradients only between instances, on port 7301.

### EXT-026 · Immutable audit ledger (P3)
- **status:** planned
- **cites:** LAW-008, LAW-011
- **depends_on:** EXT-023

Keep a hash-chained log of Thermopylae events and critical decisions, signed with ML-DSA. Mnemosyne
checkpoints already use the same chaining pattern.

Specification DR-14: the checkpoint chain is tamper-evident only while it is anchored (E22). Add
signatures.

## New from the sovereignty session

### EXT-027 · Λ-Logos v2 — stronger semantics, still our own (P1)
- **status:** planned
- **cites:** INT-004, DEC-012, LAW-006
- **evidence:** logos/benchmark.py

Learn from SPARTA's own structure: concept relations and prerequisites become positive pairs for a
supervised projection (for example canonical correlation or a contrastive linear map). Grow the
benchmark beyond 28 queries. Every release must beat v1 on the fixed benchmark (MRR 0.68), and a
model change requires a vault re-index (PRO-006).

### EXT-028 · Replace the 80 placeholder concepts with real knowledge (P0)
- **status:** planned
- **cites:** LAW-007, DEC-013, DEC-018
- **depends_on:** EXT-003

Author real 16-field concepts for EpistemicCore, UniversalPrinciples and ModesOfKnowledge, with
sources and verification, or retire the families by Commander decision. The quarantine lifts
automatically when the definitions stop being templates.

## From the Supreme Specification (DEC-020)

### EXT-029 · Wire the inputs of U: in-flight tasks and vault volume (P1)
- **status:** planned
- **cites:** INT-003, DEC-020, DEC-011
- **evidence:** core/commandprocessor.py

Specification DR-2 and result R2: `active_tasks` and `data_vault_size_mb` are never updated, so
U ≡ a and Λ-TAS is constant at about 0.695 s.
- Increment `active_tasks` on command entry and decrement it in `finally`.
- Set the vault size in MB at each save.

### EXT-030 · Single source of truth for resource thresholds (P1)
- **status:** planned
- **cites:** INT-003, LAW-003, DEC-020
- **evidence:** control/fractal_pipeline.py

Specification DR-7 and gap G-07: the FFP flags CPU and memory above 90% while Helot's configured
critical levels are 95% CPU, 90% memory and 95% disk. The FFP should read
`phalanx.helot.resource_thresholds`.

### EXT-031 · Implement the ratified derived forms CD-1 to CD-6 (P0 once ratified)
- **status:** blocked
- **cites:** LAW-005, DEC-021
- **depends_on:** EXT-003
- **evidence:** docs/SUPREME_SPECIFICATION.md

This is blocked on the Commander's ratification (DEC-021). Each change ships with a regression test
that reproduces its computed result:
- R1 for CD-1, Λ-TAS sensitivity to P;
- R5 for CD-2, Thermopylae false activation;
- R3 for CD-3, Λ-Möbius degeneration;
- R6 for CD-4, confidence bounds;
- R9 for CD-5, the Λ-Zero signs.
