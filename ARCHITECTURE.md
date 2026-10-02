# ΛΕΩΝΙΔΑΣ-AI PHALANX - Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    ΛΕΩΝΙΔΑΣ-AI PHALANX                         │
│                  Falanga Digitală Spartană                      │
│                   ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         Λ-CORE (Nucleul Central)        │
        │  ┌────────────────┬─────────────────┐   │
        │  │ LeondasBrain   │ CommandProcessor │   │
        │  │ (Homeostazie)  │ (Λ-Möbius Engine)│   │
        │  └────────────────┴─────────────────┘   │
        └─────────────┬───────────────────────────┘
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
    ┌───────────────┐   ┌───────────────┐
    │   PHALANX     │   │   HOPLITES    │
    │ (Control      │   │  (Arsenal de  │
    │  Intern)      │   │   Acțiune)    │
    └───────────────┘   └───────────────┘
```

## Λ-CORE Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ΛΕΩΝΙΔΑΣ BRAIN                           │
│                    (Nucleul Decizional)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  • Inițializare module Phalanx și Hoplites                     │
│  • Bucla de Homeostazie (dS/dt=0)                              │
│  • Calculare Λ-TAS (Timpul Autonom Spartan)                    │
│  • Monitorizare probabilitate supraviețuire                    │
│                                                                 │
│  Formula Λ-TAS (secunde, pentru k·P > 1):                      │
│    Λ-TAS = T₁·ln(U+1) / (1 − 1/(k·P)),  T₁=1s, k=100           │
│    limitat la [0.1, 10] s; fallback P/(1+U) dacă k·P ≤ 1        │
│    P = Factor de paralelism măsurat de Helot                   │
│    U = Factor de expansiune calculat de CommandProcessor       │
│  Bucla doarme Λ-TAS secunde între iterații.                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    COMMAND PROCESSOR                            │
│                   (Λ-Möbius Engine)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  • Interpretare intenție Comandant                             │
│  • Rutare comenzi către module                                 │
│  • Aplicare factor adaptare (din Agoge)                        │
│  • Procesare comenzi tactice                                   │
│                                                                 │
│  Comenzi disponibile:                                          │
│    - status         : Stare sistem                             │
│    - analyze_risk   : Analiză tactică (Oracle)                │
│    - encrypt_data   : Criptare (Guard)                         │
│    - check_airgap   : Verificare Air-Gap (Shield)             │
│    - send_message   : Mesaj securizat (Messenger)             │
│    - train_agoge    : Micro-antrenament (Agoge)               │
│    - sparta_query   : Raționament verificat (SPARTA)          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## PHALANX Modules (Control Intern)

```
┌─────────────────────────────────────────────────────────────────┐
│                        PHALANX                                  │
│                   (Module de Control)                           │
└─────────────────────────────────────────────────────────────────┘
         │              │              │              │
    ┌────▼───┐    ┌────▼───┐    ┌────▼───┐    ┌────▼───┐
    │ HELOT  │    │ AGOGE  │    │KRYPTEIA│    │THERMO- │
    │  🏺    │    │  🎓    │    │  👁️    │    │ PYLAE  │
    │        │    │        │    │        │    │  🔥    │
    └────────┘    └────────┘    └────────┘    └────────┘

