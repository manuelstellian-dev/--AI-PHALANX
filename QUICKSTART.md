# ΛΕΩΝΙΔΑΣ-AI PHALANX - Quick Start Guide

🛡️ **ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)** - *"Come and Take Them"*

## 5-Minute Quick Start

### 1. Clone and Install

```bash
# Clone repository
git clone https://github.com/manuelstellian-dev/--AI-PHALANX.git
cd --AI-PHALANX

# Run installation script
bash scripts/install_sparta.sh
```

The installation script will:
- ✅ Create Python virtual environment (`sparta-env`)
- ✅ Install all dependencies
- ✅ Create necessary directories
- ✅ Generate cryptographic keys

### 2. Activate and Start

```bash
# Activate virtual environment
source sparta-env/bin/activate

# Start ΛΕΩΝΙΔΑΣ-AI
bash scripts/activate_leonidas.sh
```

Choose option **1** (Production Mode) or **2** (Development Mode)

### 3. Test the API

Open a new terminal and test the endpoints:

```bash
# Health check (no auth required)
curl http://localhost:7300/api/v1/health

# System status (requires auth)
curl -H "Authorization: Bearer SPARTA300_SECRET_TOKEN" \
     http://localhost:7300/api/v1/health/detailed
```

### 4. Access API Documentation

Open your browser and navigate to:
- **Swagger UI**: http://localhost:7300/docs
- **ReDoc**: http://localhost:7300/redoc

## Docker Quick Start

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f leonidas-core

# Stop all services
docker-compose down
```

### Access Services

- **ΛΕΩΝΙΔΑΣ-AI API**: http://localhost:7300
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/sparta_grafana_secret)

## Common Use Cases

### 1. Encrypt Data

```bash
curl -X POST http://localhost:7300/api/v1/command/encrypt \
     -H "Authorization: Bearer SPARTA300_SECRET_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "data": "Secret Spartan message"
     }'
```

### 2. Analyze Risk

```bash
curl -X POST http://localhost:7300/api/v1/command/analyze-risk \
     -H "Authorization: Bearer SPARTA300_SECRET_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "scenario_name": "Mission Alpha",
       "risk_factors": ["enemy_presence", "terrain"],
       "severity": 0.7,
       "complexity": 0.6,
       "available_resources": 0.8
     }'
```

### 3. Check Air-Gap Status

```bash
curl -H "Authorization: Bearer SPARTA300_SECRET_TOKEN" \
     http://localhost:7300/api/v1/command/check-airgap
```

### 4. Get System Metrics

```bash
curl -H "Authorization: Bearer SPARTA300_SECRET_TOKEN" \
     http://localhost:7300/api/v1/metrics/json
```

## Python SDK Usage

```python
import asyncio
import sys
sys.path.insert(0, '.')

from core.leonidasbrain import LeondasBrain
from phalanx.helot import HelotModule
from hoplites.spartanguard import SpartanGuard

async def main():
    # Initialize modules
    config = {
        'hardware': {'cpu_cores': 4},
        'current_workload': 0.5
    }
    
    # Create Λ-Core
    brain = LeondasBrain(config)
    print(f"Brain Status: {brain.get_status()}")
    
    # Monitor resources
    helot = HelotModule(config)
    survival = await helot.get_survival_probability()
    print(f"Survival Probability: {survival:.2%}")
    
    # Encrypt data
    guard = SpartanGuard(config)
    encrypted = await guard.encrypt("Secret message")
    decrypted = await guard.decrypt(encrypted)
    print(f"Encryption test: {'✅ SUCCESS' if decrypted == 'Secret message' else '❌ FAILED'}")

asyncio.run(main())
```

## Configuration

### Environment Variables

```bash
# Override auth token
export SPARTA_AUTH_TOKEN="your-secure-token-here"

# Set master key (if not using generated keys)
export SPARTA_MASTER_KEY="your-hex-encoded-key"
```

### Configuration File (config/settings.yaml)

```yaml
# Change these in production!
auth:
  auth_token: "CHANGE_THIS_IN_PRODUCTION"

# Air-Gap configuration
hoplites:
  shield_bearer:
    airgap_mode: "strict"  # strict | permissive | disabled
  
  weapon_master:
    external_access_enabled: false  # ⚠️ Compromises Air-Gap!

# Thermopylae configuration
phalanx:
  thermopylae:
    survival_threshold: 0.95
    thermopylae_armed: false  # ⚠️ DANGER: Auto-destruction!
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_core.py

# Run with coverage
pytest --cov=. --cov-report=html
```

## Troubleshooting

### Issue: Module not found

```bash
# Make sure you're in the virtual environment
source sparta-env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Permission denied on scripts

```bash
# Make scripts executable
chmod +x scripts/*.sh scripts/*.py
```

### Issue: Port 7300 already in use

```bash
# Find process using port 7300
lsof -i :7300

# Kill the process (replace PID)
kill -9 <PID>

# Or use a different port
python -m uvicorn api.server:app --port 7301
```

### Issue: Keys not generated

```bash
# Manually generate keys
python scripts/generate_keys.py
```

## Security Checklist

Before deploying to production:

- [ ] Change `auth_token` in `config/settings.yaml`
- [ ] Set `SPARTA_AUTH_TOKEN` environment variable
- [ ] Verify `config/spartan_keys.yaml` is NOT in Git
- [ ] Review Air-Gap settings (`airgap_mode`)
- [ ] Review Thermopylae settings (`thermopylae_armed`)
- [ ] Review external access settings (`external_access_enabled`)
- [ ] Set strong passwords for Docker services
- [ ] Enable HTTPS/TLS for production API
- [ ] Review firewall rules
- [ ] Set up monitoring and alerting

## Next Steps

1. **Read the Documentation**
   - [README.md](README.md) - Overview and installation
   - [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed architecture
   
2. **Explore the API**
   - Swagger UI: http://localhost:7300/docs
   - Try different commands and see responses
   
3. **Customize Configuration**
   - Edit `config/settings.yaml` to your needs
   - Adjust thresholds and parameters
   
4. **Set Up Monitoring**
   - Configure Prometheus alerts
   - Create Grafana dashboards
   
5. **Deploy to Production**
   - Use Docker Compose or Kubernetes
   - Configure proper secrets management
   - Set up backup for cryptographic keys

## Support and Resources

- **Documentation**: See [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md)
- **Issues**: Report bugs on GitHub Issues
- **License**: MIT License

---

**ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)** - *"Come and Take Them"*

> *"The strength of the Phalanx lies not in individual soldiers, but in their unity and discipline. So too does ΛΕΩΝΙΔΑΣ-AI gain its power from the seamless coordination of its modules."*
