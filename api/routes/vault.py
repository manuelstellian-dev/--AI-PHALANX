"""
API Routes for Spartan Vault - RAG Vectorial Endpoints
REST API for semantic search and encrypted storage
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from loguru import logger

from vault.spartan_vault import SpartanVault
from vault.vector_store import SpartanVectorStore


router = APIRouter()

# Global vault instance
_vault: Optional[SpartanVault] = None


def get_vault() -> SpartanVault:
    """
    Get or create the global vault instance.
    
    Returns:
        SpartanVault instance
    """
    global _vault
    if _vault is None:
        _vault = SpartanVault()
        logger.info("🏛️ Initialized SpartanVault for API")
    return _vault


# Pydantic models for request/response
class EmbedRequest(BaseModel):
    """Request model for embedding text."""
    text: str = Field(..., description="Text to embed")


class EmbedResponse(BaseModel):
    """Response model for embedding."""
    embedding: List[float] = Field(..., description="Embedding vector")
    dimension: int = Field(..., description="Embedding dimension")


class SearchRequest(BaseModel):
    """Request model for semantic search."""
    query: str = Field(..., description="Search query")
    top_k: int = Field(5, description="Number of results", ge=1, le=100)
    min_score: float = Field(0.0, description="Minimum similarity score", ge=0.0, le=1.0)
    decrypt: bool = Field(False, description="Whether to decrypt results")


class SearchResult(BaseModel):
    """Search result item."""
    id: str
    text: str
    score: float
    metadata: Dict[str, Any]
    created_at: str


class SearchResponse(BaseModel):
    """Response model for search."""
    results: List[SearchResult]
    query: str
    total: int


class HybridSearchRequest(BaseModel):
    """Request model for hybrid search."""
    query: str = Field(..., description="Search query")
    exact_ids: Optional[List[str]] = Field(None, description="IDs for exact matches")
    top_k: int = Field(5, description="Number of semantic results", ge=1, le=100)
    min_score: float = Field(0.0, description="Minimum similarity score", ge=0.0, le=1.0)
    decrypt: bool = Field(False, description="Whether to decrypt results")


class HybridSearchResponse(BaseModel):
    """Response model for hybrid search."""
    exact_matches: List[Dict[str, Any]]
    semantic_matches: List[SearchResult]
    query: str


class StoreRequest(BaseModel):
    """Request model for storing with embedding."""
    id: str = Field(..., description="Unique identifier")
    text: str = Field(..., description="Text to store")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")
    encrypt: bool = Field(True, description="Whether to encrypt")


class StoreResponse(BaseModel):
    """Response model for store operation."""
    id: str
    encrypted: bool
    embedded: bool
    stored_at: str
    metadata: Dict[str, Any]


class BatchEmbedRequest(BaseModel):
    """Request model for batch embedding."""
    texts: List[str] = Field(..., description="List of texts to embed")


class BatchEmbedResponse(BaseModel):
    """Response model for batch embedding."""
    embeddings: List[List[float]]
    count: int
    dimension: int


@router.post("/embed", response_model=EmbedResponse, tags=["vault"])
async def embed_text(request: EmbedRequest, vault: SpartanVault = Depends(get_vault)):
    """
    Generate embedding for a text string.
    
    **ΜΟΛΩΝ ΛΑΒΕ!** - Semantic vectorization
    """
    try:
        embedding = vault.vector_store.embed_text(request.text)
        
        return EmbedResponse(
            embedding=embedding.tolist(),
            dimension=len(embedding)
        )
    except Exception as e:
        logger.error(f"❌ Error embedding text: {e}")
        raise HTTPException(status_code=500, detail=f"Error embedding text: {str(e)}")


@router.post("/search", response_model=SearchResponse, tags=["vault"])
async def semantic_search(request: SearchRequest, vault: SpartanVault = Depends(get_vault)):
    """
    Perform semantic search using embeddings.
    
    **ΜΟΛΩΝ ΛΑΒΕ!** - Find similar content by meaning
    """
    try:
        results = vault.semantic_search(
            query=request.query,
            top_k=request.top_k,
            min_score=request.min_score,
            decrypt=request.decrypt
        )
        
        search_results = [SearchResult(**r) for r in results]
        
        return SearchResponse(
            results=search_results,
            query=request.query,
            total=len(search_results)
        )
    except Exception as e:
        logger.error(f"❌ Error in semantic search: {e}")
        raise HTTPException(status_code=500, detail=f"Error in search: {str(e)}")


@router.post("/hybrid-search", response_model=HybridSearchResponse, tags=["vault"])
async def hybrid_search(request: HybridSearchRequest, vault: SpartanVault = Depends(get_vault)):
    """
    Perform hybrid search (exact + semantic).
    
    **ΜΟΛΩΝ ΛΑΒΕ!** - Combined search strategy
    """
    try:
        results = vault.hybrid_search(
            query=request.query,
            exact_ids=request.exact_ids,
            top_k=request.top_k,
            min_score=request.min_score,
            decrypt=request.decrypt
        )
        
        semantic_results = [SearchResult(**r) for r in results['semantic_matches']]
        
        return HybridSearchResponse(
            exact_matches=results['exact_matches'],
            semantic_matches=semantic_results,
            query=request.query
        )
    except Exception as e:
        logger.error(f"❌ Error in hybrid search: {e}")
        raise HTTPException(status_code=500, detail=f"Error in hybrid search: {str(e)}")


@router.get("/similar/{id}", tags=["vault"])
async def find_similar(id: str, top_k: int = 5, decrypt: bool = False, 
                      vault: SpartanVault = Depends(get_vault)):
    """
    Find entries similar to a given entry ID.
    
    **ΜΟΛΩΝ ΛΑΒΕ!** - Discover related content
    """
    try:
        # Check if entry exists first
        entry = vault.vector_store.get_entry(id)
        if not entry:
            raise HTTPException(status_code=404, detail=f"Entry not found: {id}")
        
        results = vault.find_similar(id, top_k, decrypt)
        
        return {
            'id': id,
            'similar': results,
            'count': len(results)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error finding similar: {e}")
        raise HTTPException(status_code=500, detail=f"Error finding similar: {str(e)}")


@router.post("/store-with-embedding", response_model=StoreResponse, tags=["vault"])
async def store_with_embedding(request: StoreRequest, vault: SpartanVault = Depends(get_vault)):
    """
    Store data with both encryption and embedding.
    
    **ΜΟΛΩΝ ΛΑΒΕ!** - Secure and searchable storage
    """
    try:
        result = vault.store_with_embedding(
            id=request.id,
            text=request.text,
            metadata=request.metadata,
            encrypt=request.encrypt
        )
        
        return StoreResponse(**result)
    except Exception as e:
        logger.error(f"❌ Error storing with embedding: {e}")
        raise HTTPException(status_code=500, detail=f"Error storing: {str(e)}")


@router.get("/stats", tags=["vault"])
async def get_stats(vault: SpartanVault = Depends(get_vault)):
    """
    Get vault statistics.
    
    **ΜΟΛΩΝ ΛΑΒΕ!** - System metrics
    """
    try:
        stats = vault.get_stats()
        return stats
    except Exception as e:
        logger.error(f"❌ Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


@router.post("/save", tags=["vault"])
async def save_to_disk(vault: SpartanVault = Depends(get_vault)):
    """
    Save vault to disk (persistence).
    
    **ΜΟΛΩΝ ΛΑΒΕ!** - Persist the vault
    """
    try:
        vault.save_to_disk()
        return {
            'status': 'success',
            'message': 'Vault saved to disk',
            'stats': vault.get_stats()
        }
    except Exception as e:
        logger.error(f"❌ Error saving to disk: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving: {str(e)}")


@router.post("/batch-embed", response_model=BatchEmbedResponse, tags=["vault"])
async def batch_embed(request: BatchEmbedRequest, vault: SpartanVault = Depends(get_vault)):
    """
    Generate embeddings for multiple texts (batch processing).
    
    **ΜΟΛΩΝ ΛΑΒΕ!** - Efficient batch vectorization
    """
    try:
        if not request.texts:
            raise HTTPException(status_code=400, detail="Empty text list")
        
        embeddings = vault.vector_store.embed_batch(request.texts)
        
        return BatchEmbedResponse(
            embeddings=[emb.tolist() for emb in embeddings],
            count=len(embeddings),
            dimension=len(embeddings[0]) if embeddings else 0
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in batch embedding: {e}")
        raise HTTPException(status_code=500, detail=f"Error in batch embedding: {str(e)}")
