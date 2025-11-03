"""
SPARTA Semantic Foundation - Core Knowledge Management Engine

This module implements the semantic foundation for SPARTA, providing:
- Graph-based relationship management
- Confidence scoring system
- Multi-source verification tracking
- Concept querying and validation
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
import networkx as nx
from loguru import logger


class SemanticFoundation:
    """
    Core semantic knowledge management system for SPARTA.
    
    Manages a graph-based knowledge base with concepts, relationships,
    and confidence scoring. Provides validation and querying capabilities
    for anti-hallucination mechanisms.
    
    Attributes:
        concepts (Dict[str, Dict]): Dictionary of concepts indexed by ID
        graph (nx.DiGraph): Directed graph of concept relationships
        domains (Set[str]): Set of all domains in the knowledge base
    """
    
    def __init__(self):
        """Initialize the Semantic Foundation with empty knowledge base."""
        self.concepts: Dict[str, Dict] = {}
        self.graph: nx.DiGraph = nx.DiGraph()
        self.domains: Set[str] = set()
        logger.info("🏛️ SPARTA Semantic Foundation initialized")
    
    def load_memory(self, filepath: str) -> int:
        """
        Load concepts from semantic memory JSONL file.
        
        Each line in the file should be a valid JSON object representing
        a concept with required fields: id, domain, definition, confidence,
        source, relations, created_at, verified_by.
        
        Args:
            filepath: Path to the JSONL file containing concepts
            
        Returns:
            Number of concepts successfully loaded
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If JSON parsing fails
        """
        if not os.path.exists(filepath):
            logger.error(f"❌ Semantic memory file not found: {filepath}")
            raise FileNotFoundError(f"File not found: {filepath}")
        
        loaded_count = 0
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        concept = json.loads(line)
                        
                        # Validate required fields (enhanced 16-field format)
                        required_fields = [
                            'id', 'domain', 'subdomain', 'topic', 'definition',
                            'formal_statement', 'relations', 'prerequisites', 'confidence',
                            'source', 'reflex_tag', 'examples', 'counterexamples',
                            'applications', 'verification', 'uncertainty'
                        ]
                        
                        if not all(field in concept for field in required_fields):
                            missing = [f for f in required_fields if f not in concept]
                            logger.warning(
                                f"⚠️ Line {line_num}: Missing required fields {missing}, skipping"
                            )
                            continue
                        
                        # Add concept
                        if self.add_concept(concept):
                            loaded_count += 1
                        
                    except json.JSONDecodeError as e:
                        logger.error(f"❌ Line {line_num}: JSON parse error: {e}")
                        continue
            
            logger.info(f"✅ Loaded {loaded_count} concepts from {filepath}")
            logger.info(f"📊 Total concepts: {len(self.concepts)}")
            logger.info(f"🏛️ Domains: {sorted(self.domains)}")
            
            return loaded_count
            
        except Exception as e:
            logger.error(f"❌ Error loading memory: {e}")
            raise
    
    def get_concept(self, concept_id: str) -> Optional[Dict]:
        """
        Retrieve a concept by its ID.
        
        Args:
            concept_id: Unique identifier of the concept
            
        Returns:
            Concept dictionary if found, None otherwise
        """
        concept = self.concepts.get(concept_id)
        
        if concept is None:
            logger.debug(f"🔍 Concept not found: {concept_id}")
        else:
            logger.debug(f"✅ Retrieved concept: {concept_id}")
        
        return concept
    
    def get_related(self, concept_id: str, max_depth: int = 2) -> List[Dict]:
        """
        Get related concepts up to a specified depth in the relationship graph.
        
        Uses breadth-first search to find all concepts related to the given
        concept within the specified depth.
        
        Args:
            concept_id: ID of the concept to start from
            max_depth: Maximum depth to traverse (default: 2)
            
        Returns:
            List of related concept dictionaries
        """
        if concept_id not in self.concepts:
            logger.warning(f"⚠️ Cannot get related: concept {concept_id} not found")
            return []
        
        related = []
        visited = set()
        queue = [(concept_id, 0)]  # (node_id, depth)
        
        while queue:
            current_id, depth = queue.pop(0)
            
            if current_id in visited or depth > max_depth:
                continue
            
            visited.add(current_id)
            
            # Skip the starting concept in results
            if current_id != concept_id and current_id in self.concepts:
                related.append(self.concepts[current_id])
            
            # Add neighbors to queue if we haven't reached max depth
            if depth < max_depth:
                try:
                    neighbors = list(self.graph.successors(current_id))
                    for neighbor in neighbors:
                        if neighbor not in visited:
                            queue.append((neighbor, depth + 1))
                except nx.NetworkXError:
                    # Node not in graph
                    pass
        
        logger.debug(f"🔗 Found {len(related)} related concepts for {concept_id}")
        return related
    
    def verify_statement(self, statement: str, concept_ids: List[str]) -> Dict:
        """
        Verify a statement against the foundation using specified concepts.
        
        Checks if the statement can be supported by the given concepts,
        calculating an overall confidence score based on concept confidences.
        
        Args:
            statement: Statement to verify
            concept_ids: List of concept IDs relevant to the statement
            
        Returns:
            Dictionary with verification results:
            - verified: Boolean indicating if verification succeeded
            - confidence: Overall confidence score (0.0-1.0)
            - supporting_concepts: List of concept IDs that support the statement
            - missing_concepts: List of concept IDs that weren't found
        """
        supporting_concepts = []
        missing_concepts = []
        confidence_scores = []
        
        for concept_id in concept_ids:
            concept = self.get_concept(concept_id)
            
            if concept is None:
                missing_concepts.append(concept_id)
            else:
                supporting_concepts.append(concept_id)
                confidence_scores.append(concept['confidence'])
        
        # Calculate overall confidence (average of supporting concepts)
        if confidence_scores:
            overall_confidence = sum(confidence_scores) / len(confidence_scores)
        else:
            overall_confidence = 0.0
        
        # Verification succeeds if we have at least one supporting concept
        # and confidence is above threshold (0.7)
        verified = len(supporting_concepts) > 0 and overall_confidence >= 0.7
        
        result = {
            'verified': verified,
            'confidence': overall_confidence,
            'supporting_concepts': supporting_concepts,
            'missing_concepts': missing_concepts,
            'statement': statement
        }
        
        logger.debug(f"🔍 Verification: {verified} (confidence: {overall_confidence:.2f})")
        return result
    
    def add_concept(self, concept: Dict) -> bool:
        """
        Add a new concept to the foundation.
        
        Validates the concept structure and adds it to both the concepts
        dictionary and the relationship graph.
        
        Args:
            concept: Dictionary containing concept data
            
        Returns:
            True if concept was added successfully, False otherwise
        """
        try:
            # Validate core required fields (minimum for add_concept)
            # Full 16-field validation done in load_memory
            required_fields = ['id', 'domain', 'definition', 'confidence']
            if not all(field in concept for field in required_fields):
                missing = [f for f in required_fields if f not in concept]
                logger.error(f"❌ Missing required fields in concept: {missing}")
                return False
            
            concept_id = concept['id']
            
            # Validate confidence range
            confidence = concept['confidence']
            if not 0.0 <= confidence <= 1.0:
                logger.error(f"❌ Invalid confidence value: {confidence}")
                return False
            
            # Add to concepts dictionary
            self.concepts[concept_id] = concept
            
            # Add domain to set
            self.domains.add(concept['domain'])
            
            # Add node to graph
            self.graph.add_node(concept_id, **concept)
            
            # Add edges for relations
            relations = concept.get('relations', [])
            for related_id in relations:
                self.graph.add_edge(concept_id, related_id)
            
            logger.debug(f"✅ Added concept: {concept_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error adding concept: {e}")
            return False
    
    def update_confidence(self, concept_id: str, new_confidence: float) -> bool:
        """
        Update the confidence score of a concept.
        
        Args:
            concept_id: ID of the concept to update
            new_confidence: New confidence value (0.0-1.0)
            
        Returns:
            True if update was successful, False otherwise
        """
        if concept_id not in self.concepts:
            logger.warning(f"⚠️ Concept not found: {concept_id}")
            return False
        
        if not 0.0 <= new_confidence <= 1.0:
            logger.error(f"❌ Invalid confidence value: {new_confidence}")
            return False
        
        try:
            self.concepts[concept_id]['confidence'] = new_confidence
            
            # Update in graph as well
            if self.graph.has_node(concept_id):
                self.graph.nodes[concept_id]['confidence'] = new_confidence
            
            logger.debug(f"✅ Updated confidence for {concept_id}: {new_confidence}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating confidence: {e}")
            return False
    
    def get_domain_concepts(self, domain: str) -> List[Dict]:
        """
        Get all concepts belonging to a specific domain.
        
        Args:
            domain: Domain name to filter by
            
        Returns:
            List of concept dictionaries in the specified domain
        """
        domain_concepts = [
            concept for concept in self.concepts.values()
            if concept.get('domain') == domain
        ]
        
        logger.debug(f"🏛️ Found {len(domain_concepts)} concepts in domain: {domain}")
        return domain_concepts
    
    def visualize_graph(self) -> str:
        """
        Generate a text-based visualization of the concept graph.
        
        Returns:
            String representation of the graph structure
        """
        lines = ["🏛️ SPARTA Concept Graph Visualization", "=" * 50]
        lines.append(f"Nodes (Concepts): {self.graph.number_of_nodes()}")
        lines.append(f"Edges (Relations): {self.graph.number_of_edges()}")
        lines.append(f"Domains: {len(self.domains)}")
        lines.append("")
        
        # Group by domain
        for domain in sorted(self.domains):
            domain_concepts = self.get_domain_concepts(domain)
            lines.append(f"📚 {domain.upper()}: {len(domain_concepts)} concepts")
            
            for concept in sorted(domain_concepts, key=lambda x: x['id'])[:5]:
                concept_id = concept['id']
                confidence = concept['confidence']
                relations_count = len(concept.get('relations', []))
                lines.append(f"  • {concept_id} (conf: {confidence:.2f}, rel: {relations_count})")
            
            if len(domain_concepts) > 5:
                lines.append(f"  ... and {len(domain_concepts) - 5} more")
            lines.append("")
        
        return "\n".join(lines)
    
    def expand_concept(self, concept_id: str) -> Dict:
        """
        Expand a concept with full details including related concepts.
        
        Args:
            concept_id: ID of the concept to expand
            
        Returns:
            Dictionary with expanded concept information including:
            - concept: The main concept data
            - related: List of directly related concepts
            - domain_peers: Other concepts in the same domain
        """
        concept = self.get_concept(concept_id)
        
        if concept is None:
            return {
                'found': False,
                'concept_id': concept_id
            }
        
        # Get directly related concepts (depth=1)
        related = self.get_related(concept_id, max_depth=1)
        
        # Get other concepts in same domain
        domain_peers = [
            c for c in self.get_domain_concepts(concept['domain'])
            if c['id'] != concept_id
        ]
        
        return {
            'found': True,
            'concept': concept,
            'related': related,
            'domain_peers': domain_peers[:5],  # Limit to 5 for brevity
            'stats': {
                'relation_count': len(related),
                'domain_peer_count': len(domain_peers)
            }
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the knowledge base.
        
        Returns:
            Dictionary with statistics including concept counts,
            domain distribution, confidence statistics, etc.
        """
        if not self.concepts:
            return {
                'total_concepts': 0,
                'total_domains': 0,
                'average_confidence': 0.0
            }
        
        # Calculate statistics
        confidences = [c['confidence'] for c in self.concepts.values()]
        
        stats = {
            'total_concepts': len(self.concepts),
            'total_domains': len(self.domains),
            'total_relations': self.graph.number_of_edges(),
            'average_confidence': sum(confidences) / len(confidences),
            'min_confidence': min(confidences),
            'max_confidence': max(confidences),
            'domain_distribution': {
                domain: len(self.get_domain_concepts(domain))
                for domain in self.domains
            }
        }
        
        return stats
