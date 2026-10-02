"""
ΛΕΩΝΙΔΑΣ-AI PHALANX API Server
Server FastAPI principal pe port 7300
"""

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional
import asyncio
import hmac
import time
import yaml
import os
from loguru import logger

from core.leonidasbrain import LeondasBrain
from core.commandprocessor import CommandProcessor
from control.kronos_arbiter import KronosArbiter
from phalanx.helot import HelotModule
from phalanx.agoge import AgogeModule
from phalanx.krypteia import KrypteiaModule
from phalanx.thermopylae import ThermopylaeModule
from hoplites.spartanguard import SpartanGuard
from hoplites.shieldbearer import ShieldBearer
from hoplites.battleoracle import BattleOracle
from hoplites.weaponmaster import WeaponMaster
from hoplites.messenger import Messenger
from sparta.runtime import get_runtime as get_sparta_runtime


# Rădăcina repository-ului (folosită pentru căi relative din configurație)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Token-ul implicit de dezvoltare - NU trebuie folosit în producție
DEFAULT_AUTH_TOKEN = 'SPARTA300_SECRET_TOKEN'


# Configurare logger
logger.add("logs/leonidas_{time}.log", rotation="100 MB", retention="10 days", level="INFO")

# Security
security = HTTPBearer()

# Variabile globale pentru modulele sistemului
leonidas_brain = None
command_processor = None
config = {}


def get_expected_token(cfg: Optional[Dict[str, Any]] = None) -> str:
    """
    Rezolvă token-ul de autentificare așteptat.
    
    Prioritate: variabila de mediu SPARTA_AUTH_TOKEN > auth.auth_token (settings.yaml)
    > auth_token (format vechi, la rădăcină) > token-ul implicit de dezvoltare.
    
    Args:
        cfg: Configurația (implicit: configurația globală a serverului)
        
    Returns:
        Token-ul așteptat
    """
    cfg = config if cfg is None else cfg
    env_token = os.getenv('SPARTA_AUTH_TOKEN')
    if env_token:
        return env_token
    
    auth_section = cfg.get('auth')
    if isinstance(auth_section, dict) and auth_section.get('auth_token'):
        return auth_section['auth_token']
    
    return cfg.get('auth_token', DEFAULT_AUTH_TOKEN)


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verifică token-ul de autentificare (comparație în timp constant).
    
    Args:
        credentials: Credențialele HTTP
        
    Raises:
        HTTPException: Dacă token-ul este invalid
    """
    token = credentials.credentials
    expected_token = get_expected_token()
    
    if not hmac.compare_digest(token.encode('utf-8'), expected_token.encode('utf-8')):
        # Nu se loghează niciun fragment din token-ul primit
        logger.warning("🚫 Unauthorized access attempt (invalid token)")
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    return token


def get_section(cfg: Dict[str, Any], *path: str) -> Dict[str, Any]:
    """
    Extrage o secțiune imbricată din configurație (ex: phalanx → thermopylae).
    
    Dacă secțiunea nu există, returnează configurația rădăcină - compatibil
    cu configurațiile plate folosite anterior de module.
    
    Args:
        cfg: Configurația completă
        *path: Calea către secțiune
        
    Returns:
        Secțiunea de configurație pentru modul
    """
    section: Any = cfg
    for key in path:
        if not isinstance(section, dict) or key not in section:
            return cfg
        section = section[key]
    return section if isinstance(section, dict) else cfg


def load_master_key_hex(cfg: Dict[str, Any]) -> Optional[str]:
    """
    Încarcă cheia master AES-256 din config/spartan_keys.yaml (generat de
    scripts/generate_keys.py). Calea respectă phalanx.thermopylae.keys_path,
    astfel încât Thermopylae distruge exact fișierul folosit de Spartan Guard.
    
    Args:
        cfg: Configurația completă
        
    Returns:
        Cheia master în format hex, sau None dacă nu este disponibilă
    """
    thermopylae_cfg = get_section(cfg, 'phalanx', 'thermopylae')
    keys_path = thermopylae_cfg.get('keys_path', '/config/spartan_keys.yaml')
    base_path = thermopylae_cfg.get('base_path') or REPO_ROOT
    full_path = os.path.join(base_path, keys_path.lstrip('/'))
    
    if not os.path.exists(full_path):
        return None
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            keys = yaml.safe_load(f) or {}
        key_hex = keys.get('MASTER_AES_KEY_HEX')
        if key_hex and not str(key_hex).startswith('REPLACE_WITH'):
            logger.info(f"🔑 Master key loaded from {full_path}")
            return str(key_hex)
    except Exception as e:
        logger.error(f"❌ Error reading keys file {full_path}: {e}")
    
    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionează ciclul de viață al aplicației.
    """
    global leonidas_brain, command_processor, config
    
    logger.info("🚀 Starting ΛΕΩΝΙΔΑΣ-AI PHALANX...")
    app.state.start_time = time.time()
    
    # Încarcă configurația
    config = load_config()
    
    if get_expected_token(config) == DEFAULT_AUTH_TOKEN:
        logger.warning("⚠️ Default auth token in use - set SPARTA_AUTH_TOKEN before production use")
    
    # Inițializează modulele
    leonidas_brain, command_processor = await initialize_system(config)
    
    # Pornește bucla de homeostazie
    background_tasks = [asyncio.create_task(leonidas_brain.homeostasis_loop())]
    
    # Pornește Fractal Flux Pipeline (control.ffp.enabled în settings.yaml)
    ffp_config = get_section(config, 'control', 'ffp')
    if ffp_config is not config and ffp_config.get('enabled', False):
        background_tasks.append(asyncio.create_task(leonidas_brain.start_ffp()))
        logger.info("🔄 FFP Pipeline started in background")
    
    logger.info("✅ ΛΕΩΝΙΔΑΣ-AI PHALANX online - ΜΟΛΩΝ ΛΑΒΕ")
    
    yield
    
    # Cleanup la oprire
    logger.info("🛑 Shutting down ΛΕΩΝΙΔΑΣ-AI PHALANX...")
    leonidas_brain.stop_ffp()
    await leonidas_brain.shutdown()
    krypteia = leonidas_brain.modules.get('phalanx', {}).get('krypteia')
    if krypteia is not None and krypteia.is_monitoring:
        await krypteia.stop_monitoring()
    for task in background_tasks:
        task.cancel()
    

