"""
SpartanVectorStore - RAG Vectorial Implementation
Semantic search with Λ-Logos embeddings (ΛΕΩΝΙΔΑΣ's own model) and cosine similarity
"""

import os
import pickle
import json
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timezone
from loguru import logger

from logos import MODEL_FAMILY as LOGOS_FAMILY, get_model as get_logos_model

# External backend (optional, NOT installed by default - see .memory/DECISIONS.md
# DEC-012). Kept as an explicit opt-in; imported lazily, only when an external
# model is requested, so the default path never loads torch.
SentenceTransformer = None  # resolved on demand (tests may patch it)


def _external_backend_class():
    """Return the optional SentenceTransformer class, importing it on demand."""
    if SentenceTransformer is not None:
        return SentenceTransformer
    try:
        from sentence_transformers import SentenceTransformer as backend
    except ImportError as e:
        raise RuntimeError(
            "External embedding model requested, but the optional 'sentence-transformers' "
            "package is not installed. ΛΕΩΝΙΔΑΣ uses its own model by default "
            "(model_name='logos-v1')."
        ) from e
    return backend

# Default embedding model: Λ-Logos, trained on the project's own corpus
DEFAULT_MODEL_NAME = LOGOS_FAMILY


class _LogosBackend:
    """Adapter exposing Λ-Logos through the encode() interface used below."""
    
    def __init__(self):
        self.model = get_logos_model()
        self.model_id = self.model.model_id
    
    def encode(self, texts, convert_to_numpy=True, show_progress_bar=False):
        if isinstance(texts, str):
            return self.model.embed(texts)
        return self.model.embed_batch(texts)


@dataclass
class VectorEntry:
    """Represents a single vector entry in the store."""
    id: str
    text: str
    embedding: np.ndarray
    metadata: Dict[str, Any]
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'text': self.text,
            'embedding': self.embedding.tolist() if isinstance(self.embedding, np.ndarray) else self.embedding,
            'metadata': self.metadata,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VectorEntry':
        """Create from dictionary."""
        data['embedding'] = np.array(data['embedding'])
        return cls(**data)


