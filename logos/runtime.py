"""
Λ-Logos Runtime - the process-wide model instance.

The trained model is a *frozen artifact*: once models/logos-v1.npz exists it is
loaded as-is, even if the documentation changes later. Vectors stored in the
vault therefore stay comparable. Retraining is an explicit act
(`python -m logos train --force`), followed by a vault re-index.
"""

import os
import threading
from typing import Optional

from polis.log import logger

from logos.corpus import REPO_ROOT, build_corpus
from logos.model import LogosEmbedder

DEFAULT_ARTIFACT = os.path.join(REPO_ROOT, "models", "logos-v1.npz")

_model: Optional[LogosEmbedder] = None
_lock = threading.Lock()


def artifact_path() -> str:
    """Model file location (env LOGOS_MODEL_PATH overrides the default)."""
    return os.getenv("LOGOS_MODEL_PATH") or DEFAULT_ARTIFACT


def train_default(path: Optional[str] = None, root: str = REPO_ROOT) -> LogosEmbedder:
    """
    Train on the repository corpus and save the artifact.

    Args:
        path: Destination (default: artifact_path())
        root: Repository root for the corpus

    Returns:
        Trained model
    """
    corpus = build_corpus(root)
    model = LogosEmbedder().fit([text for _, text in corpus])
    try:
        model.save(path or artifact_path())
    except OSError as e:
        logger.warning(f"⚠️ Λ-Logos artifact not saved ({e}); model kept in memory")
    return model


def get_model() -> LogosEmbedder:
    """
    Return the shared model: load the frozen artifact, or train it once.

    Returns:
        Trained LogosEmbedder
    """
    global _model
    with _lock:
        if _model is None:
            path = artifact_path()
            if os.path.exists(path):
                _model = LogosEmbedder.load(path)
                logger.info(f"🧠 Λ-Logos loaded: {_model.model_id}")
            else:
                logger.info("🧠 Λ-Logos artifact missing - training on the project corpus")
                _model = train_default(path)
        return _model


def reset_model() -> None:
    """Drop the cached model (tests, explicit retraining)."""
    global _model
    with _lock:
        _model = None
