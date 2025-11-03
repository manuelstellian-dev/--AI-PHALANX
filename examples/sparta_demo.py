#!/usr/bin/env python3
"""
SPARTA Foundation Demo - Demonstrating the 10% MVP

ΜΟΛΩΝ ΛΑΒΕ (Molon Labe) - "Come and Take Them"

This script demonstrates the core functionality of the SPARTA Foundation:
1. Loading semantic memory (44 concepts)
2. Querying concepts
3. Verifying statements
4. Anti-hallucination detection
5. Honest epistemic responses
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sparta import SemanticFoundation, FoundationBridge, ReflexiveGenerator
from loguru import logger

# Configure logger
logger.remove()
logger.add(sys.stderr, level="INFO")


def main():
    """Main demo function."""
    logger.info("🏛️ SPARTA Foundation Demo - Phase 1 (10% MVP)")
    logger.info("=" * 60)
    
    # Initialize foundation
    logger.info("\n1. Initializing Semantic Foundation...")
    foundation = SemanticFoundation()
    
    # Load semantic memory
    memory_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'sparta',
        'semantic_memory.jsonl'
    )
    
    count = foundation.load_memory(memory_path)
    logger.info(f"✅ Loaded {count} concepts")
    
    # Display statistics
    stats = foundation.get_statistics()
    logger.info(f"\n📊 Foundation Statistics:")
    logger.info(f"   Total Concepts: {stats['total_concepts']}")
    logger.info(f"   Total Domains: {stats['total_domains']}")
    logger.info(f"   Average Confidence: {stats['average_confidence']:.2f}")
    logger.info(f"   Total Relations: {stats['total_relations']}")
    
    # Display domain distribution
    logger.info(f"\n🏛️ Domain Distribution:")
    for domain, count in sorted(stats['domain_distribution'].items()):
        logger.info(f"   {domain}: {count} concepts")
    
    # Demonstrate concept retrieval
    logger.info("\n2. Demonstrating Concept Retrieval...")
    concept = foundation.get_concept('energy_conservation')
    if concept:
        logger.info(f"✅ Retrieved: {concept['id']}")
        logger.info(f"   Domain: {concept['domain']}")
        logger.info(f"   Definition: {concept['definition']}")
        logger.info(f"   Confidence: {concept['confidence']}")
        logger.info(f"   Relations: {', '.join(concept['relations'])}")
    
    # Demonstrate relationship traversal
    logger.info("\n3. Demonstrating Relationship Traversal...")
    related = foundation.get_related('neural_network', max_depth=2)
    logger.info(f"✅ Found {len(related)} related concepts for 'neural_network':")
    for rel in related[:5]:
        logger.info(f"   - {rel['id']} ({rel['domain']})")
    
    # Initialize bridge
    logger.info("\n4. Initializing Foundation Bridge...")
    bridge = FoundationBridge(foundation, confidence_threshold=0.7)
    logger.info("✅ Bridge initialized")
    
    # Demonstrate query enrichment
    logger.info("\n5. Demonstrating Query Enrichment...")
    query = "What is energy conservation?"
    enrichment = bridge.enrich_query(query)
    logger.info(f"Query: {query}")
    logger.info(f"✅ Enrichment:")
    logger.info(f"   Relevant Concepts: {', '.join(enrichment['relevant_concepts'])}")
    logger.info(f"   Confidence: {enrichment['confidence']:.2f}")
    
    # Demonstrate epistemic status
    logger.info("\n6. Demonstrating Epistemic Status...")
    status = bridge.get_epistemic_status(query)
    logger.info(f"✅ Epistemic Status: {status['status']}")
    logger.info(f"   Confidence: {status['confidence']:.2f}")
    logger.info(f"   Recommendation: {status['recommendation']}")
    
    # Initialize generator
    logger.info("\n7. Initializing Reflexive Generator...")
    generator = ReflexiveGenerator(foundation)
    logger.info("✅ Generator initialized")
    
    # Demonstrate honest response
    logger.info("\n8. Demonstrating Honest Response...")
    response = generator.honest_response(
        "Explain neural networks",
        foundation
    )
    logger.info(f"✅ Response:")
    logger.info(f"   {response[:200]}...")
    
    # Demonstrate hallucination detection
    logger.info("\n9. Demonstrating Hallucination Detection...")
    
    # Test with verified statement
    verified_statement = "Neural networks use backpropagation and gradient descent"
    is_hallucination = generator.detect_hallucination(verified_statement, foundation)
    logger.info(f"Statement: '{verified_statement}'")
    logger.info(f"✅ Hallucination detected: {is_hallucination}")
    
    # Test with unverified statement
    fake_statement = "Quantum teleportation was invented by Dr. John Smith in 1987"
    is_hallucination = generator.detect_hallucination(fake_statement, foundation)
    logger.info(f"\nStatement: '{fake_statement}'")
    logger.info(f"✅ Hallucination detected: {is_hallucination}")
    
    # Demonstrate statement tagging
    logger.info("\n10. Demonstrating Statement Tagging...")
    tagged1 = generator.tag_statement(
        "Energy cannot be created or destroyed",
        ['energy_conservation']
    )
    logger.info(f"✅ Tagged: {tagged1[:80]}...")
    
    tagged2 = generator.tag_statement(
        "This is completely made up information",
        []
    )
    logger.info(f"✅ Tagged: {tagged2[:80]}...")
    
    # Display graph visualization
    logger.info("\n11. Graph Visualization:")
    visualization = foundation.visualize_graph()
    logger.info("\n" + visualization)
    
    logger.info("\n" + "=" * 60)
    logger.info("🏛️ SPARTA Foundation Demo Complete!")
    logger.info("ΜΟΛΩΝ ΛΑΒΕ - Foundation for Truth and Accountability")


if __name__ == "__main__":
    main()
