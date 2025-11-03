"""
ΛΕΩΝΙΔΑΣ-AI PHALANX API Server
Server FastAPI principal pe port 7300
"""

from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
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


# Configurare logger
logger.add("logs/leonidas_{time}.log", rotation="100 MB", retention="10 days", level="INFO")

# Security
security = HTTPBearer()

# Variabile globale pentru modulele sistemului
leonidas_brain = None
command_processor = None
config = {}


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verifică token-ul de autentificare.
    
    Args:
        credentials: Credențialele HTTP
        
    Raises:
        HTTPException: Dacă token-ul este invalid
    """
    token = credentials.credentials
    expected_token = os.getenv('SPARTA_AUTH_TOKEN', config.get('auth_token', 'SPARTA300_SECRET_TOKEN'))
    
    if token != expected_token:
        logger.warning(f"🚫 Unauthorized access attempt with token: {token[:10]}...")
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    return token


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionează ciclul de viață al aplicației.
    """
    global leonidas_brain, command_processor, config
    
    logger.info("🚀 Starting ΛΕΩΝΙΔΑΣ-AI PHALANX...")
    
    # Încarcă configurația
    config = load_config()
    
    # Inițializează modulele
    leonidas_brain, command_processor = await initialize_system(config)
    
    # Pornește bucla de homeostazie
    import asyncio
    homeostasis_task = asyncio.create_task(leonidas_brain.homeostasis_loop())
    
    logger.info("✅ ΛΕΩΝΙΔΑΣ-AI PHALANX online - ΜΟΛΩΝ ΛΑΒΕ")
    
    yield
    
    # Cleanup la oprire
    logger.info("🛑 Shutting down ΛΕΩΝΙΔΑΣ-AI PHALANX...")
    await leonidas_brain.shutdown()
    homeostasis_task.cancel()
    

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
    
    # Inițializează modulele Phalanx
    helot = HelotModule(config)
    agoge = AgogeModule(config)
    krypteia = KrypteiaModule(config)
    thermopylae = ThermopylaeModule(config)
    
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
    guard = SpartanGuard(config)
    shield = ShieldBearer(config)
    oracle = BattleOracle(config)
    weapon = WeaponMaster(config)
    messenger = Messenger(config, spartan_guard=guard)
    
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
    
    cmd_processor = CommandProcessor(all_modules)
    
    return brain, cmd_processor


# Import routes
from api.routes import health, command, metrics

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(command.router, prefix="/api/v1", tags=["commands"])
app.include_router(metrics.router, prefix="/api/v1", tags=["metrics"])


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
