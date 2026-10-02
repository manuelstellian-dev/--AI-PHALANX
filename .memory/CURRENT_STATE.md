# CURRENT_STATE — where the project stands now

> The active node: the entry point of every session. Facts written as `measure` lines are
> **recomputed from the repository** by `python -m mnemosyne check` (rule M09), so this file
> cannot drift silently. Other facts are anchored to the latest checkpoint's `gates`.
> Verified on branch `claude/keen-dirac-lvnjul`, 2026-10-02.

### STATE-001 · Phase and headline
- **status:** in_progress
- **cites:** INT-006, MAP-001, MAP-007

**Phase 2 (Foundation & Modules) is in progress.**

- Core infrastructure is functional: Λ-Core, Phalanx (Helot, Thermopylae), Hoplites (Guard,
  Shield, Messenger), parallel execution, the vault and the API.
- SPARTA is wired into the API and the command router.
- The project now runs on its **own model**, Λ-Logos.
- Still to build: the seven Λ-Modules (EXT-011) and the simulated components: Agoge, Krypteia,
  Battle Oracle, Weapon Master and FFP heal/reinvest (EXT-012 to EXT-016).
- Phase 3 (PQC, eBPF, mesh, ledger) has not started.

### STATE-002 · Quality gates
- **status:** active
- **cites:** LAW-002, LAW-013, MAP-015
- **measure:** tests.functions = 627
- **measure:** tests.modules = 17

Test functions are counted statically. pytest collects more tests than that, because
parametrized cases are counted separately. That count and the lint, ShellCheck and coverage
results are recorded in the latest checkpoint's `gates`. Coverage at the remediation checkpoint
was 86% overall, 95% excluding `autonomous_audit_agent.py` (EXT-001).

### STATE-003 · SPARTA Foundation
- **status:** active
- **cites:** DEC-013, EXT-002, EXT-028, MAP-007
- **measure:** sparta.concepts_on_disk = 500
- **measure:** sparta.concepts_active = 420
- **measure:** sparta.concepts_quarantined = 80
- **measure:** sparta.domains_active = 22
- **measure:** sparta.dangling_references = 224

All concepts score confidence in [0.95, 1.0], so they are not yet calibrated (EXT-003).
Hallucination detection is lexical (EXT-010). The integrity report is available at
`/api/v1/sparta/integrity`.

### STATE-004 · Sovereignty — own model, no external ML runtime
- **status:** active
- **cites:** LAW-006, DEC-012, MAP-008
- **measure:** deps.external_ml_runtime = none
- **measure:** deps.requirements = 11

The current artifact is `logos-v1:7ace9ee49387`, retrained under PRO-006 once `.memory/` joined
the corpus. It has 1,948 corpus documents and 384 latent axes. On the fixed benchmark (28
queries against 420 concepts):

| | Λ-Logos | Lexical baseline |
|---|---|---|
| MRR | 0.690 | 0.527 |
| Recall@1 | 57% | 43% |
| Recall@5 | 82% | 61% |
| Mean rank | 16.5 | 40 |

The first training (1,794 documents) scored MRR 0.680 and Recall@5 86%: MRR went up while
Recall@5 went down.

Memory recall blends the latent and lexical channels (α = 0.5). It scores 8/10 top-3 hits and
MRR 0.78, against 7/10 for the latent channel alone.

A clean installation is 350 MB, compared with 5.9 GB when the external model was used. MRR 0.690
is the floor that the next model version must beat (EXT-027).

### STATE-005 · Repository composition
- **status:** active
- **cites:** LAW-012, MAP-019
- **measure:** repo.files = 141
- **measure:** repo.python_files = 79
- **measure:** repo.markdown_files = 45
- **measure:** repo.shell_scripts = 3
- **measure:** repo.packages = api,control,core,hoplites,logos,mnemosyne,parallel_execution,phalanx,polis,sparta,vault
- **measure:** config.settings_leaf_keys = 89

Every file is mapped in ATLAS (rule M08). The repository contains no Rust, C/C++ or JSON
configuration sources. The SPARTA knowledge base is JSONL.

### STATE-006 · API surface
- **status:** active
- **cites:** DEC-005, LAW-010, MAP-010
- **measure:** api.routes = 24

The routes are health (3), command (5), metrics (3), vault (8), sparta (4) and the root `/`.
Everything except `/api/v1/health` requires the bearer token.

### STATE-007 · Component maturity
- **status:** active
- **cites:** MAP-002, MAP-003, MAP-004, IDN-003

| Maturity | Components |
|---|---|
| Functional | Λ-Core, Helot, Thermopylae, Spartan Guard, Shield Bearer, Messenger, Phalanx-Executor, Task-Scheduler, Kronos and Λ-Möbius (as models), Vault, SPARTA, Λ-Logos, Mnemosyne, API |
| Simulated | Agoge (random signal), Krypteia (empty detectors), Battle Oracle (random confidence), Weapon Master (placeholder HTTP) |
| Partial | FFP (heal and reinvest only log), configuration (≥60 unread keys), audit agent (heuristic) |
| Planned | Λ-Modules, PQC, eBPF, federated mesh, immutable ledger |

### STATE-008 · Blocked — needs the Commander
- **status:** blocked
- **cites:** LAW-002, DEC-015, MAP-012

1. **GitHub Actions:** the CI jobs were assigned no runner (`runner_id 0`, no steps executed).
   That is an account-level Actions setting such as billing or spending limits, not a code issue.
2. **Docker build** in the agent sandbox: the network policy denies `deb.debian.org`. The image
   layout was verified by booting the server from the exact `COPY`'d tree.
3. **T_Hybrid intent** (DEC-015): keep `(a·b)/(a+b)`, or adopt the true harmonic mean?
4. **Ratification of CD-1 to CD-6** (DEC-021): the derived forms from the Supreme Specification.
   The most safety-relevant is CD-2. With Thermopylae armed, if 1% of samples are critical, the
   current N = 3 gives an 11.6% chance per day of self-destruction.

### STATE-009 · Next steps
- **status:** active
- **cites:** EXT-002, EXT-003, EXT-028, EXT-010, EXT-004, EXT-005

The architecture reference is `docs/SUPREME_SPECIFICATION.md` (DEC-020). The recommended order:
0. Ratify DEC-021, then implement EXT-031.
1. Make SPARTA truthful:
   - repair the graph (EXT-002);
   - calibrate confidence (EXT-003);
   - replace the placeholders (EXT-028);
   - check claims at the claim level, using Λ-Logos retrieval (EXT-010).
2. Make the Thermopylae and key guarantees real (EXT-004, EXT-005).
