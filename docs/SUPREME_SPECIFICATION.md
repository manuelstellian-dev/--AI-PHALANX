# ΛΕΩΝΙΔΑΣ-AI PHALANX — Supreme Version Specification

**ΜΟΛΩΝ ΛΑΒΕ** — *"Come and Take Them"*

| | |
|---|---|
| **Revision** | 1.0 — 2026-10-02 |
| **Basis** | Commit `7cf4cb8` + this revision (branch `claude/keen-dirac-lvnjul`), checkpoint chain `.memory/CHECKPOINT.md` |
| **Scope** | Every stratum, flow, equation, invariant, module, interface, data structure, pathway and storage lifecycle of the system, plus the derived completion of every gap |
| **Authority** | Architecture reference. Items marked ⚖ change specified behaviour and take effect only on Commander ratification (`.memory` LAW-005) |

---

## 0. Method and chain of custody

Every statement in this document is one of the following:

| Mark | Meaning | Evidence carried |
|---|---|---|
| ✅ | **Implemented**: the code behaves as stated | `[C file:line]` source location, and/or a test |
| 🔧 | **Fixed in this revision**: a defect that violated an existing law, corrected and regression-tested | test name; failure demonstrated on the pre-fix code |
| ⟐ | **Derived requirement (DR)**: a gap or contradiction whose resolution follows necessarily from the axioms and a computed result | axiom(s) + result `R#` |
| ⚖ | **Commander decision (CD)**: the derivation fixes the *form*; a constant or a behaviour change needs ratification | derivation + options |
| ✖ | **Rejected**: a candidate addition that fails the necessity test (§7) | the reason |

Notation:
- `[C path:line]` is a code location.
- `[M ID]` is a `.memory` entry.
- `R#` is a result computed for this specification. The computation is reproducible from the code at the basis commit.
- 𝟙[·] is the indicator function, and `clip_[a,b](x) = min(b, max(a, x))`.

**Admission rule for additions (the necessity test).** A module, layer or mechanism is admitted
only if all three conditions hold:
1. **Logical:** without it, some axiom A1–A8 has no enforcing mechanism.
2. **Mathematical:** a computed result shows that the existing mechanism is insufficient.
3. **Necessary:** no smaller change satisfies conditions 1 and 2.

---

## 1. Axioms

The system is the unique consequence of eight axioms. Each is extracted from the Commander's
intention and laws, not invented.

| # | Axiom (formal statement) | Source |
|---|---|---|
| **A1** | *Truth.* Every emitted claim carries a confidence that is a **guaranteed lower bound** on its correctness. When no bound ≥ θ_v can be guaranteed, the output is `UNKNOWN`. | [M INT-002], [M LAW-007] |
| **A2** | *Homeostasis.* System state x(t) is held in a viable set 𝒱 by a closed feedback loop: measure → decide → act. | [M INT-003], ARCHITECTURE "dS/dt=0" |
| **A3** | *Compromise yields nothing.* On a **sustained** breach, every secret becomes irrecoverable. A transient must never trigger it. | [M LAW-011] |
| **A4** | *Sovereignty.* No external model, external API or network dependency at runtime. Air-gap by default. | [M INT-004], [M LAW-006], [M LAW-009] |
| **A5** | *Command.* The Commander is the sole authority over intention, laws and breaking changes. The system never self-modifies its core. | [M LAW-005], [M LAW-008] |
| **A6** | *Evidence and continuity.* Every state is measurable, recorded, traceable to intention, and verifiable after the fact. | [M INT-005], [M LAW-003], [M LAW-012], [M LAW-014] |
| **A7** | *Preservation.* Capabilities evolve; they are never deleted. | [M LAW-001] |
| **A8** | *Integrity of quality.* Zero errors, zero warnings; tests are never weakened. | [M LAW-002], [M LAW-013] |

---

## 2. Stratified architecture

The system has eight strata. Each stratum consumes only the outputs of the strata below it, except
for the explicitly declared feedback edges (⟲).

```
 S7  GOVERNANCE & MEMORY   .memory/ ◄─► Mnemosyne (validate · checkpoint · recall)        A5 A6 A7 A8
 ─────────────────────────────────────────────────────────────────────────────────────────────────────
 S6  COMMAND INTERFACE     FastAPI :7300 (auth) ──► CommandProcessor (7 commands)          A5
 ─────────────────────────────────────────────────────────────────────────────────────────────────────
 S5  ACTION                Spartan Guard · Shield Bearer · Battle Oracle · Weapon Master · Messenger
 ─────────────────────────────────────────────────────────────────────────────────────────────────────
 S4  KNOWLEDGE             SPARTA (Foundation · Bridge · Generator · Λ-Modules⟐) ◄── Λ-Logos ──► Vault   A1 A4
 ─────────────────────────────────────────────────────────────────────────────────────────────────────
 S3  TEMPORAL CONTROL      Kronos-Arbiter · Λ-Möbius · Fractal Flux Pipeline                A2
 ─────────────────────────────────────────────────────────────────────────────────────────────────────
 S2  REGULATION            Λ-Core homeostasis loop (Λ-TAS) ──► Thermopylae FSM               A2 A3
 ─────────────────────────────────────────────────────────────────────────────────────────────────────
 S1  PERCEPTION            Helot (resources, P, S) · Krypteia (threats) · Shield (network)   A2
 ─────────────────────────────────────────────────────────────────────────────────────────────────────
 S0  SUBSTRATE             CPU / RAM / disk / network (psutil) · filesystem · keys · model artifact
```

Feedback edges:
- ⟲1 S2 → S1: the loop period Λ-TAS sets the sampling rate of S1.
- ⟲2 S3 → S3: T_Supreme sets the FFP cycle period.
- ⟲3 S6 → S2: the Agoge factor and the task load set U, and so Λ-TAS.
- ⟲4 S4/S5 → S1 ⟐: outcomes feed Agoge's learning signal (DR-9).
- ⟲5 S3 → S0 ⟐: FFP actuators act on the plant (DR-8).
- ⟲6 S7 → all: laws and decisions constrain every change.

### 2.1 Stratum contracts

