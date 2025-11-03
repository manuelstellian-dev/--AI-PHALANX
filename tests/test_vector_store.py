"""
Comprehensive tests for RAG Vectorial Implementation
Tests for SpartanVectorStore, SpartanVault, and API endpoints
"""

import pytest
import tempfile
import shutil
import os
import numpy as np
from httpx import AsyncClient
from unittest.mock import Mock, patch, MagicMock

from vault.vector_store import SpartanVectorStore, VectorEntry
from vault.spartan_vault import SpartanVault
from api.server import app


# Mock SentenceTransformer for tests
class MockSentenceTransformer:
    """Mock SentenceTransformer for testing without network access."""
    
    def __init__(self, model_name=None):
        """Initialize mock model."""
        self.model_name = model_name
    
    def encode(self, text, convert_to_numpy=True, show_progress_bar=False):
        """Generate mock embeddings."""
        if isinstance(text, str):
            # Single text
            np.random.seed(hash(text) % (2**32))
            embedding = np.random.randn(384).astype(np.float32)
            return embedding
        else:
            # Batch
            embeddings = []
            for t in text:
                np.random.seed(hash(t) % (2**32))
                embeddings.append(np.random.randn(384).astype(np.float32))
            return np.array(embeddings)


@pytest.fixture(autouse=True)
def mock_sentence_transformer():
    """Mock SentenceTransformer to avoid network calls."""
    with patch('vault.vector_store.SentenceTransformer', MockSentenceTransformer):
        yield


class TestVectorEntry:
    """Tests for VectorEntry dataclass."""
    
    def test_vector_entry_creation(self):
        """Test creating a VectorEntry."""
        embedding = np.array([0.1, 0.2, 0.3])
        entry = VectorEntry(
            id="test1",
            text="test text",
            embedding=embedding,
            metadata={"key": "value"},
            created_at="2024-01-01T00:00:00"
        )
        
        assert entry.id == "test1"
        assert entry.text == "test text"
        assert np.array_equal(entry.embedding, embedding)
        assert entry.metadata == {"key": "value"}
    
    def test_vector_entry_to_dict(self):
        """Test converting VectorEntry to dictionary."""
        embedding = np.array([0.1, 0.2, 0.3])
        entry = VectorEntry(
            id="test1",
            text="test text",
            embedding=embedding,
            metadata={"key": "value"},
            created_at="2024-01-01T00:00:00"
        )
        
        entry_dict = entry.to_dict()
        assert entry_dict['id'] == "test1"
        assert entry_dict['embedding'] == [0.1, 0.2, 0.3]
    
    def test_vector_entry_from_dict(self):
        """Test creating VectorEntry from dictionary."""
        data = {
            'id': "test1",
            'text': "test text",
            'embedding': [0.1, 0.2, 0.3],
            'metadata': {"key": "value"},
            'created_at': "2024-01-01T00:00:00"
        }
        
        entry = VectorEntry.from_dict(data)
        assert entry.id == "test1"
        assert isinstance(entry.embedding, np.ndarray)


