# ATLAS — every file, compressed into the graph

> Each component entry condenses a part of the repository: its role, key elements, maturity and
> evidence. `files` patterns must cover **every** repository file (validator rule M08). A new file
> without an ATLAS entry fails the check (PRO-007). Maturity values: functional, simulated,
> partial, planned.

## Runtime

### MAP-001 · Λ-Core — brain and command router
- **status:** active
- **maturity:** functional
- **cites:** INT-001, ONT-001
- **files:** core/*
- **evidence:** tests/test_core.py, tests/test_brain_ffp_integration.py

`LeondasBrain`:
- runs the homeostasis loop, using Λ-TAS from Helot's P and the CommandProcessor's U (ONT-004,
  DEC-011);
- consults Thermopylae at its configured threshold;
- runs the FFP.

`CommandProcessor` routes seven commands: status, analyze_risk, encrypt_data, check_airgap,
send_message, train_agoge and sparta_query.

### MAP-002 · Phalanx — internal control
- **status:** active
- **maturity:** partial
- **cites:** INT-003, ONT-002
- **depends_on:** MAP-001
- **files:** phalanx/*
- **evidence:** tests/test_phalanx.py

- **Helot** (functional): psutil metrics sampled in a worker thread, P factor, survival
  probability, `last_resources`.
- **Thermopylae** (functional): armed flag, sustained-breach gate, destroys keys and every vault
  path (DEC-009).
- **Agoge** (simulated): random performance signal (EXT-012).
- **Krypteia** (simulated): monitoring thread, but its detectors are empty (EXT-014).

### MAP-003 · Hoplites — action arsenal
- **status:** active
- **maturity:** partial
- **cites:** INT-001, ONT-003
- **depends_on:** MAP-001
- **files:** hoplites/*
- **evidence:** tests/test_hoplites.py, tests/test_system_integrity.py

- **Spartan Guard** (functional): AES-256-GCM, master key from `config/spartan_keys.yaml`.
- **Shield Bearer** (functional): strict and permissive air-gap that ignores loopback, firewall
  probe.
- **Messenger** (functional): in-memory, encrypted through the Guard.
- **Battle Oracle** (simulated): random confidence and Monte Carlo (EXT-013).
- **Weapon Master** (simulated): the allowlist is real; HTTP calls are placeholders (EXT-016).

### MAP-004 · Control — Kronos-Arbiter, Λ-Möbius, Fractal Flux Pipeline
- **status:** active
- **maturity:** partial
- **cites:** DEC-002, ONT-011, ONT-012, ONT-013
- **files:** control/*
- **evidence:** tests/test_lambda_mobius.py, tests/test_fractal_pipeline.py, tests/test_api_lambda_mobius.py

- Kronos computes `N·Θ·Λ·η` with an Amdahl bound.
- Λ-Möbius computes five temporal layers and arbitrates between them. With k = 100, the arbiter
  always selects WRAP (EXT-017).
- FFP runs six phases; HEAL and REINVEST only log (EXT-015).
- The models are unvalidated by benchmark.

### MAP-005 · Parallel execution — Phalanx-Executor and Task-Scheduler
- **status:** active
- **maturity:** functional
- **cites:** DEC-002
- **files:** parallel_execution/*
- **evidence:** tests/test_supreme_parallel.py

Execution uses a ProcessPool with spawn safety. A dependency graph produces execution levels, and
speedup is measured.

### MAP-006 · Vault — encrypted RAG store
- **status:** active
- **maturity:** functional
- **cites:** DEC-008, DEC-010, LAW-011, LAW-014
- **depends_on:** MAP-008
- **files:** vault/*
- **evidence:** tests/test_vector_store.py, tests/test_logos.py

- `SpartanVault`: Fernet encryption, redacted index (ONT-016), key resolution chain, and
  `reindex()` after a model change.
- `SpartanVectorStore`: Λ-Logos embeddings by default, records the model ID, JSON-first
  persistence, external backend as a lazy opt-in (DEC-012).

### MAP-007 · SPARTA — verified reasoning
- **status:** active
- **maturity:** functional
- **cites:** INT-002, ONT-008, DEC-003, DEC-013
- **files:** sparta/*
- **evidence:** tests/test_sparta.py, tests/test_system_integrity.py

- Foundation: 500 concepts on disk, 420 active and 80 quarantined, in 22 active domains.
- `FoundationBridge`, `ReflexiveGenerator` and `SpartaRuntime` sit on top of it.
- Integrity is reported for dangling references and placeholders.
- `semantic_memory.jsonl.backup` is the 44-concept Phase 1 snapshot.
- Gaps: lexical matching (EXT-010), confidence calibration (EXT-003), graph repair (EXT-002).

### MAP-008 · Λ-Logos — our own embedding model
- **status:** active
- **maturity:** functional
- **cites:** INT-004, ONT-014, DEC-012, DEC-017
- **files:** logos/*
- **evidence:** tests/test_logos.py, logos/benchmark.py

The tokenizer extracts hashed word, bigram and character n-gram features. The model applies
TF-IDF and a randomized SVD with a fingerprint. The corpus is SPARTA plus `.memory/` plus the docs.
The runtime keeps a frozen artifact at `models/logos-v1.npz`. The fixed benchmark is MRR 0.68 and
Recall@5 86%. The CLI provides train, info, similar and explain.

### MAP-009 · Mnemosyne and `.memory/` — the project memory graph
- **status:** active
- **maturity:** functional
- **cites:** INT-005, DEC-014, LAW-012
- **depends_on:** MAP-008
- **files:** mnemosyne/*, .memory/*
- **evidence:** tests/test_mnemosyne.py

`mnemosyne/` has five modules:
- `graph`: parser.
- `validate`: rules M01–M13 and W01.
- `measures`: recomputed facts.
- `checkpoint`: hash chain.
- `recall`: Λ-Logos query and the boot pack.

`.memory/` holds the 11 typed files and a README.

### MAP-010 · API — FastAPI surface on port 7300
- **status:** active
- **maturity:** functional
- **cites:** DEC-005, LAW-010
- **depends_on:** MAP-001, MAP-006, MAP-007
- **files:** api/*
- **evidence:** tests/test_api.py, tests/test_system_integrity.py

`server.py` handles section-wired initialization, constant-time auth, and a lifespan that runs
homeostasis, FFP and Krypteia. Routes: health, command, metrics (Prometheus text), lambda-mobius,
vault and sparta. All routes except `/health` require authentication.

## Configuration, deployment, tooling

### MAP-011 · Configuration and dependencies
- **status:** active
- **maturity:** partial
- **cites:** DEC-007, LAW-006
- **files:** config/*, requirements.txt, .coveragerc
- **evidence:** config/settings.yaml

- `settings.yaml` has one section per module. At least 60 leaf keys are declarative or not yet
  wired (EXT-007).
- Other files: the key template, `prometheus.yml` (authorization block) and `requirements.txt`
  (no ML runtime).

### MAP-012 · Deployment and CI
- **status:** active
- **maturity:** partial
- **cites:** LAW-002, LAW-009
- **files:** Dockerfile, .dockerignore, docker-compose.yml, .github/workflows/*
- **evidence:** Dockerfile, .github/workflows/ci.yml

- The image copies every package plus the corpus and trains Λ-Logos at build time.
- Compose adds Prometheus and Grafana; Redis and Postgres are reserved (EXT-019).
- CI runs ruff, shellcheck, `mnemosyne check`, `pytest -W error` and a Docker build.
- CI runners have not executed yet (STATE-008).

### MAP-013 · Scripts
- **status:** active
- **maturity:** functional
- **cites:** LAW-002
- **files:** scripts/*
- **evidence:** scripts/install_sparta.sh

- `install_sparta.sh` (Python ≥ 3.10 check)
- `activate_leonidas.sh` (menu; tests run via pytest)
- `run_coverage.sh`
- `generate_keys.py` (writes `MASTER_AES_KEY_HEX`)

All are ShellCheck-clean.

### MAP-014 · Audit tools
- **status:** active
- **maturity:** partial
- **cites:** DEC-016, LAW-003
- **files:** audit_analyzer.py, autonomous_audit_agent.py
- **evidence:** tests/test_audit_analyzer.py, tests/test_autonomous_audit_agent.py

`audit_analyzer.py` is static analysis with 98% coverage. `autonomous_audit_agent.py` uses a
file-length completion heuristic (EXT-001); it is now barred from overwriting authoritative docs.

### MAP-015 · Test suite
- **status:** active
- **maturity:** functional
- **cites:** LAW-002, LAW-013
- **files:** tests/*
- **evidence:** tests/conftest.py

The suite has one test module per component plus `test_system_integrity` (regression for the
audit), `test_logos`, `test_mnemosyne` and `test_autonomous_audit_agent`. Counts are measured in
STATE-002.

### MAP-016 · Examples
- **status:** active
- **maturity:** functional
- **cites:** ONT-008
- **files:** examples/*
- **evidence:** examples/sparta_demo.py

`sparta_demo.py` is a runnable SPARTA walkthrough.

## Documentation

### MAP-017 · Authoritative documentation (kept in sync with code)
- **status:** active
- **cites:** LAW-003, DEC-006
- **files:** README.md, PROJECT_STATUS.md, BACKLOG.md, ARCHITECTURE.md, QUICKSTART.md, docs/RAG_VECTORIAL.md, docs/LAMBDA_MOBIUS.md, docs/LAMBDA_MOBIUS_QUICKSTART.md
- **evidence:** PROJECT_STATUS.md

- PROJECT_STATUS: measured status and remediation log.
- BACKLOG: prioritized tasks, mirrored as EXT entries here.
- README, ARCHITECTURE, QUICKSTART: overview, structure and usage.
- RAG and Λ-Möbius guides.

### MAP-018 · Vision and specifications (design intent, not status)
- **status:** active
- **cites:** INT-001, INT-002, INT-006
- **files:** docs/SUPREME_SPECIFICATION.md, ADVANCED_CAPABILITIES.md, TEMPORAL_COMPRESSION_MASTER_PLAN.md, docs/sparta/*
- **evidence:** docs/sparta/SPARTA_LAMBDA_MODULES.md

- SUPREME_SPECIFICATION: the derived architecture reference (DEC-020). It contains axioms A1–A8,
  strata S0–S7, flows F1–F9, equations E1–E25, the gap register and the optimality theorem.
- ADVANCED_CAPABILITIES: the Λ-TAS, P and U mathematics, the Spartan Laws, hardware allocation,
  and the PQC/eBPF/mesh/ledger roadmap.
- The master plan: temporal compression, Spartanization and the roadmap.
- `docs/sparta/`: Overview, Foundation (the planned 445-concept, 11-domain design), Architecture,
  Λ-Modules (complete specification) and Flow examples. Each opens with a note on what is
  actually implemented.

### MAP-019 · Historical records (November 2025 snapshots)
- **status:** superseded
- **cites:** DEC-006, IDN-002
- **files:** AUDIT_*.md, AUDIT_DELIVERABLES.txt, FINAL_*.md, COMPLETE_*.md, PROGRESS_AUDIT.md, STATUS_REPORT.md, PHASE4_COMPLETION_REPORT.md, MISSING_FEATURES.md, TEST_COVERAGE.md, COMPATIBILITY_MATRIX.md, SPARTA_FOUNDATION.md
- **evidence:** PROJECT_STATUS.md

Sixteen audit, status and phase reports plus the early SPARTA stub. They are kept intact under
historical banners. The figures in them (for example "77.8% complete" and "production ready") are
not current; JOURNAL keeps the timeline they describe (EVT-005).

### MAP-020 · Repository hygiene and licence
- **status:** active
- **cites:** LAW-010
- **files:** .gitignore, LICENSE
- **evidence:** .gitignore

- MIT licence.
- `.gitignore` keeps keys, `data/`, `models/`, logs and coverage output out of git.
