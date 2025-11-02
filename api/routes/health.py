"""
Health Check Routes
Verifică starea sistemului ΛΕΩΝΙΔΑΣ-AI
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any
from loguru import logger
import api.server as server

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Verifică starea de sănătate a sistemului.
    
    Returns:
        Starea sistemului
    """
    return {
        "status": "healthy",
        "system": "ΛΕΩΝΙΔΑΣ-AI PHALANX",
        "motto": "ΜΟΛΩΝ ΛΑΒΕ",
        "version": "0.1.0"
    }


@router.get("/health/detailed")
async def detailed_health_check(token: str = Depends(server.verify_token)) -> Dict[str, Any]:
    """
    Verifică starea detaliată a tuturor modulelor (necesită autentificare).
    
    Returns:
        Starea detaliată a sistemului
    """
    if not server.leonidas_brain or not server.command_processor:
        return {
            "status": "initializing",
            "system": "ΛΕΩΝΙΔΑΣ-AI PHALANX"
        }
    
    # Obține starea de la Λ-Core
    brain_status = server.leonidas_brain.get_status()
    
    # Obține starea de la toate modulele
    system_status = await server.command_processor.process_command({
        "type": "status",
        "priority": "normal"
    })
    
    return {
        "status": "healthy",
        "system": "ΛΕΩΝΙΔΑΣ-AI PHALANX",
        "brain": brain_status,
        "modules": system_status.get('modules', {}),
        "adaptation_factor": server.command_processor.get_adaptation_factor()
    }


@router.get("/health/survival")
async def survival_probability(token: str = Depends(server.verify_token)) -> Dict[str, Any]:
    """
    Verifică probabilitatea de supraviețuire a sistemului (necesită autentificare).
    
    Returns:
        Probabilitatea de supraviețuire
    """
    if not server.leonidas_brain:
        return {
            "status": "initializing",
            "survival_probability": None
        }
    
    modules = server.leonidas_brain.modules
    
    if 'phalanx' in modules and 'helot' in modules['phalanx']:
        survival_prob = await modules['phalanx']['helot'].get_survival_probability()
        resources = await modules['phalanx']['helot'].monitor_resources()
        
        return {
            "status": "ok",
            "survival_probability": survival_prob,
            "resources": resources,
            "warning": "critical" if survival_prob < 0.95 else None
        }
    
    return {
        "status": "error",
        "error": "Helot module not available"
    }
