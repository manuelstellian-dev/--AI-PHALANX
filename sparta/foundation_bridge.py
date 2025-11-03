"""
SPARTA Foundation Bridge - LLM Integration Layer

This module provides integration between the SPARTA Foundation and
LLM systems (LeondasBrain), enabling:
- Query enrichment with semantic context
- Response validation against Foundation
- Confidence scoring for LLM outputs
- Honest epistemic responses
"""

from typing import Dict, List, Optional, Any
from loguru import logger
from sparta.semantic_foundation import SemanticFoundation


class FoundationBridge:
    """
    Bridge between SPARTA Foundation and LLM systems.
    
    Provides integration hooks for enriching queries with semantic context,
    validating LLM responses against the foundation, and ensuring honest
    epistemic responses when knowledge is uncertain.
    
    Attributes:
        foundation (SemanticFoundation): The semantic foundation instance
        confidence_threshold (float): Minimum confidence for validated responses
    """
    
    def __init__(self, foundation: SemanticFoundation, confidence_threshold: float = 0.7):
        """
        Initialize the Foundation Bridge.
        
        Args:
            foundation: SemanticFoundation instance to bridge with
            confidence_threshold: Minimum confidence for response validation (default: 0.7)
        """
        self.foundation = foundation
        self.confidence_threshold = confidence_threshold
        logger.info(f"🌉 SPARTA Foundation Bridge initialized (threshold: {confidence_threshold})")
    
    def enrich_query(self, query: str) -> Dict:
        """
        Enrich a query with relevant semantic context from the foundation.
        
        Analyzes the query to identify relevant concepts and provides
        contextual information to improve LLM response quality.
        
        Args:
            query: User query to enrich
            
        Returns:
            Dictionary containing:
            - original_query: The original query
            - relevant_concepts: List of relevant concepts
            - context: Additional semantic context
            - confidence: Confidence in the enrichment
        """
        logger.debug(f"🔍 Enriching query: {query[:50]}...")
        
        # Extract potential concept IDs from query (simple keyword matching)
        query_lower = query.lower()
        relevant_concepts = []
        
        # Search for concepts mentioned in query
        for concept_id, concept in self.foundation.concepts.items():
            # Check if concept ID or definition keywords appear in query
            if concept_id.replace('_', ' ') in query_lower:
                relevant_concepts.append(concept)
                continue
            
            # Check definition for relevance (simple keyword match)
            definition_words = concept['definition'].lower().split()
            query_words = query_lower.split()
            
            # Count matching words
            matches = sum(1 for word in query_words if word in definition_words)
            if matches >= 2:  # At least 2 matching words
                relevant_concepts.append(concept)
        
        # Build context from relevant concepts
        context_parts = []
        for concept in relevant_concepts[:5]:  # Limit to top 5
            context_parts.append(
                f"[{concept['id']}] {concept['definition']} "
                f"(confidence: {concept['confidence']:.2f})"
            )
        
        # Calculate overall confidence
        if relevant_concepts:
            confidence = sum(c['confidence'] for c in relevant_concepts) / len(relevant_concepts)
        else:
            confidence = 0.0
        
        result = {
            'original_query': query,
            'relevant_concepts': [c['id'] for c in relevant_concepts],
            'context': '\n'.join(context_parts) if context_parts else "No relevant concepts found",
            'confidence': confidence,
            'concept_count': len(relevant_concepts)
        }
        
        logger.debug(f"✅ Query enriched with {len(relevant_concepts)} concepts")
        return result
    
    def validate_response(self, response: str, source_concepts: List[str]) -> Dict:
        """
        Validate an LLM response against the foundation.
        
        Checks if the response is supported by the specified source concepts
        and calculates a confidence score for the response.
        
        Args:
            response: LLM response to validate
            source_concepts: List of concept IDs that should support the response
            
        Returns:
            Dictionary containing:
            - validated: Boolean indicating if response is validated
            - confidence: Confidence score (0.0-1.0)
            - supporting_concepts: Concepts that support the response
            - issues: List of validation issues found
        """
        logger.debug(f"🔍 Validating response against {len(source_concepts)} concepts")
        
        issues = []
        supporting_concepts = []
        confidence_scores = []
        
        # Check each source concept
        for concept_id in source_concepts:
            concept = self.foundation.get_concept(concept_id)
            
            if concept is None:
                issues.append(f"Concept not found: {concept_id}")
                continue
            
            # Check if concept definition appears in response
            if concept['definition'].lower() in response.lower():
                supporting_concepts.append(concept_id)
                confidence_scores.append(concept['confidence'])
            else:
                # Check for partial matches (at least 50% of keywords)
                def_words = set(concept['definition'].lower().split())
                resp_words = set(response.lower().split())
                overlap = len(def_words & resp_words)
                
                if overlap >= len(def_words) * 0.5:
                    supporting_concepts.append(concept_id)
                    # Reduce confidence for partial match
                    confidence_scores.append(concept['confidence'] * 0.8)
        
        # Calculate overall confidence
        if confidence_scores:
            overall_confidence = sum(confidence_scores) / len(confidence_scores)
        else:
            overall_confidence = 0.0
            issues.append("No supporting concepts found in response")
        
        validated = overall_confidence >= self.confidence_threshold
        
        result = {
            'validated': validated,
            'confidence': overall_confidence,
            'supporting_concepts': supporting_concepts,
            'issues': issues,
            'threshold': self.confidence_threshold
        }
        
        logger.debug(f"✅ Validation: {validated} (confidence: {overall_confidence:.2f})")
        return result
    
    def get_epistemic_status(self, query: str) -> Dict:
        """
        Determine the epistemic status of a query.
        
        Analyzes what the foundation knows about the query topic and
        provides honest assessment of knowledge availability.
        
        Args:
            query: Query to analyze
            
        Returns:
            Dictionary containing:
            - status: One of 'KNOWN', 'PARTIAL', 'UNKNOWN'
            - confidence: Confidence in available knowledge
            - known_concepts: Concepts related to the query
            - recommendation: Recommended action
        """
        logger.debug(f"🔍 Determining epistemic status for query")
        
        # Enrich query to find relevant concepts
        enrichment = self.enrich_query(query)
        relevant_concepts = enrichment['relevant_concepts']
        confidence = enrichment['confidence']
        
        # Determine status based on concept availability and confidence
        if not relevant_concepts:
            status = 'UNKNOWN'
            recommendation = "I don't have verified knowledge about this topic."
        elif confidence >= 0.9:
            status = 'KNOWN'
            recommendation = "I have high-confidence knowledge about this topic."
        elif confidence >= 0.6:
            status = 'PARTIAL'
            recommendation = "I have partial knowledge about this topic."
        else:
            status = 'UNCERTAIN'
            recommendation = "I have low-confidence knowledge about this topic."
        
        result = {
            'status': status,
            'confidence': confidence,
            'known_concepts': relevant_concepts,
            'concept_count': len(relevant_concepts),
            'recommendation': recommendation
        }
        
        logger.debug(f"📊 Epistemic status: {status} (confidence: {confidence:.2f})")
        return result
    
    def bridge_to_brain(self, brain_instance: Any, query: str) -> Dict:
        """
        Bridge a query to LeondasBrain with semantic enrichment.
        
        This method enriches the query with semantic context before
        passing it to the brain and validates the response afterward.
        
        Args:
            brain_instance: Instance of LeondasBrain to query
            query: User query
            
        Returns:
            Dictionary containing:
            - original_query: The original query
            - enriched_query: Query with semantic context
            - brain_response: Response from LeondasBrain (if available)
            - validation: Validation results
            - epistemic_status: Epistemic status of the query
        """
        logger.info(f"🌉 Bridging query to LeondasBrain")
        
        # Enrich the query
        enrichment = self.enrich_query(query)
        
        # Get epistemic status
        epistemic_status = self.get_epistemic_status(query)
        
        # Build enriched query with context
        enriched_query = f"{query}\n\nContext: {enrichment['context']}"
        
        # Note: Actual LeondasBrain integration would call brain_instance here
        # For now, we prepare the structure
        result = {
            'original_query': query,
            'enriched_query': enriched_query,
            'enrichment': enrichment,
            'epistemic_status': epistemic_status,
            'brain_response': None,  # Would be filled by actual brain call
            'validation': None,  # Would be filled after brain response
            'bridge_info': {
                'threshold': self.confidence_threshold,
                'foundation_concepts': len(self.foundation.concepts),
                'foundation_domains': len(self.foundation.domains)
            }
        }
        
        logger.debug(f"✅ Query bridged (status: {epistemic_status['status']})")
        return result
    
    def honest_response(self, query: str, response: str, source_concepts: List[str]) -> Dict:
        """
        Generate an honest response with epistemic markers.
        
        Analyzes the response and adds appropriate epistemic markers
        ([VERIFIED], [INFERRED], [UNCERTAIN], [UNKNOWN]) based on
        foundation validation.
        
        Args:
            query: Original query
            response: Generated response
            source_concepts: Concepts used to generate the response
            
        Returns:
            Dictionary containing:
            - original_response: The original response
            - honest_response: Response with epistemic markers
            - epistemic_status: Status assessment
            - validation: Validation results
        """
        logger.debug("🎯 Generating honest response with epistemic markers")
        
        # Validate the response
        validation = self.validate_response(response, source_concepts)
        
        # Get epistemic status
        epistemic_status = self.get_epistemic_status(query)
        
        # Add appropriate epistemic marker
        if validation['validated'] and validation['confidence'] >= 0.95:
            marker = "[VERIFIED]"
        elif validation['validated'] and validation['confidence'] >= 0.75:
            marker = "[HIGH-CONFIDENCE]"
        elif validation['confidence'] >= 0.5:
            marker = "[INFERRED]"
        elif epistemic_status['status'] == 'UNKNOWN':
            marker = "[UNKNOWN]"
            response = f"I don't have verified knowledge about this topic. {response}"
        else:
            marker = "[UNCERTAIN]"
            response = f"I have limited knowledge about this topic. {response}"
        
        honest_response = f"{marker} {response}"
        
        result = {
            'original_response': response,
            'honest_response': honest_response,
            'epistemic_marker': marker,
            'epistemic_status': epistemic_status,
            'validation': validation
        }
        
        logger.debug(f"✅ Honest response generated with marker: {marker}")
        return result
    
    def balance_entropy(self) -> Dict:
        """
        Verify Foundation consistency and quality.
        
        Analyzes the foundation to ensure all concepts meet quality standards
        (confidence >= 0.95) and calculates overall consistency metrics.
        
        Returns:
            Dictionary containing:
            - mean_confidence: Average confidence across all concepts
            - concept_count: Total number of concepts
            - consistency_score: Score from 0-1 indicating quality
            - low_quality_concepts: List of concept IDs with confidence < 0.95
        """
        logger.debug("⚖️ Balancing entropy - checking Foundation quality")
        
        if not self.foundation.concepts:
            return {
                'mean_confidence': 0.0,
                'concept_count': 0,
                'consistency_score': 0.0,
                'low_quality_concepts': []
            }
        
        # Calculate statistics
        confidences = [c['confidence'] for c in self.foundation.concepts.values()]
        mean_confidence = sum(confidences) / len(confidences)
        
        # Find low-quality concepts (< 0.95)
        low_quality = [
            concept_id 
            for concept_id, concept in self.foundation.concepts.items()
            if concept['confidence'] < 0.95
        ]
        
        # Calculate consistency score
        # Perfect score (1.0) = all concepts >= 0.95
        # Score decreases with low-quality concepts
        consistency_score = 1.0 - (len(low_quality) / len(self.foundation.concepts))
        
        result = {
            'mean_confidence': mean_confidence,
            'concept_count': len(self.foundation.concepts),
            'consistency_score': consistency_score,
            'low_quality_concepts': low_quality
        }
        
        if low_quality:
            logger.warning(
                f"⚠️ Found {len(low_quality)} low-quality concepts (< 0.95): {low_quality[:5]}"
            )
        else:
            logger.info("✅ All concepts meet SPARTA quality standards (>= 0.95)")
        
        logger.debug(
            f"📊 Entropy balance: mean={mean_confidence:.3f}, "
            f"consistency={consistency_score:.3f}"
        )
        
        return result
    
    def route_to_reflexive_generator(self, topic: Optional[str] = None) -> List[Dict]:
        """
        Prepare concepts for ReflexiveGenerator (NOT raw definitions).
        
        This method extracts concepts WITHOUT their definitions, forcing the
        Generator to use logical reasoning rather than text repetition. This
        is a key anti-hallucination mechanism.
        
        Args:
            topic: Optional topic to filter concepts (if None, returns all)
            
        Returns:
            List of dictionaries containing:
            - concept: concept ID
            - trigger: topic name (human-readable)
            - relations: list of related concept IDs
            - weight: confidence score
            - reflex_tag: reflex tag identifier
            
            NOTE: Definitions, examples, and other detail fields are NOT included.
                  This forces logical expansion rather than text regurgitation.
        """
        logger.debug(f"🔀 Routing concepts to Reflexive Generator (topic: {topic or 'all'})")
        
        # TODO: Integrate with Λ-Guide (selects best concept for topic)
        # TODO: Integrate with Λ-Pattern (detects which concepts apply to query pattern)
        
        # Get relevant concepts
        if topic:
            # Filter by topic (simple keyword matching for now)
            topic_lower = topic.lower()
            relevant_concepts = [
                concept for concept in self.foundation.concepts.values()
                if (topic_lower in concept.get('topic', '').lower() or
                    topic_lower in concept['id'].replace('_', ' '))
            ]
        else:
            relevant_concepts = list(self.foundation.concepts.values())
        
        # Prepare routing information (NO definitions or examples!)
        routed_concepts = []
        
        for concept in relevant_concepts:
            routed_concepts.append({
                'concept': concept['id'],
                'trigger': concept.get('topic', concept['id']),
                'relations': concept.get('relations', []),
                'weight': concept['confidence'],
                'reflex_tag': concept.get('reflex_tag', 'UNKNOWN')
            })
        
        logger.debug(f"✅ Routed {len(routed_concepts)} concepts to Generator")
        
        return routed_concepts
