"""
Tests for SPARTA Foundation modules.
"""

import pytest
import os
import json
import tempfile
from sparta.semantic_foundation import SemanticFoundation
from sparta.foundation_bridge import FoundationBridge
from sparta.reflexive_generator import ReflexiveGenerator


class TestSemanticFoundation:
    """Test suite for SemanticFoundation."""
    
    def test_initialization(self):
        """Test SemanticFoundation initialization."""
        foundation = SemanticFoundation()
        assert foundation is not None
        assert isinstance(foundation.concepts, dict)
        assert len(foundation.concepts) == 0
        assert foundation.graph is not None
    
    def test_load_memory(self):
        """Test loading concepts from semantic memory file."""
        foundation = SemanticFoundation()
        
        # Load from the actual semantic_memory.jsonl file
        memory_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 'sparta', 'semantic_memory.jsonl'
        )
        
        if os.path.exists(memory_path):
            count = foundation.load_memory(memory_path)
            assert count == 500  # Should load 500 concepts (Phase 1 + Phase 2 + Phase 3 + Phase 4)
            assert len(foundation.concepts) == 500
            assert len(foundation.domains) >= 24  # At least 24 domains
    
    def test_load_memory_file_not_found(self):
        """Test load_memory with non-existent file."""
        foundation = SemanticFoundation()
        
        with pytest.raises(FileNotFoundError):
            foundation.load_memory('/nonexistent/path/file.jsonl')
    
    def test_add_concept(self):
        """Test adding a concept to foundation."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        result = foundation.add_concept(concept)
        assert result is True
        assert 'test_concept' in foundation.concepts
        assert 'test' in foundation.domains
    
    def test_add_concept_invalid(self):
        """Test adding invalid concept."""
        foundation = SemanticFoundation()
        
        # Missing required fields
        invalid_concept = {
            'id': 'invalid',
            'domain': 'test'
        }
        
        result = foundation.add_concept(invalid_concept)
        assert result is False
    
    def test_add_concept_invalid_confidence(self):
        """Test adding concept with invalid confidence."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 1.5,  # Invalid: > 1.0
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        result = foundation.add_concept(concept)
        assert result is False
    
    def test_get_concept(self):
        """Test retrieving a concept."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        retrieved = foundation.get_concept('test_concept')
        
        assert retrieved is not None
        assert retrieved['id'] == 'test_concept'
        assert retrieved['definition'] == 'A test concept'
    
    def test_get_concept_not_found(self):
        """Test retrieving non-existent concept."""
        foundation = SemanticFoundation()
        retrieved = foundation.get_concept('nonexistent')
        assert retrieved is None
    
    def test_get_related(self):
        """Test getting related concepts."""
        foundation = SemanticFoundation()
        
        # Add concepts with relations
        concept1 = {
            'id': 'concept1',
            'domain': 'test',
            'definition': 'First concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': ['concept2'],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        concept2 = {
            'id': 'concept2',
            'domain': 'test',
            'definition': 'Second concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': ['concept3'],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        concept3 = {
            'id': 'concept3',
            'domain': 'test',
            'definition': 'Third concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept1)
        foundation.add_concept(concept2)
        foundation.add_concept(concept3)
        
        related = foundation.get_related('concept1', max_depth=2)
        
        # Should find concept2 and concept3
        related_ids = [c['id'] for c in related]
        assert 'concept2' in related_ids
        assert 'concept3' in related_ids
    
    def test_verify_statement(self):
        """Test statement verification."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        
        result = foundation.verify_statement(
            'This is a statement about test concept',
            ['test_concept']
        )
        
        assert 'verified' in result
        assert 'confidence' in result
        assert result['confidence'] == 0.95
        assert 'test_concept' in result['supporting_concepts']
    
    def test_update_confidence(self):
        """Test updating concept confidence."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        result = foundation.update_confidence('test_concept', 0.98)
        
        assert result is True
        assert foundation.concepts['test_concept']['confidence'] == 0.98
    
    def test_update_confidence_invalid(self):
        """Test updating confidence with invalid value."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        result = foundation.update_confidence('test_concept', 1.5)
        
        assert result is False
    
    def test_get_domain_concepts(self):
        """Test getting concepts by domain."""
        foundation = SemanticFoundation()
        
        concept1 = {
            'id': 'concept1',
            'domain': 'physics',
            'definition': 'Physics concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        concept2 = {
            'id': 'concept2',
            'domain': 'mathematics',
            'definition': 'Math concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept1)
        foundation.add_concept(concept2)
        
        physics_concepts = foundation.get_domain_concepts('physics')
        assert len(physics_concepts) == 1
        assert physics_concepts[0]['id'] == 'concept1'
    
    def test_visualize_graph(self):
        """Test graph visualization."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        visualization = foundation.visualize_graph()
        
        assert isinstance(visualization, str)
        assert 'SPARTA Concept Graph' in visualization
    
    def test_expand_concept(self):
        """Test concept expansion."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        expansion = foundation.expand_concept('test_concept')
        
        assert expansion['found'] is True
        assert expansion['concept']['id'] == 'test_concept'
        assert 'related' in expansion
        assert 'domain_peers' in expansion
    
    def test_get_statistics(self):
        """Test getting foundation statistics."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        stats = foundation.get_statistics()
        
        assert stats['total_concepts'] == 1
        assert stats['total_domains'] == 1
        assert 'average_confidence' in stats


class TestFoundationBridge:
    """Test suite for FoundationBridge."""
    
    def test_initialization(self):
        """Test FoundationBridge initialization."""
        foundation = SemanticFoundation()
        bridge = FoundationBridge(foundation)
        
        assert bridge is not None
        assert bridge.foundation == foundation
        assert bridge.confidence_threshold == 0.7
    
    def test_enrich_query(self):
        """Test query enrichment."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'energy_conservation',
            'domain': 'physics',
            'definition': 'Energy cannot be created or destroyed',
            'confidence': 1.0,
            'source': 'axiom',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        bridge = FoundationBridge(foundation)
        
        result = bridge.enrich_query('What is energy conservation?')
        
        assert 'original_query' in result
        assert 'relevant_concepts' in result
        assert 'context' in result
        assert 'confidence' in result
    
    def test_validate_response(self):
        """Test response validation."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept for validation',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        bridge = FoundationBridge(foundation)
        
        result = bridge.validate_response(
            'This is a test concept for validation',
            ['test_concept']
        )
        
        assert 'validated' in result
        assert 'confidence' in result
        assert 'supporting_concepts' in result
    
    def test_get_epistemic_status(self):
        """Test epistemic status determination."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'known_concept',
            'domain': 'test',
            'definition': 'A well-known concept',
            'confidence': 0.95,
            'source': 'verified',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        bridge = FoundationBridge(foundation)
        
        result = bridge.get_epistemic_status('What is a known concept?')
        
        assert 'status' in result
        assert result['status'] in ['KNOWN', 'PARTIAL', 'UNCERTAIN', 'UNKNOWN']
        assert 'confidence' in result
        assert 'recommendation' in result
    
    def test_bridge_to_brain(self):
        """Test bridging to LeondasBrain."""
        foundation = SemanticFoundation()
        bridge = FoundationBridge(foundation)
        
        # Mock brain instance (None is acceptable for this test)
        result = bridge.bridge_to_brain(None, 'Test query')
        
        assert 'original_query' in result
        assert 'enriched_query' in result
        assert 'epistemic_status' in result
    
    def test_honest_response(self):
        """Test honest response generation."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        bridge = FoundationBridge(foundation)
        
        result = bridge.honest_response(
            'Tell me about test concept',
            'This is information about test concept',
            ['test_concept']
        )
        
        assert 'original_response' in result
        assert 'honest_response' in result
        assert 'epistemic_marker' in result
        assert result['epistemic_marker'] in ['[VERIFIED]', '[HIGH-CONFIDENCE]', '[INFERRED]', '[UNCERTAIN]', '[UNKNOWN]']


class TestReflexiveGenerator:
    """Test suite for ReflexiveGenerator."""
    
    def test_initialization(self):
        """Test ReflexiveGenerator initialization."""
        foundation = SemanticFoundation()
        generator = ReflexiveGenerator(foundation)
        
        assert generator is not None
        assert generator.foundation == foundation
    
    def test_tag_statement(self):
        """Test statement tagging."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        generator = ReflexiveGenerator(foundation)
        
        tagged = generator.tag_statement('Test statement', ['test_concept'])
        
        assert isinstance(tagged, str)
        assert any(tag in tagged for tag in ['[VERIFIED]', '[INFERRED]', '[UNCERTAIN]', '[UNKNOWN]'])
    
    def test_tag_statement_unknown(self):
        """Test tagging statement with no source concepts."""
        foundation = SemanticFoundation()
        generator = ReflexiveGenerator(foundation)
        
        tagged = generator.tag_statement('Unknown statement', [])
        
        assert '[UNKNOWN]' in tagged
    
    def test_detect_hallucination(self):
        """Test hallucination detection."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'verified_concept',
            'domain': 'test',
            'definition': 'A verified test concept',
            'confidence': 0.95,
            'source': 'verified',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        generator = ReflexiveGenerator(foundation)
        
        # Statement with no verifiable concepts should be flagged as hallucination
        is_hallucination = generator.detect_hallucination(
            'This is completely made up information',
            foundation
        )
        
        assert isinstance(is_hallucination, bool)
    
    def test_honest_response(self):
        """Test honest response generation."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'known_topic',
            'domain': 'test',
            'definition': 'Information about a known topic',
            'confidence': 0.95,
            'source': 'verified',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        generator = ReflexiveGenerator(foundation)
        
        result = generator.honest_response('Tell me about known topic', foundation)
        
        assert isinstance(result, dict)
        assert 'response' in result
        assert 'confidence' in result
        assert any(tag in result['response'] for tag in ['[VERIFIED]', '[INFERRED]', '[UNCERTAIN]', '[UNKNOWN]'])
    
    def test_honest_response_unknown_topic(self):
        """Test honest response for unknown topic."""
        foundation = SemanticFoundation()
        generator = ReflexiveGenerator(foundation)
        
        result = generator.honest_response('Tell me about completely unknown topic', foundation)
        
        assert isinstance(result, dict)
        assert 'response' in result
        assert '[UNKNOWN]' in result['response']
        assert "don't have verified knowledge" in result['response']
    
    def test_verify_generation_batch(self):
        """Test batch verification of statements."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        generator = ReflexiveGenerator(foundation)
        
        statements = [
            'Statement about test concept',
            'Another statement',
            'Third statement'
        ]
        
        results = generator.verify_generation_batch(statements, foundation)
        
        assert len(results) == 3
        assert all('verification' in r for r in results)
        assert all('tagged_statement' in r for r in results)
    
    def test_generate_with_reflection(self):
        """Test generation with reflection."""
        foundation = SemanticFoundation()
        
        concept = {
            'id': 'test_concept',
            'domain': 'test',
            'definition': 'A test concept',
            'confidence': 0.95,
            'source': 'test',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(concept)
        generator = ReflexiveGenerator(foundation)
        
        result = generator.generate_with_reflection('Tell me about test concept', foundation)
        
        assert 'response' in result
        assert 'confidence' in result
        assert 'sources' in result
        assert 'reasoning_chain' in result
        assert 'verified' in result


class TestIntegration:
    """Integration tests for SPARTA Foundation."""
    
    def test_full_pipeline(self):
        """Test complete SPARTA pipeline from load to verification."""
        # Initialize foundation
        foundation = SemanticFoundation()
        
        # Add test concept with full 16 fields
        concept = {
            'id': 'energy_conservation',
            'domain': 'physics',
            'subdomain': 'thermodynamics',
            'topic': 'Energy Conservation',
            'definition': 'Energy cannot be created or destroyed',
            'formal_statement': 'E_total = constant',
            'confidence': 1.0,
            'source': 'axiom',
            'reflex_tag': 'RFX_TEST_001',
            'relations': [],
            'prerequisites': [],
            'examples': ['Example 1'],
            'counterexamples': ['Not this'],
            'applications': ['Physics'],
            'verification': 'Tested',
            'uncertainty': 'None'
        }
        
        foundation.add_concept(concept)
        
        # Initialize bridge
        bridge = FoundationBridge(foundation)
        
        # Enrich query
        enrichment = bridge.enrich_query('What is energy conservation?')
        assert 'energy_conservation' in enrichment['relevant_concepts']
        
        # Initialize generator
        generator = ReflexiveGenerator(foundation)
        
        # Generate with reflection (new API)
        result = generator.generate_with_reflection('Explain energy conservation', foundation)
        assert 'response' in result
        assert '[VERIFIED]' in result['response'] or '[INFERRED]' in result['response'] or '[UNKNOWN]' in result['response']
    
    def test_confidence_thresholds(self):
        """Test different confidence thresholds."""
        foundation = SemanticFoundation()
        
        # High confidence concept
        high_conf = {
            'id': 'high_confidence',
            'domain': 'test',
            'definition': 'High confidence concept',
            'confidence': 0.98,
            'source': 'verified',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        # Low confidence concept
        low_conf = {
            'id': 'low_confidence',
            'domain': 'test',
            'definition': 'Low confidence concept',
            'confidence': 0.55,
            'source': 'unverified',
            'relations': [],
            'created_at': '2025-11-03T18:55:38Z',
            'verified_by': 'test'
        }
        
        foundation.add_concept(high_conf)
        foundation.add_concept(low_conf)
        
        generator = ReflexiveGenerator(foundation)
        
        # High confidence should get VERIFIED or INFERRED tag
        high_tagged = generator.tag_statement('High confidence statement', ['high_confidence'])
        assert '[VERIFIED]' in high_tagged or '[INFERRED]' in high_tagged
        
        # Low confidence should get UNCERTAIN tag
        low_tagged = generator.tag_statement('Low confidence statement', ['low_confidence'])
        assert '[UNCERTAIN]' in low_tagged or '[UNKNOWN]' in low_tagged