| Stratum | Inputs | Transformation | Outputs | State | Status |
|---|---|---|---|---|---|
| S0 | hardware counters, files | none (the plant) | `cpu%`, `mem%`, `disk%`, cores, connections, bytes | the physical world | ✅ |
| S1 Helot | S0 counters, `resource_thresholds` | E3 (P), E4 (S) | `resources{…, parallelism_factor}`, S | `last_resources`, S | ✅ [C phalanx/helot.py:35-64] |
| S1 Krypteia | reported threats | E10 (threat level) | `threat_level` ∈ {low, medium, high, critical} | threat list | ✅ API · ⟐ detectors (DR-10) |
| S1 Shield | `psutil.net_connections` | predicate E14 | `airgap_active` ∈ {T, F} | — | ✅ |
| S2 Λ-Core | P, U | E1 (Λ-TAS), E5 (FSM input) | sleep period; Thermopylae observations | `lambda_tas`, `is_running` | ✅ 🔧 |
| S2 Thermopylae | S at every tick | E5 FSM | destruction or no-op | (armed, n, activated) | ✅ 🔧 |
| S3 Kronos | T_seq, N, Θ, Λ, η, f | E6 | T_par, speedup, efficiency | history (≤ 100) | ✅ |
| S3 Λ-Möbius | k, P, U | E7 | T_wrap … T_supreme, state | history (≤ 100) | ✅ (⚖ CD-3) |
| S3 FFP | S1 state, Agoge | 6-phase cycle (F4) | anomalies, (⟐ actions) | `cycle_count`, `running` | ✅ scan/detect · ⟐ heal (DR-8) |
| S4 SPARTA | query text | E11–E13 | response, confidence, sources, chain | Foundation (420 active + 80 quarantined) | ✅ (⚖ CD-4) |
| S4 Λ-Logos | text | E15–E18 | 384-d unit vector | frozen artifact (fingerprint) | ✅ |
| S4 Vault | id, text, metadata | E19, Fernet | encrypted store + index | `encrypted.json`, `vector_store.json`, key | ✅ |
| S5 Hoplites | commands | E9, E14, AES-GCM | analyses, ciphertexts, messages | in-memory histories | ✅ / simulated (see §6) |
| S6 API | HTTP + bearer token | auth E20 → route | JSON / Prometheus text | — | ✅ |
| S7 Mnemosyne | `.memory/*.md`, repository tree | E21–E23, rules M01–M13 | report, checkpoint, recall | hash chain | ✅ |

---

## 3. Operational flows

Each flow lists its trigger, its ordered steps, its state transitions and its failure behaviour.

### F1 — System boot (`api.server.lifespan`) ✅
1. `app.state.start_time ← now` [C api/server.py:lifespan].
2. `config ← load_config()`. If settings are missing, use the built-in defaults.
3. If `get_expected_token(config) = DEFAULT`, log a warning (A5 hardening: CD-6).
4. `initialize_system(config)`:
   - Brain, then Kronos(n_cores).
   - Phalanx: Helot, Agoge, Krypteia and Thermopylae, each with its own config section ([M DEC-007]).
   - `krypteia.start_monitoring()` (daemon thread, 5 s period).
   - Guard (master key from `spartan_keys.yaml`, else `SPARTA_MASTER_KEY`, else an ephemeral key), then Shield, Oracle, Weapon and Messenger.
   - CommandProcessor({phalanx, hoplites, sparta}).
   - `brain.command_processor ← processor`.
5. Spawn the tasks `homeostasis_loop` (F2) and, if `control.ffp.enabled`, `ffp.run_forever` (F4).
6. On shutdown, in order: `stop_ffp` → `brain.shutdown` → `krypteia.stop_monitoring` → cancel the tasks.

Failure behaviour: if SPARTA fails to load, the system still boots and `sparta_query` returns
`success: false`. That is a graceful degradation, consistent with A1, since it returns no answer
rather than a wrong one.

### F2 — Homeostasis cycle (period Λ-TAS) ✅ 🔧
```
loop while is_running:
    S   ← Helot.get_survival_probability()         # samples S0; updates last_resources (P)
    if S < θ_T: log warning
    Thermopylae.observe(S)                         # EVERY tick (single-sampler rule, DEC-019)
    T   ← Λ-TAS(P = last_resources.P, U = processor.U)     # E1
    sleep(T)
on exception: log; sleep 1 s; continue           # the loop is never terminated by a fault
```
🔧 **Defect fixed (G-01).** Before this revision, the Thermopylae observation was fed *only on breach
ticks*, and the FFP fed the same counter a second time. Recoveries therefore never reset the
counter: four non-consecutive breaches **activated destruction**. This is demonstrated on the pre-fix
code by `tests/test_system_integrity.py::TestThermopylaeSingleSampler`.

### F3 — Thermopylae finite-state machine ✅ 🔧
States: `(armed ∈ {0,1}, n ∈ ℕ, activated ∈ {0,1})`. `activated = 1` is **absorbing**.

| Event | Guard | Transition | Effect |
|---|---|---|---|
| observe(S) | S ≥ θ_T | n ← 0 | — |
| observe(S) | S < θ_T, n + 1 < N | n ← n + 1 | critical log |
| observe(S) | S < θ_T, n + 1 ≥ N, armed | n ← n + 1, activated ← 1 | destroy the keys file, then every vault path (F3a) |
| observe(S) | S < θ_T, n + 1 ≥ N, ¬armed | n ← n + 1 | "manual intervention" warning |
| arm / disarm | — | armed ← 1 / 0 | — |

F3a, the destruction order:
1. Overwrite the keys file with 1 MiB of random bytes, then unlink it.
2. `rmtree` each path in `vault_path`.

**Invariant I-T1:** destruction requires N consecutive observations below θ_T, made by a single
sampler. **Invariant I-T2:** activation is idempotent (the `protocol_activated` guard).

### F4 — Fractal Flux Pipeline cycle (period τ_ffp) ✅ / ⟐
1. **SCAN:** read Helot resources, S and the Krypteia level.
2. **DETECT:** emit anomalies `low_survival` (S < 0.95), `high_cpu` (> 90) and `high_memory` (> 90)
   [C control/fractal_pipeline.py:146-172]. ⟐ G-07: these thresholds must be the *same* ones Helot
   uses (DR-7).
3. **QUARANTINE:** if the brain is running, breach counting belongs to F2 (🔧 DEC-019). Otherwise
   (standalone mode) feed Thermopylae.
4. **HEAL:** ✅ logs only. ⟐ It must actuate (DR-8), which closes loop ⟲5.
5. **IMPROVE:** if the Agoge factor a < 1, recommend training.
6. **REINVEST:** ✅ logs only. ⟐ It must apply bounded, reversible actions (DR-8).
7. `sleep(τ_ffp)` (E8).

### F5 — Command processing ✅
`POST /api/v1/command`, then the bearer check (E20), then `CommandProcessor.process_command`, which
dispatches on `type` ∈ {status, analyze_risk, encrypt_data, check_airgap, send_message,
train_agoge, sparta_query}. An unknown type returns `success: false` plus the list of commands. An
exception returns `success: false, error`, and the route maps it to HTTP 500.
⟐ DR-2: the processor must increment `active_tasks` on entry and decrement it in `finally`, so that
U observes the load (G-03).

