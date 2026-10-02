# ΛΕΩΝΙΔΑΣ-AI PHALANX — Project Status (Authoritative)

**ΜΟΛΩΝ ΛΑΒΕ** — *"Come and Take Them"*

> **This file is the single source of truth for the project's state.**
> Every number below was measured from the code, not copied from earlier reports.
> Older audit and status reports in the repository root are **historical snapshots** (see [Document Map](#10-document-map)).
>
> **Verified:** 2026-10-02 — branch `claude/keen-dirac-lvnjul`, Python 3.11.
> **Next actions:** [BACKLOG.md](BACKLOG.md)

---

## 1. The Object — what is being built

ΛΕΩΝΙΔΑΣ-AI PHALANX is an **autonomous, sovereign AI decision core** for high-stakes environments (military, medical, critical infrastructure). Three ideas define it:

1. **Spartan military architecture** — `Λ-Core → Phalanx → Hoplites`.
   - **Λ-Core**: `LeondasBrain` runs a homeostasis loop (dS/dt = 0) paced by the Autonomous Spartan Time
     `Λ-TAS = T₁·ln(U+1) / (1 − 1/(k·P))` (seconds), where **P** (parallelism) comes from Helot and
     **U** (universe expansion) from the `CommandProcessor` (Λ-Möbius Engine) and Agoge.
   - **Phalanx** (internal control): Helot (resources, survival probability), Agoge (adaptation),
     Krypteia (silent threat watch), Thermopylae (controlled self-destruction).
   - **Hoplites** (action): Spartan Guard (AES-256-GCM), Shield Bearer (air-gap), Battle Oracle (risk),
     Weapon Master (controlled external access), Messenger (encrypted communications).
   - **Spartan Laws**: Commander supremacy, no self-modification, mandatory air-gap; priority order
     threat neutralization → data integrity → homeostasis → adaptation.
2. **SPARTA** — an *epistemic fortress* against hallucination: answers are built by logical traversal of a
   curated Foundation of verified concepts (16 fields each), never by token prediction; unknowns are
   answered honestly. Seven **Λ-Modules** (Identity, Pattern, Meta, Guide, Affect, Reflect, Zero) are
   specified to extend it.
3. **Temporal compression** — concepts extracted from "Omega-AIOS" and *Spartanized* (extract and
   transform, never combine): Kronos-Arbiter, Phalanx-Executor, Λ-Möbius, Fractal Flux Pipeline.

4. **Sovereignty**: no external models or APIs. The embedding model, **Λ-Logos**, is built in this
   repository and trained on the project's own corpus.
5. **Continuity**: the project carries a persistent, executable memory, **`.memory/`**, which
   Mnemosyne validates. That memory is the canonical source for intention, laws, decisions and state.

Future capabilities: post-quantum cryptography, eBPF kernel monitoring, a federated Phalanx mesh,
and an immutable audit ledger.

> The compact, machine-checkable form of this whole document is `.memory/`. Start any session
> with `python -m mnemosyne boot`.

## 2. Genesis and history

| Date (2025) | PRs | Milestone |
|---|---|---|
| Nov 2 | #1 | Scaffold: Core, Phalanx, Hoplites, FastAPI, Docker |
| Nov 2 | #2 | SPARTA specification (5 docs, ~5,100 lines) |
| Nov 2 | #3 | First repository audit |
| Nov 2 | #4 | Temporal Compression Master Plan |
| Nov 2 | #5–#6 | Kronos-Arbiter, Phalanx-Executor, Task-Scheduler |
| Nov 2 | #7–#9 | Test-coverage campaign (221 → 326 tests) |
| Nov 2–3 | #10–#11 | Λ-Möbius Engine, Fractal Flux Pipeline in LeondasBrain |
| Nov 3 | #12 | RAG Vectorial vault |
| Nov 3 | #13–#16 | SPARTA Foundation implementation; knowledge base 44 → 132 → 308 → 500 concepts |
| Nov 4 | #17–#19 | Three documentation-only audit rounds |
| 2026 Oct 2 | — | Forensic audit and integrity remediation (this document) |
| 2026 Oct 2 | — | Sovereignty and memory: Λ-Logos replaces the external model; 80 placeholder concepts quarantined; `.memory/` and Mnemosyne |

All code from #1–#19 was authored by an AI coding agent and merged by the project owner. The history is
linear and never rewritten. The last three PRs before this audit added documentation only. Their status
figures ("77.8% complete", "PRODUCTION READY") came from `autonomous_audit_agent.py`, which counts a
component as 100% done when its file exists with more than 50 lines. That metric never checked behaviour.

## 3. Architecture as implemented

```
HTTP :7300 ──► FastAPI (api/server.py) ── Bearer auth (constant-time) on all routes except /health
                 │
                 ├─ /api/v1/health, /command/*, /metrics*, /lambda-mobius
                 ├─ /api/v1/vault/*    ──► SpartanVault (Fernet + RAG index)       [auth]
                 └─ /api/v1/sparta/*   ──► SpartaRuntime (Foundation/Bridge/Generator) [auth]
                 │
   embeddings ───┴─► Λ-Logos (logos/, own model; frozen artifact models/logos-v1.npz)
   memory ─────────► .memory/ (11 typed files) ◄── Mnemosyne (validate · checkpoint · recall)
                 │
   lifespan ─────┼─► LeondasBrain.homeostasis_loop  (Λ-TAS from Helot P + CommandProcessor U)
                 ├─► FractalFluxPipeline.run_forever (control.ffp.enabled)
                 └─► Krypteia monitoring thread
                 │
   CommandProcessor (Λ-Möbius routing): status, analyze_risk, encrypt_data,
                    check_airgap, send_message, train_agoge, sparta_query
```

Every module receives **its own section** of `config/settings.yaml` (`phalanx.*`, `hoplites.*`, `control.*`,
`vault.*`); flat legacy configs remain accepted.

## 4. Component maturity (verified)

Legend: **Functional** — real behaviour, tested · **Simulated** — runs, but core logic is a placeholder or random ·
**Planned** — specified, no code.

| Component | Maturity | Evidence / gap |
|---|---|---|
| LeondasBrain (homeostasis, Λ-TAS) | Functional | P from Helot, U from CommandProcessor, sleeps Λ-TAS seconds |
| CommandProcessor | Functional | 7 commands incl. `sparta_query` |
| Helot | Functional | psutil metrics, P factor, survival probability; GPU/NPU load simulated |
| Agoge | **Simulated** | adaptation uses `random.uniform(0.8, 1.2)` |
| Krypteia | **Simulated** | network/process/file-integrity checks are empty placeholders |
| Thermopylae | Functional | armed flag, sustained-breach gate, destroys keys + vault paths |
| Spartan Guard | Functional | AES-256-GCM; master key from `spartan_keys.yaml` / `SPARTA_MASTER_KEY` |
| Shield Bearer | Functional | strict/permissive air-gap (loopback-aware), firewall probe |
| Battle Oracle | **Simulated** | rule-based threat level; confidence and Monte Carlo are random |
| Weapon Master | **Simulated** | allowlist is real; HTTP calls return placeholder data |
| Messenger | Functional | encryption via Spartan Guard; in-memory only |
| Kronos-Arbiter / Λ-Möbius | Functional (model) | formulas implemented and tested; predictions not validated against measurements |
| Fractal Flux Pipeline | Partly simulated | scan/detect/quarantine real; heal/reinvest only log |
| Phalanx-Executor / Task-Scheduler | Functional | ProcessPool execution, dependency levels |
| SpartanVault + Vector Store | Functional | Fernet, persisted key, redacted index, JSON persistence |
| SPARTA Foundation / Bridge / Generator | Functional | exposed via API and command; matching is lexical (see Backlog) |
| SPARTA knowledge base | Functional, **integrity issues** | 500 concepts on disk; **80 template placeholders quarantined** (were served as `[VERIFIED]`), leaving 420 active in 22 domains; 224 dangling references among active concepts; confidences all in [0.95, 1.0] |
| Λ-Logos (own embedding model) | Functional | NumPy and SciPy only; benchmark MRR 0.690 (lexical baseline 0.527); ~30 ms per embedding |
| `.memory/` + Mnemosyne | Functional | 138 entries, 615 typed edges, 0 validation errors; hash-chained checkpoints; Λ-Logos recall |
| Λ-Modules (7) | **Planned** | full specification in `docs/sparta/SPARTA_LAMBDA_MODULES.md` |
| PQC, eBPF, Federated mesh, Ledger | **Planned** | `ADVANCED_CAPABILITIES.md`, `MISSING_FEATURES.md` |
| Audit tools | Functional | `audit_analyzer.py` tested (98%); `autonomous_audit_agent.py` 25% — only its doc-protection guard is tested |

## 5. Quality gates (measured)

| Gate | Result |
|---|---|
| Tests | **613 passed**, 0 failed |
| Memory | `python -m mnemosyne check`: 0 errors (references, enforcers, ATLAS coverage, measured facts, hash chain) |
| Sovereignty | No external ML runtime: the full suite passes in a clean environment without torch or sentence-transformers (350 MB instead of 5.9 GB) |
| Warnings | **0** (`pytest -W error`) |
| Lint | **0** findings (`ruff check .`) |
| Shell scripts | **0** findings (`shellcheck scripts/*.sh`), `bash -n` clean |
| YAML / Compose | all parse; `docker compose config` valid |
| Coverage | **87%** overall; `logos/` and `mnemosyne/` ~98%; `autonomous_audit_agent.py` 25% |
| CI | Workflow defined (ruff, shellcheck, tests, Docker build + health check). **First runs were never executed**: GitHub assigned no runner (`runner_id 0`, no steps), which points to an account-level Actions restriction. The gates above were run locally |
| Container | Image layout verified by booting the server from exactly the `COPY`'d tree. A full `docker build` was blocked in the audit sandbox by network policy (`deb.debian.org` 403) |

The authoritative test count is the `tests.functions` measure in `.memory/CURRENT_STATE.md`
(STATE-002). Mnemosyne recomputes it on every check.

Source size: 11,097 lines of Python (excluding tests) and 10,145 lines of tests.

## 6. Configuration reference (keys the code reads)

| Key | Effect |
|---|---|
| `auth.auth_token` (env `SPARTA_AUTH_TOKEN` wins) | API bearer token; default token logs a warning |
| `phalanx.helot.resource_thresholds.*` | survival-probability penalties |
| `phalanx.agoge.learning_rate` | adaptation step |
| `phalanx.thermopylae.survival_threshold` | critical threshold (also used by Λ-Core) |
| `phalanx.thermopylae.thermopylae_armed` | allows automatic destruction |
| `phalanx.thermopylae.consecutive_breaches_required` | sustained-breach gate (3) |
| `phalanx.thermopylae.keys_path` / `vault_path` / `base_path` | destruction targets; `keys_path` is also where Spartan Guard reads the master key |
| `hoplites.shield_bearer.airgap_mode`, `allowed_connections` | air-gap policy |
| `hoplites.weapon_master.external_access_enabled`, `allowed_domains` | external access |
| `hoplites.battle_oracle.npu_tops` | reported NPU allocation |
| `control.ffp.enabled` | start the Fractal Flux Pipeline with the server |
| `vault.storage_path`, `vault.index_plaintext` | vault location and index policy |
| env `SPARTA_MASTER_KEY`, `SPARTA_VAULT_KEY` | key overrides |
| env `LOGOS_MODEL_PATH` | location of the Λ-Logos artifact (default `models/logos-v1.npz`) |

At least 60 of the 89 leaf keys in `settings.yaml` are not read by any code. They fall into two groups:
- **Declarative:** the laws and the NPU/VRAM allocation tables.
- **Promised behaviour that is not implemented:** `security.*`, `logging.*`, `api.*`, `auth.token_expiry_hours`, and the retention and queue limits.

See BACKLOG B-07.

## 7. Security model and known limitations

**In place**
- Bearer authentication on every route except `/health`.
- Constant-time token comparison; no token fragments in logs.
- AES-256-GCM in Spartan Guard, using a persistent master key.
- Vault: Fernet encryption. Encrypted entries appear in the semantic index only as `[ENCRYPTED]`, and plaintext is never written to disk. The key survives restarts.
- Thermopylae requires a sustained breach.
- Air-gap and domain allowlists use exact or subdomain matching.
- No external model or API: Λ-Logos is trained into the image at build time, so the container needs no network at runtime.

**Known limitations** (tracked in BACKLOG)
- The vault key is stored beside the ciphertext unless `SPARTA_VAULT_KEY` is set, and the vault uses Fernet (AES-128) rather than AES-256 (B-04).
- Embeddings of encrypted entries remain in the index and can leak semantic similarity (B-04).
- CORS allows `*` with credentials, there is no token expiry and no rate limiting (B-06).
- Compose mounts `./config` read-only, so Thermopylae cannot destroy the keys file inside the container (B-05).
- SPARTA's hallucination check is lexical: it verifies that known concepts are *mentioned*, not that a claim is *true* (B-10).

## 8. Remediation log (2026-10-02 audit)

| # | Defect found | Resolution |
|---|---|---|
| 1 | Docker image omitted `control/`, `vault/`, `sparta/`, `parallel_execution/` → `ModuleNotFoundError` | All packages copied; CPU torch; model pre-baked; CI builds and health-checks the image |
| 2 | Every module received the root config → all per-module settings ignored (e.g. `thermopylae_armed`) | Section wiring via `get_section`; regression tests |
| 3 | `auth.auth_token` never read; non-constant-time compare; token prefix logged | `get_expected_token`, `hmac.compare_digest`, no token logging |
| 4 | `spartan_keys.yaml` written by `generate_keys.py` but never read | `load_master_key_hex` feeds Spartan Guard |
| 5 | Vault plaintext returned and persisted regardless of `decrypt`; key never reloaded (data lost on restart); vault API unauthenticated | Redacted index, key resolution chain, router-level auth |
| 6 | Pickle loaded from disk (code execution on tampered file) | JSON with embeddings is primary; pickle fallback only |
| 7 | Thermopylae: single spike could trigger; CI-runner base path; targeted `data/encrypted_vault` while vault lived in `data/vault` | Sustained-breach gate, repo-root default, list of vault paths from one config source |
| 8 | Λ-TAS used configured cores instead of Helot P; sleep used `1/Λ-TAS` contrary to spec | P/U interconnection; sleeps Λ-TAS seconds |
| 9 | Helot blocked the event loop 100 ms per sample | `asyncio.to_thread` |
| 10 | FFP never started; uptime always 0 | Started in lifespan, stopped on shutdown; `start_time` recorded |
| 11 | SPARTA unreachable from the system | `SpartaRuntime`, `/api/v1/sparta/*`, `sparta_query` command |
| 12 | Shield Bearer counted loopback as violations; permissive mode rejected everything | Loopback-aware; string allowlist matching |
| 13 | Weapon Master substring allowlist (`evil-example.com` passed) | Exact-or-subdomain matching |
| 14 | `/metrics` returned a JSON-encoded string (Prometheus could not scrape) | `text/plain` exposition |
| 15 | Kronos ignored `amdahl_fraction` | Amdahl upper bound applied |
| 16 | 101 lint findings; empty and state-leaking tests; uid- and timing-fragile tests | Lint 0; tests given real assertions and made deterministic |
| 20 | `autonomous_audit_agent.py` would overwrite corrected status with its file-length metric | Documents marked `<!-- status:authoritative -->` are skipped unless `--force-doc-update`; 5 tests |
| 21 | `T_Λ^Hybrid` labelled "harmonic mean" but is half of it; doc examples and Λ-Möbius API example (port, path, auth) wrong | Labels, examples and endpoint docs corrected; formula intent is an open owner decision (B-17) |
| 22 | Docs described behaviour that did not exist (`start_homeostasis()`, vault env vars, "audit trail complet") | Corrected to match code |
| 23 | Vault depended on an external pretrained model (HuggingFace download, torch, 5.9 GB), against the air-gap | Replaced by Λ-Logos, our own model; the external backend kept as a lazy opt-in |
| 24 | 80 of 500 SPARTA concepts were numbered templates ("Epistemic concept N …", confidence 0.97) served as `[VERIFIED]` | Quarantined on load (file untouched, opt-out flag); SPARTA now answers from real concepts |
| 25 | Project knowledge was scattered prose that could drift silently | `.memory/` graph with executable laws, measured state and hash-chained checkpoints; Mnemosyne in CI |
| 26 | Thermopylae counted breaches only on breach ticks and from two loops: recoveries never reset it, so 4 non-consecutive breaches destroyed the data | Single-sampler rule (DEC-019); the regression test fails on the pre-fix code |
| 17 | Shell: test menu ran a non-existent file; unreachable dependency check; 4 ShellCheck findings | Fixed; ShellCheck clean |
| 18 | `prometheus.yml` used removed `bearer_token`; obsolete Compose `version` | Updated |
| 19 | README claimed Python 3.8+; current dependencies require ≥ 3.10 | Docs and installer enforce 3.10+ |

No capability was removed: legacy behaviours are kept as explicit options. Examples are `index_plaintext=True`, a flat config dict, a single-string `vault_path`, and `consecutive_breaches_required=1`.

## 9. File inventory by type

| Type | Count | Role | Requirements honoured |
|---|---|---|---|
| Python `.py` | 73 (55 runtime/tools/example, 18 under `tests/`) | runtime packages, tests, audit tools, example | ruff-clean, typed signatures, 3.10+ |
| Markdown `.md` | 44 (incl. 12 in `.memory/`) | memory graph, vision, specifications, guides, historical audits | `.memory/` validated by Mnemosyne; authoritative vs historical separated |
| Shell `.sh` | 3 | install, activate, coverage | `set -e` correctness, ShellCheck-clean |
| YAML `.yaml/.yml` | 4 | settings, Prometheus, Compose, CI | parse-validated; keys mapped in §6 |
| JSONL | 1 (+1 `.backup`) | SPARTA knowledge base (500 concepts, 80 quarantined; backup = 44-concept phase-1 snapshot) | 16-field schema validated on load |
| Text `.txt` | 2 | `requirements.txt`, `AUDIT_DELIVERABLES.txt` (historical) | — |
| Docker | `Dockerfile`, `.dockerignore`, Compose | container build and stack | build context excludes secrets |
| Other | `.gitignore`, `.coveragerc`, `LICENSE`, key template | repository hygiene, MIT licence | `spartan_keys.yaml` and data are git-ignored |

**No Rust, C/C++ or JSON configuration files exist in the repository.** The vision does not currently call for them. eBPF monitoring (B-24) would be the first place a C component appears.

## 10. Document map

**Canonical memory (machine-checked)**
- [.memory/](.memory/README.md): intention, identity, laws, ontology, decisions, atlas, state,
  checkpoints, journal, extensions and protocol

**Authoritative (kept in sync with code)**
- [PROJECT_STATUS.md](PROJECT_STATUS.md)
- [BACKLOG.md](BACKLOG.md)
- [README.md](README.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [QUICKSTART.md](QUICKSTART.md)
- [docs/RAG_VECTORIAL.md](docs/RAG_VECTORIAL.md)
- [docs/LAMBDA_MOBIUS.md](docs/LAMBDA_MOBIUS.md)
- [docs/sparta/](docs/sparta/README.md)

**Architecture reference (derived)**
- [docs/SUPREME_SPECIFICATION.md](docs/SUPREME_SPECIFICATION.md): axioms, strata, flows, equations E1–E25, gap register, derived requirements and optimality theorem. Ratification pending: DEC-021

**Vision and specification (design intent, not status)**
- [ADVANCED_CAPABILITIES.md](ADVANCED_CAPABILITIES.md)
- [TEMPORAL_COMPRESSION_MASTER_PLAN.md](TEMPORAL_COMPRESSION_MASTER_PLAN.md)
- [docs/sparta/SPARTA_LAMBDA_MODULES.md](docs/sparta/SPARTA_LAMBDA_MODULES.md)

**Historical snapshots (November 2025; superseded by this file)**
- `AUDIT_REPORT.md`, `AUDIT_SUMMARY.md`, `AUDIT_SUMMARY_VISUAL.md`
- `AUDIT_CHANGELOG.md`, `AUDIT_AGENT_CHANGELOG.md`, `AUDIT_DELIVERABLES.txt`
- `FINAL_AUDIT_SUMMARY.md`, `FINAL_COMPREHENSIVE_AUDIT.md`, `COMPLETE_SYSTEM_AUDIT.md`
- `COMPLETE_IMPLEMENTATION_STATUS.md`, `PROGRESS_AUDIT.md`, `STATUS_REPORT.md`
- `PHASE4_COMPLETION_REPORT.md`, `MISSING_FEATURES.md`, `TEST_COVERAGE.md`
- `COMPATIBILITY_MATRIX.md`, `SPARTA_FOUNDATION.md` (root stub; the full version is in `docs/sparta/`)

---

**ΜΟΛΩΝ ΛΑΒΕ** ⚔️