class SpartanVectorStore:
    """
    SPARTAN VECTOR STORE - RAG Vectorial System
    
    Features:
    - Λ-Logos embeddings (own model, 384-dim, no network); optional external backend
    - Cosine similarity search
    - Persistent storage (JSON with embeddings; legacy pickle read as fallback)
    - Batch processing
    - CRUD operations
    """
    
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME, storage_path: str = './data/vector_store'):
        """
        Initialize the Spartan Vector Store.
        
        Args:
            model_name: 'logos-v1' (default, own model) or the name of an external
                SentenceTransformer model (requires the optional package)
            storage_path: Path for persistent storage
        """
        self.model_name = model_name
        self.storage_path = storage_path
        self.entries: Dict[str, VectorEntry] = {}
        self.model: Optional[Any] = None
        # Identity of the model that produced the stored vectors
        self.model_id: Optional[str] = None
        self.stored_model_id: Optional[str] = None
        self.stale_embeddings = False
        
        # Create storage directory
        os.makedirs(storage_path, exist_ok=True)
        
        logger.info(f"🏛️ SpartanVectorStore initialized with model: {model_name}")
        
        # Try to load existing data
        self._load_from_disk()
    
    def _init_model(self):
        """Lazy initialization of the embedding model."""
        if self.model is not None:
            return
        
        if self.model_name.startswith(LOGOS_FAMILY):
            logger.info("⚡ Loading Λ-Logos (own model)")
            self.model = _LogosBackend()
            self.model_id = self.model.model_id
        else:
            backend = _external_backend_class()
            logger.warning(f"⚠️ Loading EXTERNAL model: {self.model_name} (opt-in)")
            self.model = backend(self.model_name)
            self.model_id = f"external:{self.model_name}"
        logger.info(f"✅ Embedding model ready: {self.model_id}")
        
        if self.stored_model_id and self.entries and self.stored_model_id != self.model_id:
            self.stale_embeddings = True
            logger.warning(
                f"⚠️ Stored vectors come from {self.stored_model_id}, current model is "
                f"{self.model_id}: similarity is not meaningful until re-indexed"
            )
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a text string.
        
        Args:
            text: Input text to embed
            
        Returns:
            Numpy array with embedding vector
        """
        self._init_model()
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts (batch processing).
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of numpy arrays with embedding vectors
        """
        self._init_model()
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return [emb for emb in embeddings]
    
    def add_entry(self, id: str, text: str, metadata: Optional[Dict[str, Any]] = None,
                  stored_text: Optional[str] = None) -> VectorEntry:
        """
        Add a new entry to the vector store.
        
        Args:
            id: Unique identifier for the entry
            text: Text content to embed
            metadata: Optional metadata dictionary
            stored_text: Text kept in the index instead of `text` (e.g. a
                redaction marker when the plaintext lives only encrypted)
            
        Returns:
            VectorEntry object
        """
        if id in self.entries:
            logger.warning(f"⚠️ Entry {id} already exists, updating...")
        
        embedding = self.embed_text(text)
        
        entry = VectorEntry(
            id=id,
            text=text if stored_text is None else stored_text,
            embedding=embedding,
            metadata=metadata or {},
            created_at=datetime.now(timezone.utc).isoformat()
        )
        
        self.entries[id] = entry
        logger.info(f"✅ Added entry: {id}")
        
        return entry
    
    def add_entries_batch(self, entries: List[Tuple[str, str, Optional[Dict[str, Any]]]]) -> List[VectorEntry]:
        """
        Add multiple entries in batch (more efficient).
        
        Args:
            entries: List of tuples (id, text, metadata)
            
        Returns:
            List of VectorEntry objects
        """
        ids = [e[0] for e in entries]
        texts = [e[1] for e in entries]
        metadatas = [e[2] if len(e) >= 3 else {} for e in entries]
        
        # Batch embed all texts
        embeddings = self.embed_batch(texts)
        
        results = []
        for id, text, embedding, metadata in zip(ids, texts, embeddings, metadatas):
            entry = VectorEntry(
                id=id,
                text=text,
                embedding=embedding,
                metadata=metadata or {},
                created_at=datetime.now(timezone.utc).isoformat()
            )
            self.entries[id] = entry
            results.append(entry)
        
        logger.info(f"✅ Added {len(results)} entries in batch")
        return results
    
    def get_entry(self, id: str) -> Optional[VectorEntry]:
        """
        Retrieve an entry by ID.
        
        Args:
            id: Entry identifier
            
        Returns:
            VectorEntry or None if not found
        """
        return self.entries.get(id)
    
    def delete_entry(self, id: str) -> bool:
        """
        Delete an entry by ID.
        
        Args:
            id: Entry identifier
            
        Returns:
            True if deleted, False if not found
        """
        if id in self.entries:
            del self.entries[id]
            logger.info(f"🗑️ Deleted entry: {id}")
            return True
        return False
    
    def update_entry(self, id: str, text: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Optional[VectorEntry]:
        """
        Update an existing entry.
        
        Args:
            id: Entry identifier
            text: New text (will re-embed if provided)
            metadata: New metadata (will merge with existing)
            
        Returns:
            Updated VectorEntry or None if not found
        """
        if id not in self.entries:
            return None
        
        entry = self.entries[id]
        
        if text is not None:
            entry.text = text
            entry.embedding = self.embed_text(text)
        
        if metadata is not None:
            entry.metadata.update(metadata)
        
        logger.info(f"🔄 Updated entry: {id}")
        return entry
    
    def reembed(self, texts: Dict[str, str]) -> int:
        """
        Recompute embeddings with the current model (after a model change).
        
        Args:
            texts: entry id -> source text to embed (the stored text may be a
                redaction marker, so the caller supplies the real text)
        
        Returns:
            Number of entries re-embedded
        """
        self._init_model()
        ids = [i for i in texts if i in self.entries]
        if ids:
            vectors = self.embed_batch([texts[i] for i in ids])
            for entry_id, vector in zip(ids, vectors):
                self.entries[entry_id].embedding = vector
        self.stale_embeddings = False
        self.stored_model_id = self.model_id
        logger.info(f"🔄 Re-embedded {len(ids)} entries with {self.model_id}")
        return len(ids)
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score (0-1)
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def search_similar(self, query: str, top_k: int = 5, min_score: float = 0.0) -> List[Tuple[VectorEntry, float]]:
        """
        Search for similar entries using semantic search.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            min_score: Minimum similarity score threshold
            
        Returns:
            List of tuples (VectorEntry, similarity_score) sorted by relevance
        """
        if not self.entries:
            logger.warning("⚠️ No entries in vector store")
            return []
        
        # Generate query embedding
        query_embedding = self.embed_text(query)
        
        # Calculate similarities
        results = []
        for entry in self.entries.values():
            similarity = self.cosine_similarity(query_embedding, entry.embedding)
            if similarity >= min_score:
                results.append((entry, similarity))
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top_k results
        return results[:top_k]
    
    def find_similar_to_id(self, id: str, top_k: int = 5) -> List[Tuple[VectorEntry, float]]:
        """
        Find entries similar to a given entry ID.
        
        Args:
            id: Entry identifier
            top_k: Number of results to return
            
        Returns:
            List of tuples (VectorEntry, similarity_score) sorted by relevance
        """
        entry = self.get_entry(id)
        if entry is None:
            logger.warning(f"⚠️ Entry not found: {id}")
            return []
        
        # Calculate similarities
        results = []
        for other_entry in self.entries.values():
            if other_entry.id == id:
                continue  # Skip self
            
            similarity = self.cosine_similarity(entry.embedding, other_entry.embedding)
            results.append((other_entry, similarity))
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top_k results
        return results[:top_k]
    
    def get_all_entries(self) -> List[VectorEntry]:
        """
        Get all entries in the store.
        
        Returns:
            List of all VectorEntry objects
        """
        return list(self.entries.values())
    
    def count(self) -> int:
        """
        Get the number of entries in the store.
        
        Returns:
            Number of entries
        """
        return len(self.entries)
    
    def clear(self):
        """Clear all entries from the store."""
        self.entries.clear()
        logger.info("🧹 Cleared all entries")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with statistics
        """
        if not self.entries:
            return {
                'total_entries': 0,
                'model_name': self.model_name,
                'model_id': self.model_id,
                'storage_path': self.storage_path
            }
        
        # Calculate average embedding norm
        embeddings = [entry.embedding for entry in self.entries.values()]
        avg_norm = float(np.mean([np.linalg.norm(emb) for emb in embeddings]))
        
        return {
            'total_entries': len(self.entries),
            'model_name': self.model_name,
            'model_id': self.model_id or self.stored_model_id,
            'stale_embeddings': self.stale_embeddings,
            'storage_path': self.storage_path,
            'avg_embedding_norm': avg_norm,
            'embedding_dim': len(embeddings[0]) if embeddings else 0
        }
    
    def save_to_disk(self):
        """
        Save the vector store to disk.
        
        vector_store.json holds entries *with* embeddings and is the primary
        format loaded back. vector_store.pkl is still written for backward
        compatibility with older readers, but is only read as a fallback.
        """
        try:
            # Save as pickle (with embeddings)
            pickle_path = os.path.join(self.storage_path, 'vector_store.pkl')
            with open(pickle_path, 'wb') as f:
                pickle.dump(self.entries, f)
            
            # Save as JSON (with embeddings) - primary, safe-to-load format
            json_path = os.path.join(self.storage_path, 'vector_store.json')
            json_data = {
                'model_name': self.model_name,
                'model_id': self.model_id or self.stored_model_id,
                'format_version': 2,
                'entries': [entry.to_dict() for entry in self.entries.values()]
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Saved vector store to disk: {self.storage_path}")
        except Exception as e:
            logger.error(f"❌ Error saving to disk: {e}")
            raise
    
    def _load_from_disk(self):
        """
        Load the vector store from disk.
        
        Prefers vector_store.json (no code execution on load). Falls back to the
        legacy pickle only when no JSON with embeddings is available.
        """
        json_path = os.path.join(self.storage_path, 'vector_store.json')
        pickle_path = os.path.join(self.storage_path, 'vector_store.pkl')
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                raw_entries = json_data.get('entries', [])
                self.stored_model_id = json_data.get('model_id')
                if all('embedding' in e for e in raw_entries):
                    self.entries = {
                        e['id']: VectorEntry.from_dict(dict(e)) for e in raw_entries
                    }
                    logger.info(f"📂 Loaded {len(self.entries)} entries from JSON")
                    return
            except Exception as e:
                logger.warning(f"⚠️ Error loading JSON store, trying legacy pickle: {e}")
        
        if os.path.exists(pickle_path):
            try:
                with open(pickle_path, 'rb') as f:
                    self.entries = pickle.load(f)
                logger.info(f"📂 Loaded {len(self.entries)} entries from disk")
            except Exception as e:
                logger.warning(f"⚠️ Error loading from disk: {e}")
                self.entries = {}
        else:
            logger.info("📂 No existing data found, starting fresh")
