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
│  Formula Λ-TAS: Λ-TAS = P / (1 + U)                           │
│    P = Paralelism (număr nucleuri)                             │
│    U = Workload (volum sarcini)                                │
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
│ • Update interval: 5 secunde                                 │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 🎓 AGOGE MODULE - Învățare Continuă                          │
├───────────────────────────────────────────────────────────────┤
│ • Cicluri de micro-antrenament                               │
│ • Factor de adaptare: [0.5, 2.0]                            │
│ • Learning rate: 0.01                                        │
│ • Furnizează adaptare pentru Λ-Möbius Engine                │
│ • Training interval: 60 secunde                              │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 👁️ KRYPTEIA MODULE - Monitorizare Amenințări                │
├───────────────────────────────────────────────────────────────┤
│ • Observare tăcută (thread separat)                         │
│ • Detectare amenințări în timp real                         │
│ • Nivele amenințare: low, medium, high, critical            │
│ • Monitoring interval: 5 secunde                             │
│ • Ajustare probabilitate supraviețuire                       │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ 🔥 THERMOPYLAE MODULE - Protocol Urgență                     │
├───────────────────────────────────────────────────────────────┤
│ • Prag critic: 95% probabilitate supraviețuire              │
│ • Auto-distrugere controlată (IREVERSIBILĂ!)                │
│ • Acțiuni la activare:                                       │
│   1. Ștergere chei criptografice                            │
│   2. Distrugere vault criptat                               │
│   3. Suprascrie cu date random                              │
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

- `start_ffp()`: Start FFP Pipeline in background
- `get_ffp_status()`: Get current FFP status
- `stop_ffp()`: Stop FFP Pipeline
- `start_homeostasis()`: Start both homeostasis + FFP in parallel

### Usage

```python
from core.leonidasbrain import LeondasBrain

# Initialize
brain = LeondasBrain(config)

# FFP is automatically initialized
# To start it:
await brain.start_ffp()

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
│  Autentificare: Bearer Token                                   │
│  Token: SPARTA300_SECRET_TOKEN (schimbă în producție!)         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌──────────┐       ┌──────────┐       ┌──────────┐
    │  HEALTH  │       │ COMMAND  │       │ METRICS  │
    │  Routes  │       │  Routes  │       │  Routes  │
    └──────────┘       └──────────┘       └──────────┘

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
│ GET  /api/v1/metrics             : Prometheus format (auth)  │
│ GET  /api/v1/metrics/json        : JSON format (auth)        │
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
         │    └─ Cache de memorie
         │
         ├──► postgres-armory (Port 5432)
         │    └─ Bază de date persistentă
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
│ • AES-256-GCM pentru toate datele sensibile                   │
│ • Chei generate securizat (256-bit random)                    │
│ • Nonce unic pentru fiecare operație                          │
│ • SHA-256 pentru hash și integritate                          │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ STRAT 2: Autentificare                                        │
├───────────────────────────────────────────────────────────────┤
│ • Bearer token pentru toate endpoint-urile protejate          │
│ • Token configurat în settings.yaml sau environment           │
│ • Validare la fiecare request                                 │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ STRAT 3: Air-Gap                                              │
├───────────────────────────────────────────────────────────────┤
│ • Izolare strictă de rețea (default)                          │
│ • Verificare conexiuni active                                 │
│ • Firewall enforcement                                        │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ STRAT 4: Protocol Thermopylae                                 │
├───────────────────────────────────────────────────────────────┤
│ • Auto-distrugere în caz de compromitere                      │
│ • Ștergere ireversibilă chei și vault                         │
│ • Trigger la < 95% probabilitate supraviețuire               │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ STRAT 5: Audit și Logging                                     │
├───────────────────────────────────────────────────────────────┤
│ • Loguri structurate (Loguru)                                 │
│ • Audit trail complet                                         │
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

**ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)** - *"Come and Take Them"*