### F6 — SPARTA query ✅ (⚖ CD-4)
1. Extract concepts (E11) over the **active** Foundation only. Quarantined placeholders are
   invisible ([M DEC-013]).
2. If none are found, return the honest `UNKNOWN` response (`I don't know`, confidence 0).
3. Logical expansion: definition, formal statement, relations (the reasoning chain).
4. Confidence c ← aggregate(c_i): currently `min` (E12). ⚖ CD-4: change it to the Fréchet lower
   bound (E13).
5. `verified ← c ≥ 0.95`, then a tag ∈ {[VERIFIED], [HIGH CONFIDENCE], …}.
6. Bridge: `epistemic_status` ∈ {KNOWN, PARTIAL, UNKNOWN}.
7. The response carries {response, confidence, sources, reasoning_chain, verified, epistemic_status}.

### F7 — Vault operations ✅
- **Store:** `encrypt=True` produces Fernet(plaintext) stored in `encrypted_storage[id]`, and an index
  entry with **embedding = Λ-Logos(plaintext)** and **text = `[ENCRYPTED]`**.
- **Search:** cosine over the index. The plaintext is restored only when `decrypt = true` (and
  authenticated).
- **Save:** write `encrypted.json`, `vector_store.json` (with embeddings and `model_id`), the
  compatibility `vector_store.pkl`, and `encryption.key` (0600, unless the key came from the
  environment).
- **Load:** JSON first, pickle only as a fallback. Key resolution: `SPARTA_VAULT_KEY` →
  `encryption.key` → generate.
- **Reindex** (after a model change): re-embed every entry, using the decrypted plaintext for
  encrypted entries, then clear `stale`.

### F8 — Model lifecycle (Λ-Logos) ✅
`get_model()` loads `models/logos-v1.npz` **as-is** if it exists. Otherwise it trains on the corpus
(F8a) and saves. Retraining happens only through `python -m logos train --force` ([M PRO-006]) and
is followed by a vault `reindex()`. **Invariant I-L1:** every stored vector's `model_id` equals the
fingerprint of the model that produced it ([M LAW-014]).

F8a, the corpus: the 500 SPARTA concepts (flattened) plus every Markdown chunk (split by heading)
from the root, `docs/` and `.memory/`, in sorted file order. This makes the corpus deterministic.

### F9 — Memory session protocol ✅
- **Boot** ([M PRO-001]): `mnemosyne boot` → `mnemosyne check` → git state → `mnemosyne query`.
- **Work** ([M PRO-002]).
- **Close** ([M PRO-003]): all gates green → update STATE, DEC, ATLAS and EVT → `check` →
  commit → `checkpoint` → `check --strict` → commit → push.

---

## 4. Equations, derivations, invariants and computed results

### E1 — Autonomous Spartan Time (Λ-TAS) ✅ [C core/leonidasbrain.py:42-89]
$$
T(P,U) = \operatorname{clip}_{[0.1,\,10]}\!\left(\frac{T_1\,\ln(U+1)}{1-\frac{1}{kP}}\right),\qquad T_1=1\,\mathrm{s},\;k=100,\;kP>1
$$
For kP ≤ 1 the fallback is T = P/(1+U). This branch is unreachable for k ≥ 1, because P ≥ 1 (E3).

Derivatives on the unclamped domain:
$$
\frac{\partial T}{\partial U}=\frac{T_1}{(U+1)\left(1-\frac{1}{kP}\right)}>0,\qquad
\frac{P}{T}\frac{\partial T}{\partial P}=-\frac{1}{kP-1}
$$

**R1 (P-insensitivity).** The ratio T(P)/T(∞) = kP/(kP−1) ∈ (1, k/(k−1)]. For k = 100 the whole
influence of P is at most **1.01%**. The measured relative span over P ∈ [1, 64] is 0.99% for every
U tested. The documented purpose, that the rhythm "adjusts … based on available parallel processing
capacity" (ADVANCED_CAPABILITIES §I.1), is therefore **not realized**. This is contradiction G-02.

⚖ **CD-1 (derived form).** For P to modulate T by a factor r between P = 1 and P → ∞, k must
satisfy k/(k−1) = r, that is **k = r/(r−1)**. The design choice r = 2 gives k = 2, so
T(1) = 2·ln(U+1), T(2) = 1.33·ln(U+1), T(4) = 1.14·ln(U+1), and T(∞) = ln(U+1). The value of r is
the Commander's choice. The form k = r/(r−1) is forced.

### E2 — Universe expansion factor U ✅ (inputs ⟐) [C core/commandprocessor.py:32-48]
$$
U = \bigl(1 + n_{\text{tasks}} + \ln\max(1, V_{\text{MB}})\bigr)\cdot a
$$

**R2 (dead inputs).** `n_tasks` and `V_MB` are initialized to 0 [C core/commandprocessor.py:28-29]
and never updated, so U ≡ a. Since a changes only through `train_agoge`, U ≡ 1 in practice, and
**T ≡ ln 2 / (1 − 1/(100P)) ≈ 0.695 s**. That is a constant rhythm (G-03).

⟐ **DR-2.** `n_tasks` = number of in-flight commands (F5). `V_MB` = vault bytes / 2²⁰, refreshed at
each save. Both are the definitions the specification already states; only the wiring is missing.

### E3 — Parallelism factor P ✅ [C phalanx/helot.py:66-90]
$$
P = \max\!\bigl(1,\; 1 + c\,(1 - L/100) + 5g\bigr),\qquad c=\text{logical cores},\;L=\text{CPU \%},\;g\in[0,1]
$$
The domain is P ∈ [1, 1 + c + 5]. The GPU load g is configured, not measured (G-11, [M EXT-018]).

### E4 — Survival score S ✅ [C phalanx/helot.py:92-119]
$$
S = 1 - 0.10\,\mathbb 1[L>\theta_{cpu}] - 0.15\,\mathbb 1[M>\theta_{mem}] - 0.10\,\mathbb 1[D>\theta_{disk}],\quad (\theta_{cpu},\theta_{mem},\theta_{disk}) = (95,90,95)
$$

**R4 (lattice).** S ∈ {1, 0.90, 0.85, 0.80, 0.75, 0.65}. The clamp to [0, 1] never binds. For any
threshold θ_T ∈ (0.90, 1], the condition S < θ_T is equivalent to "at least one resource is critical".
The value 0.95 is therefore one representative of an equivalence class, not a calibrated probability.
S is a **severity score**. Calling it a probability is nominal until it is calibrated (G-11,
[M EXT-018]).

