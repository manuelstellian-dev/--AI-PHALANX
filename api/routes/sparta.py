"""
SPARTA Routes
Expune SPARTA Foundation (raționament anti-halucinație) prin API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
from polis.log import logger

from sparta.runtime import get_runtime

router = APIRouter()


class SpartaQuery(BaseModel):
    """Model pentru interogări SPARTA."""
    query: str = Field(..., min_length=1, description="Întrebarea în limbaj natural")


@router.post("/query")
async def sparta_query(request: SpartaQuery) -> Dict[str, Any]:
    """
    Răspunde prin raționament logic peste Foundation (nu prin predicție de token-uri).
    
    Returns:
        response, confidence, sources, reasoning_chain, verified, epistemic_status
    """
    try:
        return get_runtime().query(request.query)
    except Exception as e:
        logger.error(f"❌ SPARTA query error: {e}")
        raise HTTPException(status_code=500, detail=f"SPARTA query error: {e}")


@router.get("/concept/{concept_id}")
async def get_concept(concept_id: str) -> Dict[str, Any]:
    """
    Returnează un concept verificat din Foundation.
    
    Returns:
        Conceptul complet (16 câmpuri)
    """
    concept = get_runtime().foundation.get_concept(concept_id)
    if concept is None:
        raise HTTPException(status_code=404, detail=f"Concept not found: {concept_id}")
    return concept


@router.get("/stats")
async def get_stats() -> Dict[str, Any]:
    """
    Statistici despre baza de cunoștințe (concepte, domenii, încredere).
    """
    return get_runtime().foundation.get_statistics()


@router.get("/integrity")
async def get_integrity() -> Dict[str, Any]:
    """
    Raport de integritate a grafului de cunoștințe (referințe lipsă).
    """
    return get_runtime().foundation.get_integrity_report()