┌───────────────────────────────────────────────────────────────┐
│ 🏺 HELOT MODULE - Monitorizare Resurse                       │
├───────────────────────────────────────────────────────────────┤
│ • Monitorizare CPU, RAM, GPU, NPU                            │
│ • Calculare probabilitate supraviețuire                      │
│ • Praguri critice:                                           │
│   - CPU: 95%                                                 │
│   - Memory: 90%                                              │
│   - Disk: 95%                                                │
│ • Factor paralelism P → Λ-TAS (ultima citire: last_resources)│
│ • Eșantionare CPU în thread (nu blochează bucla async)       │
│ • Interval: dictat de Λ-TAS (monitoring_interval_sec: B-07)  │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 🎓 AGOGE MODULE - Învățare Continuă                          │
├───────────────────────────────────────────────────────────────┤
│ • Cicluri de micro-antrenament                               │
│ • Factor de adaptare: [0.5, 2.0]                            │
│ • Learning rate: 0.01                                        │
│ • Furnizează adaptare pentru Λ-Möbius Engine                │
│ • ⚠️ Simulat: performanța este aleatoare (BACKLOG B-12)      │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 👁️ KRYPTEIA MODULE - Monitorizare Amenințări                │
├───────────────────────────────────────────────────────────────┤
│ • Observare tăcută (thread separat)                         │
│ • Detectare amenințări în timp real                         │
│ • Nivele amenințare: low, medium, high, critical            │
│ • Monitoring interval: 5 secunde                             │
│ • ⚠️ Detectoarele (rețea/procese/fișiere) sunt placeholder   │
│   - amenințările se raportează manual (BACKLOG B-14)         │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 🔥 THERMOPYLAE MODULE - Protocol Urgență                     │
├───────────────────────────────────────────────────────────────┤
│ • Prag critic: 95% probabilitate supraviețuire              │
│ • Declanșare: consecutive_breaches_required (3) verificări  │
│   consecutive sub prag - un vârf izolat nu declanșează      │
│ • Auto-distrugere controlată (IREVERSIBILĂ!)                │
│ • Acțiuni la activare:                                       │
│   1. Suprascrie fișierul de chei cu date random, apoi șterge│
│   2. Distruge toate căile vault (data/vault,                │
│      data/encrypted_vault)                                   │
│ • Status: ARMED / DISARMED                                   │
│ ⚠️ PERICOL: Activare doar în situații critice!              │
└───────────────────────────────────────────────────────────────┘
```

## FFP Integration with LeondasBrain

The Fractal Flux Pipeline is fully integrated into the LeondasBrain core:

### Integration Architecture

```
┌─────────────────────────────────────────────────┐
│           LEONIDAS BRAIN (Core)                 │
│  ┌──────────────────────────────────────────┐  │
│  │  • Homeostasis loop                      │  │
│  │  • Module orchestration                  │  │
│  │  • Survival monitoring                   │  │
│  └──────────────────────────────────────────┘  │
│                    │                            │
│                    ├──► FFP Pipeline            │
│                    │    (autoreparatory)        │
│                    │                            │
│  ┌──────────────────────────────────────────┐  │
│  │  FFP: Scan → Detect → Quarantine →      │  │
│  │       Heal → Improve → Reinvest          │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Methods

- `start_ffp()`: Run the FFP loop (awaits until stopped)
- `get_ffp_status()`: Get current FFP status
- `stop_ffp()`: Stop FFP Pipeline

The API server starts FFP automatically in its lifespan when `control.ffp.enabled: true`
(default in `config/settings.yaml`) and stops it on shutdown. HEAL and REINVEST currently
only log their actions (BACKLOG B-15).

### Usage

```python
from core.leonidasbrain import LeondasBrain

# Initialize
brain = LeondasBrain(config)

# FFP is automatically initialized; run it as a background task
task = asyncio.create_task(brain.start_ffp())

# Check status
status = brain.get_ffp_status()
print(f"FFP running: {status['running']}")
print(f"Cycles completed: {status['cycle_count']}")

# Stop when needed
brain.stop_ffp()
```

## HOPLITES Arsenal (Module de Acțiune)