### E5 — Thermopylae persistence ✅ 🔧 (⚖ CD-2)
The input is one observation per F2 tick (period T from E1). Activation happens iff N consecutive
observations have S < θ_T and the protocol is armed. **Activation latency** after the first breach
sample is in [(N−1)T, NT). With N = 3 and T = 0.695 s, that is **≈ 1.39 s**.

**R5 (false-activation probability).** Model breach observations as Bernoulli(p) per tick. The
exact probability of at least one run of N in M ticks was computed by dynamic programming over the
current run length (M = 86 400/T = 124 337 ticks per day):

| p (fraction of critical samples) | P(activation within 1 day), N = 3 |
|---|---|
| 0.001 | 0.0001 |
| 0.01 | **0.116** |
| 0.05 | **1.000** |
| 0.10 | **1.000** |

Real load is positively autocorrelated, so these are *lower* bounds on the risk. Requiring 3 samples
over ≈ 1.4 s does not satisfy A3's "a transient must never trigger it".

⚖ **CD-2 (derived form).** Specify persistence as a **duration τ**, with N = ⌈τ/T⌉, chosen from a
false-activation budget α over a horizon H:
$$
M(1-p)\,p^{N} \le \alpha,\qquad M = H/T \;\Longrightarrow\; N_{\min} = \left\lceil \frac{\ln\bigl(\alpha / (M(1-p))\bigr)}{\ln p} \right\rceil
$$
For α = 10⁻⁶ per day, i.i.d. N_min = 6, 9 and 12 for p = 0.01, 0.05 and 0.10. Because the loads are
autocorrelated, τ must also exceed the load's autocorrelation time. Practical operating values are
τ ≥ 30–60 s. The value of α is the Commander's choice; the formula is forced.

### E6 — Kronos-Arbiter ✅ [C control/kronos_arbiter.py:185-336]
$$
s = \min\!\left(N\Theta\Lambda\eta,\; \frac{1}{(1-f) + f/N}\right),\qquad T_{par} = T_{seq}/s,\qquad \epsilon = s/N
$$
The defaults are Θ = 0.85, Λ = 0.95, η = 0.90, so s = 0.727·N. **Invariant I-K1:** s ≤ N.
**Invariant I-K2:** s ≤ the Amdahl bound for f < 1. With f = 1 the Amdahl cap is N, which
N·Θ·Λ·η never exceeds, so the bound is inactive.

### E7 — Λ-Möbius engine ✅ (⚖ CD-3) [C control/lambda_mobius.py:108-330]
$$
T_W = \frac{T_1}{1-\frac{1}{kP(1+\ln U)}},\quad T_M = \frac{T_1\ln U}{1-\frac{1}{kP}},\quad T_H=\frac{T_WT_M}{T_W+T_M},\quad T_B=\sqrt{T_WT_M}
$$
The arbiter selects WRAP if kP(1 + ln U) > 100, else UNWRAP if U > 1000, else STEADY. Then
T_S = T_W (WRAP), T_M (UNWRAP) or T_H (STEADY). The property ½·min(T_W, T_M) ≤ T_H < min(T_W, T_M)
holds, because T_H is half the harmonic mean ([M DEC-015]).

**R3 (degeneration).** For k = 100, P ≥ 1 and U > 1, the product kP(1 + ln U) exceeds 100, so the
arbiter **always selects WRAP**. This was verified over P ∈ [1, 64] and U ∈ [2, 5000]. Moreover
T_W ∈ [1.00001, 1.00594] s, so T_S ≡ T₁ = 1 s to within 0.6%. The five-layer engine, as
parametrized, is a constant (G-04).

⚖ **CD-3 (derived form).** *Reachability invariant:* every state of an arbiter must be reachable
on the operating domain 𝒟; otherwise the state is dead specification. On
𝒟 = [1, P_max] × [1, U_max], WRAP and STEADY are both reachable iff the threshold
κ ∈ (min_𝒟 kP(1 + ln U), max_𝒟 kP(1 + ln U)). Replace the literal 100 with κ = k·P_ref·(1 + ln U_ref)
at a reference operating point. This form is forced; the reference point is the Commander's choice,
together with the T_H intent ([M DEC-015]).

### E8 — FFP period ✅
$$\tau_{ffp} = \max\bigl(0.1,\; \min(T_S, 5)\bigr) \overset{R3}{\approx} 1.0008\ \mathrm{s}$$

### E9 — Battle Oracle ✅ (simulated parts marked) [C hoplites/battleoracle.py:67-110]
- threat = critical if σ > 0.8 or |F| > 5; high if σ > 0.6 or |F| > 3; medium if σ > 0.3 or
  |F| > 1; low otherwise.
- p_success = clip_[0,1]( R·(1 − 0.5C)·(1 − 0.3τ) ).
- `confidence ~ U(0.7, 0.95)` and the Monte Carlo `successes ~ Bin(n, 0.6)` are **random and ignore
  their inputs** (G-12, [M EXT-013]).

### E10 — Krypteia threat level ✅
Let n be the number of threats. Level = low if n = 0, medium if n < 3, high if n < 5, critical
otherwise. The detectors are empty (G-10).

### E11 — SPARTA concept extraction ✅ [C sparta/reflexive_generator.py:371-409]
A concept c matches query q iff `id(c)` (underscores read as spaces) ⊂ q, or
|W_def(c) ∩ W_q| ≥ max(2, ⌈0.3 · |W_def(c)|⌉) under whitespace tokenization. This is lexical; the
known limitation is G-08 ([M EXT-010]).

### E12 — Confidence aggregation (as implemented) ✅ [C sparta/reflexive_generator.py:88-91]
$$c_{\text{ans}} = \min_i c_i,\qquad \text{verified} \iff c_{\text{ans}}\ge 0.95$$

### E13 — Confidence aggregation (derived) ⚖ CD-4
An answer composed from concepts 1…n is correct only if **all** of them hold, so it is a
conjunction. Without an independence assumption, which no source licenses, the Fréchet bounds give:
$$
\max\!\Bigl(0,\; 1-\sum_i (1-c_i)\Bigr) \;\le\; \Pr\Bigl[\bigwedge_i \text{correct}_i\Bigr] \;\le\; \min_i c_i
$$

**R6.** E12 reports the **upper** bound, but A1 demands a **guaranteed lower bound**. Examples:
- 5 concepts at 0.97: E12 reports 0.97, but the guaranteed confidence is 0.85.
- 7 concepts at 0.95: E12 reports 0.95 and "verified", but the guaranteed confidence is 0.65.

The bridge's mean aggregation [C sparta/semantic_foundation.py:194-233] is weaker still. Hence the
derived law is
$$
c_{\text{ans}} = L_F(c_1,\dots,c_n) = \max\!\Bigl(0,\; 1-\sum_i (1-c_i)\Bigr)
$$

