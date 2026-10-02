"""
Tests for Λ-Logos, ΛΕΩΝΙΔΑΣ's own embedding model.

Covers determinism, the untrained (lexical) fallback, training, persistence,
benchmark quality, the vector-store integration, and the guarantee that no
external model or ML runtime is used by default.
"""

import os
import subprocess
import sys

import numpy as np
import pytest

from logos import LogosEmbedder, build_corpus, get_model
from logos.benchmark import QUERIES, evaluate
from logos.tokenizer import hashed_features, normalize, words
from sparta import SemanticFoundation, DEFAULT_MEMORY_PATH

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

SMALL_CORPUS = [
    "Energy cannot be created or destroyed, only transformed between forms.",
    "Entropy measures disorder and grows in isolated thermodynamic systems.",
    "Natural selection: organisms adapted to their environment reproduce more.",
    "DNA stores genetic information in sequences of nucleotides.",
    "Recursion solves a problem by calling the same function on smaller inputs.",
    "Encryption protects data confidentiality using secret keys.",
    "The phalanx was a dense formation of heavily armed Spartan infantry.",
    "Thermopylae was a narrow pass defended by Leonidas and his soldiers.",
]


@pytest.fixture(scope="module")
def foundation():
    f = SemanticFoundation()
    f.load_memory(DEFAULT_MEMORY_PATH)
    return f


class TestTokenizer:

    def test_normalization_folds_diacritics_and_case(self):
        assert normalize("Ștefan ÎNVAȚĂ") == "stefan invata"
        assert words("Λ-TAS și ΜΟΛΩΝ") == ["λ", "tas", "si", "μολων"]

    def test_hashing_is_stable_and_bounded(self):
        a = hashed_features("Spartan phalanx formation", 1024)
        b = hashed_features("Spartan phalanx formation", 1024)
        assert a == b
        assert all(0 <= j < 1024 for j in a)

    def test_empty_text_has_no_features(self):
        assert hashed_features("   ", 64) == {}


class TestUntrainedModel:

    def test_deterministic_unit_vectors(self):
        m1, m2 = LogosEmbedder(dim=64), LogosEmbedder(dim=64)
        v1, v2 = m1.embed("Spartan shield"), m2.embed("Spartan shield")
        assert v1.shape == (64,)
        assert np.allclose(v1, v2)
        assert np.linalg.norm(v1) == pytest.approx(1.0, abs=1e-5)
        assert m1.model_id.startswith("logos-v1:untrained")

    def test_lexical_similarity(self):
        m = LogosEmbedder(dim=128)
        assert m.similarity("energy conservation law", "law of energy conservation") > \
            m.similarity("energy conservation law", "Spartan infantry formation")

    def test_empty_inputs(self):
        m = LogosEmbedder(dim=16)
        assert m.embed_batch([]).shape == (0, 16)
        assert np.allclose(m.embed(""), 0.0)