```
┌─────────────────────────────────────────────────────────────────┐
│                         HOPLITES                                │
│                    (Arsenal de Acțiune)                         │
└─────────────────────────────────────────────────────────────────┘
      │         │         │         │         │
  ┌───▼──┐  ┌──▼──┐  ┌──▼──┐  ┌──▼──┐  ┌──▼──┐
  │GUARD │  │SHIELD│  │ORACLE│  │WEAPON│  │MSNGR│
  │ 🛡️   │  │ 🛡️  │  │ 🔮  │  │ 🗡️  │  │ 📨  │
  └──────┘  └─────┘  └─────┘  └─────┘  └─────┘

┌───────────────────────────────────────────────────────────────┐
│ 🛡️ SPARTAN GUARD - Criptografie                              │
├───────────────────────────────────────────────────────────────┤
│ • Algoritm: AES-256-GCM                                       │
│ • Generare chei: 256-bit master key                          │
│ • Nonce unic: 96-bit pentru fiecare operație                 │
│ • Hash: SHA-256                                               │
│ • Verificare integritate                                      │
│ • Associated Data support pentru GCM                          │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 🛡️ SHIELD BEARER - Air-Gap și Firewall                       │
├───────────────────────────────────────────────────────────────┤
│ • Moduri Air-Gap:                                             │
│   - strict: ZERO conexiuni externe                           │
│   - permissive: Doar conexiuni permise                       │
│   - disabled: Toate conexiuni permise                        │
│ • Verificare firewall (iptables/Windows)                     │
│ • Monitorizare conexiuni active                              │
│ • Test acces extern                                          │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 🔮 BATTLE ORACLE - Predicții și Analiză Tactică              │
├───────────────────────────────────────────────────────────────┤
│ • Alocare NPU: 50 TOPS                                        │
│ • Analiză risc: threat level, success probability            │
│ • Recomandări acțiuni tactice                                │
│ • Simulări Monte Carlo                                        │
│ • Predicții rezultate operațiuni                             │
│ • Istoric predicții                                           │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 🗡️ WEAPON MASTER - Interacțiune Externă Controlată           │
├───────────────────────────────────────────────────────────────┤
│ • Acces extern: DISABLED by default                          │
│ • ⚠️ Compromite Air-Gap când activat!                        │
│ • Allowlist domenii permise                                  │
│ • Suport HTTP GET/POST                                       │
│ • DNS lookup                                                 │
│ • Request timeout: 30 secunde                                │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 📨 MESSENGER - Comunicații Securizate                         │
├───────────────────────────────────────────────────────────────┤
│ • Criptare mesaje (via Spartan Guard)                        │
│ • Queue management                                            │
│ • Prioritizare mesaje: high, normal, low                     │
│ • Broadcast către multiple destinații                        │
│ • Istoric mesaje: 7 zile                                      │
│ • Queue max size: 1000 mesaje                                │
└───────────────────────────────────────────────────────────────┘
```

## API Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     API SERVER (Port 7300)                      │
│                       FastAPI + Uvicorn                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Autentificare: Bearer Token (comparație în timp constant)     │
│  Sursă: SPARTA_AUTH_TOKEN > auth.auth_token > implicit         │
│  Implicit: SPARTA300_SECRET_TOKEN (avertisment la pornire!)    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
    │  HEALTH  │  │ COMMAND  │  │ METRICS  │  │  VAULT   │  │  SPARTA  │
    │  Routes  │  │  Routes  │  │  Routes  │  │  Routes  │  │  Routes  │
    └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘

┌───────────────────────────────────────────────────────────────┐
│ HEALTH ROUTES                                                 │
├───────────────────────────────────────────────────────────────┤
│ GET  /api/v1/health              : Health check (public)     │
│ GET  /api/v1/health/detailed     : Status detaliat (auth)    │
│ GET  /api/v1/health/survival     : Probabilitate (auth)      │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ COMMAND ROUTES                                                │
├───────────────────────────────────────────────────────────────┤
│ POST /api/v1/command             : Execută comandă (auth)    │
│ GET  /api/v1/command/status      : Status sistem (auth)      │
│ POST /api/v1/command/analyze-risk: Analiză risc (auth)       │
│ POST /api/v1/command/encrypt     : Criptare date (auth)      │
│ GET  /api/v1/command/check-airgap: Verificare Air-Gap (auth) │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ METRICS ROUTES                                                │
├───────────────────────────────────────────────────────────────┤
│ GET  /api/v1/metrics             : Prometheus text (auth)    │
│ GET  /api/v1/metrics/json        : JSON format (auth)        │
│ GET  /api/v1/lambda-mobius       : Metrici Λ-Möbius (auth)   │
│                                                               │
│ Metrici expuse:                                               │
│  • leonidas_survival_probability                              │
│  • leonidas_cpu_percent                                       │
│  • leonidas_memory_percent                                    │
│  • leonidas_lambda_tas                                        │
│  • leonidas_adaptation_factor                                 │
│  • leonidas_threats_detected                                  │
│  • leonidas_messages_sent                                     │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ VAULT ROUTES (toate cu auth)                                  │
├───────────────────────────────────────────────────────────────┤
│ POST /api/v1/vault/embed | /batch-embed  : Embeddings         │
│ POST /api/v1/vault/store-with-embedding  : Stocare criptată   │
│ POST /api/v1/vault/search | /hybrid-search: Căutare semantică │
│ GET  /api/v1/vault/similar/{id}          : Intrări similare   │
│ GET  /api/v1/vault/stats  POST /save     : Statistici/persist │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ SPARTA ROUTES (toate cu auth)                                 │
├───────────────────────────────────────────────────────────────┤
│ POST /api/v1/sparta/query          : Răspuns verificat        │
│ GET  /api/v1/sparta/concept/{id}   : Concept (16 câmpuri)     │
│ GET  /api/v1/sparta/stats          : Statistici Foundation    │
│ GET  /api/v1/sparta/integrity      : Referințe lipsă în graf  │
└───────────────────────────────────────────────────────────────┘
```

## Docker Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKER COMPOSE STACK                         │
└─────────────────────────────────────────────────────────────────┘
         │
         ├──► leonidas-core (Port 7300)
         │    └─ ΛΕΩΝΙΔΑΣ-AI main service
         │
         ├──► redis-fortress (Port 6379)
         │    └─ Cache de memorie (REZERVAT - nefolosit încă, B-19)
         │
         ├──► postgres-armory (Port 5432)
         │    └─ Bază de date persistentă (REZERVAT - nefolosit încă, B-19)
         │
         ├──► prometheus-monitor (Port 9090)
         │    └─ Colectare metrici
         │
         └──► grafana-oracle (Port 3000)
              └─ Vizualizare metrici

Network: sparta-network (172.30.0.0/24)
Volumes: redis-data, postgres-data, prometheus-data, grafana-data
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITATE MULTI-STRAT                       │
└─────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ STRAT 1: Criptografie                                         │
├───────────────────────────────────────────────────────────────┤
│ • AES-256-GCM (Spartan Guard), cheie master din              │
│   config/spartan_keys.yaml sau SPARTA_MASTER_KEY              │
│ • Vault: Fernet; indexul semantic ține doar "[ENCRYPTED]"     │
│ • Chei generate securizat (256-bit random)                    │
│ • Nonce unic pentru fiecare operație                          │
│ • SHA-256 pentru hash și integritate                          │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ STRAT 2: Autentificare                                        │
├───────────────────────────────────────────────────────────────┤
│ • Bearer token pe toate endpoint-urile în afară de /health    │
│ • Token din SPARTA_AUTH_TOKEN sau auth.auth_token             │
│ • Comparație în timp constant; token-ul nu este logat         │
│ • Validare la fiecare request                                 │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ STRAT 3: Air-Gap                                              │
├───────────────────────────────────────────────────────────────┤
│ • Izolare strictă de rețea (default)                          │
│ • Verificare conexiuni active (loopback-ul local e permis)    │
│ • Firewall enforcement                                        │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ STRAT 4: Protocol Thermopylae                                 │
├───────────────────────────────────────────────────────────────┤
│ • Auto-distrugere în caz de compromitere                      │
│ • Ștergere ireversibilă chei și vault                         │
│ • Trigger la < 95% supraviețuire, susținut N verificări      │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ STRAT 5: Audit și Logging                                     │
├───────────────────────────────────────────────────────────────┤
│ • Loguri structurate (Loguru)                                 │
│ • Audit trail dedicat: planificat (BACKLOG B-07, B-26)        │
│ • Rotație automată (100 MB)                                   │
│ • Retenție 10 zile                                            │
└───────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌─────────────┐
│ Comandant   │
│ (User/API)  │
└──────┬──────┘
       │ Bearer Token
       ▼
┌──────────────────────────────────────┐
│   FastAPI Server (Port 7300)         │
│   • Verificare autentificare         │
│   • Validare input                   │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│   Command Processor                  │
│   • Parse comandă                    │
│   • Rutare către modul               │
└──────┬───────────────────────────────┘
       │
       ├─────────────┐
       ▼             ▼
┌──────────┐   ┌──────────┐
│ Phalanx  │   │ Hoplites │
│ Modules  │   │ Arsenal  │
└──────┬───┘   └────┬─────┘
       │            │
       └─────┬──────┘
             ▼
      ┌──────────────┐
      │   Response   │
      └──────────────┘
```