**Corollary (Λ-Guide is necessary).** To keep L_F ≥ θ_v = 0.95, the total doubt Σ(1 − c_i) ≤ 0.05.
An answer must therefore be built from the **minimal** sufficient set of high-confidence concepts,
and that is exactly the specified role of Λ-Guide (concept selection and scoring,
`docs/sparta/SPARTA_LAMBDA_MODULES.md`). Λ-Guide is not an enhancement: it is the optimizer that A1
requires, namely max L_F subject to covering the query. This is DR-11, which orders [M EXT-011].

Threshold unification (G-09): the thresholds 0.95, 0.80, 0.75 and 0.70 collapse to **one** verified
threshold θ_v applied to L_F, plus one refusal threshold θ_u below which the answer is `UNKNOWN`.
Every other number is a display tier. The values are calibrated under [M EXT-003].

### E14 — Network predicates ✅
- **Air-gap (strict):** active ⇔ the set of ESTABLISHED connections whose remote endpoint is not
  loopback is empty.
- **Permissive:** every such connection c satisfies c ∈ A, or remote(c) ∈ A, or host(c) ∈ A.
- **Domain allowlist:** d is allowed ⇔ ∃a ∈ A : d = a ∨ d ends with "." + a (case-folded, port
  stripped). An empty A means "allow all" while access is enabled, which conflicts with A4
  (G-13, [M EXT-016]).

### E15 — Λ-Logos feature map ✅ [C logos/tokenizer.py]
For feature f in group g ∈ {w, b, c} (word, bigram, char 3–5-gram), with weight w_g ∈ {1, 0.7, 0.35},
hash h(f) ∈ [0, F) and sign s(f) ∈ {±1} from BLAKE2b, and F = 2¹⁵:
$$
\varphi_j(x) = \sum_{f:\,h(f)=j} s(f)\, w_{g(f)}\,\bigl(1 + \ln \mathrm{tf}_f(x)\bigr)
$$
Signed hashing gives E[⟨φ(x), φ(y)⟩] = ⟨x, y⟩ (Weinberger et al., 2009).

**R7 (collision load).** The corpus has 101 798 distinct features in F = 32 768 buckets, so the
expected occupied buckets are F(1 − (1 − 1/F)ⁿ) ≈ 31 302, and **69.3%** of features share a bucket.
A measured sweep gave MRR 0.690 (F = 2¹⁵), 0.677 (2¹⁶) and 0.700 (2¹⁷). These differences are within
the 28-query benchmark's resolution of about 0.03. The collision load is **not** the binding
constraint, so enlarging F (2–4× memory) is ✖ rejected (§7).

### E16 — IDF and normalization ✅
$$
\mathrm{idf}_j = \ln\frac{1+N}{1+\mathrm{df}_j} + 1,\qquad \hat x = \frac{\varphi(x)\odot \mathrm{idf}}{\lVert \varphi(x)\odot \mathrm{idf}\rVert_2}
$$

### E17 — Latent projection (randomized SVD) ✅ [C logos/model.py:_randomized_svd]
With X ∈ ℝ^{N×F} (rows x̂), Ω ~ 𝒩(0, 1)^{F×(k+p)}, p = 10 and q = 4 power iterations:
1. Y = (XXᵀ)^q XΩ (re-orthonormalized at each step), then Q = qr(Y).
2. B = QᵀX = U_B Σ V_kᵀ.
3. The embedding is e(x) = normalize([x̂ V_k, 0_{d−k}]) with d = 384.

The sign convention makes the largest-magnitude loading of each axis positive, which makes training
deterministic. **R8 (energy).** Since rows are unit-norm, ‖X‖_F² = N, and the retained energy is
Σσ_i²/N = **0.599** (k = 384, N = 1 948, σ₁ = 8.27, σ_k = 1.03).

Untrained fallback (Johnson–Lindenstrauss): e(x) = normalize(Σ_j x̂_j r_j), with r_j ~ 𝒩(0, I_d/d)
seeded by (seed, j).

### E18 — Recall scoring ✅ [C mnemosyne/recall.py]
$$\mathrm{score}(q,e) = \alpha\cos\bigl(e_{sem}(q),e_{sem}(e)\bigr) + (1-\alpha)\cos\bigl(e_{lex}(q),e_{lex}(e)\bigr),\quad \alpha=0.5$$
Measured on the memory recall set: top-3 hits 8/10 and MRR 0.78, against 7/10 and 0.70 at α = 1.

Model quality, measured on the fixed benchmark: MRR 0.690, R@1 57%, R@5 82%, mean rank 16.5. The
lexical baseline scores 0.527, 43%, 61% and 40.

### E19 — Vault staleness ✅
`stale ⇔ entries ≠ ∅ ∧ stored_model_id ≠ None ∧ stored_model_id ≠ current_model_id`.

### E20 — Authentication ✅
`authorized ⇔ hmac.compare_digest(token, expected)`, where expected is the first non-empty value of
⟨env SPARTA_AUTH_TOKEN, auth.auth_token, auth_token, DEFAULT⟩. The comparison is constant-time.

### E21 — Repository tree hash ✅ [C mnemosyne/checkpoint.py]
$$
H_T = \mathrm{SHA256}\Bigl(\big\Vert_{f \in \mathcal F \setminus \{\texttt{CHECKPOINT.md}\},\ \text{sorted}} \; f \,\Vert\, \texttt{0x00} \,\Vert\, \mathrm{SHA256}(\text{content}_f) \,\Vert\, \texttt{\textbackslash n}\Bigr)
$$

### E22 — Checkpoint chain ✅
$$
h_i = \mathrm{SHA256}(\mathrm{id}_i \,|\, \mathrm{title}_i \,|\, \text{date} \,|\, \text{agent} \,|\, \text{commit} \,|\, H_T \,|\, \mathrm{prev}_i \,|\, \text{gates}),\qquad \mathrm{prev}_1 = \texttt{GENESIS},\ \mathrm{prev}_i = h_{i-1}
$$
Security note (chain of custody): the chain is **self-consistent**. An adversary who rewrites entry i
and recomputes h_i … h_n produces a valid-looking chain. Tamper-*evidence* therefore comes from
**anchoring**: the pushed git history and the commit field. An anchored copy reduces forgery to a
SHA-256 second preimage. ⟐ DR-14 (planned with [M EXT-026]): sign checkpoints with ML-DSA.

### E23 — Memory validity ✅
`valid ⇔ M01 ∧ … ∧ M13` (see `mnemosyne/validate.py`). M13 is connectivity: every non-checkpoint
entry lies in the connected component of the INTENTION nodes, in the undirected entry graph.