class TestTraining:

    def test_fit_learns_axes_and_fingerprint(self):
        m = LogosEmbedder(n_features=4096, dim=32).fit(SMALL_CORPUS)
        assert m.is_trained
        assert m.components.shape[0] == 4096
        assert 1 <= m.components.shape[1] <= len(SMALL_CORPUS)
        assert m.model_id == f"logos-v1:{m.fingerprint[:12]}"
        # Vectors are zero-padded to the declared dimension
        assert m.embed("energy").shape == (32,)

    def test_training_is_deterministic(self):
        a = LogosEmbedder(n_features=4096, dim=16).fit(SMALL_CORPUS)
        b = LogosEmbedder(n_features=4096, dim=16).fit(SMALL_CORPUS)
        assert a.fingerprint == b.fingerprint
        assert np.allclose(a.embed("phalanx at Thermopylae"), b.embed("phalanx at Thermopylae"), atol=1e-6)

    def test_fingerprint_tracks_corpus(self):
        a = LogosEmbedder(n_features=4096, dim=16).fit(SMALL_CORPUS)
        b = LogosEmbedder(n_features=4096, dim=16).fit(SMALL_CORPUS + ["one more document about bronze shields"])
        assert a.fingerprint != b.fingerprint

    def test_needs_two_documents(self):
        with pytest.raises(ValueError):
            LogosEmbedder().fit(["only one"])

    def test_invalid_parameters(self):
        with pytest.raises(ValueError):
            LogosEmbedder(n_features=1)

    def test_save_load_roundtrip(self, tmp_path):
        m = LogosEmbedder(n_features=4096, dim=16).fit(SMALL_CORPUS)
        path = str(tmp_path / "model.npz")
        m.save(path)
        loaded = LogosEmbedder.load(path)
        assert loaded.model_id == m.model_id
        assert np.allclose(loaded.embed("Leonidas"), m.embed("Leonidas"), atol=1e-2)  # float16 storage
        assert loaded.info()["trained"] is True

    def test_untrained_model_cannot_be_saved(self, tmp_path):
        with pytest.raises(RuntimeError):
            LogosEmbedder().save(str(tmp_path / "x.npz"))


class TestProjectModel:
    """The default model trained on the project's own corpus."""

    def test_corpus_is_local_and_deterministic(self):
        a, b = build_corpus(REPO_ROOT), build_corpus(REPO_ROOT)
        assert a == b
        sources = {src.split(":")[0].split("#")[0] for src, _ in a}
        assert "sparta" in sources
        assert any(src.endswith(".md") for src in sources)

    def test_default_model_is_trained(self):
        model = get_model()
        assert model.is_trained
        assert model.dim == 384

    def test_benchmark_beats_lexical_baseline(self, foundation):
        trained = evaluate(get_model(), foundation.concepts)
        lexical = evaluate(LogosEmbedder(), foundation.concepts)
        assert trained["queries"] == len(QUERIES)
        # Measured at introduction (2026-10-02): MRR 0.68, R@5 0.86 vs lexical 0.53 / 0.61
        assert trained["mrr"] > lexical["mrr"]
        assert trained["recall_at_5"] >= 0.75
        assert trained["mean_rank"] < lexical["mean_rank"]


class TestVectorStoreIntegration:

    def test_vault_uses_own_model_by_default(self, tmp_path):
        from vault.spartan_vault import SpartanVault
        vault = SpartanVault(storage_path=str(tmp_path))
        vault.store_with_embedding(id="d1", text="Energy is conserved in closed systems")
        vault.store_with_embedding(id="d2", text="Spartan hoplites fought in a phalanx")
        results = vault.semantic_search("conservation of energy", top_k=2)
        assert results[0]['id'] == "d1"
        assert vault.vector_store.model_id.startswith("logos-v1:")

    def test_unregistered_backend_is_refused(self, tmp_path):
        """Nothing outside Λ-Logos is ever loaded implicitly (LAW-015)."""
        import vault.vector_store as vs
        store = vs.SpartanVectorStore(model_name="all-MiniLM-L6-v2", storage_path=str(tmp_path))
        with pytest.raises(RuntimeError, match="No embedding backend registered"):
            store.embed_text("x")

    def test_external_backend_still_available_as_opt_in(self, tmp_path):
        """The plug-in capability is preserved: an explicitly registered encoder is used."""
        import vault.vector_store as vs
        
        class StubEncoder:  # any operator-supplied encoder with encode()
            def __init__(self, name):
                self.name = name
            
            def encode(self, texts, convert_to_numpy=True, show_progress_bar=False):
                return np.ones(384, dtype=np.float32)
        
        vs.register_backend("stub-encoder", StubEncoder)
        try:
            store = vs.SpartanVectorStore(model_name="stub-encoder", storage_path=str(tmp_path))
            assert store.embed_text("x").shape == (384,)
            assert store.model_id == "registered:stub-encoder"
        finally:
            vs.unregister_backend("stub-encoder")

    def test_model_change_marks_vectors_stale_and_reindex_fixes(self, tmp_path):
        import json
        from vault.spartan_vault import SpartanVault
        vault = SpartanVault(storage_path=str(tmp_path))
        vault.store_with_embedding(id="s1", text="classified energy research")
        vault.save_to_disk()

        # Simulate vectors produced by another model version
        json_path = tmp_path / "vectors" / "vector_store.json"
        data = json.loads(json_path.read_text())
        data["model_id"] = "logos-v1:000000000000"
        json_path.write_text(json.dumps(data))

        reopened = SpartanVault(storage_path=str(tmp_path))
        reopened.vector_store.embed_text("trigger model load")
        assert reopened.vector_store.stale_embeddings is True

        assert reopened.reindex() == 1
        assert reopened.vector_store.stale_embeddings is False
        # Re-embedded from decrypted plaintext; the index still holds only the marker
        assert reopened.vector_store.get_entry("s1").text == "[ENCRYPTED]"
        assert reopened.semantic_search("energy research", top_k=1)[0]['id'] == "s1"