# Creează aplicația FastAPI
app = FastAPI(
    title="ΛΕΩΝΙΔΑΣ-AI PHALANX",
    description="Nucleu Decizional AI cu Arhitectură Spartană",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_config() -> dict:
    """
    Încarcă configurația din settings.yaml.
    
    Returns:
        Dicționar cu configurația
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logger.info(f"✅ Configuration loaded from {config_path}")
                return config
        else:
            logger.warning(f"⚠️ Config file not found: {config_path}, using defaults")
    except Exception as e:
        logger.error(f"❌ Error loading config: {e}")
    
    # Configurație default
    return {
        "system": {
            "name": "ΛΕΩΝΙΔΑΣ-AI PHALANX",
            "motto": "ΜΟΛΩΝ ΛΑΒΕ",
            "version": "0.1.0"
        },
        "hardware": {
            "cpu_cores": 4,
            "npu_tops": 50
        },
        "auth_token": "SPARTA300_SECRET_TOKEN"
    }


async def initialize_system(config: dict):
    """
    Inițializează toate modulele sistemului.
    
    Args:
        config: Configurația sistemului
        
    Returns:
        Tuple (leonidas_brain, command_processor)
    """
    # Inițializează Λ-Core
    brain = LeondasBrain(config)
    
    # Initialize Kronos-Arbiter
    cpu_cores = config.get('hardware', {}).get('cpu_cores', 4)
    brain.kronos = KronosArbiter(n_cores=cpu_cores)
    logger.info(f"⏱️ Kronos-Arbiter initialized with {cpu_cores} cores")
    
    # Inițializează modulele Phalanx (fiecare primește propria secțiune din settings.yaml)
    helot = HelotModule(get_section(config, 'phalanx', 'helot'))
    agoge = AgogeModule(get_section(config, 'phalanx', 'agoge'))
    krypteia = KrypteiaModule(get_section(config, 'phalanx', 'krypteia'))
    thermopylae = ThermopylaeModule(get_section(config, 'phalanx', 'thermopylae'))
    
    phalanx_modules = {
        'helot': helot,
        'agoge': agoge,
        'krypteia': krypteia,
        'thermopylae': thermopylae
    }
    
    await brain.initialize_phalanx(phalanx_modules)
    
    # Pornește monitorizarea Krypteia
    await krypteia.start_monitoring()
    
    # Inițializează modulele Hoplites
    guard_config = dict(get_section(config, 'hoplites', 'spartan_guard'))
    if not guard_config.get('master_key_hex'):
        master_key_hex = load_master_key_hex(config)
        if master_key_hex:
            guard_config['master_key_hex'] = master_key_hex
    guard = SpartanGuard(guard_config)
    shield = ShieldBearer(get_section(config, 'hoplites', 'shield_bearer'))
    oracle = BattleOracle(get_section(config, 'hoplites', 'battle_oracle'))
    weapon = WeaponMaster(get_section(config, 'hoplites', 'weapon_master'))
    messenger = Messenger(get_section(config, 'hoplites', 'messenger'), spartan_guard=guard)
    
    hoplite_modules = {
        'guard': guard,
        'shield': shield,
        'oracle': oracle,
        'weapon': weapon,
        'messenger': messenger
    }
    
    await brain.initialize_hoplites(hoplite_modules)
    
    # Inițializează Command Processor
    all_modules = {
        'phalanx': phalanx_modules,
        'hoplites': hoplite_modules
    }
    
    # SPARTA Foundation (comanda 'sparta_query'); sistemul pornește și fără ea
    try:
        all_modules['sparta'] = get_sparta_runtime()
    except Exception as e:
        logger.error(f"❌ SPARTA runtime unavailable: {e}")
    
    cmd_processor = CommandProcessor(all_modules)
    
    # Interconectare: Λ-Core folosește U (Factorul de Expansiune) al procesorului de comenzi
    brain.command_processor = cmd_processor
    
    return brain, cmd_processor


# Import routes
from api.routes import health, command, metrics, vault, sparta  # noqa: E402 - routes import server (circular), must follow app creation

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(command.router, prefix="/api/v1", tags=["commands"])
app.include_router(metrics.router, prefix="/api/v1", tags=["metrics"])
# Vault: toate endpoint-urile (inclusiv decriptarea) necesită autentificare
app.include_router(vault.router, prefix="/api/v1/vault", tags=["vault"],
                   dependencies=[Depends(verify_token)])
# SPARTA: raționament anti-halucinație peste Foundation (necesită autentificare)
app.include_router(sparta.router, prefix="/api/v1/sparta", tags=["sparta"],
                   dependencies=[Depends(verify_token)])


@app.get("/")
async def root():
    """
    Endpoint rădăcină.
    """
    return {
        "system": "ΛΕΩΝΙΔΑΣ-AI PHALANX",
        "motto": "ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)",
        "version": "0.1.0",
        "status": "online",
        "api_docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.server:app",
        host="0.0.0.0",
        port=7300,
        reload=False,
        log_level="info"
    )
