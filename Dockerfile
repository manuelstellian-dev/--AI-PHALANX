# ΛΕΩΝΙΔΑΣ-AI PHALANX - Dockerfile
# Container image pentru Falanga Digitală

FROM python:3.11-slim

# Metadata
LABEL maintainer="ΛΕΩΝΙΔΑΣ-AI PHALANX"
LABEL version="0.1.0"
LABEL description="Nucleu Decizional AI cu Arhitectură Spartană"

# Set environment
# Λ-Logos (modelul propriu) este antrenat la build din corpusul proiectului:
# fără modele externe, fără descărcări la runtime (Air-Gap)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    LOGOS_MODEL_PATH=/app/models/logos-v1.npz

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

# Copy application code (toate pachetele importate de api.server)
COPY core/ ./core/
COPY control/ ./control/
COPY parallel_execution/ ./parallel_execution/
COPY phalanx/ ./phalanx/
COPY hoplites/ ./hoplites/
COPY vault/ ./vault/
COPY sparta/ ./sparta/
COPY logos/ ./logos/
COPY api/ ./api/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Corpusul Λ-Logos: memoria proiectului + documentația (sursă de cunoaștere, nu cod)
COPY .memory/ ./.memory/
COPY docs/ ./docs/
COPY *.md ./

# Antrenează Λ-Logos o singură dată; artefactul (amprentat) este înghețat în imagine
RUN python -m logos train --out /app/models/logos-v1.npz

# Create necessary directories
RUN mkdir -p /app/data/vault /app/data/encrypted_vault /app/logs

# Expose API port
EXPOSE 7300

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:7300/api/v1/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "7300"]