### E24 — Λ-Zero (specified, not implemented) ⚖ CD-5 [`docs/sparta/SPARTA_LAMBDA_MODULES.md`]
The specification gives Λ₀ = tanh(k₁·ℓ + k₂·χ − k₃·|θ̇|), with (k₁, k₂, k₃) = (1, 0.5, 0.3),
logic ℓ ∈ [0, 1] and creativity χ ∈ [0, 1]. The regimes are Λ₀ > 0.5 → LOGIC_DOMINANT and
Λ₀ < −0.5 → CREATIVE_DOMINANT.

**R9 (sign contradiction).**
1. ∂Λ₀/∂χ = k₂·sech²(·) > 0, so **more creativity pushes toward LOGIC_DOMINANT**.
2. CREATIVE_DOMINANT requires k₁ℓ + k₂χ − k₃|θ̇| < −atanh(0.5) = −0.549. Since ℓ, χ ≥ 0, that
   forces |θ̇| > 1.83: **only instability can produce "creativity"**.

The specification thus contradicts its own regime semantics, and it conflicts with A1 + A2, under
which an unstable system must become *more* conservative, not exploratory.

⚖ **Derived form:** Λ₀ = tanh(k₁·ℓ − k₂·χ + k₃·|θ̇|). Creativity pulls toward exploration,
instability pulls toward verified logic (safety), and both regimes are reachable inside the unit
domain:
- Λ₀(ℓ = 0, χ = 1, θ̇ = 0) = tanh(−0.5) = −0.46;
- with k₂ = 0.6, Λ₀ = −0.54 < −0.5, so CREATIVE_DOMINANT is reachable.

The value of k₂ is the Commander's choice. **Constraint:** k₂ > atanh(0.5) = 0.549 is required
for CREATIVE_DOMINANT to be reachable when ℓ = 0 and θ̇ = 0.

### E25 — AES-GCM usage bound ⟐ DR-13 [C hoplites/spartanguard.py:79]
With random 96-bit nonces, the nonce-collision probability after q encryptions is ≈ q²/2⁹⁷.
NIST SP 800-38D limits random-IV usage to **q ≤ 2³² per key**. **Invariant I-C1:** a per-key
invocation counter must trigger rotation before 2³². The current code has no counter (G-14).

---

## 5. Extended architecture

### 5.1 Modules and interfaces

| Module | Public interface | Consumes | Produces | Status |
|---|---|---|---|---|
| `core.LeondasBrain` | `calculate_lambda_tas(P,U)`, `initialize_phalanx/hoplites`, `homeostasis_loop()`, `start_ffp/stop_ffp/get_ffp_status`, `get_status`, `shutdown` | Helot, Thermopylae, CommandProcessor | Λ-TAS, Thermopylae observations | ✅ |
| `core.CommandProcessor` | `process_command(cmd)`, `calculate_universe_expansion_factor()`, `set/get_adaptation_factor` | all modules | command results, U | ✅ (DR-2) |
| `phalanx.Helot` | `monitor_resources()`, `get_survival_probability()`, `get_status()` | S0 | resources, P, S | ✅ |
| `phalanx.Agoge` | `run_training_cycle(data)`, `get_adaptation_factor()`, `adjust_learning_rate(r)`, `reset_adaptation()` | (⟐ outcomes) | a ∈ [0.5, 2] | simulated (DR-9) |
| `phalanx.Krypteia` | `start/stop_monitoring()`, `report_threat(t)`, `get_threat_assessment()`, `clear_threat_history()` | (⟐ detectors) | threat level | partial (DR-10) |
| `phalanx.Thermopylae` | `check_emergency_protocol(S)`, `arm/disarm_protocol()`, `activate_protocol()`, `test_protocol()`, `get_status()` | S per tick | destruction | ✅ 🔧 |
| `hoplites.SpartanGuard` | `encrypt/decrypt(text, aad)`, `hash_data`, `verify_integrity` | master key | AES-GCM b64 | ✅ (DR-13) |
| `hoplites.ShieldBearer` | `check_airgap()`, `enforce_firewall()`, `test_external_access(h,p)` | connections | air-gap state | ✅ |
| `hoplites.BattleOracle` | `analyze_risk(s)`, `predict_outcome(a,c)`, `run_simulation(p,n)` | scenario | analysis | simulated (DR-12) |
| `hoplites.WeaponMaster` | `execute_external_query(q)`, `enable/disable_external_access()`, `add/remove_allowed_domain()` | allowlist | (placeholder) responses | simulated ([M EXT-016]) |
| `hoplites.Messenger` | `send_secure_message`, `receive_message`, `queue_message`, `process_queue`, `broadcast_message` | Guard | messages | ✅ |
| `control.KronosArbiter` | `calculate_theta`, `calculate_parallel_time`, `calculate_amdahl_aristeia`, `calculate_metrikos`, `calculate_supreme_time` | parameters | metrics | ✅ |
| `control.LambdaMobiusEngine` | `calculate_T_Wrap/Mult/Hybrid/Balance/Supreme`, `arbiter_select`, `get_history` | k, P, U | T_S, state | ✅ (CD-3) |
| `control.FractalFluxPipeline` | `run_forever`, `scan/detect/quarantine/heal/analyze/apply`, `stop`, `get_status` | brain modules | anomalies | partial (DR-7, DR-8) |
| `parallel_execution` | `PhalanxExecutor.execute_tasks/map_parallel/batch_execute`, `TaskScheduler.add_task/get_execution_plan/execute_sequential` | callables | results + timings | ✅ |
| `sparta.SpartaRuntime` | `query(text)`; `foundation`, `bridge`, `generator` | Foundation | answer record | ✅ (CD-4) |
| `sparta.SemanticFoundation` | `load_memory`, `get_concept`, `get_related`, `verify_statement`, `find_placeholder_concepts`, `quarantine_placeholder_concepts`, `find_dangling_references`, `get_integrity_report`, `get_statistics` | JSONL | concept graph | ✅ |
| `logos.LogosEmbedder` | `fit(texts)`, `embed(t)`, `embed_batch(ts)`, `similarity(a,b)`, `save/load`, `info` | corpus | vectors | ✅ |
| `vault.SpartanVault` | `store`, `retrieve`, `store_with_embedding`, `semantic_search`, `exact_search`, `hybrid_search`, `find_similar`, `delete`, `reindex`, `save_to_disk`, `get_stats` | Λ-Logos | encrypted records | ✅ |
| `mnemosyne` | `load_graph`, `validate`, `checkpoint.create/verify_chain/drift`, `recall.query/boot_pack`; CLI | `.memory/`, tree | report, chain | ✅ |

### 5.2 Data structures

