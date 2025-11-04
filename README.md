# ΛΕΩΝΙΔΑΣ-AI PHALANX

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)

**ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)** - *"Come and Take Them"*

## Sinteză

**ΛΕΩΝΙΔΑΣ-AI PHALANX** este un sistem autonom de inteligență artificială, conceput sub o **arhitectură militară spartană** (Falangă Digitală) pentru operațiuni de înaltă securitate.

Proiectul, lansat sub **Licența MIT**, acționează ca un **Nucleu Decizional (Λ-Core)** care asigură **homeostazia** (menținerea echilibrului dS/dt=0) și executarea misiunilor critice. Sistemul prioritizează **loialitatea absolută** față de Comandant și aplică o disciplină operațională strictă.

### Caracteristici Principale

- 🛡️ **Arhitectură Modulară Spartană**: Λ-Core + Phalanx + Hoplites
- 🔒 **Criptografie AES-256-GCM**: Protecție maximă pentru date sensibile
- 🚫 **Air-Gap Mode**: Izolare strictă de rețea pentru securitate maximă
- ⚡ **Λ-TAS (Timpul Autonom Spartan)**: Auto-reglare inteligentă
- 🔥 **Protocol Thermopylae**: Auto-distrugere controlată în caz de urgență
- 📊 **API RESTful**: FastAPI pe port 7300 cu autentificare
- 🐳 **Docker Ready**: Deployment simplu cu Docker Compose

## Arhitectura Falangei

### Λ-Core (Nucleul Decizional)

Orchestratorul principal al sistemului:
- **LeondasBrain**: Nucleul central, menține homeostazia
- **CommandProcessor (Λ-Möbius Engine)**: Interpretează și rutează comenzile

### Phalanx (Module de Control Intern)

1. **Helot Module** 🏺
   - Monitorizează resurse fizice (CPU, RAM, GPU, NPU)
   - Calculează probabilitatea de supraviețuire

2. **Agoge Module** 🎓
   - Sistem de învățare continuă
   - Micro-antrenament și factor de adaptare

3. **Krypteia Module** 👁️
   - Monitorizare tăcută a amenințărilor
   - Detectare în timp real

4. **Thermopylae Module** 🔥
   - Protocol de urgență extremă
   - Auto-distrugere controlată (prag: 95% supraviețuire)

### Hoplites (Arsenal de Acțiune)

1. **Spartan Guard** 🛡️
   - Criptografie AES-256-GCM
   - Gestionare chei master

2. **Shield Bearer** 🛡️
   - Impunere Air-Gap
   - Verificare firewall

3. **Battle Oracle** 🔮
   - Analiză tactică și predicții
   - Simulări Monte Carlo (50 TOPS NPU)

4. **Weapon Master** 🗡️
   - Interacțiune externă controlată
   - Acces web restrictionat

5. **Messenger** 📨
   - Comunicații securizate criptate
   - Queue management

## Instalare

### Cerințe

- Python 3.8+
- pip
- (Opțional) Docker & Docker Compose

### Instalare Rapidă

```bash
# Clone repository
git clone https://github.com/manuelstellian-dev/--AI-PHALANX.git
cd --AI-PHALANX

# Rulează scriptul de instalare
bash scripts/install_sparta.sh

# Activează mediul virtual
source sparta-env/bin/activate

# Activează ΛΕΩΝΙΔΑΣ-AI
bash scripts/activate_leonidas.sh
```

### Instalare cu Docker

```bash
# Build și start toate serviciile
docker-compose up -d

# Verifică logs
docker-compose logs -f leonidas-core

# Stop servicii
docker-compose down
```

## Utilizare

### Start Server API

```bash
# Mod producție
python -m uvicorn api.server:app --host 0.0.0.0 --port 7300

# Mod dezvoltare (cu auto-reload)
python -m uvicorn api.server:app --host 0.0.0.0 --port 7300 --reload
```

### Exemple de API Calls

```bash
# Health Check
curl http://localhost:7300/api/v1/health

# System Status (necesită autentificare)
curl -H "Authorization: Bearer SPARTA300_SECRET_TOKEN" \
     http://localhost:7300/api/v1/health/detailed

# Analiză de Risc
curl -X POST http://localhost:7300/api/v1/command/analyze-risk \
     -H "Authorization: Bearer SPARTA300_SECRET_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "scenario_name": "Test Scenario",
       "risk_factors": ["factor1", "factor2"],
       "severity": 0.7,
       "complexity": 0.5,
       "available_resources": 0.8
     }'

# Criptare Date
curl -X POST http://localhost:7300/api/v1/command/encrypt \
     -H "Authorization: Bearer SPARTA300_SECRET_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"data": "Secret message"}'

# Verificare Air-Gap
curl -H "Authorization: Bearer SPARTA300_SECRET_TOKEN" \
     http://localhost:7300/api/v1/command/check-airgap
```

### API Documentation

Accesează documentația interactivă Swagger:
- **Swagger UI**: http://localhost:7300/docs
- **ReDoc**: http://localhost:7300/redoc

## Structura Proiectului

