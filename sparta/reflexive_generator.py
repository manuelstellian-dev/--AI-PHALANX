"""
SPARTA Reflexive Generator - Anti-Hallucination System

This module implements reflexive generation with verification, providing:
- Reflex tagging system for epistemic markers
- Real-time hallucination detection
- Source concept tracking
- Honest uncertainty admission
"""

from typing import Dict, List, Optional
from loguru import logger
from sparta.semantic_foundation import SemanticFoundation


class ReflexiveGenerator:
    """
    Reflexive generation system with anti-hallucination mechanisms.
    
    Provides generation capabilities that include real-time verification
    against the SPARTA Foundation, tagging statements with epistemic
    markers, and detecting potential hallucinations.
    
    Epistemic Tags:
    - [VERIFIED]: High confidence (>0.95), verified against foundation
    - [INFERRED]: Medium confidence (0.75-0.95), supported by foundation
    - [UNCERTAIN]: Low confidence (0.5-0.75), weak foundation support
    - [UNKNOWN]: No foundation support, honest admission of ignorance
    """
    
    def __init__(self, foundation: SemanticFoundation):
        """
        Initialize the Reflexive Generator.
        
        Args:
            foundation: SemanticFoundation instance for verification
        """
        self.foundation = foundation
        logger.info("🎯 SPARTA Reflexive Generator initialized")
    
    def generate_with_reflection(self, prompt: str, foundation: SemanticFoundation) -> Dict:
        """
        Generate a response with reflexive verification.
        
        This method would integrate with an LLM to generate a response,
        then verify it against the foundation and tag appropriately.
        
        Args:
            prompt: Input prompt for generation
            foundation: SemanticFoundation to verify against
            
        Returns:
            Dictionary containing:
            - prompt: Original prompt
            - raw_response: Untagged response
            - tagged_response: Response with epistemic tags
            - verification: Verification details
            - source_concepts: Concepts used for verification
        """
        logger.debug(f"🎯 Generating with reflection for prompt: {prompt[:50]}...")
        
        # Extract relevant concepts from prompt
        relevant_concepts = self._extract_concepts_from_text(prompt, foundation)
        
        # Simulate generation (in real implementation, this would call LLM)
        raw_response = f"Response based on concepts: {', '.join(relevant_concepts)}"
        
        # Verify the response
        verification = foundation.verify_statement(raw_response, relevant_concepts)
        
        # Tag the response based on verification
        tagged_response = self.tag_statement(raw_response, relevant_concepts)
        
        result = {
            'prompt': prompt,
            'raw_response': raw_response,
            'tagged_response': tagged_response,
            'verification': verification,
            'source_concepts': relevant_concepts,
            'hallucination_detected': not verification['verified']
        }
        
        logger.debug(f"✅ Generation complete (verified: {verification['verified']})")
        return result
    
    def tag_statement(self, statement: str, source_concepts: List[str]) -> str:
        """
        Tag a statement with appropriate epistemic marker.
        
        Analyzes the statement against source concepts and adds an
        epistemic tag indicating the confidence level.
        
        Args:
            statement: Statement to tag
            source_concepts: List of concept IDs supporting the statement
            
        Returns:
            Tagged statement with epistemic marker
        """
        logger.debug(f"🏷️ Tagging statement with {len(source_concepts)} source concepts")
        
        # Verify statement against concepts
        verification = self.foundation.verify_statement(statement, source_concepts)
        confidence = verification['confidence']
        
        # Determine appropriate tag
        if not source_concepts or not verification['verified']:
            tag = "[UNKNOWN]"
            statement = f"I don't have verified information about this. {statement}"
        elif confidence >= 0.95:
            tag = "[VERIFIED]"
        elif confidence >= 0.75:
            tag = "[INFERRED]"
        elif confidence >= 0.5:
            tag = "[UNCERTAIN]"
        else:
            tag = "[UNKNOWN]"
            statement = f"I have very limited information about this. {statement}"
        
        tagged = f"{tag} {statement}"
        logger.debug(f"✅ Statement tagged: {tag}")
        
        return tagged
    
    def detect_hallucination(self, statement: str, foundation: SemanticFoundation) -> bool:
        """
        Detect if a statement contains potential hallucinations.
        
        Analyzes the statement to identify content that cannot be
        verified against the foundation, indicating potential hallucination.
        
        Args:
            statement: Statement to analyze
            foundation: SemanticFoundation to verify against
            
        Returns:
            True if hallucination is detected, False otherwise
        """
        logger.debug("🔍 Detecting potential hallucinations")
        
        # Extract concepts mentioned in statement
        mentioned_concepts = self._extract_concepts_from_text(statement, foundation)
        
        if not mentioned_concepts:
            # No verifiable concepts found - potential hallucination
            logger.warning("⚠️ Hallucination detected: No verifiable concepts")
            return True
        
        # Verify statement against found concepts
        verification = foundation.verify_statement(statement, mentioned_concepts)
        
        # Hallucination if confidence is below threshold or not verified
        is_hallucination = not verification['verified'] or verification['confidence'] < 0.5
        
        if is_hallucination:
            logger.warning(
                f"⚠️ Hallucination detected: confidence {verification['confidence']:.2f}"
            )
        else:
            logger.debug("✅ No hallucination detected")
        
        return is_hallucination
    
    def honest_response(self, query: str, foundation: SemanticFoundation) -> str:
        """
        Generate an honest response that admits uncertainty when appropriate.
        
        Analyzes what is known about the query and generates a response
        that honestly reflects the epistemic status, including admissions
        of uncertainty or ignorance when warranted.
        
        Args:
            query: User query
            foundation: SemanticFoundation to query
            
        Returns:
            Honest response string with appropriate epistemic framing
        """
        logger.debug(f"🎯 Generating honest response for query")
        
        # Extract relevant concepts
        relevant_concepts = self._extract_concepts_from_text(query, foundation)
        
        if not relevant_concepts:
            return (
                "[UNKNOWN] I don't have verified knowledge about this topic in my "
                "foundation. I cannot provide a reliable answer without risking "
                "hallucination. Please provide more context or rephrase your question."
            )
        
        # Get concepts and calculate confidence
        concepts = [foundation.get_concept(cid) for cid in relevant_concepts]
        concepts = [c for c in concepts if c is not None]
        
        if not concepts:
            return (
                "[UNKNOWN] While I recognize some terms in your query, I cannot "
                "verify them against my knowledge foundation. I prefer to admit "
                "uncertainty rather than risk providing incorrect information."
            )
        
        # Calculate average confidence
        avg_confidence = sum(c['confidence'] for c in concepts) / len(concepts)
        
        # Build honest response based on confidence
        if avg_confidence >= 0.9:
            prefix = "[VERIFIED]"
            framing = "I have high-confidence verified knowledge about this:"
        elif avg_confidence >= 0.75:
            prefix = "[INFERRED]"
            framing = "Based on my knowledge foundation, I can provide this information:"
        elif avg_confidence >= 0.5:
            prefix = "[UNCERTAIN]"
            framing = "I have some information, but with lower confidence:"
        else:
            prefix = "[UNKNOWN]"
            framing = "I have very limited verified information about this:"
        
        # Build response with concept information
        response_parts = [f"{prefix} {framing}"]
        
        for concept in concepts[:3]:  # Limit to top 3 concepts
            response_parts.append(
                f"\n- {concept['id']}: {concept['definition']} "
                f"(confidence: {concept['confidence']:.2f})"
            )
        
        if len(concepts) > 3:
            response_parts.append(f"\n- ... and {len(concepts) - 3} more related concepts")
        
        response = ''.join(response_parts)
        logger.debug(f"✅ Honest response generated with {len(concepts)} concepts")
        
        return response
    
    def _extract_concepts_from_text(
        self, text: str, foundation: SemanticFoundation
    ) -> List[str]:
        """
        Extract concept IDs mentioned in text.
        
        This is a helper method that searches the text for mentions of
        concepts from the foundation.
        
        Args:
            text: Text to analyze
            foundation: SemanticFoundation to search
            
        Returns:
            List of concept IDs found in the text
        """
        text_lower = text.lower()
        found_concepts = []
        
        for concept_id, concept in foundation.concepts.items():
            # Check if concept ID appears in text (with underscores replaced by spaces)
            if concept_id.replace('_', ' ') in text_lower:
                found_concepts.append(concept_id)
                continue
            
            # Check if key words from definition appear in text
            definition_words = set(concept['definition'].lower().split())
            text_words = set(text_lower.split())
            
            # If significant overlap (>30% of definition words), consider it a match
            overlap = len(definition_words & text_words)
            if overlap >= len(definition_words) * 0.3 and overlap >= 2:
                found_concepts.append(concept_id)
        
        return found_concepts
    
    def verify_generation_batch(
        self, statements: List[str], foundation: SemanticFoundation
    ) -> List[Dict]:
        """
        Verify a batch of generated statements.
        
        Processes multiple statements and verifies each against the
        foundation, useful for batch generation scenarios.
        
        Args:
            statements: List of statements to verify
            foundation: SemanticFoundation to verify against
            
        Returns:
            List of verification results for each statement
        """
        logger.debug(f"🔍 Verifying batch of {len(statements)} statements")
        
        results = []
        
        for i, statement in enumerate(statements):
            # Extract concepts from statement
            concepts = self._extract_concepts_from_text(statement, foundation)
            
            # Verify statement
            verification = foundation.verify_statement(statement, concepts)
            
            # Detect hallucination
            is_hallucination = self.detect_hallucination(statement, foundation)
            
            # Tag statement
            tagged = self.tag_statement(statement, concepts)
            
            results.append({
                'index': i,
                'statement': statement,
                'tagged_statement': tagged,
                'verification': verification,
                'hallucination_detected': is_hallucination,
                'source_concepts': concepts
            })
        
        logger.debug(f"✅ Batch verification complete")
        return results