def test_no_external_ml_runtime_is_imported():
    """Default code paths never import torch or sentence-transformers."""
    code = (
        "import sys; import api.server; import vault.vector_store; import logos; "
        "bad = [m for m in ('torch', 'sentence_transformers', 'transformers') if m in sys.modules]; "
        "print(bad); sys.exit(1 if bad else 0)"
    )
    result = subprocess.run([sys.executable, "-c", code], cwd=REPO_ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


class TestCommandLine:
    """`python -m logos` subcommands."""

    def test_info_similar_explain(self, capsys):
        from logos.__main__ import main
        assert main(["info"]) == 0
        assert '"trained": true' in capsys.readouterr().out
        assert main(["similar", "energy conservation", "conservation of energy"]) == 0
        assert 0.0 < float(capsys.readouterr().out) <= 1.0
        assert main(["explain", "0"]) == 0
        assert len(capsys.readouterr().out.split(", ")) == 10

    def test_train_respects_existing_artifact_and_force(self, tmp_path, capsys, monkeypatch):
        from logos import runtime
        from logos.__main__ import main
        out = tmp_path / "m.npz"
        out.write_bytes(b"placeholder")
        assert main(["train", "--out", str(out)]) == 0
        assert "Artifact exists" in capsys.readouterr().out

        # --force retrains; use a tiny corpus to keep the test fast
        monkeypatch.setattr(runtime, "build_corpus", lambda root: [(str(i), t) for i, t in enumerate(SMALL_CORPUS)])
        assert main(["train", "--force", "--out", str(out)]) == 0
        assert LogosEmbedder.load(str(out)).corpus_size == len(SMALL_CORPUS)

    def test_runtime_trains_when_artifact_missing(self, tmp_path, monkeypatch):
        from logos import runtime
        monkeypatch.setenv("LOGOS_MODEL_PATH", str(tmp_path / "fresh.npz"))
        monkeypatch.setattr(runtime, "build_corpus", lambda root: [(str(i), t) for i, t in enumerate(SMALL_CORPUS)])
        runtime.reset_model()
        try:
            model = runtime.get_model()
            assert model.is_trained and (tmp_path / "fresh.npz").exists()
            assert runtime.get_model() is model  # cached
        finally:
            runtime.reset_model()

    def test_unwritable_artifact_keeps_model_in_memory(self, tmp_path, monkeypatch):
        from logos import runtime
        monkeypatch.setattr(runtime, "build_corpus", lambda root: [(str(i), t) for i, t in enumerate(SMALL_CORPUS)])
        blocker = tmp_path / "file"
        blocker.write_text("x")
        model = runtime.train_default(str(blocker / "sub" / "m.npz"))  # parent is a file -> OSError
        assert model.is_trained
