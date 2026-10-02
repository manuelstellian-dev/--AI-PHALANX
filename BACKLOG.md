# ΛΕΩΝΙΔΑΣ-AI PHALANX — Backlog

**ΜΟΛΩΝ ΛΑΒΕ** — *"Come and Take Them"*

Prioritized engineering backlog derived from the 2026-10-02 forensic audit ([PROJECT_STATUS.md](PROJECT_STATUS.md)).
Each task states **why** it is needed relative to the vision and **how we know it is done**.

Priority scale:
- **P0** — integrity or security: the system's claims are not yet true.
- **P1** — turn simulated components into real ones; this is the substance of the vision.
- **P2** — roadmap and tooling.
- **P3** — advanced capabilities.

Ordering principle: *a fortress is only as strong as its foundation*. SPARTA promises truth, and Thermopylae promises that a compromise yields nothing of value. Both promises must hold before new capability is added.

---

## P0 — Integrity and security

### B-01 · Make the audit agent measure behaviour, not file length
**Why.** `autonomous_audit_agent.py` marks a component 100% done when its file has more than 50 lines. This produced the false "77.8% complete / PRODUCTION READY" claims. Its README rewrite would also overwrite the corrected status. Its coverage is 25%: only the documentation guard added in the audit is tested.
**Done when:**
- Completion is derived from tests that pass per component, plus the maturity classes in PROJECT_STATUS §4.
- The agent writes its findings to a report instead of editing authoritative docs.
- Test coverage of the agent is at least 90%.

### B-02 · Repair the SPARTA knowledge graph (224 dangling references among active concepts)
**Why.**
- Of the 544 dangling references originally measured, 320 came from the 80 quarantined placeholder concepts (B-28).
- 224 remain among the 420 active concepts. Most use **domain names as concept IDs**, such as `philosophy`, `epistemology`, `logic` and `cognitive_psychology`.
- `verify_concept`-style prerequisite checks fail on these, and graph traversal silently drops edges. A foundation that "knows what it knows" cannot contain unresolved references.

**Done when:**
- Each target is resolved by one of: a domain hub concept (a full 16-field entry), remapping to an existing concept, or moving the domain to the `domain` field.
- `GET /api/v1/sparta/integrity` reports `healthy: true`.
- A CI test fails on any new dangling reference.

### B-03 · Calibrate concept confidence
**Why.**
- All 500 confidences lie in [0.95, 1.0], so the thresholds 0.70 (Bridge), 0.80 (hallucination) and 0.95 (verified) can never separate concepts. Every answer is "verified".
- Confidence is self-assigned at authoring time and has no provenance.

**Done when:**
- A written rubric maps `source` and `verification` to confidence bands. For example, `mathematical_theorem` gets 1.0, while `philosophical_consensus` and `theoretical_framework` get lower values.
- The knowledge base is re-scored against the rubric.
- Thresholds are documented in one place and tested.

### B-04 · Key management and vault cryptography
**Why.**
- Without `SPARTA_VAULT_KEY`, the vault key is stored beside the ciphertext. That defends against index leaks, not disk compromise.
- The vault uses Fernet (AES-128-CBC with HMAC), while the documents promise AES-256.
- Embeddings of encrypted entries remain searchable and leak semantic similarity.
- There is no key rotation.

**Done when:**
- The vault key is derived from the Spartan Guard master key (for example with HKDF) or loaded from a secrets mount.
- Vault encryption runs through AES-256-GCM in Spartan Guard.
- Key rotation re-encrypts all stored data.
- The leakage from embeddings is documented, with an option to disable indexing of encrypted entries.

### B-05 · Thermopylae must be able to reach its targets in Docker
**Why.** Compose mounts `./config:/app/config:ro`, so key destruction fails inside the container and the "compromise yields nothing" guarantee breaks.

**Done when:**
- Keys live on a writable secrets volume referenced by `keys_path`.
- An integration test arms Thermopylae in a container-like layout and verifies that both the keys and every vault path are gone.

### B-06 · Harden the API perimeter
**Why.**
- CORS uses `allow_origins=["*"]` together with `allow_credentials=True`.
- There is no token expiry, even though `auth.token_expiry_hours` exists.
- There is no rate limiting.
- The server starts with the default token, while `security.strict_mode` is unused.

**Done when:**
- CORS origins come from `api.*` configuration.
- Strict mode refuses to start with the default token.
- Tokens expire, or the setting is removed from the docs.
- Failed authentication attempts are rate-limited.

### B-07 · Close the configuration gap (at least 60 of 89 settings are unread)
**Why.** Settings that do nothing are false promises. Examples are `security.audit_log_enabled`, `logging.*`, `messenger.queue_max_size`, `battle_oracle.simulation_default_iterations` and the retention windows.

**Done when:**
- Every key is either wired into code with a test, or moved under a clearly marked `declarative:` or `planned:` section.
- A test fails when settings.yaml gains a key that no code reads.

