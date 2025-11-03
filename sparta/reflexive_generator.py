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
    
    def generate_with_reflection(self, query: str, foundation: SemanticFoundation) -> Dict:
        """
        Generate response through LOGICAL reasoning, not text prediction.
        
        Process:
        1. Classify query → extract topic
        2. Get relevant concepts from Foundation (via Bridge pattern)
        3. If NO concepts found → return honest "I don't know"
        4. Build logical reasoning chain from concepts
        5. Return response with confidence tracking
        
        Args:
            query: User query to respond to
            foundation: SemanticFoundation to reason from
            
        Returns:
            Dictionary containing:
            - response: Generated text with logical reasoning
            - confidence: Minimum confidence of all used concepts
            - sources: List of concept IDs used
            - reasoning_chain: List of reasoning steps
            - verified: Boolean indicating if response is verified
        """
        logger.debug(f"🎯 Generating with logical reflection for query: {query[:50]}...")
        
        # TODO: Integrate with Λ-Identity (knows knowledge sources)
        # TODO: Integrate with Λ-Pattern (detects deviations from Foundation)
        # TODO: Integrate with Λ-Meta (explains reasoning choices)
        
        # Step 1: Extract relevant concepts
        relevant_concepts = self._extract_concepts_from_text(query, foundation)
        
        # Step 2: If no concepts found, return honest unknown
        if not relevant_concepts:
            return self.honest_response(query, foundation)
        
        # Step 3: Get full concept data
        concepts = [foundation.get_concept(cid) for cid in relevant_concepts]
        concepts = [c for c in concepts if c is not None]
        
        if not concepts:
            return self.honest_response(query, foundation)
        
        # Step 4: Build logical reasoning chain
        reasoning_chain, response_text = self._logical_expansion(concepts)
        
        # Step 5: Calculate minimum confidence
        min_confidence = min(c['confidence'] for c in concepts)
        
        # Step 6: Verify response meets SPARTA standards (>= 0.95)
        verified = min_confidence >= 0.95
        
        # Add verification tag
        verification_tag = self._verify_statement(response_text, foundation)
        tagged_response = f"{verification_tag} {response_text}"
        
        result = {
            'response': tagged_response,
            'confidence': min_confidence,
            'sources': [c['id'] for c in concepts],
            'reasoning_chain': reasoning_chain,
            'verified': verified
        }
        
        logger.debug(
            f"✅ Logical generation complete: "
            f"verified={verified}, confidence={min_confidence:.2f}"
        )
        
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
        
        Returns True if statement has NO support in Foundation (confidence < 0.80).
        This implements SPARTA's strict anti-hallucination standards.
        
        Args:
            statement: Statement to analyze
            foundation: SemanticFoundation to verify against
            
        Returns:
            True if hallucination is detected (confidence < 0.80), False otherwise
        """
        logger.debug("🔍 Detecting potential hallucinations")
        
        # Extract concepts mentioned in statement
        mentioned_concepts = self._extract_concepts_from_text(statement, foundation)
        
        if not mentioned_concepts:
            # No verifiable concepts found - definite hallucination
            logger.warning("⚠️ Hallucination detected: No verifiable concepts")
            return True
        
        # Get concept objects and check confidence
        concept_objs = [foundation.get_concept(cid) for cid in mentioned_concepts]
        concept_objs = [c for c in concept_objs if c is not None]
        
        if not concept_objs:
            logger.warning("⚠️ Hallucination detected: Concepts not found in Foundation")
            return True
        
        # Check minimum confidence against SPARTA threshold
        min_confidence = min(c['confidence'] for c in concept_objs)
        
        # Hallucination if confidence below 0.80
        is_hallucination = min_confidence < 0.80
        
        if is_hallucination:
            logger.warning(
                f"⚠️ Hallucination detected: confidence {min_confidence:.2f} < 0.80"
            )
        else:
            logger.debug(f"✅ No hallucination detected (confidence: {min_confidence:.2f})")
        
        return is_hallucination
    
    def honest_response(self, query: str, foundation: SemanticFoundation) -> Dict:
        """
        When concepts NOT in Foundation or confidence < 0.95.
        
        Returns honest admission following SPARTA principles:
        - Only provide information with confidence >= 95%
        - Admit when knowledge is missing or uncertain
        - Provide context about current coverage
        
        Args:
            query: User query
            foundation: SemanticFoundation to query
            
        Returns:
            Dictionary with honest admission and Foundation status
        """
        logger.debug("🎯 Generating honest UNKNOWN response")
        
        # TODO: Integrate with Λ-Affect (emotional response to confidence - honesty feels right)
        # TODO: Integrate with Λ-Reflect (learns from rejected responses)
        # TODO: Integrate with Λ-Zero (balances logic vs creative expansion - prefers honesty)
        
        # Extract relevant concepts
        relevant_concepts = self._extract_concepts_from_text(query, foundation)
        
        # Check if any concepts found and their quality
        low_confidence = False
        if relevant_concepts:
            concepts = [foundation.get_concept(cid) for cid in relevant_concepts]
            concepts = [c for c in concepts if c is not None]
            if concepts:
                min_confidence = min(c['confidence'] for c in concepts)
                if min_confidence < 0.95:
                    low_confidence = True
        
        # Get available domains
        stats = foundation.get_statistics()
        available_domains = sorted(stats.get('domain_distribution', {}).keys())
        
        # Build honest response
        if not relevant_concepts or not concepts:
            reason = "I don't have verified knowledge (confidence >= 0.95) about this topic."
        elif low_confidence:
            reason = f"I have information about this topic, but with confidence < 0.95 (actual: {min_confidence:.2f}), which does not meet SPARTA standards."
        else:
            reason = "The concepts found do not sufficiently address your query."
        
        response = (
            f"[UNKNOWN] {reason}\n\n"
            f"SPARTA Foundation principles:\n"
            f"- Only provide information with confidence >= 95%\n"
            f"- Current coverage: Phase 1 (10% - {stats['total_concepts']} concepts)\n"
            f"- Available domains: {', '.join(available_domains)}\n\n"
            f"ΜΟΛΩΝ ΛΑΒΕ - Truth or Silence! 🏛️"
        )
        
        result = {
            'response': response,
            'confidence': 0.0,
            'sources': [],
            'reasoning_chain': ["Query analysis", "No sufficient high-confidence concepts found", "Honest admission of limitations"],
            'verified': False
        }
        
        logger.debug("✅ Honest UNKNOWN response generated")
        return result
    
    def _logical_expansion(self, concepts: List[Dict]) -> tuple[List[str], str]:
        """
        CRITICAL: This is NOT text generation!
        
        Build response by logical reasoning:
        1. Select primary concept (highest confidence + most relevant)
        2. Explore relations (connected concepts)
        3. Build logical chain: A → B → conclusion
        4. Construct response explaining reasoning
        
        Args:
            concepts: List of concept dictionaries to reason from
            
        Returns:
            Tuple of (reasoning_chain, response_text)
        """
        logger.debug(f"🧠 Building logical expansion from {len(concepts)} concepts")
        
        if not concepts:
            return ([], "No concepts available for logical expansion")
        
        # Step 1: Select primary concept (highest confidence)
        primary = max(concepts, key=lambda c: c['confidence'])
        
        reasoning_chain = [
            f"Primary concept: {primary['id']} (confidence: {primary['confidence']:.2f})",
            f"Definition: {primary['definition']}"
        ]
        
        # Step 2: Explore relations
        related_ids = primary.get('relations', [])
        related_concepts = [c for c in concepts if c['id'] in related_ids]
        
        if related_concepts:
            reasoning_chain.append(
                f"Related concepts found: {', '.join(c['id'] for c in related_concepts)}"
            )
            
            # Build logical chain
            for related in related_concepts[:2]:  # Limit to 2 for clarity
                reasoning_chain.append(
                    f"Connection: {primary['id']} relates to {related['id']}"
                )
                reasoning_chain.append(
                    f"  {related['id']}: {related['definition']}"
                )
        
        # Step 3: Construct response with explicit reasoning
        response_parts = [f"Based on {primary.get('topic', primary['id'])}:"]
        response_parts.append(f"\n{primary['definition']}")
        
        if related_concepts:
            response_parts.append(f"\n\nThis concept is related to:")
            for related in related_concepts[:2]:
                response_parts.append(
                    f"\n- {related.get('topic', related['id'])}: {related['definition']}"
                )
        
        # Add formal statement if available
        if 'formal_statement' in primary and primary['formal_statement']:
            response_parts.append(f"\n\nFormal statement: {primary['formal_statement']}")
            reasoning_chain.append(f"Formal statement provided: {primary['formal_statement']}")
        
        response_text = ''.join(response_parts)
        reasoning_chain.append("Response constructed from logical connections")
        
        logger.debug(f"✅ Logical expansion complete: {len(reasoning_chain)} steps")
        return (reasoning_chain, response_text)
    
    def _verify_statement(self, statement: str, foundation: SemanticFoundation) -> str:
        """
        SPARTAN STANDARDS: confidence >= 0.95 only
        
        Verifies a statement against SPARTA quality standards and returns
        the appropriate epistemic marker.
        
        Args:
            statement: Statement to verify
            foundation: SemanticFoundation to verify against
            
        Returns:
            One of: "[VERIFIED]", "[UNCERTAIN]", "[UNKNOWN]"
        """
        # Extract concepts from statement
        concepts = self._extract_concepts_from_text(statement, foundation)
        
        if not concepts:
            return "[UNKNOWN]"
        
        # Get concept objects and calculate confidence
        concept_objs = [foundation.get_concept(cid) for cid in concepts]
        concept_objs = [c for c in concept_objs if c is not None]
        
        if not concept_objs:
            return "[UNKNOWN]"
        
        min_confidence = min(c['confidence'] for c in concept_objs)
        
        # SPARTA standards: only >= 0.95 is VERIFIED
        if min_confidence >= 0.95:
            return "[VERIFIED]"
        elif min_confidence >= 0.80:
            return "[UNCERTAIN]"
        else:
            return "[UNKNOWN]"
    
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
        # Constant for minimum word overlap threshold
        MIN_WORD_OVERLAP_RATIO = 0.3
        MIN_ABSOLUTE_OVERLAP = 2
        
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
            
            # If significant overlap, consider it a match
            overlap = len(definition_words & text_words)
            if overlap >= len(definition_words) * MIN_WORD_OVERLAP_RATIO and overlap >= MIN_ABSOLUTE_OVERLAP:
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
