"""
Λ-Logos - ΛΕΩΝΙΔΑΣ-AI PHALANX's own embedding model.

ΜΟΛΩΝ ΛΑΒΕ - no external model, no downloaded weights, no network.

- LogosEmbedder: latent semantic embedder (hashed features → TF-IDF → randomized SVD)
- build_corpus: training documents from SPARTA concepts, .memory/ and docs
- get_model / train_default: frozen, fingerprinted model artifact (models/logos-v1.npz)
"""

from logos.model import LogosEmbedder, MODEL_FAMILY, DEFAULT_DIM
from logos.corpus import build_corpus
from logos.runtime import get_model, reset_model, train_default, artifact_path

__all__ = [
    "LogosEmbedder",
    "MODEL_FAMILY",
    "DEFAULT_DIM",
    "build_corpus",
    "get_model",
    "reset_model",
    "train_default",
    "artifact_path",
]
