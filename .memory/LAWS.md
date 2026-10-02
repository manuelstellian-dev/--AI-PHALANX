# LAWS — inviolable constraints

> Laws are not guidelines. Each law names its **enforcer** (a test, a CI gate or a tool); the
> validator fails if an enforcer does not exist (M06, M07). A law whose enforcement is partly human
> says so. Only the Commander adds, changes or retires a law (LAW-005).

## Commander's mandates

### LAW-001 · No capability is ever deleted
- **status:** active
- **cites:** IDN-002, INT-005
- **enforced_by:** tests/test_logos.py::test_external_backend_still_available_as_opt_in, tests/test_sparta.py::test_load_memory_without_quarantine_keeps_all, tests/test_vector_store.py::test_index_plaintext_opt_in_preserves_legacy_behaviour

Existing functionality is evolved, extended, made optional or quarantined, never removed. When
behaviour must change, the old behaviour stays reachable through an explicit option, and the
change is recorded as a decision. Precedents:
- the external embedding backend (DEC-012);
- `index_plaintext` (DEC-008);
- placeholder quarantine (DEC-013);
- `consecutive_breaches_required=1` (DEC-009).

### LAW-002 · Zero errors, zero warnings
- **status:** active
- **cites:** IDN-003
- **enforced_by:** .github/workflows/ci.yml, scripts/run_coverage.sh

The following must all pass with no findings before work is considered done:
- `ruff check .`
- `shellcheck scripts/*.sh`
- `python -m pytest -W error` (warnings are errors)
- `python -m mnemosyne check`

### LAW-003 · Documentation, memory and code stay synchronized; status is measured
- **status:** active
- **cites:** IDN-003, INT-005
- **enforced_by:** mnemosyne/validate.py, tests/test_mnemosyne.py::test_repository_memory_is_valid, tests/test_autonomous_audit_agent.py::test_repository_docs_carry_the_marker

Every fact in CURRENT_STATE is either a measure that is recomputed from the repository (M09) or
anchored to a checkpoint. Authoritative documents (PROJECT_STATUS.md, README, the master-plan
progress) are protected from heuristic overwrites (DEC-016).

### LAW-004 · Never skip a microstep
- **status:** active
- **cites:** INT-005
- **enforced_by:** .memory/PROTOCOL.md, tests/test_mnemosyne.py::test_checkpoint_refuses_invalid_memory

Every session follows the boot sequence (PRO-001), the work loop (PRO-002) and the close sequence
(PRO-003). A checkpoint cannot be created while the memory is invalid. Enforcement is partly
procedural.

### LAW-005 · No breaking change, and no change to intention or laws, without the Commander
- **status:** active
- **cites:** IDN-004
- **enforced_by:** .memory/PROTOCOL.md

Breaking changes to APIs, behaviour or data, and any change to INTENTION or LAWS, require explicit
authorization from the Commander. The authorization is recorded in DECISIONS. Agents surface such
changes as open decisions (PRO-005). Enforcement is procedural.

### LAW-006 · No external models and no external APIs at runtime
- **status:** active
- **cites:** INT-004
- **enforced_by:** tests/test_logos.py::test_no_external_ml_runtime_is_imported, mnemosyne/measures.py

Default code paths import no external ML runtime (torch, sentence-transformers, transformers) and
call no remote model API. `requirements.txt` declares none (measure `deps.external_ml_runtime`,
STATE-004). The embedding model is Λ-Logos (DEC-012). External backends exist only as explicit,
non-default opt-ins, preserved under LAW-001.

## Spartan laws (system behaviour)

### LAW-007 · SPARTA never invents
- **status:** active
- **cites:** INT-002
- **enforced_by:** tests/test_system_integrity.py::test_placeholders_never_answer_as_verified, tests/test_system_integrity.py::TestSpartaIntegration

An unverifiable query receives an honest "unknown", never an invented answer. Template
placeholders and unverified entries are never served as `[VERIFIED]` (DEC-013). Known gap: the
current hallucination check is lexical (EXT-010).

### LAW-008 · Commander supremacy; no self-modification of the core (Spartan Law I)
- **status:** active
- **cites:** IDN-004, INT-001
- **enforced_by:** tests/test_autonomous_audit_agent.py::test_authoritative_readme_is_not_overwritten, config/settings.yaml

The system does not rewrite its own core, laws or authoritative records without approval. The
settings `commander_supremacy` and `auto_modification_forbidden` declare this. Tools that write
documents must respect authoritative markers. Enforcement is partial: FFP self-repair actions must
stay bounded and reversible (EXT-015).

### LAW-009 · Air-gap by default
- **status:** active
- **cites:** INT-004
- **enforced_by:** tests/test_system_integrity.py::TestShieldBearerAirGap, tests/test_system_integrity.py::TestWeaponMasterAllowlist, Dockerfile

Strict air-gap mode is the default and external access is disabled. Domain allowlists match
exact domains or subdomains, never substrings. The container needs no network at runtime, and
its model is trained at build time from the project's own corpus.

### LAW-010 · Secrets never enter version control; every non-health endpoint requires authentication
- **status:** active
- **cites:** INT-001
- **enforced_by:** .gitignore, .dockerignore, tests/test_system_integrity.py::TestAuthentication, tests/test_vector_store.py::test_vault_requires_authentication

The following stay out of git and out of the image build context:
- `config/spartan_keys.yaml`
- `data/` and the vault keys
- `models/`

Tokens are compared in constant time and are never logged.

### LAW-011 · A compromise yields nothing, and destruction needs a sustained breach
- **status:** active
- **cites:** INT-003
- **enforced_by:** tests/test_system_integrity.py::TestThermopylaeSafety, tests/test_system_integrity.py::TestThermopylaeSingleSampler, tests/test_vector_store.py::test_no_plaintext_written_to_disk

When armed, Thermopylae destroys every configured secret: the master key file and every vault
path. It acts only after `consecutive_breaches_required` consecutive breaches (DEC-009).
Plaintext of encrypted data never reaches disk or the semantic index (DEC-008). Open gap: in
Docker, `./config` is mounted read-only (EXT-005).

## Memory laws

### LAW-012 · The memory graph is complete and connected
- **status:** active
- **cites:** INT-005
- **enforced_by:** mnemosyne/validate.py, tests/test_mnemosyne.py::test_repository_memory_is_valid

- Every repository file is mapped by an ATLAS entry (M08).
- Every entry traces back to INTENTION (M13).
- Every reference resolves (M04, M05).
- The checkpoint chain is intact (M10).

### LAW-013 · Tests are never skipped, disabled or weakened to obtain green
- **status:** active
- **cites:** IDN-003
- **enforced_by:** .github/workflows/ci.yml, .memory/PROTOCOL.md

A failing test is fixed at its root cause. A test assertion may change only when it encoded a
defect. Examples: the plaintext-fallback leak, the 500-concept count that included placeholders,
and the mislabelled harmonic mean. The reason is recorded in the commit and in DECISIONS.

### LAW-014 · Every vector is traceable to the model that produced it
- **status:** active
- **cites:** INT-004
- **enforced_by:** tests/test_logos.py::TestVectorStoreIntegration

Stored embeddings record the model ID (family plus fingerprint, ONT-015). A model change marks the
stored vectors stale until the vault is re-indexed (PRO-006, DEC-017).
