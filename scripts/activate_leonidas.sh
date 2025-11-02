#!/bin/bash

# ΛΕΩΝΙΔΑΣ-AI PHALANX - Script de Activare
# Pornește serverul API al Falangei Digitale

set -e

# Culori pentru output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║            ΛΕΩΝΙΔΑΣ-AI PHALANX                                ║"
echo "║            Nucleu Decizional cu Arhitectură Spartană         ║"
echo "║                                                                ║"
echo "║            ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)                           ║"
echo "║            \"Come and Take Them\"                               ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Detectează directorul repository-ului
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo -e "${BLUE}📂 Repository: $REPO_DIR${NC}"
echo ""

# Verifică dacă mediul virtual există
if [ ! -d "sparta-env" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo "   Please run: bash scripts/install_sparta.sh"
    exit 1
fi

# Verifică dacă mediul virtual este activat
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚡ Activating virtual environment...${NC}"
    source sparta-env/bin/activate
fi

echo -e "${GREEN}✅ Virtual environment active${NC}"

# Verifică dependențele
echo -e "${BLUE}🔍 Checking dependencies...${NC}"
python3 -c "import fastapi, uvicorn, loguru, yaml, cryptography" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All dependencies available${NC}"
else
    echo -e "${RED}❌ Missing dependencies. Run: bash scripts/install_sparta.sh${NC}"
    exit 1
fi

# Verifică configurația
if [ ! -f "config/settings.yaml" ]; then
    echo -e "${YELLOW}⚠️  settings.yaml not found, using defaults${NC}"
fi

# Verifică cheile criptografice
if [ ! -f "config/spartan_keys.yaml" ]; then
    echo -e "${YELLOW}⚠️  spartan_keys.yaml not found${NC}"
    echo -e "${YELLOW}   Cryptographic keys will be generated automatically${NC}"
fi

# Afișează informații despre sistem
echo ""
echo -e "${MAGENTA}🏛️  System Configuration:${NC}"
echo -e "   • API Port: ${GREEN}7300${NC}"
echo -e "   • Air-Gap Mode: ${GREEN}STRICT${NC}"
echo -e "   • Encryption: ${GREEN}AES-256-GCM${NC}"
echo -e "   • Auth Token: ${YELLOW}SPARTA300_SECRET_TOKEN${NC} (change in production!)"
echo ""

# Opțiuni de pornire
echo -e "${CYAN}Select startup mode:${NC}"
echo "   1) Start API Server (Production Mode)"
echo "   2) Start API Server (Development Mode with reload)"
echo "   3) Run Tests"
echo "   4) Show System Status"
echo "   5) Exit"
echo ""
read -p "Enter your choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}🚀 Starting ΛΕΩΝΙΔΑΣ-AI PHALANX API Server (Production Mode)...${NC}"
        echo ""
        python3 -m uvicorn api.server:app --host 0.0.0.0 --port 7300 --log-level info
        ;;
    2)
        echo ""
        echo -e "${GREEN}🚀 Starting ΛΕΩΝΙΔΑΣ-AI PHALANX API Server (Development Mode)...${NC}"
        echo ""
        python3 -m uvicorn api.server:app --host 0.0.0.0 --port 7300 --reload --log-level debug
        ;;
    3)
        echo ""
        echo -e "${GREEN}🧪 Running Tests...${NC}"
        echo ""
        if [ -f "tests/run_tests.py" ]; then
            python3 tests/run_tests.py
        else
            echo -e "${YELLOW}⚠️  No tests found${NC}"
        fi
        ;;
    4)
        echo ""
        echo -e "${GREEN}📊 System Status:${NC}"
        echo ""
        python3 -c "
import sys
sys.path.insert(0, '.')
from core.leonidasbrain import LeondasBrain
from phalanx.helot import HelotModule
import asyncio

async def show_status():
    config = {'hardware': {'cpu_cores': 4}, 'current_workload': 0.5}
    brain = LeondasBrain(config)
    helot = HelotModule(config)
    
    print('🛡️  ΛΕΩΝΙΔΑΣ-AI PHALANX Status')
    print('=' * 50)
    print(f'Brain Status: {brain.get_status()}')
    print(f'Survival Probability: {await helot.get_survival_probability():.2%}')
    print(f'Resources: {await helot.monitor_resources()}')
    print('=' * 50)

asyncio.run(show_status())
"
        ;;
    5)
        echo -e "${CYAN}Exiting...${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting...${NC}"
        exit 1
        ;;
esac
