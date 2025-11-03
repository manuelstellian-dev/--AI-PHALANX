# 🏛️ RAG VECTORIAL SYSTEM

**ΜΟΛΩΝ ΛΑΒΕ!** - Semantic Search for SPARTA

## 📋 Overview

The RAG (Retrieval-Augmented Generation) Vectorial system provides semantic search capabilities using SentenceTransformer embeddings and cosine similarity. It combines encrypted storage with vector embeddings for secure and intelligent data retrieval.

## 🏗️ Architecture

### Components

1. **SpartanVectorStore** (`vault/vector_store.py`)
   - Embedding generation using SentenceTransformer (all-MiniLM-L6-v2)
   - Cosine similarity search
   - In-memory vector storage
   - Persistent storage (pickle + JSON)
   - Batch processing support

2. **SpartanVault** (`vault/spartan_vault.py`)
   - AES-256 encryption for sensitive data
   - Integration with SpartanVectorStore
   - Hybrid search (exact + semantic)
   - Encrypted data persistence

3. **REST API** (`api/routes/vault.py`)
   - 8 REST endpoints for vault operations
   - FastAPI-based with Pydantic validation
   - Comprehensive error handling

### Data Flow

```
Input Text
    ↓
[Encryption] → Encrypted Storage
    ↓
[Embedding] → Vector Store (384-dim vectors)
    ↓
[Cosine Similarity] → Search Results
```

## 🚀 Quick Start

### Python API

```python
from vault.spartan_vault import SpartanVault

# Initialize vault
vault = SpartanVault()

# Store with encryption and embedding
vault.store_with_embedding(
    id="doc1",
    text="Python is a high-level programming language",
    metadata={"category": "programming", "lang": "en"}
)

# Semantic search
results = vault.semantic_search(
    query="programming languages",
    top_k=5,
    min_score=0.3
)

# Hybrid search (exact + semantic)
results = vault.hybrid_search(
    query="Python programming",
    exact_ids=["doc1", "doc2"],
    top_k=5
)

# Find similar entries
similar = vault.find_similar("doc1", top_k=5)

# Save to disk
vault.save_to_disk()
```

### Vector Store Only

```python
from vault.vector_store import SpartanVectorStore

# Initialize vector store
store = SpartanVectorStore()

# Add entry
store.add_entry(
    id="doc1",
    text="Machine learning is a subset of AI",
    metadata={"topic": "AI"}
)

# Batch add
entries = [
    ("doc2", "Deep learning uses neural networks", {"topic": "AI"}),
    ("doc3", "Natural language processing", {"topic": "NLP"}),
]
store.add_entries_batch(entries)

# Search
results = store.search_similar("artificial intelligence", top_k=3)
for entry, score in results:
    print(f"{entry.id}: {score:.3f} - {entry.text}")
```

## 🔌 API Reference

### Base URL
```
http://localhost:7300/api/v1/vault
```

### 1. Generate Embedding

**Endpoint:** `POST /embed`

Generate embedding vector for text.

**Request:**
```json
{
  "text": "Python programming language"
}
```

**Response:**
```json
{
  "embedding": [0.123, -0.456, ...],
  "dimension": 384
}
```

**cURL:**
```bash
curl -X POST "http://localhost:7300/api/v1/vault/embed" \
  -H "Content-Type: application/json" \
  -d '{"text": "Python programming"}'
```

### 2. Store with Embedding

**Endpoint:** `POST /store-with-embedding`

Store data with encryption and embedding.

**Request:**
```json
{
  "id": "doc1",
  "text": "Python is a programming language",
  "metadata": {"category": "tech"},
  "encrypt": true
}
```

**Response:**
```json
{
  "id": "doc1",
  "encrypted": true,
  "embedded": true,
  "stored_at": "2024-01-01T12:00:00",
  "metadata": {"category": "tech"}
}
```