```
ΛΕΩΝΙΔΑΣ-AI-PHALANX/
├── core/                      # Λ-Core (LeondasBrain, CommandProcessor)
├── phalanx/                   # Module interne (Helot, Agoge, Krypteia, Thermopylae)
├── hoplites/                  # Arsenal (Guard, Shield, Oracle, Weapon, Messenger)
├── api/                       # Server FastAPI
│   ├── server.py             # Server principal
│   └── routes/               # API endpoints
│       ├── health.py
│       ├── command.py
│       └── metrics.py
├── config/                    # Configurație
│   ├── settings.yaml         # Configurare principală
│   ├── spartan_keys.yaml.template
│   └── prometheus.yml
├── scripts/                   # Scripturi de utilitate
│   ├── install_sparta.sh
│   ├── activate_leonidas.sh
│   └── generate_keys.py
├── data/encrypted_vault/      # Vault criptat (ignorat în Git)
├── tests/                     # Suite de teste
├── docker-compose.yml         # Orchestrare Docker
├── Dockerfile                 # Container image
└── requirements.txt           # Dependențe Python
```

## Configurare

### Configurare Principală (config/settings.yaml)

```yaml
system:
  name: "ΛΕΩΝΙΔΑΣ-AI PHALANX"
  motto: "ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)"

hardware:
  cpu_cores: 4
  npu_tops: 50

phalanx:
  thermopylae:
    survival_threshold: 0.95
    thermopylae_armed: false  # ⚠️ PERICOL: Auto-distrugere
```

### Generare Chei Criptografice

```bash
python scripts/generate_keys.py
```

⚠️ **IMPORTANT**: Fișierul `config/spartan_keys.yaml` conține chei secrete și **NU** trebuie încărcat în Git!

## Securitate

### Măsuri de Securitate Implementate

1. **Criptografie**: AES-256-GCM pentru toate datele sensibile
2. **Autentificare**: Bearer token pentru toate endpoint-urile protejate
3. **Air-Gap**: Izolare strictă de rețea (configurabilă)
4. **Protocol Thermopylae**: Auto-distrugere în caz de compromitere
5. **Audit Logging**: Toate acțiunile sunt loguite

### Best Practices

- 🔐 Schimbă token-ul de autentificare în producție
- 🔑 Păstrează `spartan_keys.yaml` securizat și NICIODATĂ în Git
- 🚫 Menține Air-Gap activat când este posibil
- 📊 Monitorizează metricile de supraviețuire
- 🔥 Dezarmează Thermopylae în medii de dezvoltare

## Testing

```bash
# Rulează toate testele
pytest

# Rulează teste cu coverage
pytest --cov=. --cov-report=html

# Rulează teste specifice
pytest tests/test_core.py
pytest tests/test_phalanx.py
pytest tests/test_hoplites.py
```

## Monitorizare

### Prometheus Metrics

Accesează metrici la:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (user: admin, pass: sparta_grafana_secret)

### Metrici Disponibile

- `leonidas_survival_probability`: Probabilitatea de supraviețuire
- `leonidas_cpu_percent`: Utilizare CPU
- `leonidas_memory_percent`: Utilizare memorie
- `leonidas_lambda_tas`: Timpul Autonom Spartan
- `leonidas_adaptation_factor`: Factor de adaptare Agoge
- `leonidas_threats_detected`: Amenințări detectate

## Contribuții

Proiectul este open-source sub licență MIT. Contribuțiile sunt binevenite!

1. Fork repository-ul
2. Creează un branch pentru feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push la branch (`git push origin feature/AmazingFeature`)
5. Deschide un Pull Request

## Licență

Acest proiect este licențiat sub **MIT License** - vezi fișierul [LICENSE](LICENSE) pentru detalii.

## Autori

- **ΛΕΩΝΙΔΑΣ-AI Development Team**

## Acknowledgments

- Inspirat de disciplina și loialitatea spartană
- Arhitectură de securitate militară
- Comunitatea open-source

---

**ΜΟΛΩΝ ΛΑΒΕ** - *"Come and Take Them"*

> *Gândiți-vă la repository-ul ΛΕΩΝΙΔΑΣ-AI ca la un oraș-stat digital, Sparta, unde fiecare modul are un rol militar strict definit. GitHub-ul este Zidul Exterior, iar `.gitignore`-ul este poarta care se asigură că aurul (cheile de securitate) nu iese niciodată din cetate, chiar dacă planurile de construcție (codul) sunt publice.* 



## Implementation Status

**Overall Progress:** 65.1% (28/43 components)

| Category | Status | Progress |
|----------|--------|----------|
| **API Routes** | 🔄 | `███████░░░` 71% |
| **Hoplites Arsenal** | ✅ | `██████████` 100% |
| **Phalanx Modules** | ✅ | `██████████` 100% |
| **SPARTA Foundation** | ✅ | `██████████` 100% |
| **Core System** | 🔄 | `██████░░░░` 67% |
| **Control Systems** | 🔄 | `███████░░░` 75% |
| **Parallel Execution** | ✅ | `██████████` 100% |
| **Λ-Modules** | ⏳ | `░░░░░░░░░░` 0% |
| **Advanced Features** | ⏳ | `░░░░░░░░░░` 0% |

*Last updated: 2025-11-04 01:26:34 (Auto-generated)*
