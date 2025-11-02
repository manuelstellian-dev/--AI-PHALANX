"""
Command Routes
Procesează comenzile tactice către ΛΕΩΝΙΔΑΣ-AI
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from loguru import logger
import api.server as server

router = APIRouter()


class TacticalCommand(BaseModel):
    """Model pentru comenzi tactice."""
    type: str = Field(..., description="Tipul comenzii")
    payload: Optional[Dict[str, Any]] = Field(default={}, description="Payload-ul comenzii")
    priority: Optional[str] = Field(default="normal", description="Prioritatea: high, normal, low")


@router.post("/command")
async def execute_command(
    command: TacticalCommand,
    token: str = Depends(server.verify_token)
) -> Dict[str, Any]:
    """
    Execută o comandă tactică (necesită autentificare).
    
    Args:
        command: Comanda tactică de executat
        
    Returns:
        Rezultatul execuției
    """
    if not server.command_processor:
        raise HTTPException(status_code=503, detail="Command processor not initialized")
    
    logger.info(f"📥 Tactical command received: {command.type} (priority: {command.priority})")
    
    try:
        result = await server.command_processor.process_command({
            "type": command.type,
            "payload": command.payload,
            "priority": command.priority
        })
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Command execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/command/status")
async def get_system_status(token: str = Depends(server.verify_token)) -> Dict[str, Any]:
    """
    Obține starea completă a sistemului (necesită autentificare).
    
    Returns:
        Starea sistemului
    """
    if not server.command_processor:
        raise HTTPException(status_code=503, detail="Command processor not initialized")
    
    return await server.command_processor.process_command({
        "type": "status",
        "priority": "normal"
    })


class RiskAnalysisRequest(BaseModel):
    """Model pentru cereri de analiză de risc."""
    scenario_name: str = Field(..., description="Numele scenariului")
    risk_factors: list = Field(default=[], description="Factori de risc")
    severity: float = Field(default=0.5, ge=0.0, le=1.0, description="Severitatea (0.0-1.0)")
    complexity: float = Field(default=0.5, ge=0.0, le=1.0, description="Complexitatea (0.0-1.0)")
    available_resources: float = Field(default=1.0, ge=0.0, le=1.0, description="Resurse disponibile (0.0-1.0)")


@router.post("/command/analyze-risk")
async def analyze_risk(
    request: RiskAnalysisRequest,
    token: str = Depends(server.verify_token)
) -> Dict[str, Any]:
    """
    Cere Battle Oracle să analizeze un scenariu de risc (necesită autentificare).
    
    Args:
        request: Cererea de analiză de risc
        
    Returns:
        Analiza de risc
    """
    if not server.command_processor:
        raise HTTPException(status_code=503, detail="Command processor not initialized")
    
    result = await server.command_processor.process_command({
        "type": "analyze_risk",
        "payload": {
            "name": request.scenario_name,
            "risk_factors": request.risk_factors,
            "severity": request.severity,
            "complexity": request.complexity,
            "available_resources": request.available_resources
        },
        "priority": "high"
    })
    
    return result


class EncryptionRequest(BaseModel):
    """Model pentru cereri de criptare."""
    data: str = Field(..., description="Datele de criptat")


@router.post("/command/encrypt")
async def encrypt_data(
    request: EncryptionRequest,
    token: str = Depends(server.verify_token)
) -> Dict[str, Any]:
    """
    Criptează date folosind Spartan Guard (necesită autentificare).
    
    Args:
        request: Cererea de criptare
        
    Returns:
        Datele criptate
    """
    if not server.command_processor:
        raise HTTPException(status_code=503, detail="Command processor not initialized")
    
    result = await server.command_processor.process_command({
        "type": "encrypt_data",
        "payload": {"data": request.data},
        "priority": "normal"
    })
    
    return result


@router.get("/command/check-airgap")
async def check_airgap(token: str = Depends(server.verify_token)) -> Dict[str, Any]:
    """
    Verifică starea Air-Gap prin Shield Bearer (necesită autentificare).
    
    Returns:
        Starea Air-Gap
    """
    if not server.command_processor:
        raise HTTPException(status_code=503, detail="Command processor not initialized")
    
    result = await server.command_processor.process_command({
        "type": "check_airgap",
        "priority": "high"
    })
    
    return result
