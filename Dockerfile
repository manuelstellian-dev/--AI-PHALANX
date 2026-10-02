# ΛΕΩΝΙΔΑΣ-AI PHALANX - Dockerfile
# Container image pentru Falanga Digitală

FROM python:3.11-slim

# Metadata
LABEL maintainer="ΛΕΩΝΙΔΑΣ-AI PHALANX"
LABEL version="0.1.0"
LABEL description="Nucleu Decizional AI cu Arhitectură Spartană"

# Set environment
# PIP_EXTRA_INDEX_URL: roți PyTorch doar-CPU (fără ~GB de biblioteci CUDA)
# HF_HUB_OFFLINE: modelul de embedding este inclus în imagine - fără rețea la runtime (Air-Gap)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cpu \
    HF_HOME=/app/models

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the RAG embedding model at build time
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
ENV HF_HUB_OFFLINE=1

# Copy application code (toate pachetele importate de api.server)
COPY core/ ./core/
COPY control/ ./control/
COPY parallel_execution/ ./parallel_execution/
COPY phalanx/ ./phalanx/
COPY hoplites/ ./hoplites/
COPY vault/ ./vault/
COPY sparta/ ./sparta/
COPY api/ ./api/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Create necessary directories
RUN mkdir -p /app/data/vault /app/data/encrypted_vault /app/logs

# Expose API port
EXPOSE 7300

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:7300/api/v1/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "7300"]