| Structure | Fields | Invariants |
|---|---|---|
| Concept (JSONL) | the 16 fields of [M ONT-009] | c ∈ [0, 1]; unique id; placeholder ⇒ quarantined |
| VectorEntry | id, text, embedding ∈ ℝ³⁸⁴, metadata, created_at | ‖embedding‖ = 1 (Λ-Logos); text = `[ENCRYPTED]` iff encrypted ∧ ¬index_plaintext |
| Vector store file | model_name, model_id, format_version = 2, entries[] | model_id identifies the model of every embedding (I-L1) |
| Encrypted record | id → Fernet token (hex) | decryptable only with the resolved key |
| Model artifact `.npz` | components (float16), idf, singular_values, meta{family, n_features, dim, seed, oversample, power_iterations, fingerprint, corpus_size, model_id} | `allow_pickle = False`; the fingerprint covers params + corpus |
| Memory entry | id, title, file, kind, fields{…}, body | the ID prefix matches its file; references resolve |
| Checkpoint | id, title, date, agent, commit, tree, prev, gates, hash | E22 chain; tree = E21 at creation |
| Thermopylae state | armed, n, activated, threshold, N | I-T1, I-T2 |
| Metrics | survival, cpu, mem, disk, λ_tas, a, threats, messages | Prometheus text exposition |

### 5.3 Communication pathways

| Pathway | Protocol | Security | Direction |
|---|---|---|---|
| Client ↔ API | HTTP/JSON on :7300 | bearer (E20); CORS ⟐ CD-6 | inbound only |
| Prometheus → API | HTTP text exposition | `authorization: Bearer` | inbound scrape |
| API → modules | in-process async calls | — | — |
| Krypteia | daemon thread, 5 s | — | internal |
| Helot → S0 | psutil (CPU sampled in a worker thread) | read-only | internal |
| Weapon Master → network | disabled by default (A4) | allowlist E14 | outbound (opt-in) |
| Federated mesh :7301 | ⟐ planned ([M EXT-025]) | — | — |

### 5.4 Storage lifecycles

| Asset | Created | Read | Rotated / changed | Destroyed |
|---|---|---|---|---|
| Master key `config/spartan_keys.yaml` | `generate_keys.py` (0600) | Guard at boot | ⟐ DR-13 (rotation) | Thermopylae F3a |
| Vault key | env, `encryption.key`, or generated at first save | vault init | ⟐ derived from the master key (DR-13) | Thermopylae (vault paths) |
| Vault data `data/vault/` | `save_to_disk` | vault init | `reindex` after a model change | Thermopylae |
| Model artifact `models/logos-v1.npz` | first `get_model` or `logos train` | each process, once | explicit retrain (PRO-006) | — (regenerable) |
| `.memory/` | by humans and agents under PROTOCOL | Mnemosyne | append (JOURNAL, CHECKPOINT); supersede (DEC) | never (A7) |
| Logs `logs/` | loguru, rotation 100 MB | operators | retention 10 days | rotation |

---

## 6. Gap register (complete)

Type: **G** gap, **C** contradiction, **I** improvement zone. Resolution status as in §0.

| ID | Type | Finding (evidence) | Derivation | Resolution |
|---|---|---|---|---|
| G-01 | C | Thermopylae counter fed only on breaches, and fed twice (F2, F4). Recoveries never reset it; 4 non-consecutive breaches destroyed the data [C core/leonidasbrain.py, control/fractal_pipeline.py] | A3 requires *consecutive* ⇒ one sampler must observe every tick | 🔧 **Fixed**: single-sampler rule; FFP defers while the brain runs (A7 kept). Test fails on the pre-fix code ([M DEC-019]) |
| G-02 | C | Λ-TAS insensitive to P (R1, ≤ 1.01%) | A2 + documented purpose | ⚖ CD-1: k = r/(r−1) |
| G-03 | G | U's inputs are never updated (R2) | specification of U | ⟐ DR-2: wire n_tasks and V_MB |
| G-04 | C | Λ-Möbius pinned to WRAP and ≈ 1 s (R3) | reachability invariant | ⚖ CD-3: κ at a reference point; plus the T_H intent ([M DEC-015]) |
| G-05 | C | Persistence N = 3 at 0.69 s gives 11.6%/day activation at p = 0.01 (R5) | A3 "a transient must never trigger" | ⚖ CD-2: τ from the budget α (E5) |
| G-06 | C | SPARTA reports the upper Fréchet bound as confidence (R6) | A1 requires a lower bound | ⚖ CD-4: L_F (E13); ⟐ DR-11: Λ-Guide as the optimizer |
| G-07 | C | FFP thresholds (90/90) ≠ Helot thresholds (95/90/95) | single source of truth for a measured quantity | ⟐ DR-7: FFP reads `phalanx.helot.resource_thresholds` |
| G-08 | G | Lexical concept matching and mention-based hallucination check | A1 | ⟐ [M EXT-010] with Λ-Logos retrieval |
| G-09 | C | Four uncoordinated confidence thresholds (0.95, 0.80, 0.75, 0.70) | A1: one verified threshold | ⟐ θ_v and θ_u on L_F (E13) + calibration [M EXT-003] |
| G-10 | G | Krypteia detectors empty | A2 perception | ⟐ DR-10 ([M EXT-014]) |
| G-11 | G | GPU load configured, not measured; S is not a probability (R4) | A6 evidence | ⟐ [M EXT-018] |
| G-12 | G | Oracle confidence and Monte Carlo random, input-blind | A1 (no unfounded confidence) | ⟐ DR-12 ([M EXT-013]) |
| G-13 | C | Empty allowlist means allow-all when access is enabled | A4 | ⟐ deny-by-default ([M EXT-016]) |
| G-14 | G | No AES-GCM invocation counter or key rotation (E25) | NIST bound | ⟐ DR-13 ([M EXT-004]) |
| G-15 | G | Overwrite-and-delete is not erasure on SSD/CoW/journaled media; the vault key is independent of the master key | A3 + physical media | ⟐ DR-13: **crypto-erasure via a key hierarchy**: every secret is wrapped by the master key (HKDF), so destroying the master key destroys everything |
| G-16 | C | "Homeostasis" loop has no actuator on the plant (HEAL logs, `optimize_resources` is `pass`) (R12) | A2 requires a closed loop | ⟐ DR-8: bounded, reversible actuators ([M EXT-015]) |
| G-17 | G | Agoge signal is noise: π ~ U(0.8, 1.2), E[π − 1] = 0 ⇒ log a is a driftless random walk (step variance ≈ 1.3 × 10⁻⁶) | A2 (adaptation needs an error signal) | ⟐ DR-9: π = 1 − e_t from observed outcomes ([M EXT-012]) |
| G-18 | C | Λ-Zero sign contradiction (R9) | regime semantics + A1/A2 | ⚖ CD-5: Λ₀ = tanh(k₁ℓ − k₂χ + k₃\|θ̇\|), k₂ > 0.549 |
| G-19 | G | 224 dangling references; 80 placeholders | A1, A6 | ⟐ [M EXT-002], [M EXT-028] |
| G-20 | G | Checkpoint chain self-consistent only when anchored (E22) | A6 | ⟐ DR-14: ML-DSA signatures ([M EXT-026]) |
| G-21 | I | 60+ settings keys unread | A6 | ⟐ [M EXT-007] |
| G-22 | I | CORS `*` with credentials; no expiry; default token allowed | A5 | ⚖ CD-6 ([M EXT-006]) |