**cURL:**
```bash
curl -X POST "http://localhost:7300/api/v1/vault/store-with-embedding" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "doc1",
    "text": "Python programming language",
    "metadata": {"category": "programming"}
  }'
```

### 3. Semantic Search

**Endpoint:** `POST /search`

Search by semantic similarity.

**Request:**
```json
{
  "query": "programming languages",
  "top_k": 5,
  "min_score": 0.3,
  "decrypt": false
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "doc1",
      "text": "Python programming",
      "score": 0.85,
      "metadata": {"category": "tech"},
      "created_at": "2024-01-01T12:00:00"
    }
  ],
  "query": "programming languages",
  "total": 1
}
```

**cURL:**
```bash
curl -X POST "http://localhost:7300/api/v1/vault/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "programming languages",
    "top_k": 5,
    "min_score": 0.3
  }'
```

### 4. Hybrid Search

**Endpoint:** `POST /hybrid-search`

Combine exact ID matches with semantic search.

**Request:**
```json
{
  "query": "programming",
  "exact_ids": ["doc1", "doc2"],
  "top_k": 5,
  "min_score": 0.3,
  "decrypt": false
}
```

**Response:**
```json
{
  "exact_matches": [
    {
      "id": "doc1",
      "text": "Python programming",
      "metadata": {},
      "created_at": "2024-01-01T12:00:00"
    }
  ],
  "semantic_matches": [
    {
      "id": "doc3",
      "text": "Java programming",
      "score": 0.78,
      "metadata": {},
      "created_at": "2024-01-01T12:01:00"
    }
  ],
  "query": "programming"
}
```

**cURL:**
```bash
curl -X POST "http://localhost:7300/api/v1/vault/hybrid-search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "programming",
    "exact_ids": ["doc1"],
    "top_k": 5
  }'
```

### 5. Find Similar Entries

**Endpoint:** `GET /similar/{id}`

Find entries similar to a given entry.

**Query Parameters:**
- `top_k` (optional): Number of results (default: 5)
- `decrypt` (optional): Decrypt results (default: false)

**Response:**
```json
{
  "id": "doc1",
  "similar": [
    {
      "id": "doc2",
      "text": "Java programming",
      "score": 0.82,
      "metadata": {},
      "created_at": "2024-01-01T12:00:00"
    }
  ],
  "count": 1
}
```

**cURL:**
```bash
curl -X GET "http://localhost:7300/api/v1/vault/similar/doc1?top_k=5"
```

### 6. Get Statistics

**Endpoint:** `GET /stats`

Get vault statistics.

**Response:**
```json
{
  "encrypted_entries": 10,
  "vector_entries": 10,
  "storage_path": "./data/vault",
  "encryption_enabled": true,
  "vector_stats": {
    "total_entries": 10,
    "model_name": "all-MiniLM-L6-v2",
    "storage_path": "./data/vault/vectors",
    "avg_embedding_norm": 12.5,
    "embedding_dim": 384
  }
}
```

**cURL:**
```bash
curl -X GET "http://localhost:7300/api/v1/vault/stats"
```

### 7. Save to Disk

**Endpoint:** `POST /save`

Persist vault to disk.

**Response:**
```json
{
  "status": "success",
  "message": "Vault saved to disk",
  "stats": {
    "encrypted_entries": 10,
    "vector_entries": 10
  }
}
```

**cURL:**
```bash
curl -X POST "http://localhost:7300/api/v1/vault/save"
```

### 8. Batch Embedding

**Endpoint:** `POST /batch-embed`

Generate embeddings for multiple texts.

**Request:**
```json
{
  "texts": [
    "First document",
    "Second document",
    "Third document"
  ]
}
```

**Response:**
```json
{
  "embeddings": [
    [0.123, -0.456, ...],
    [0.789, -0.012, ...],
    [0.345, -0.678, ...]
  ],
  "count": 3,
  "dimension": 384
}
```