class TestSpartanVectorStore:
    """Tests for SpartanVectorStore."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def vector_store(self, temp_storage):
        """Create a vector store instance."""
        return SpartanVectorStore(storage_path=temp_storage)
    
    def test_vector_store_initialization(self, temp_storage):
        """Test vector store initialization."""
        store = SpartanVectorStore(storage_path=temp_storage)
        assert store.model_name == 'all-MiniLM-L6-v2'
        assert store.storage_path == temp_storage
        assert len(store.entries) == 0
    
    def test_embed_text(self, vector_store):
        """Test text embedding generation."""
        text = "This is a test sentence"
        embedding = vector_store.embed_text(text)
        
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) == 384  # all-MiniLM-L6-v2 dimension
        assert embedding.dtype == np.float32
    
    def test_embed_batch(self, vector_store):
        """Test batch embedding generation."""
        texts = ["First sentence", "Second sentence", "Third sentence"]
        embeddings = vector_store.embed_batch(texts)
        
        assert len(embeddings) == 3
        assert all(isinstance(emb, np.ndarray) for emb in embeddings)
        assert all(len(emb) == 384 for emb in embeddings)
    
    def test_add_entry(self, vector_store):
        """Test adding a single entry."""
        entry = vector_store.add_entry(
            id="test1",
            text="Test document",
            metadata={"category": "test"}
        )
        
        assert entry.id == "test1"
        assert entry.text == "Test document"
        assert entry.metadata["category"] == "test"
        assert len(vector_store.entries) == 1
    
    def test_add_entry_update_existing(self, vector_store):
        """Test updating an existing entry."""
        vector_store.add_entry(id="test1", text="Original text")
        entry = vector_store.add_entry(id="test1", text="Updated text")
        
        assert len(vector_store.entries) == 1
        assert entry.text == "Updated text"
    
    def test_add_entries_batch(self, vector_store):
        """Test adding multiple entries in batch."""
        entries_data = [
            ("id1", "First document", {"type": "doc"}),
            ("id2", "Second document", {"type": "doc"}),
            ("id3", "Third document", {"type": "doc"})
        ]
        
        entries = vector_store.add_entries_batch(entries_data)
        
        assert len(entries) == 3
        assert len(vector_store.entries) == 3
        assert all(isinstance(e, VectorEntry) for e in entries)
    
    def test_get_entry(self, vector_store):
        """Test retrieving an entry by ID."""
        vector_store.add_entry(id="test1", text="Test")
        entry = vector_store.get_entry("test1")
        
        assert entry is not None
        assert entry.id == "test1"
    
    def test_get_entry_not_found(self, vector_store):
        """Test retrieving non-existent entry."""
        entry = vector_store.get_entry("nonexistent")
        assert entry is None
    
    def test_delete_entry(self, vector_store):
        """Test deleting an entry."""
        vector_store.add_entry(id="test1", text="Test")
        result = vector_store.delete_entry("test1")
        
        assert result is True
        assert len(vector_store.entries) == 0
    
    def test_delete_entry_not_found(self, vector_store):
        """Test deleting non-existent entry."""
        result = vector_store.delete_entry("nonexistent")
        assert result is False
    
    def test_update_entry(self, vector_store):
        """Test updating an entry."""
        vector_store.add_entry(id="test1", text="Original")
        updated = vector_store.update_entry(
            id="test1",
            text="Updated text",
            metadata={"updated": True}
        )
        
        assert updated is not None
        assert updated.text == "Updated text"
        assert updated.metadata["updated"] is True
    
    def test_update_entry_not_found(self, vector_store):
        """Test updating non-existent entry."""
        result = vector_store.update_entry(id="nonexistent", text="Test")
        assert result is None
    
    def test_cosine_similarity(self, vector_store):
        """Test cosine similarity calculation."""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([1.0, 0.0, 0.0])
        vec3 = np.array([0.0, 1.0, 0.0])
        
        # Identical vectors
        sim1 = vector_store.cosine_similarity(vec1, vec2)
        assert abs(sim1 - 1.0) < 0.001
        
        # Orthogonal vectors
        sim2 = vector_store.cosine_similarity(vec1, vec3)
        assert abs(sim2) < 0.001
    
    def test_cosine_similarity_zero_vectors(self, vector_store):
        """Test cosine similarity with zero vectors."""
        vec1 = np.array([0.0, 0.0, 0.0])
        vec2 = np.array([1.0, 0.0, 0.0])
        
        sim = vector_store.cosine_similarity(vec1, vec2)
        assert sim == 0.0
    
    def test_search_similar(self, vector_store):
        """Test semantic similarity search."""
        vector_store.add_entry(id="doc1", text="Python programming language")
        vector_store.add_entry(id="doc2", text="Java programming language")
        vector_store.add_entry(id="doc3", text="Cooking recipes")
        
        results = vector_store.search_similar("Programming languages", top_k=2)
        
        assert len(results) <= 2
        assert all(isinstance(r, tuple) for r in results)
        assert all(isinstance(r[0], VectorEntry) for r in results)
        assert all(isinstance(r[1], float) for r in results)
        
        # Check results are sorted by similarity
        if len(results) > 1:
            assert results[0][1] >= results[1][1]
    
    def test_search_similar_with_min_score(self, vector_store):
        """Test search with minimum score threshold."""
        vector_store.add_entry(id="doc1", text="Python programming")
        vector_store.add_entry(id="doc2", text="Cooking recipes")
        
        results = vector_store.search_similar(
            "Python code",
            top_k=10,
            min_score=0.5
        )
        
        # All results should meet minimum score
        assert all(score >= 0.5 for _, score in results)
    
    def test_search_similar_empty_store(self, vector_store):
        """Test search on empty store."""
        results = vector_store.search_similar("test query")
        assert len(results) == 0
    
    def test_find_similar_to_id(self, vector_store):
        """Test finding similar entries to a given ID."""
        vector_store.add_entry(id="doc1", text="Python programming")
        vector_store.add_entry(id="doc2", text="Java programming")
        vector_store.add_entry(id="doc3", text="Cooking")
        
        results = vector_store.find_similar_to_id("doc1", top_k=2)
        
        assert len(results) <= 2
        # doc1 should not be in results (excluded self)
        assert all(entry.id != "doc1" for entry, _ in results)
    
    def test_find_similar_to_id_not_found(self, vector_store):
        """Test finding similar to non-existent ID."""
        results = vector_store.find_similar_to_id("nonexistent")
        assert len(results) == 0
    
    def test_get_all_entries(self, vector_store):
        """Test getting all entries."""
        vector_store.add_entry(id="doc1", text="First")
        vector_store.add_entry(id="doc2", text="Second")
        
        all_entries = vector_store.get_all_entries()
        assert len(all_entries) == 2
    
    def test_count(self, vector_store):
        """Test counting entries."""
        assert vector_store.count() == 0
        
        vector_store.add_entry(id="doc1", text="Test")
        assert vector_store.count() == 1
        
        vector_store.add_entry(id="doc2", text="Test")
        assert vector_store.count() == 2
    
    def test_clear(self, vector_store):
        """Test clearing all entries."""
        vector_store.add_entry(id="doc1", text="Test")
        vector_store.add_entry(id="doc2", text="Test")
        
        vector_store.clear()
        assert vector_store.count() == 0
    
    def test_get_stats(self, vector_store):
        """Test getting statistics."""
        stats = vector_store.get_stats()
        assert stats['total_entries'] == 0
        assert stats['model_name'] == 'all-MiniLM-L6-v2'
        
        vector_store.add_entry(id="doc1", text="Test document")
        stats = vector_store.get_stats()
        assert stats['total_entries'] == 1
        assert stats['embedding_dim'] == 384
    
    def test_save_and_load_from_disk(self, temp_storage):
        """Test persistence to disk."""
        # Create store and add entries
        store1 = SpartanVectorStore(storage_path=temp_storage)
        store1.add_entry(id="doc1", text="Test document")
        store1.add_entry(id="doc2", text="Another document")
        store1.save_to_disk()
        
        # Create new store from same path (should load data)
        store2 = SpartanVectorStore(storage_path=temp_storage)
        
        assert store2.count() == 2
        assert store2.get_entry("doc1") is not None
        assert store2.get_entry("doc2") is not None
    
    def test_save_creates_files(self, vector_store, temp_storage):
        """Test that save creates necessary files."""
        vector_store.add_entry(id="doc1", text="Test")
        vector_store.save_to_disk()
        
        pickle_file = os.path.join(temp_storage, 'vector_store.pkl')
        json_file = os.path.join(temp_storage, 'vector_store.json')
        
        assert os.path.exists(pickle_file)
        assert os.path.exists(json_file)


class TestSpartanVault:
    """Tests for SpartanVault."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def vault(self, temp_storage):
        """Create a vault instance."""
        return SpartanVault(storage_path=temp_storage)
    
    def test_vault_initialization(self, temp_storage):
        """Test vault initialization."""
        vault = SpartanVault(storage_path=temp_storage)
        
        assert vault.storage_path == temp_storage
        assert vault.encryption_key is not None
        assert vault.vector_store is not None
    
    def test_store_encrypted(self, vault):
        """Test storing encrypted data."""
        result = vault.store(id="test1", data="Secret data", metadata={"type": "secret"})
        
        assert result['id'] == "test1"
        assert result['encrypted'] is True
        assert "test1" in vault.encrypted_storage
    
    def test_retrieve_decrypted(self, vault):
        """Test retrieving and decrypting data."""
        vault.store(id="test1", data="Secret data")
        decrypted = vault.retrieve("test1")
        
        assert decrypted == "Secret data"
    
    def test_retrieve_not_found(self, vault):
        """Test retrieving non-existent data."""
        result = vault.retrieve("nonexistent")
        assert result is None
    
    def test_store_with_embedding(self, vault):
        """Test storing with both encryption and embedding."""
        result = vault.store_with_embedding(
            id="doc1",
            text="Python programming",
            metadata={"lang": "en"}
        )
        
        assert result['id'] == "doc1"
        assert result['encrypted'] is True
        assert result['embedded'] is True
        
        # Check both storages
        assert "doc1" in vault.encrypted_storage
        assert vault.vector_store.get_entry("doc1") is not None
    
    def test_store_with_embedding_no_encrypt(self, vault):
        """Test storing with embedding only (no encryption)."""
        result = vault.store_with_embedding(
            id="doc1",
            text="Test",
            encrypt=False
        )
        
        assert result['encrypted'] is False
        assert result['embedded'] is True
        assert "doc1" not in vault.encrypted_storage
    
    def test_semantic_search(self, vault):
        """Test semantic search."""
        vault.store_with_embedding(id="doc1", text="Python programming")
        vault.store_with_embedding(id="doc2", text="Java programming")
        vault.store_with_embedding(id="doc3", text="Cooking recipes")
        
        results = vault.semantic_search("programming languages", top_k=2)
        
        assert len(results) <= 2
        assert all('id' in r for r in results)
        assert all('score' in r for r in results)
    
    def test_semantic_search_with_decrypt(self, vault):
        """Test semantic search with decryption."""
        vault.store_with_embedding(id="doc1", text="Secret programming guide for Python developers")
        
        # Use the same text for query to ensure high similarity
        results = vault.semantic_search("Secret programming guide for Python developers", decrypt=True, min_score=0.0, top_k=10)
        
        assert len(results) > 0
        # Decrypted text should be returned
        assert results[0]['text'] == "Secret programming guide for Python developers"
    
    def test_exact_search(self, vault):
        """Test exact search by ID."""
        vault.store_with_embedding(id="doc1", text="Test document")
        
        result = vault.exact_search("doc1")
        
        assert result is not None
        assert result['id'] == "doc1"
        assert result['text'] == "Test document"
    
    def test_exact_search_not_found(self, vault):
        """Test exact search for non-existent entry."""
        result = vault.exact_search("nonexistent")
        assert result is None
    
    def test_hybrid_search(self, vault):
        """Test hybrid search (exact + semantic)."""
        vault.store_with_embedding(id="doc1", text="Python guide")
        vault.store_with_embedding(id="doc2", text="Java guide")
        vault.store_with_embedding(id="doc3", text="Cooking")
        
        results = vault.hybrid_search(
            query="programming",
            exact_ids=["doc1"],
            top_k=2
        )
        
        assert 'exact_matches' in results
        assert 'semantic_matches' in results
        assert len(results['exact_matches']) > 0
    
    def test_find_similar(self, vault):
        """Test finding similar entries."""
        vault.store_with_embedding(id="doc1", text="Python programming")
        vault.store_with_embedding(id="doc2", text="Java programming")
        vault.store_with_embedding(id="doc3", text="Cooking")
        
        results = vault.find_similar("doc1", top_k=2)
        
        assert len(results) <= 2
        # doc1 should not be in results
        assert all(r['id'] != "doc1" for r in results)
    
    def test_delete(self, vault):
        """Test deleting an entry."""
        vault.store_with_embedding(id="doc1", text="Test")
        
        result = vault.delete("doc1")
        
        assert result is True
        assert "doc1" not in vault.encrypted_storage
        assert vault.vector_store.get_entry("doc1") is None
    
    def test_get_stats(self, vault):
        """Test getting vault statistics."""
        vault.store_with_embedding(id="doc1", text="Test")
        
        stats = vault.get_stats()
        
        assert 'encrypted_entries' in stats
        assert 'vector_entries' in stats
        assert stats['encryption_enabled'] is True
    
    def test_save_and_load(self, temp_storage):
        """Test vault persistence."""
        # Create vault and add data
        vault1 = SpartanVault(storage_path=temp_storage)
        vault1.store_with_embedding(id="doc1", text="Test document")
        vault1.save_to_disk()
        
        # Create new vault from same path
        from cryptography.fernet import Fernet
        key_path = os.path.join(temp_storage, 'encryption.key')
        with open(key_path, 'rb') as f:
            key = f.read()
        
        vault2 = SpartanVault(encryption_key=key, storage_path=temp_storage)
        
        assert vault2.vector_store.count() == 1
        assert len(vault2.encrypted_storage) == 1


