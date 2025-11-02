#!/bin/bash

# ΛΕΩΝΙΔΑΣ-AI PHALANX - Script de Instalare
# Instalează mediul virtual și dependențele necesare pentru Falanga Digitală

set -e

echo "🏛️  ΛΕΩΝΙΔΑΣ-AI PHALANX - Installation Script"
echo "================================================"
echo ""

# Culori pentru output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detectează directorul repository-ului
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "📂 Repository directory: $REPO_DIR"
echo ""

# Verifică Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Creează mediul virtual sparta-env
if [ ! -d "sparta-env" ]; then
    echo "🔧 Creating virtual environment (sparta-env)..."
    python3 -m venv sparta-env
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi

# Activează mediul virtual
echo "⚡ Activating virtual environment..."
source sparta-env/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Instalează dependențele
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found, installing minimal dependencies...${NC}"
    pip install fastapi uvicorn loguru pyyaml cryptography psutil pydantic
fi

# Creează directoare necesare
echo "📁 Creating necessary directories..."
mkdir -p data/encrypted_vault
mkdir -p logs
mkdir -p config
echo -e "${GREEN}✅ Directories created${NC}"

# Generează cheile criptografice
echo "🔑 Generating cryptographic keys..."
if [ -f "scripts/generate_keys.py" ]; then
    python3 scripts/generate_keys.py
    echo -e "${GREEN}✅ Cryptographic keys generated${NC}"
else
    echo -e "${YELLOW}⚠️  generate_keys.py not found, skipping key generation${NC}"
fi

# Verifică configurația
if [ -f "config/settings.yaml" ]; then
    echo -e "${GREEN}✅ Configuration file found${NC}"
else
    echo -e "${YELLOW}⚠️  settings.yaml not found${NC}"
fi

echo ""
echo "================================================"
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo "🗡️  To activate ΛΕΩΝΙΔΑΣ-AI PHALANX:"
echo "   1. Activate the virtual environment:"
echo "      source sparta-env/bin/activate"
echo "   2. Run the activation script:"
echo "      bash scripts/activate_leonidas.sh"
echo ""
echo "   Or use the combined command:"
echo "      source sparta-env/bin/activate && bash scripts/activate_leonidas.sh"
echo ""
echo "🛡️  ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)"
echo "================================================"
