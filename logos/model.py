"""
Λ-Logos Model - ΛΕΩΝΙΔΑΣ's own embedding model.

No external model, no downloaded weights, no network. The model is learned from
the project's own corpus (SPARTA concepts + documentation) with classic,
fully inspectable linear algebra:

    text ──► hashed sparse features (logos.tokenizer)
         ──► TF-IDF (idf learned from the corpus)
         ──► L2 normalization
         ──► projection onto the top-k latent semantic axes (randomized SVD)
         ──► L2-normalized dense vector (dimension `dim`, zero-padded if k < dim)

Before training, the model still works: it falls back to a deterministic
Johnson–Lindenstrauss random projection of the same features (lexical
similarity only). Training adds latent semantics (co-occurrence structure).

Every trained model carries a fingerprint of its parameters and corpus, so a
stored vector can always be traced to the exact model that produced it.
"""

import hashlib
import json
import os
from typing import Dict, Iterable, List, Optional, Sequence

import numpy as np
from loguru import logger
from scipy import sparse

from logos.tokenizer import hashed_features

MODEL_FAMILY = "logos-v1"
DEFAULT_N_FEATURES = 2 ** 15
DEFAULT_DIM = 384


class LogosEmbedder:
    """
    Λ-Logos latent semantic embedder.

    Attributes:
        n_features: Size of the hashed feature space
        dim: Output dimension (vectors are zero-padded when rank < dim)
        seed: Seed for every random choice (determinism)
        idf: Learned inverse document frequencies (None until trained)
        components: Latent axes, shape (n_features, k) (None until trained)
        singular_values: Strength of each latent axis
        fingerprint: SHA-256 of parameters + training corpus
    """

    def __init__(self, n_features: int = DEFAULT_N_FEATURES, dim: int = DEFAULT_DIM,
                 seed: int = 1337, oversample: int = 10, power_iterations: int = 4):
        if n_features < 2 or dim < 1:
            raise ValueError("n_features must be >= 2 and dim >= 1")
        self.n_features = n_features
        self.dim = dim
        self.seed = seed
        self.oversample = oversample
        self.power_iterations = power_iterations
        self.idf: Optional[np.ndarray] = None
        self.components: Optional[np.ndarray] = None
        self.singular_values: Optional[np.ndarray] = None
        self.fingerprint: Optional[str] = None
        self.corpus_size = 0
        self._jl_cache: Dict[int, np.ndarray] = {}

    # ------------------------------------------------------------------ state

    @property
    def is_trained(self) -> bool:
        """True once fit() has learned IDF and latent axes."""
        return self.components is not None

    @property
    def model_id(self) -> str:
        """Identifier stored next to every vector (family + fingerprint)."""
        if self.fingerprint is None:
            return f"{MODEL_FAMILY}:untrained:{self.n_features}x{self.dim}:s{self.seed}"
        return f"{MODEL_FAMILY}:{self.fingerprint[:12]}"

    # --------------------------------------------------------------- features

    def _matrix(self, texts: Sequence[str]) -> sparse.csr_matrix:
        """Hashed (unweighted) feature matrix, one row per text."""
        rows, cols, vals = [], [], []
        for i, text in enumerate(texts):
            for j, v in hashed_features(text, self.n_features).items():
                rows.append(i)
                cols.append(j)
                vals.append(v)
        return sparse.csr_matrix(
            (np.asarray(vals, dtype=np.float64), (rows, cols)),
            shape=(len(texts), self.n_features),
        )

    def _weight_and_normalize(self, X: sparse.csr_matrix) -> sparse.csr_matrix:
        """Apply IDF (if trained) and L2-normalize each row."""
        if self.idf is not None:
            X = X @ sparse.diags(self.idf)
        X = sparse.csr_matrix(X)
        norms = np.sqrt(np.asarray(X.multiply(X).sum(axis=1)).ravel())
        norms[norms == 0] = 1.0
        return sparse.diags(1.0 / norms) @ X

    # ---------------------------------------------------------------- training

    @staticmethod
    def corpus_fingerprint(texts: Iterable[str], params: Dict) -> str:
        """SHA-256 over model parameters and every corpus text (in order)."""
        h = hashlib.sha256(json.dumps(params, sort_keys=True).encode("utf-8"))
        for text in texts:
            h.update(b"\x1e")
            h.update(text.encode("utf-8"))
        return h.hexdigest()

    def _params(self) -> Dict:
        return {"family": MODEL_FAMILY, "n_features": self.n_features, "dim": self.dim,
                "seed": self.seed, "oversample": self.oversample,
                "power_iterations": self.power_iterations}

    def fit(self, texts: Sequence[str]) -> "LogosEmbedder":
        """
        Learn IDF weights and latent semantic axes from a corpus.

        Args:
            texts: Training documents (order matters only for the fingerprint)

        Returns:
            self
        """
        texts = [t for t in texts if t and t.strip()]
        if len(texts) < 2:
            raise ValueError("Λ-Logos needs at least 2 non-empty documents to train")

        counts = self._matrix(texts)
        n_docs = counts.shape[0]
        df = np.asarray((counts != 0).sum(axis=0)).ravel()
        self.idf = (np.log((1.0 + n_docs) / (1.0 + df)) + 1.0).astype(np.float64)

        X = self._weight_and_normalize(counts)
        k = min(self.dim, n_docs)
        V, S = self._randomized_svd(X, k)

        keep = S > 1e-10
        # float32 halves memory; output vectors are float32 anyway
        self.components = np.ascontiguousarray(V[:, keep], dtype=np.float32)
        self.singular_values = S[keep]
        self.corpus_size = n_docs
        self.fingerprint = self.corpus_fingerprint(texts, self._params())
        logger.info(f"🧠 Λ-Logos trained: {n_docs} documents, {self.components.shape[1]} latent axes, "
                    f"id={self.model_id}")
        return self

    def _randomized_svd(self, X: sparse.csr_matrix, k: int):
        """
        Halko–Martinsson–Tropp randomized SVD (deterministic via seed).

        Returns:
            (V, S): right singular vectors (n_features × k) and singular values
        """
        rng = np.random.default_rng(self.seed)
        n_docs = X.shape[0]
        width = min(k + self.oversample, n_docs)
        Omega = rng.standard_normal((X.shape[1], width))
        Y = X @ Omega
        for _ in range(self.power_iterations):
            Y, _ = np.linalg.qr(Y)
            Y = X @ (X.T @ Y)
        Q, _ = np.linalg.qr(Y)
        B = np.asarray((X.T @ Q).T)          # (width × n_features), dense
        _, S, Vt = np.linalg.svd(B, full_matrices=False)
        k = min(k, len(S))
        V = Vt[:k].T
        # Sign convention: largest-magnitude loading positive (stable across runs)
        signs = np.sign(V[np.abs(V).argmax(axis=0), np.arange(k)])
        signs[signs == 0] = 1.0
        return V * signs, S[:k]

    # --------------------------------------------------------------- embedding

    def _jl_row(self, j: int) -> np.ndarray:
        """Deterministic random-projection row for feature j (untrained mode)."""
        row = self._jl_cache.get(j)
        if row is None:
            row = np.random.default_rng([self.seed, j]).standard_normal(self.dim) / np.sqrt(self.dim)
            if len(self._jl_cache) < 200_000:
                self._jl_cache[j] = row
        return row

    def embed_batch(self, texts: Sequence[str]) -> np.ndarray:
        """
        Embed texts into L2-normalized vectors.

        Args:
            texts: Texts to embed

        Returns:
            Array of shape (len(texts), dim), dtype float32
        """
        texts = list(texts)
        if not texts:
            return np.zeros((0, self.dim), dtype=np.float32)

        X = self._weight_and_normalize(self._matrix(texts))
        out = np.zeros((len(texts), self.dim), dtype=np.float64)

        if self.is_trained:
            Z = np.asarray(X @ self.components)
            out[:, :Z.shape[1]] = Z
        else:
            X = sparse.csr_matrix(X)
            for i in range(X.shape[0]):
                start, end = X.indptr[i], X.indptr[i + 1]
                for j, v in zip(X.indices[start:end], X.data[start:end]):
                    out[i] += v * self._jl_row(int(j))

        norms = np.linalg.norm(out, axis=1)
        norms[norms == 0] = 1.0
        return (out / norms[:, None]).astype(np.float32)

    def embed(self, text: str) -> np.ndarray:
        """Embed a single text (shape (dim,))."""
        return self.embed_batch([text])[0]

    def similarity(self, a: str, b: str) -> float:
        """Cosine similarity between two texts."""
        va, vb = self.embed_batch([a, b])
        return float(np.dot(va, vb))

    # ------------------------------------------------------------- persistence

    def save(self, path: str) -> None:
        """
        Persist a trained model (.npz; components stored as float16).

        Args:
            path: Destination file
        """
        if not self.is_trained:
            raise RuntimeError("Only a trained Λ-Logos model can be saved")
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        meta = {**self._params(), "fingerprint": self.fingerprint, "corpus_size": self.corpus_size,
                "model_id": self.model_id}
        tmp = path + ".tmp.npz"
        np.savez_compressed(
            tmp,
            components=self.components.astype(np.float16),
            idf=self.idf.astype(np.float32),
            singular_values=self.singular_values.astype(np.float64),
            meta=np.array(json.dumps(meta)),
        )
        os.replace(tmp, path)
        logger.info(f"💾 Λ-Logos saved: {path} ({self.model_id})")

    @classmethod
    def load(cls, path: str) -> "LogosEmbedder":
        """
        Load a model saved with save(). Uses allow_pickle=False (no code execution).

        Args:
            path: Model file

        Returns:
            Trained LogosEmbedder
        """
        with np.load(path, allow_pickle=False) as data:
            meta = json.loads(str(data["meta"]))
            if meta.get("family") != MODEL_FAMILY:
                raise ValueError(f"Not a {MODEL_FAMILY} model: {meta.get('family')}")
            model = cls(n_features=meta["n_features"], dim=meta["dim"], seed=meta["seed"],
                        oversample=meta["oversample"], power_iterations=meta["power_iterations"])
            model.components = np.ascontiguousarray(data["components"], dtype=np.float32)
            model.idf = data["idf"].astype(np.float64)
            model.singular_values = data["singular_values"]
        model.fingerprint = meta["fingerprint"]
        model.corpus_size = meta["corpus_size"]
        return model

    def info(self) -> Dict:
        """Human-readable model description."""
        return {
            "model_id": self.model_id,
            "trained": self.is_trained,
            "n_features": self.n_features,
            "dim": self.dim,
            "latent_axes": 0 if self.components is None else int(self.components.shape[1]),
            "corpus_size": self.corpus_size,
            "fingerprint": self.fingerprint,
        }


def top_terms(model: LogosEmbedder, texts: List[str], axis: int, n: int = 10) -> List[str]:
    """
    Explain a latent axis by the corpus words that load on it most strongly.

    Args:
        model: Trained model
        texts: Corpus to draw candidate words from
        axis: Latent axis index
        n: Number of terms

    Returns:
        Words with the highest loading on the axis
    """
    from logos.tokenizer import words, _hash
    if not model.is_trained:
        raise RuntimeError("Model is not trained")
    vocab = sorted({w for t in texts for w in words(t)})
    scored = []
    for w in vocab:
        j, sign = _hash("w:" + w, model.n_features)
        scored.append((sign * model.components[j, axis] * model.idf[j], w))
    scored.sort(reverse=True)
    return [w for _, w in scored[:n]]
