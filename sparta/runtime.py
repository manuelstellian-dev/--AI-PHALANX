"""
SPARTA Runtime - shared, lazily-loaded SPARTA instance for the running system.

Connects the SPARTA Foundation (semantic_memory.jsonl) to ΛΕΩΝΙΔΑΣ:
the API route /api/v1/sparta/* and the CommandProcessor command
``sparta_query`` both use the same runtime, so the knowledge base is
loaded once per process.
"""

import os
import threading
from typing import Any, Dict, Optional

from polis.log import logger

from sparta.foundation_bridge import FoundationBridge
from sparta.reflexive_generator import ReflexiveGenerator
from sparta.semantic_foundation import SemanticFoundation

# Default knowledge base shipped with the repository
DEFAULT_MEMORY_PATH = os.path.join(os.path.dirname(__file__), 'semantic_memory.jsonl')


class SpartaRuntime:
    """
    SPARTA Foundation + Bridge + Reflexive Generator wired together.
    
    Attributes:
        foundation: Loaded SemanticFoundation
        bridge: FoundationBridge over the foundation
        generator: ReflexiveGenerator over the foundation
        memory_path: Path of the loaded JSONL knowledge base
    """
    
    def __init__(self, memory_path: str = DEFAULT_MEMORY_PATH, confidence_threshold: float = 0.7):
        """
        Load the knowledge base and build the reasoning components.
        
        Args:
            memory_path: Path to the JSONL knowledge base
            confidence_threshold: FoundationBridge validation threshold
        """
        self.memory_path = memory_path
        self.foundation = SemanticFoundation()
        self.foundation.load_memory(memory_path)
        self.bridge = FoundationBridge(self.foundation, confidence_threshold=confidence_threshold)
        self.generator = ReflexiveGenerator(self.foundation)
        logger.info(f"🏛️ SPARTA runtime ready ({len(self.foundation.concepts)} concepts)")
    
    def query(self, query: str) -> Dict[str, Any]:
        """
        Answer a query by logical reasoning over the Foundation.
        
        Args:
            query: Natural-language query
            
        Returns:
            Reflexive Generator result (response, confidence, sources,
            reasoning_chain, verified) plus the Bridge's epistemic status
        """
        result = self.generator.generate_with_reflection(query, self.foundation)
        result['epistemic_status'] = self.bridge.get_epistemic_status(query)
        return result


_runtime: Optional[SpartaRuntime] = None
_runtime_lock = threading.Lock()


def get_runtime(memory_path: Optional[str] = None) -> SpartaRuntime:
    """
    Return the process-wide SPARTA runtime, loading it on first use.
    
    Args:
        memory_path: Knowledge base path (only used on first load)
        
    Returns:
        Shared SpartaRuntime instance
    """
    global _runtime
    with _runtime_lock:
        if _runtime is None:
            _runtime = SpartaRuntime(memory_path or DEFAULT_MEMORY_PATH)
        return _runtime


def reset_runtime() -> None:
    """Drop the cached runtime (used by tests and reloads)."""
    global _runtime
    with _runtime_lock:
        _runtime = None