## Deployment Flow

```
1. Instalare
   └─► bash scripts/install_sparta.sh
       ├─► Creare virtual env (sparta-env)
       ├─► Instalare dependencies
       ├─► Creare directories
       └─► Generare chei criptografice

2. Activare
   └─► source sparta-env/bin/activate
       └─► bash scripts/activate_leonidas.sh
           ├─► Verificare dependencies
           ├─► Verificare configurație
           └─► Start API server

3. Deployment Docker
   └─► docker-compose up -d
       ├─► Build leonidas-core image
       ├─► Start toate serviciile
       ├─► Creare network și volumes
       └─► Health checks active
```

---

## Λ-Logos — Our Own Embedding Model

```
text ──► tokenizer (NFKD fold · words · bigrams · char 3–5-grams)
     ──► signed feature hashing (BLAKE2b, 2¹⁵ buckets)
     ──► TF-IDF (idf learned from the project corpus)
     ──► randomized SVD projection (384 latent axes)
     ──► L2-normalized vector  ·  model id = logos-v1:<sha256(params+corpus)[:12]>
```

- **No external model or API** (LAW-006): NumPy and SciPy only. Trained on SPARTA concepts,
  `.memory/` and the documentation. The untrained fallback is a deterministic random projection.
- **Frozen artifact** `models/logos-v1.npz`: loaded as-is, retrained only explicitly. A retrain
  marks stored vectors stale until `SpartanVault.reindex()` runs.
- **Consumers:** `SpartanVectorStore` (vault RAG) and Mnemosyne recall. Planned: SPARTA concept
  retrieval (BACKLOG B-10).

## Project Memory — `.memory/` and Mnemosyne

```
INTENTION (root) ─► IDENTITY ─► LAWS ─► ONTOLOGY ─► DECISIONS ─► ATLAS
      ─► CURRENT_STATE (measured) ─► CHECKPOINT (hash chain) ─► JOURNAL ─► EXTENSIONS ─► PROTOCOL
```

- Entries have stable IDs (`LAW-006`, `DEC-012`). Typed edges are `cites`, `supersedes`,
  `depends_on`, `evidence`, `enforced_by` and `files`.
- `mnemosyne check` enforces:
  - resolvable references;
  - existing law enforcers;
  - ATLAS coverage of every repository file;
  - recomputed facts;
  - an intact checkpoint chain;
  - a lineage to INTENTION for every entry.
- `mnemosyne boot` prints the session context. `mnemosyne query` provides hybrid Λ-Logos recall.
- The memory runs in CI and is protected by PROTOCOL (boot, work and close microsteps).

## 📊 Implementation Status

The verified, measured status (component maturity, quality gates, remediation log) is maintained in
**[PROJECT_STATUS.md](PROJECT_STATUS.md)**; the prioritized next steps are in **[BACKLOG.md](BACKLOG.md)**.
This document describes the architecture only, so that status numbers live in exactly one place.

---

**ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)** - *"Come and Take Them"*
