"""
SpartanVault - Encrypted Storage with RAG Vectorial Integration
Combines encryption with semantic search capabilities
"""

import os
import json
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
from loguru import logger
from cryptography.fernet import Fernet
from .vector_store import SpartanVectorStore, VectorEntry


class SpartanVault:
    """
    SPARTAN VAULT - Encrypted Storage with RAG Vectorial
    
    Features:
    - AES-256 encryption for sensitive data
    - Vector embeddings for semantic search
    - Hybrid search (exact + semantic)
    - Persistent storage
    """
    
    def __init__(self, encryption_key: Optional[bytes] = None, 
                 storage_path: str = './data/vault',
                 vector_model: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the Spartan Vault.
        
        Args:
            encryption_key: Fernet encryption key (generated if None)
            storage_path: Path for persistent storage
            vector_model: SentenceTransformer model name
        """
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # Initialize encryption
        if encryption_key is None:
            encryption_key = Fernet.generate_key()
        self.cipher = Fernet(encryption_key)
        self.encryption_key = encryption_key
        
        # Initialize vector store
        vector_store_path = os.path.join(storage_path, 'vectors')
        self.vector_store = SpartanVectorStore(
            model_name=vector_model,
            storage_path=vector_store_path
        )
        
        # In-memory storage for encrypted data
        self.encrypted_storage: Dict[str, bytes] = {}
        
        logger.info(f"🔐 SpartanVault initialized at: {storage_path}")
        
        # Load existing encrypted data
        self._load_encrypted_data()
    
    def store(self, id: str, data: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Store encrypted data (without embedding).
        
        Args:
            id: Unique identifier
            data: Data to encrypt and store
            metadata: Optional metadata
            
        Returns:
            Storage result dictionary
        """
        # Encrypt data
        encrypted = self.cipher.encrypt(data.encode('utf-8'))
        self.encrypted_storage[id] = encrypted
        
        result = {
            'id': id,
            'encrypted': True,
            'stored_at': datetime.utcnow().isoformat(),
            'metadata': metadata or {}
        }
        
        logger.info(f"🔐 Stored encrypted data: {id}")
        return result
    
    def retrieve(self, id: str) -> Optional[str]:
        """
        Retrieve and decrypt data.
        
        Args:
            id: Entry identifier
            
        Returns:
            Decrypted data or None if not found
        """
        encrypted = self.encrypted_storage.get(id)
        if encrypted is None:
            return None
        
        try:
            decrypted = self.cipher.decrypt(encrypted).decode('utf-8')
            return decrypted
        except Exception as e:
            logger.error(f"❌ Error decrypting data for {id}: {e}")
            return None
    
    def store_with_embedding(self, id: str, text: str, 
                           metadata: Optional[Dict[str, Any]] = None,
                           encrypt: bool = True) -> Dict[str, Any]:
        """
        Store data with both encryption and embedding.
        
        Args:
            id: Unique identifier
            text: Text to store and embed
            metadata: Optional metadata
            encrypt: Whether to encrypt the data
            
        Returns:
            Storage result dictionary
        """
        # Store encrypted version
        if encrypt:
            encrypted = self.cipher.encrypt(text.encode('utf-8'))
            self.encrypted_storage[id] = encrypted
        
        # Add to vector store for semantic search
        entry = self.vector_store.add_entry(id, text, metadata)
        
        result = {
            'id': id,
            'encrypted': encrypt,
            'embedded': True,
            'stored_at': entry.created_at,
            'metadata': metadata or {}
        }
        
        logger.info(f"🔐⚡ Stored with encryption and embedding: {id}")
        return result
    
    def semantic_search(self, query: str, top_k: int = 5, 
                       min_score: float = 0.0,
                       decrypt: bool = False) -> List[Dict[str, Any]]:
        """
        Perform semantic search using embeddings.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            min_score: Minimum similarity score
            decrypt: Whether to include decrypted text in results
            
        Returns:
            List of search results with scores
        """
        results = self.vector_store.search_similar(query, top_k, min_score)
        
        output = []
        for entry, score in results:
            result_dict = {
                'id': entry.id,
                'text': entry.text if not decrypt else self.retrieve(entry.id) or entry.text,
                'score': score,
                'metadata': entry.metadata,
                'created_at': entry.created_at
            }
            output.append(result_dict)
        
        logger.info(f"🔍 Semantic search returned {len(output)} results")
        return output
    
    def exact_search(self, id: str, decrypt: bool = True) -> Optional[Dict[str, Any]]:
        """
        Exact search by ID.
        
        Args:
            id: Entry identifier
            decrypt: Whether to decrypt the data
            
        Returns:
            Entry data or None if not found
        """
        entry = self.vector_store.get_entry(id)
        if entry is None:
            return None
        
        text = entry.text
        if decrypt and id in self.encrypted_storage:
            decrypted = self.retrieve(id)
            if decrypted:
                text = decrypted
        
        return {
            'id': entry.id,
            'text': text,
            'metadata': entry.metadata,
            'created_at': entry.created_at
        }
    
    def hybrid_search(self, query: str, exact_ids: Optional[List[str]] = None,
                     top_k: int = 5, min_score: float = 0.0,
                     decrypt: bool = False) -> Dict[str, Any]:
        """
        Hybrid search combining exact matches and semantic similarity.
        
        Args:
            query: Search query text
            exact_ids: Optional list of IDs for exact matches
            top_k: Number of semantic results
            min_score: Minimum similarity score
            decrypt: Whether to decrypt results
            
        Returns:
            Dictionary with exact and semantic results
        """
        results = {
            'exact_matches': [],
            'semantic_matches': []
        }
        
        # Exact matches
        if exact_ids:
            for id in exact_ids:
                match = self.exact_search(id, decrypt)
                if match:
                    results['exact_matches'].append(match)
        
        # Semantic search
        semantic_results = self.semantic_search(query, top_k, min_score, decrypt)
        results['semantic_matches'] = semantic_results
        
        logger.info(f"🔍 Hybrid search: {len(results['exact_matches'])} exact, {len(results['semantic_matches'])} semantic")
        return results
    
    def find_similar(self, id: str, top_k: int = 5, 
                    decrypt: bool = False) -> List[Dict[str, Any]]:
        """
        Find entries similar to a given entry.
        
        Args:
            id: Entry identifier
            top_k: Number of results
            decrypt: Whether to decrypt results
            
        Returns:
            List of similar entries with scores
        """
        results = self.vector_store.find_similar_to_id(id, top_k)
        
        output = []
        for entry, score in results:
            result_dict = {
                'id': entry.id,
                'text': entry.text if not decrypt else self.retrieve(entry.id) or entry.text,
                'score': score,
                'metadata': entry.metadata,
                'created_at': entry.created_at
            }
            output.append(result_dict)
        
        return output
    
    def delete(self, id: str) -> bool:
        """
        Delete an entry from both encrypted storage and vector store.
        
        Args:
            id: Entry identifier
            
        Returns:
            True if deleted, False if not found
        """
        deleted_encrypted = id in self.encrypted_storage
        if deleted_encrypted:
            del self.encrypted_storage[id]
        
        deleted_vector = self.vector_store.delete_entry(id)
        
        return deleted_encrypted or deleted_vector
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get vault statistics.
        
        Returns:
            Dictionary with statistics
        """
        vector_stats = self.vector_store.get_stats()
        
        return {
            'encrypted_entries': len(self.encrypted_storage),
            'vector_entries': vector_stats['total_entries'],
            'storage_path': self.storage_path,
            'encryption_enabled': True,
            'vector_stats': vector_stats
        }
    
    def save_to_disk(self):
        """
        Save vault data to disk.
        """
        # Save vector store
        self.vector_store.save_to_disk()
        
        # Save encrypted storage
        encrypted_path = os.path.join(self.storage_path, 'encrypted.json')
        encrypted_data = {
            id: encrypted.hex()
            for id, encrypted in self.encrypted_storage.items()
        }
        
        with open(encrypted_path, 'w') as f:
            json.dump(encrypted_data, f, indent=2)
        
        # Save encryption key
        key_path = os.path.join(self.storage_path, 'encryption.key')
        with open(key_path, 'wb') as f:
            f.write(self.encryption_key)
        
        logger.info(f"💾 Saved vault to disk: {self.storage_path}")
    
    def _load_encrypted_data(self):
        """
        Load encrypted data from disk.
        """
        encrypted_path = os.path.join(self.storage_path, 'encrypted.json')
        
        if os.path.exists(encrypted_path):
            try:
                with open(encrypted_path, 'r') as f:
                    encrypted_data = json.load(f)
                
                self.encrypted_storage = {
                    id: bytes.fromhex(hex_str)
                    for id, hex_str in encrypted_data.items()
                }
                
                logger.info(f"📂 Loaded {len(self.encrypted_storage)} encrypted entries")
            except Exception as e:
                logger.warning(f"⚠️ Error loading encrypted data: {e}")
