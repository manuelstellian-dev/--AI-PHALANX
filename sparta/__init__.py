"""
SPARTA - Semantic Processing And Reasoning Through Axioms
Foundation system for ΛΕΩΝΙΔΑΣ-AI PHALANX

ΜΟΛΩΝ ΛΑΒΕ (Molon Labe) - "Come and Take Them"

This module provides:
- SemanticFoundation: Core knowledge management engine
- FoundationBridge: LLM integration layer
- ReflexiveGenerator: Anti-hallucination generation system
"""

from sparta.semantic_foundation import SemanticFoundation
from sparta.foundation_bridge import FoundationBridge
from sparta.reflexive_generator import ReflexiveGenerator

__version__ = "0.1.0"
__author__ = "ΛΕΩΝΙΔΑΣ-AI PHALANX Team"
__all__ = [
    "SemanticFoundation",
    "FoundationBridge",
    "ReflexiveGenerator",
]