### B-08 · Container hardening
**Why.**
- The image runs as root.
- The Prometheus scrape token is duplicated in `prometheus.yml` instead of following `SPARTA_AUTH_TOKEN`.

**Done when:**
- The image runs as a non-root user, with writable `data/` and `logs/` volumes.
- Prometheus reads its token from `credentials_file`, provisioned from the same secret.

### B-09 · Reproducible dependencies and a wider CI matrix
**Why.** Unpinned dependencies silently raised the minimum Python version from 3.8 to 3.10. That was first `sentence-transformers` (now removed); today numpy and scipy are also unpinned. CI verifies only 3.11.

**Done when:**
- A lock file (or `pip-compile` output) is committed.
- The CI matrix covers 3.10–3.12.
- A scheduled job detects upstream breakage.

---

## P1 — Make the simulated parts real

### B-10 · Semantic, claim-level anti-hallucination for SPARTA
**Why.**
- `ReflexiveGenerator._extract_concepts_from_text` matches concepts by word overlap.
- `detect_hallucination` checks that known concepts are *mentioned*, not that a statement is *consistent* with them. For example, "energy can be created" mentions energy conservation and passes.
- This is the central promise of SPARTA.

**Done when:**
- Statements are checked against each concept's `formal_statement` and `counterexamples`.
- Embeddings from the vault model are used for concept retrieval.
- A benchmark of true, false and unknown claims reaches agreed precision and recall, and runs in CI.

### B-11 · Implement the seven Λ-Modules (`lambda_modules/`)
**Why.**
- These are the largest unbuilt part of the vision. The full specification with code is in `docs/sparta/SPARTA_LAMBDA_MODULES.md`.
- `ReflexiveGenerator` already contains TODO hooks for Λ-Identity, Λ-Pattern and Λ-Meta.

**Order:**
1. Λ-Identity, Λ-Guide and Λ-Meta, which build on existing data.
2. Λ-Pattern, which depends on B-10.
3. Λ-Zero, the critical module. It needs θ̇ from Kronos.
4. Λ-Affect, then Λ-Reflect, which needs persistence (B-19).

**Done when:**
- Each module has tests and is wired into `SpartaRuntime.query` following the "Flow complet" pipeline in the specification.
- `/api/v1/sparta/query` returns `identity`, `reasoning`, `affect`, `lambda_zero` and `parameters`.

### B-12 · Real learning signal for Agoge
**Why.** The adaptation factor is driven by `random.uniform(0.8, 1.2)`, so U, and therefore Λ-TAS, contain noise rather than learning.

**Done when:** performance is computed from observed outcomes, such as Battle Oracle accuracy, SPARTA verification rates and Λ-Reflect error logs, and is tested to be deterministic for a given history.

### B-13 · Model-based Battle Oracle
**Why.** `confidence`, `predict_outcome` and the Monte Carlo simulation are random and ignore their parameters. The simulation even reports a fixed confidence interval of [0.5, 0.7].

**Done when:**
- The simulation samples from scenario parameters and reports an empirical confidence interval.
- `simulation_default_iterations` and `prediction_confidence_threshold` are honoured.

### B-14 · Real Krypteia detectors
**Why.** Network, process and file-integrity checks are empty, so `threat_level` is always "low" unless threats are reported manually. This is also a prerequisite for eBPF (B-24).

**Done when:**
- Detectors cover a baseline file-hash manifest, unexpected listening sockets and process anomalies.
- Detected threats feed the survival probability and FFP quarantine.
- The interval and retention settings are honoured.

### B-15 · Bounded healing and reinvestment in FFP
**Why.** The HEAL and REINVEST phases only log. Self-repair is a core claim of FFP.

**Done when:**
- Each anomaly type maps to a bounded, reversible action, such as garbage collection, cache eviction or triggering an Agoge cycle.
- Actions respect Law I, which forbids self-modification of the core.
- Actions are audited (see B-26).

### B-16 · Real Weapon Master client, deny-by-default
**Why.**
- HTTP calls return placeholder data.
- An empty `allowed_domains` currently means *allow everything* once access is enabled, which contradicts the mandatory air-gap.

**Done when:**
- A real HTTP client honours `request_timeout_sec`.
- An empty allowlist denies every request.
- Every outbound request is logged.

### B-17 · Validate the temporal-compression models
**Why.**
- With k = 100, the Λ-Arbiter selects WRAP for every U > 1, so UNWRAP is reachable only with very small k·P.
- The master plan's 714× speedup and its "16 weeks → 2–3 weeks" claim multiply assumed factors and have never been measured.

**Open design decision (owner):** `T_Λ^Hybrid = (T_wrap·T_mult)/(T_wrap+T_mult)` has always been labelled "harmonic mean", but it is **half** the harmonic mean `2ab/(a+b)`. The code and tests implement the specified formula, and the labels have been corrected. Switching to the true harmonic mean would double STEADY-state timing (FFP cycle intervals, `/api/v1/lambda-mobius`).

**Done when:**
- Benchmarks following the master plan's §8.6 methodology compare Kronos predictions with measured `PhalanxExecutor` runs.
- Arbiter thresholds are calibrated.
- The T_Hybrid intent is confirmed.
- The documents report measured, not projected, speedups.

