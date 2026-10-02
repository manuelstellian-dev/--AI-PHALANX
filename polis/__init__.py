"""
polis — the foundation of ΛΕΩΝΙΔΑΣ-AI PHALANX.

ΜΟΛΩΝ ΛΑΒΕ. Every capability the system needs below its own modules is built
here from first principles, on the only substrate the system accepts: the
Python interpreter and its standard library (.memory LAW-015).

Modules:
- log        structured logging (replaces loguru)
- yamlite    YAML subset parser and emitter (replaces PyYAML)
- sysinfo    CPU, memory, disk, network connections (replaces psutil)
- graph      directed graph (replaces networkx)
- crypto     AES-256, GCM, HKDF, Fernet-compatible reader (replaces cryptography)
- linalg     dense and sparse linear algebra, QR, eigen, randomized SVD (replaces numpy/scipy)
- http       models, validation, routing, ASGI-free server and client (replaces fastapi/pydantic/uvicorn/httpx)
- testing    test runner (replaces pytest)
- lint       static checker (replaces ruff)
- coverage   line coverage (replaces coverage.py)
"""

__version__ = "1.0.0"