@pytest.mark.asyncio
class TestVaultAPIEndpoints:
    """Tests for Vault API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return AsyncClient(app=app, base_url="http://test")
    
    async def test_embed_endpoint(self, client):
        """Test /embed endpoint."""
        async with client:
            response = await client.post(
                "/api/v1/vault/embed",
                json={"text": "Test text"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert 'embedding' in data
            assert 'dimension' in data
            assert data['dimension'] == 384
    
    async def test_store_with_embedding_endpoint(self, client):
        """Test /store-with-embedding endpoint."""
        async with client:
            response = await client.post(
                "/api/v1/vault/store-with-embedding",
                json={
                    "id": "test1",
                    "text": "Test document",
                    "metadata": {"type": "test"}
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data['id'] == "test1"
            assert data['embedded'] is True
    
    async def test_search_endpoint(self, client):
        """Test /search endpoint."""
        async with client:
            # First store some documents
            await client.post(
                "/api/v1/vault/store-with-embedding",
                json={"id": "doc1", "text": "Python programming"}
            )
            
            # Then search
            response = await client.post(
                "/api/v1/vault/search",
                json={"query": "programming", "top_k": 5}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert 'results' in data
            assert 'query' in data
            assert data['query'] == "programming"
    
    async def test_hybrid_search_endpoint(self, client):
        """Test /hybrid-search endpoint."""
        async with client:
            await client.post(
                "/api/v1/vault/store-with-embedding",
                json={"id": "doc1", "text": "Python guide"}
            )
            
            response = await client.post(
                "/api/v1/vault/hybrid-search",
                json={
                    "query": "programming",
                    "exact_ids": ["doc1"],
                    "top_k": 5
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert 'exact_matches' in data
            assert 'semantic_matches' in data
    
    async def test_find_similar_endpoint(self, client):
        """Test /similar/{id} endpoint."""
        async with client:
            await client.post(
                "/api/v1/vault/store-with-embedding",
                json={"id": "doc1", "text": "Test"}
            )
            
            response = await client.get("/api/v1/vault/similar/doc1?top_k=5")
            
            assert response.status_code == 200
            data = response.json()
            assert 'id' in data
            assert 'similar' in data
    
    async def test_find_similar_not_found(self, client):
        """Test /similar/{id} with non-existent ID."""
        async with client:
            response = await client.get("/api/v1/vault/similar/nonexistent")
            assert response.status_code == 404
    
    async def test_stats_endpoint(self, client):
        """Test /stats endpoint."""
        async with client:
            response = await client.get("/api/v1/vault/stats")
            
            assert response.status_code == 200
            data = response.json()
            assert 'encrypted_entries' in data
            assert 'vector_entries' in data
    
    async def test_save_endpoint(self, client):
        """Test /save endpoint."""
        async with client:
            response = await client.post("/api/v1/vault/save")
            
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'success'
    
    async def test_batch_embed_endpoint(self, client):
        """Test /batch-embed endpoint."""
        async with client:
            response = await client.post(
                "/api/v1/vault/batch-embed",
                json={"texts": ["First text", "Second text", "Third text"]}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert 'embeddings' in data
            assert 'count' in data
            assert data['count'] == 3
    
    async def test_batch_embed_empty_list(self, client):
        """Test /batch-embed with empty list."""
        async with client:
            response = await client.post(
                "/api/v1/vault/batch-embed",
                json={"texts": []}
            )
            
            assert response.status_code == 400