---

## 7. Derived additions and rejected candidates

### 7.1 Admitted (each passes the three-part necessity test)

| DR | Addition | Logical (axiom without it) | Mathematical (result) | Necessary (minimal) |
|---|---|---|---|---|
| DR-1 | Single-sampler rule for Thermopylae 🔧 | A3 | G-01 counterexample (destruction on non-consecutive breaches) | one ownership flag; no new module |
| DR-2 | Wire U's inputs | A2 | R2 (U ≡ 1) | two counters already specified |
| DR-7 | Single threshold source | A2, A6 | G-07 (90 ≠ 95) | read an existing config section |
| DR-8 | FFP actuators (bounded, reversible, audited) | A2 (closed loop) | R12 (no actuator ⇒ open loop) | uses the existing HEAL/REINVEST phases |
| DR-9 | Agoge error signal | A2 | G-17 (driftless walk) | replaces one random draw |
| DR-10 | Krypteia detectors | A2 perception, A3 | G-10 | fills existing empty methods |
| DR-11 | Λ-Guide as the L_F optimizer | A1 | E13 corollary (Σ doubt ≤ 0.05) | already specified; its role is now forced |
| DR-12 | Model-based Oracle | A1 | G-12 | fills existing methods |
| DR-13 | Key hierarchy + crypto-erasure + nonce budget | A3 | E25, G-15 | HKDF from the existing master key |
| DR-14 | Signed checkpoints | A6 | E22 note | one signature field |

### 7.2 Rejected (fail at least one criterion)

| Candidate | Why rejected |
|---|---|
| A generative LLM for answers | violates A1 (no lower bound on fabricated text) and A4 (external or opaque model) |
| A larger hashed feature space for Λ-Logos | R7: no measurable gain; 2–4× memory (fails *mathematical*) |
| An external vector DB or graph DB for memory | violates A4; git-reviewable files already satisfy A6 (fails *necessary*) |
| A "neuromorphic", spiking or biological-metaphor layer | no axiom lacks enforcement without it; no result shows an insufficiency (fails *logical* and *mathematical*). Biology and neuroscience enter only where the mathematics is identical: the adaptation law (DR-9) is a gradient-free error-driven update, and Λ-Affect is specified as a confidence-driven state, not a new substrate |
| Blockchain consensus for the ledger | single-authority system (A5): a hash chain plus signatures (DR-14) suffices; consensus adds nothing provable |
| Redis or Postgres for the in-memory histories *now* | needed only once Λ-Reflect exists ([M EXT-019] is ordered after it), so not yet necessary |
| Changing T_H to the harmonic mean unilaterally | a behaviour change (A5); kept as CD |

---

## 8. Conclusion — the balanced form, and a theorem of optimality

**Definition (balanced form Σ\*).** Σ\* is the system of §§2–5 with:
- every 🔧 fix applied;
- every ⟐ derived requirement DR-1 … DR-14 implemented;
- every ⚖ decision instantiated by the Commander *within its derived form*: k = r/(r−1);
  κ = kP_ref(1 + ln U_ref); N = ⌈τ/T⌉ with τ from α; c_ans = L_F; Λ₀ with the corrected signs.

**Theorem (necessity, sufficiency and minimality relative to A1–A8).**

1. **Necessity.** Removing any stratum S0–S7, or any admitted DR, leaves at least one axiom without
   an enforcing mechanism. *Proof sketch.* Each stratum is the unique holder of some axiom's
   mechanism (§2 table). S1 is the only perception, needed by A2. S2 is the only actuator of A3.
   S4 is the only producer of bounded-confidence claims (A1) and the only sovereign model (A4).
   S6 is the only command channel (A5). S7 is the only verifier of A6–A8. Each DR's row in §7.1
   names the axiom it alone enforces and the computed result showing the prior mechanism
   insufficient. ∎
2. **Sufficiency.** In Σ\*, every axiom has a mechanism, and every mechanism has an executable
   enforcer:
   - A1: L_F ≥ θ_v or `UNKNOWN` (E13); quarantine; Λ-Guide.
   - A2: closed loop F2 + DR-8, with live P and U.
   - A3: τ-persistent FSM (E5) + crypto-erasure (DR-13).
   - A4: Λ-Logos + `deps.external_ml_runtime = none` + air-gap predicates.
   - A5: PROTOCOL + CD gates.
   - A6: Mnemosyne M01–M13 + E21/E22 + DR-14.
   - A7: opt-in preservation of every superseded behaviour.
   - A8: CI gates.

   Each enforcer is named in [M LAWS] and checked by M06. ∎
3. **Minimality.** Every candidate outside Σ\* fails the necessity test (§7.2). Every admitted
   addition reuses an existing module, method or configuration section rather than introducing a
   new stratum. ∎

**What the theorem does not claim, by necessity rather than modesty.** Four constants (r, κ, α,
k₂) and three calibrations cannot be *deduced* from the sources: confidence bands ([M EXT-003]),
resource and survival traces ([M EXT-018]), and arbiter reference points ([M EXT-017]). The
constants express the Commander's risk preferences (A5). The calibrations require measurement
(A6). A specification that "deduced" them would violate the very axioms it serves. Σ\* is therefore
**closed under the axioms**: no further *architectural* revision is derivable from the current
sources. What remains are **parameter choices and measurements**, each with its formula and
enforcer already fixed.

In that precise sense, the balanced form is the necessary consequence of the system's intention:
- a regulator that actually regulates;
- a guardian that destroys only on sustained evidence, and destroys cryptographically;
- a knowledge core whose confidence is a proven floor, not an optimistic ceiling;
- a model that owes nothing to any outside party;
- a memory that can prove what it claims.

---

*Reproducibility:* R1–R3 and R5–R6 are computed from the functions cited at the basis commit. R5 uses
an exact dynamic program over the current run length. R7 and R8 come from the corpus and the trained
artifact (`logos-v1:7ace9ee49387`). G-01 is reproduced by
`tests/test_system_integrity.py::TestThermopylaeSingleSampler`.