### B-18 · Hardware truth for Helot
**Why.** GPU and NPU load come from `simulated_gpu_load`. The survival-probability penalties are uncalibrated constants, and they decide Thermopylae.

**Done when:**
- Optional GPU telemetry is added (via GPUtil or NVML).
- The survival model is documented and tested against recorded resource traces.

### B-19 · Persistence layer
**Why.**
- Threat history, messages, Oracle predictions and Kronos history live only in memory and are lost on restart.
- Redis and Postgres are deployed in Compose but unused.
- Λ-Reflect (B-11) needs durable error logs.

**Done when:** a storage interface backs these stores, either with the Compose services or with SQLite, and `docker compose up` exercises it.

---

## P2 — Roadmap execution and tooling

### B-20 · Decide the fate of the roadmap executor
**Why.** Master plan Phases 2–4 (`roadmap_parser`, `task_generator`, `parallel_implementer`) were never built. In practice, AI-agent PRs replaced them.

**Done when:** the tools are implemented with tests, or the master plan records the decision to drop them.

### B-21 · Windows support scripts
**Why.** `MISSING_FEATURES.md` §4 and `COMPATIBILITY_MATRIX.md` promise PowerShell installers, and Shield Bearer already supports Windows Firewall.

**Done when:** `install_sparta.ps1` and `activate_leonidas.ps1` exist and are exercised by a Windows CI job.

### B-22 · Documentation consolidation
**Why.** There are 17 historical audit and status files next to the authoritative documents, and the documentation mixes Romanian and English.

**Done when:**
- The historical files move to `docs/history/`, keeping their content and git history.
- A language convention is recorded in the README.

---

## P3 — Advanced capabilities

### B-23 · Post-quantum cryptography
**Why.** Protection against "harvest now, decrypt later" attacks (`ADVANCED_CAPABILITIES.md` §IV). Kyber and Dilithium are now standardized as **ML-KEM (FIPS 203)** and **ML-DSA (FIPS 204)**.

**Done when:**
- A hybrid scheme is in place: ML-KEM-1024 key encapsulation wraps the AES-256-GCM keys, and ML-DSA signs keys and ledger entries.
- `advanced_capabilities.post_quantum_cryptography.enabled` is honoured.

### B-24 · eBPF monitoring for Krypteia (Linux)
**Why.** Kernel-level detection of system calls and network activity.

**Depends on:** B-14. This would be the project's first C (or Rust) component, with its own build and toolchain checks in CI.

### B-25 · Federated Phalanx mesh
**Why.** Coordination between multiple Phalanx instances by sharing gradients only (`advanced_capabilities.federated_learning`, port 7301).

**Depends on:** B-12 (a real learning signal) and B-04 (key management).

### B-26 · Immutable audit ledger
**Why.** Thermopylae events and critical decisions must be tamper-evident (`advanced_capabilities.immutable_ledger`).

**Done when:**
- An append-only, hash-chained log exists, signed with ML-DSA once B-23 is done.
- Thermopylae, Weapon Master and FFP actions are recorded in it.

---

---

## Added in the sovereignty session (2026-10-02)

### B-27 · Λ-Logos v2: stronger semantics, still our own (P1)
**Why.** Λ-Logos v1 beats the lexical baseline (MRR 0.690 against 0.527), but it is below large
pretrained transformers, which the project no longer uses (LAW-006). SPARTA's own relations and
prerequisites are free supervision.

**Done when:**
- A supervised projection learned from concept relations (for example CCA or a contrastive linear map) beats v1 on the fixed benchmark.
- The benchmark has grown beyond 28 queries.
- Vaults are re-indexed after the switch (`.memory` PRO-006).

### B-28 · Replace the 80 quarantined placeholder concepts (P0)
**Why.**
- `epistemic_01..40`, `universal_principle_01..20` and `knowledge_mode_01..20` are numbered templates carrying confidence 0.97.
- They were served as `[VERIFIED]` answers until the quarantine (`.memory` DEC-013).
- Two whole domains (UniversalPrinciples, ModesOfKnowledge) contain no real knowledge.

**Done when:** the families are replaced with sourced 16-field concepts, or retired by Commander
decision. The quarantine count then reaches 0.

> The machine-checked form of this backlog is `.memory/EXTENSIONS.md` (EXT-NNN mirrors B-NNN).

## Dependency summary

```
B-28 ──► B-02, B-03 ──► B-10 ──► B-11 (Λ-Pattern, Λ-Zero) ──► B-12
B-27 ──► B-10 (Λ-Logos retrieval for SPARTA)
B-14 ──► B-24
B-04 ──► B-23 ──► B-26
B-19 ──► B-11 (Λ-Reflect)
B-12, B-04 ──► B-25
```

Recommended next sprint: **B-02, B-03 and B-10** (SPARTA truthfulness), followed by **B-04 and B-05**, which are the Thermopylae and key-management guarantees.