**cURL:**
```bash
curl -X POST "http://localhost:7300/api/v1/vault/batch-embed" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["First text", "Second text", "Third text"]
  }'
```

## 📊 Performance Metrics

### Model Specifications
- **Model:** all-MiniLM-L6-v2
- **Embedding Dimension:** 384
- **Max Sequence Length:** 256 tokens
- **Model Size:** ~80 MB

### Benchmarks (on CPU)
- **Single Embedding:** ~50ms
- **Batch (100 texts):** ~2 seconds (~20ms per text)
- **Search (1000 vectors):** ~5ms
- **Save to Disk:** ~100ms (1000 entries)

### Memory Usage
- **Model:** ~150 MB RAM
- **Storage:** ~4 KB per entry (384 float32 values)
- **1000 entries:** ~4 MB + text data

## 🔒 Security Features

### Encryption
- **Algorithm:** AES-256 (Fernet)
- **Key Generation:** Cryptographically secure random
- **Key Storage:** Separate encryption.key file
- **Data:** Encrypted at rest

### Best Practices
1. Store encryption keys securely (not in version control)
2. Use environment variables for sensitive data
3. Implement access control on API endpoints
4. Regular backups of encrypted data
5. Rotate encryption keys periodically

## 🧪 Testing

Run the comprehensive test suite:

```bash
# All tests
pytest tests/test_vector_store.py -v

# Specific test class
pytest tests/test_vector_store.py::TestSpartanVectorStore -v

# With coverage
pytest tests/test_vector_store.py --cov=vault --cov-report=html
```

Test coverage: **50+ tests** covering:
- Embedding generation
- Vector storage operations
- Similarity search
- Persistence
- API endpoints
- Error handling

## 🛠️ Configuration

### Environment Variables

```bash
# Storage path
export VAULT_STORAGE_PATH="./data/vault"

# Model selection
export VECTOR_MODEL="all-MiniLM-L6-v2"

# API settings
export VAULT_API_TIMEOUT=30
```

### Custom Model

Use a different SentenceTransformer model:

```python
vault = SpartanVault(vector_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
```

## 📈 Scaling Considerations

### For Large Datasets (>100k entries)
1. Consider using Faiss for approximate nearest neighbor search
2. Implement pagination for search results
3. Use database backend (PostgreSQL with pgvector)
4. Implement caching for frequent queries
5. Use async I/O for disk operations

### Memory Optimization
- Use float16 for embeddings (halves memory)
- Implement LRU cache for embeddings
- Lazy load model (only when needed)
- Batch operations when possible

## 🔍 Use Cases

### 1. Document Search
```python
# Index documents
vault.store_with_embedding("doc1", "AI research paper on transformers")
vault.store_with_embedding("doc2", "Machine learning best practices")

# Search
results = vault.semantic_search("neural networks research")
```

### 2. Knowledge Base
```python
# Store knowledge articles
vault.store_with_embedding("kb001", "How to reset password", 
                          metadata={"category": "help", "priority": "high"})

# Find relevant articles
results = vault.semantic_search("forgot password")
```

### 3. Code Snippet Search
```python
# Index code snippets
vault.store_with_embedding("snippet1", "def quicksort(arr): ...",
                          metadata={"lang": "python", "algo": "sorting"})

# Search by description
results = vault.semantic_search("sorting algorithm implementation")
```

## 🤝 Contributing

To extend the system:

1. Add new embedding models in `vector_store.py`
2. Implement custom similarity metrics
3. Add new API endpoints in `api/routes/vault.py`
4. Write tests for new features

## 📚 References

- [SentenceTransformers Documentation](https://www.sbert.net/)
- [all-MiniLM-L6-v2 Model Card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
- [RAG Architecture](https://arxiv.org/abs/2005.11401)

---

**ΜΟΛΩΝ ΛΑΒΕ!** 🏛️⚡

*The semantic search capabilities of SPARTA are ready for battle.*
