# SPARTA Λ-Modules - Integration with ΛΕΩΝΙΔΑΣ-AI PHALANX

**ΜΟΛΩΝ ΛΑΒΕ** - Modules Spartane 🏛️⚡🔥

---

## ⚠️ IMPLEMENTATION STATUS: NOT IMPLEMENTED (0%)

**Current State:** This document describes the PLANNED implementation of Λ-Modules.  
**Status:** ❌ **NOT IMPLEMENTED** - Directory `lambda_modules/` does not exist  
**Priority:** Medium - Enhancement features for Phase 3  
**Estimated Effort:** 6-8 weeks for complete implementation

**Verified:** 2025-11-04 - Full Repository Deep Scan

---

## Introducere: Λ-Modules și SPARTA

**Λ-Modules** (Lambda Modules) sunt componentele specializate ale ΛΕΩΝΙΔΑΣ-AI PHALANX care se integrează cu SPARTA pentru:
- **Identitate** (Λ-Identity): Tracking surse și provenență
- **Pattern Detection** (Λ-Pattern): Detectare halucinații
- **Meta-Reasoning** (Λ-Meta): Explicare raționament
- **Guidance** (Λ-Guide): Selecție concepte optime
- **Affect** (Λ-Affect): Stare emoțională bazată pe confidence
- **Reflection** (Λ-Reflect): Învățare din erori
- **Balance** (Λ-Zero): Echilibru Logic vs Creativitate

Fiecare modul **extinde capacitățile SPARTA** cu funcționalități specifice.

---

## Λ-Identity: Source Tracking și Provenință

### Scop

**Λ-Identity** asigură că **ΛΕΩΝΙΔΑΣ-AI PHALANX știe de unde știe** - fiecare răspuns are identitate clară (sources, foundation_ids).

**Principiu Spartan**: "Know thyself" (Cunoaște-te pe tine însuți) - Înscripția de la Delphi.

### Implementare Completă

```python
"""
lambda_identity.py

Λ-Identity Module - Source Tracking și Identity Context
"""

from typing import Dict, Any, List
from loguru import logger


class LambdaIdentity:
    """
    Λ-Identity Module
    
    Responsabilități:
    - Tracking surse pentru fiecare răspuns
    - Construire identity context (de unde știm?)
    - Verificare că toate claims au surse
    - Audit trail (istoric de sources)
    """
    
    def __init__(self):
        """Inițializează Λ-Identity."""
        self.source_history = []  # Istoric toate sources folosite
        logger.info("🆔 Λ-Identity initialized")
    
    
    def get_identity_for_response(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extrage identity context din răspuns SPARTA.
        
        Identity context = metadata despre provenința informației:
        - Sources (de unde vine?)
        - Foundation IDs (ce concepte?)
        - Confidence (cât de sigur?)
        - Timestamp (când?)
        
        Args:
            response: Răspuns generat de Reflexive Generator
        
        Returns:
            dict: {
                'knows_from': list (sources),
                'foundation_ids': list (concept IDs),
                'confidence': float,
                'epistemic_status': str,
                'timestamp': str,
                'traceable': bool
            }
        """
        sources = response.get('sources', [])
        concepts_used = response.get('concepts_used', [])
        confidence = response.get('confidence', 0.0)
        epistemic_status = response.get('epistemic_status', 'UNKNOWN')
        
        # Verifică traceability
        traceable = len(sources) > 0 and len(concepts_used) > 0
        
        # Log sources
        for source in sources:
            if source not in [s['source'] for s in self.source_history]:
                self.source_history.append({
                    'source': source,
                    'first_used': self._get_timestamp()
                })
        
        identity = {
            'knows_from': sources,
            'foundation_ids': concepts_used,
            'confidence': confidence,
            'epistemic_status': epistemic_status,
            'timestamp': self._get_timestamp(),
            'traceable': traceable
        }
        
        if not traceable:
            logger.warning("⚠ Response not fully traceable (missing sources or concepts)")
        
        return identity
    
    
    def verify_sources_present(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Verifică că răspunsul are sources pentru toate claims.
        
        Args:
            response: Răspunsul de verificat
        
        Returns:
            dict: {
                'verified': bool,
                'sources_present': int,
                'sources_missing': int,
                'issues': list
            }
        """
        sources = response.get('sources', [])
        concepts_used = response.get('concepts_used', [])
        
        issues = []
        
        # Check: Există sources?
        if not sources:
            issues.append("No sources present in response")
        
        # Check: Există concepts?
        if not concepts_used:
            issues.append("No Foundation concepts used")
        
        # Check: Sources cover concepts?
        if len(sources) < len(concepts_used):
            issues.append(f"Sources ({len(sources)}) < Concepts ({len(concepts_used)})")
        
        verified = len(issues) == 0
        
        return {
            'verified': verified,
            'sources_present': len(sources),
            'concepts_used': len(concepts_used),
            'issues': issues
        }
    
    
    def get_source_history(self) -> List[Dict[str, Any]]:
        """
        Returnează istoric complet de sources folosite.
        
        Returns:
            list: Istoric sources
        """
        return self.source_history
    
    
    def _get_timestamp(self) -> str:
        """Obține timestamp curent."""
        from datetime import datetime
        return datetime.utcnow().isoformat()


# Example usage
if __name__ == "__main__":
    identity = LambdaIdentity()
    
    # Exemplu răspuns SPARTA
    response = {
        'response': "Conservarea energiei...",
        'confidence': 0.99,
        'sources': ["Noether (1915)", "Experiments (1800-2023)"],
        'concepts_used': ["PHYS_MECHANICS_001", "PHYS_THERMO_001"],
        'epistemic_status': 'KNOWN'
    }
    
    # Get identity
    id_context = identity.get_identity_for_response(response)
    print(f"Identity: {id_context}")
    
    # Verify sources
    verification = identity.verify_sources_present(response)
    print(f"Verification: {verification}")
```

### Beneficii

1. **Transparență completă**: User vede de unde vine fiecare informație
2. **Audit trail**: Istoric complet de sources
3. **Trust**: Confidence bazat pe sources reale, nu speculație

---

## Λ-Pattern: Deviation Detection și Anti-Hallucination

### Scop

**Λ-Pattern** detectează **pattern-uri de halucinație** și **devieri de la Foundation**.

**Principiu Spartan**: "Trust but verify" - Verifică tot ce iese din sistem.

### Implementare Completă

```python
"""
lambda_pattern.py

Λ-Pattern Module - Hallucination Detection
"""

from typing import Dict, Any, List
import re
from loguru import logger


class LambdaPattern:
    """
    Λ-Pattern Module
    
    Responsabilități:
    - Detectare halucinații (responses fără sources)
    - Comparare response cu Foundation
    - Identificare pattern-uri suspecte
    - Rejectare responses invalide
    """
    
    def __init__(self, phalanx_bridge):
        """
        Inițializează Λ-Pattern.
        
        Args:
            phalanx_bridge: PhalanxBridge pentru acces la Foundation
        """
        self.bridge = phalanx_bridge
        
        # Hallucination patterns (red flags)
        self.hallucination_patterns = [
            r'dr\.?\s+\w+\s+smith',  # Generic names (Dr. John Smith)
            r'recent[ly]?\s+discover',  # Vague recency
            r'some\s+scientist',  # Vague attribution
            r'it\s+is\s+believed',  # Weasel words
            r'probably',  # Speculation
            r'might\s+have',  # Uncertainty presented as fact
        ]
        
        logger.info("🔍 Λ-Pattern initialized")
    
    
    def compare_response_to_foundation(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compară răspunsul cu Foundation pentru a detecta devieri.
        
        Args:
            response: Răspunsul de verificat
        
        Returns:
            dict: {
                'aligned': bool,
                'concepts_verified': int,
                'deviations': list,
                'risk_score': float (0-1, lower is better)
            }
        """
        concepts_used = response.get('concepts_used', [])
        response_text = response.get('response', '')
        
        deviations = []
        verified_count = 0
        
        # Verifică că toate concepts_used există în Foundation
        for concept_id in concepts_used:
            concept = self.bridge.get_concept_by_id(concept_id)
            if concept:
                verified_count += 1
            else:
                deviations.append(f"Concept {concept_id} not in Foundation")
        
        # Verifică hallucination patterns în text
        for pattern in self.hallucination_patterns:
            matches = re.findall(pattern, response_text, re.IGNORECASE)
            if matches:
                deviations.append(f"Hallucination pattern detected: {matches}")
        
        # Calculate risk score
        if verified_count == 0:
            risk_score = 1.0  # Maximum risk (no verified concepts)
        else:
            deviation_penalty = len(deviations) * 0.2
            risk_score = min(1.0, deviation_penalty)
        
        aligned = risk_score < 0.3 and verified_count > 0
        
        return {
            'aligned': aligned,
            'concepts_verified': verified_count,
            'concepts_total': len(concepts_used),
            'deviations': deviations,
            'risk_score': round(risk_score, 2)
        }
    
    
    def detect_hallucination_patterns(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Detectează pattern-uri de halucinație în text.
        
        Red flags:
        - Generic names (Dr. Smith, John Doe)
        - Vague attributions (some scientist, recent study)
        - Weasel words (probably, might, it is believed)
        - Specific claims without specifics (in 1987, at MIT)
        
        Args:
            text: Text de analizat
        
        Returns:
            dict: {
                'hallucination_detected': bool,
                'patterns_found': list,
                'risk_level': 'LOW' | 'MEDIUM' | 'HIGH'
            }
        """
        patterns_found = []
        
        for pattern in self.hallucination_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                patterns_found.append({
                    'pattern': pattern,
                    'matches': matches
                })
        
        # Determine risk level
        if len(patterns_found) == 0:
            risk_level = 'LOW'
            hallucination_detected = False
        elif len(patterns_found) <= 2:
            risk_level = 'MEDIUM'
            hallucination_detected = True
        else:
            risk_level = 'HIGH'
            hallucination_detected = True
        
        return {
            'hallucination_detected': hallucination_detected,
            'patterns_found': patterns_found,
            'risk_level': risk_level,
            'pattern_count': len(patterns_found)
        }
    
    
    def reject_if_invalid(
        self,
        response: Dict[str, Any],
        threshold: float = 0.3
    ) -> Dict[str, Any]:
        """
        Reject response dacă risk score > threshold.
        
        Args:
            response: Response de evaluat
            threshold: Risk threshold (default 0.3)
        
        Returns:
            dict: {
                'accepted': bool,
                'reason': str (if rejected)
            }
        """
        comparison = self.compare_response_to_foundation(response)
        risk = comparison['risk_score']
        
        if risk > threshold:
            return {
                'accepted': False,
                'reason': f"Risk score {risk} exceeds threshold {threshold}",
                'deviations': comparison['deviations']
            }
        
        return {
            'accepted': True,
            'risk_score': risk
        }


# Example usage
if __name__ == "__main__":
    from phalanx_bridge import PhalanxBridge
    
    bridge = PhalanxBridge("foundation.json")
    bridge.load_foundation()
    
    pattern = LambdaPattern(bridge)
    
    # Test hallucination detection
    hallucinated_text = "Dr. John Smith at MIT recently discovered..."
    detection = pattern.detect_hallucination_patterns(hallucinated_text)
    print(f"Hallucination: {detection}")
    
    # Test response validation
    response = {
        'response': "Energy is conserved...",
        'concepts_used': ["PHYS_MECHANICS_001"],
        'sources': ["Noether (1915)"]
    }
    comparison = pattern.compare_response_to_foundation(response)
    print(f"Comparison: {comparison}")
```

### Beneficii

1. **Detectare automată** de halucinații
2. **Reject responses** cu risk mare
3. **Pattern learning**: Învață pattern-uri noi de halucinație

---

## Λ-Meta: Meta-Reasoning și Explicabilitate

### Scop

**Λ-Meta** explică **cum a ajuns la răspuns** - transparență completă în raționament.

**Principiu Spartan**: "Show your work" - Arată cum ai ajuns la concluzie.

### Implementare Completă

```python
"""
lambda_meta.py

Λ-Meta Module - Meta-Reasoning and Explainability
"""

from typing import Dict, Any, List
from loguru import logger


class LambdaMeta:
    """
    Λ-Meta Module
    
    Responsabilități:
    - Explicare reasoning chain
    - Meta-reasoning (raționament despre raționament)
    - Transparență completă
    - Confidence justification
    """
    
    def __init__(self, phalanx_bridge):
        """
        Inițializează Λ-Meta.
        
        Args:
            phalanx_bridge: PhalanxBridge pentru acces la Foundation
        """
        self.bridge = phalanx_bridge
        logger.info("🧠 Λ-Meta initialized")
    
    
    def explain_reasoning(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Explică în detaliu cum s-a ajuns la răspuns.
        
        Args:
            response: Răspunsul de explicat
        
        Returns:
            dict: {
                'reasoning_chain': list,
                'logical_steps': list,
                'confidence_justification': str,
                'sources_used': list,
                'uncertainty_acknowledged': str
            }
        """
        concepts_used = response.get('concepts_used', [])
        reasoning_chain = response.get('reasoning_chain', [])
        confidence = response.get('confidence', 0.0)
        sources = response.get('sources', [])
        uncertainty = response.get('uncertainty', '')
        
        # Build logical steps
        logical_steps = []
        for i, concept_id in enumerate(concepts_used):
            concept = self.bridge.get_concept_by_id(concept_id)
            if concept:
                step = f"Step {i+1}: Used concept '{concept['topic']}' "
                step += f"(domain: {concept['domain']}, "
                step += f"confidence: {concept['confidence']})"
                logical_steps.append(step)
        
        # Justify confidence
        if confidence >= 0.98:
            conf_justification = f"High confidence ({confidence}) - Based on well-established concepts"
        elif confidence >= 0.95:
            conf_justification = f"Moderate confidence ({confidence}) - Some uncertainty in sources"
        else:
            conf_justification = f"Low confidence ({confidence}) - Significant uncertainty"
        
        return {
            'reasoning_chain': reasoning_chain,
            'logical_steps': logical_steps,
            'confidence_justification': conf_justification,
            'sources_used': sources,
            'uncertainty_acknowledged': uncertainty,
            'total_steps': len(logical_steps)
        }
    
    
    def build_reasoning_graph(
        self,
        concepts_used: List[str]
    ) -> Dict[str, Any]:
        """
        Construiește graful de raționament (concept dependencies).
        
        Args:
            concepts_used: Lista de concept IDs
        
        Returns:
            dict: {
                'nodes': list (concepts),
                'edges': list (relations),
                'depth': int
            }
        """
        nodes = []
        edges = []
        visited = set()
        
        for concept_id in concepts_used:
            if concept_id in visited:
                continue
            
            concept = self.bridge.get_concept_by_id(concept_id)
            if not concept:
                continue
            
            nodes.append({
                'id': concept_id,
                'topic': concept['topic'],
                'confidence': concept['confidence']
            })
            visited.add(concept_id)
            
            # Add edges (relations)
            for relation_id in concept.get('relations', []):
                if relation_id in concepts_used:
                    edges.append({
                        'from': concept_id,
                        'to': relation_id,
                        'type': 'relation'
                    })
        
        # Calculate depth (max path length)
        depth = self._calculate_graph_depth(nodes, edges)
        
        return {
            'nodes': nodes,
            'edges': edges,
            'depth': depth,
            'complexity': len(edges)
        }
    
    
    def _calculate_graph_depth(
        self,
        nodes: List[Dict],
        edges: List[Dict]
    ) -> int:
        """
        Calculează adâncimea maximă a grafului.
        
        Args:
            nodes: Noduri
            edges: Muchii
        
        Returns:
            int: Adâncimea maximă
        """
        # Simplified - în realitate ar folosi BFS/DFS
        if not edges:
            return 1
        return min(len(nodes), 5)  # Cap la 5


# Example usage
if __name__ == "__main__":
    from phalanx_bridge import PhalanxBridge
    
    bridge = PhalanxBridge("foundation.json")
    bridge.load_foundation()
    
    meta = LambdaMeta(bridge)
    
    # Test explanation
    response = {
        'response': "Energy is conserved...",
        'concepts_used': ["PHYS_MECHANICS_001", "PHYS_THERMO_001"],
        'reasoning_chain': ["Conservation of Energy", "First Law of Thermodynamics"],
        'confidence': 0.99,
        'sources': ["Noether (1915)"],
        'uncertainty': "Quantum gravity scales unknown"
    }
    
    explanation = meta.explain_reasoning(response)
    print(f"Explanation: {explanation}")
```

---

## Λ-Guide: Concept Selection și Scoring

### Scop

**Λ-Guide** selectează **cele mai bune concepte** pentru un query (scoring: confidence 40% + relevance 40% + relations 20%).

### Implementare Completă

```python
"""
lambda_guide.py

Λ-Guide Module - Concept Selection and Scoring
"""

from typing import Dict, Any, List, Tuple
from loguru import logger


class LambdaGuide:
    """
    Λ-Guide Module
    
    Responsabilități:
    - Scoring concepte pentru query
    - Selecție concepte optime
    - Ranking bazat pe: confidence (40%), relevance (40%), relations (20%)
    """
    
    def __init__(self, phalanx_bridge):
        """
        Inițializează Λ-Guide.
        
        Args:
            phalanx_bridge: PhalanxBridge pentru acces la Foundation
        """
        self.bridge = phalanx_bridge
        
        # Scoring weights
        self.weight_confidence = 0.4
        self.weight_relevance = 0.4
        self.weight_relations = 0.2
        
        logger.info("🧭 Λ-Guide initialized")
    
    
    def select_best_concept(
        self,
        query: str,
        domain: str = None,
        top_k: int = 5
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Selectează cele mai bune concepte pentru query.
        
        Scoring formula:
            score = 0.4 * confidence + 0.4 * relevance + 0.2 * relations_density
        
        Args:
            query: Query de la user
            domain: Domain hint (opțional)
            top_k: Număr concepte de returnat
        
        Returns:
            list: [(concept, score), ...] sorted by score descending
        """
        # Get candidate concepts
        candidates = self.bridge.get_concepts(
            domain=domain,
            min_confidence=0.95,
            max_results=20
        )
        
        if not candidates:
            return []
        
        # Score each concept
        scored = []
        for concept in candidates:
            score = self._calculate_score(concept, query)
            scored.append((concept, score))
        
        # Sort by score (descending)
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Return top_k
        top_concepts = scored[:top_k]
        
        logger.info(f"Selected {len(top_concepts)} best concepts for query")
        
        return top_concepts
    
    
    def _calculate_score(
        self,
        concept: Dict[str, Any],
        query: str
    ) -> float:
        """
        Calculează score pentru concept față de query.
        
        Args:
            concept: Conceptul de scorat
            query: Query-ul
        
        Returns:
            float: Score (0-1)
        """
        # 1. Confidence component (40%)
        confidence_score = concept.get('confidence', 0.95) * self.weight_confidence
        
        # 2. Relevance component (40%)
        relevance_score = self._calculate_relevance(concept, query) * self.weight_relevance
        
        # 3. Relations density component (20%)
        relations_density = len(concept.get('relations', [])) / 10.0  # Normalize (assume max 10)
        relations_density = min(1.0, relations_density)  # Cap at 1.0
        relations_score = relations_density * self.weight_relations
        
        # Total score
        total_score = confidence_score + relevance_score + relations_score
        
        return total_score
    
    
    def _calculate_relevance(
        self,
        concept: Dict[str, Any],
        query: str
    ) -> float:
        """
        Calculează relevanța concept față de query.
        
        Simplified: keyword overlap între query și topic/definition
        
        Args:
            concept: Conceptul
            query: Query-ul
        
        Returns:
            float: Relevance (0-1)
        """
        query_lower = query.lower()
        topic_lower = concept.get('topic', '').lower()
        definition_lower = concept.get('definition', '').lower()
        
        # Keyword overlap (simplified)
        query_words = set(query_lower.split())
        topic_words = set(topic_lower.split())
        definition_words = set(definition_lower.split())
        
        # Overlap în topic (weighted more)
        topic_overlap = len(query_words & topic_words) / max(len(query_words), 1)
        
        # Overlap în definition
        definition_overlap = len(query_words & definition_words) / max(len(query_words), 1)
        
        # Combined relevance
        relevance = 0.7 * topic_overlap + 0.3 * definition_overlap
        
        return min(1.0, relevance)


# Example usage
if __name__ == "__main__":
    from phalanx_bridge import PhalanxBridge
    
    bridge = PhalanxBridge("foundation.json")
    bridge.load_foundation()
    
    guide = LambdaGuide(bridge)
    
    # Select best concepts
    query = "conservarea energiei"
    top_concepts = guide.select_best_concept(query, domain="Physics", top_k=3)
    
    for concept, score in top_concepts:
        print(f"Concept: {concept['topic']}, Score: {score:.3f}")
```

---

## Λ-Affect: Emotional State Based on Confidence

### Scop

**Λ-Affect** determină **starea emoțională** a sistemului bazată pe confidence răspunsurilor.

**Formula**: `E_t = tanh(confidence - 0.5) * 2` → range [-1, +1]

### Implementare

```python
"""
lambda_affect.py

Λ-Affect Module - Emotional State Tracking
"""

import math
from typing import Dict, Any
from loguru import logger


class LambdaAffect:
    """
    Λ-Affect Module
    
    Responsabilități:
    - Tracking stare emoțională (E_t)
    - Ajustare bazată pe confidence
    - Feedback către user (emoji/tone)
    """
    
    def __init__(self):
        """Inițializează Λ-Affect."""
        self.E_t = 0.0  # Emotional state (-1 to +1)
        logger.info("😊 Λ-Affect initialized")
    
    
    def update_affect(self, confidence: float) -> Dict[str, Any]:
        """
        Update emotional state bazat pe confidence.
        
        Formula: E_t = tanh(confidence - 0.5) * 2
        
        Args:
            confidence: Confidence răspunsului (0-1)
        
        Returns:
            dict: {
                'E_t': float (-1 to +1),
                'mood': str,
                'emoji': str
            }
        """
        # Calculate E_t
        self.E_t = math.tanh(confidence - 0.5) * 2
        
        # Determine mood
        if self.E_t > 0.5:
            mood = "CONFIDENT"
            emoji = "😊"
        elif self.E_t > 0:
            mood = "OPTIMISTIC"
            emoji = "🙂"
        elif self.E_t > -0.5:
            mood = "UNCERTAIN"
            emoji = "😐"
        else:
            mood = "DOUBTFUL"
            emoji = "😟"
        
        return {
            'E_t': round(self.E_t, 3),
            'mood': mood,
            'emoji': emoji,
            'confidence': confidence
        }
```

---

## Λ-Reflect: Learning from Errors

### Scop

**Λ-Reflect** învață din erori - log responses, track success rate, identify improvements.

### Implementare

```python
"""
lambda_reflect.py

Λ-Reflect Module - Learning from Errors
"""

from typing import Dict, Any, List
from loguru import logger


class LambdaReflect:
    """
    Λ-Reflect Module
    
    Responsabilități:
    - Log toate responses
    - Track success/failure
    - Identify patterns în erori
    - Suggest improvements
    """
    
    def __init__(self):
        """Inițializează Λ-Reflect."""
        self.response_log = []
        self.success_count = 0
        self.failure_count = 0
        logger.info("🔄 Λ-Reflect initialized")
    
    
    def log_response(
        self,
        query: str,
        response: Dict[str, Any],
        success: bool
    ):
        """
        Log răspunsul pentru learning.
        
        Args:
            query: Query-ul original
            response: Răspunsul generat
            success: Dacă răspunsul a fost corect
        """
        log_entry = {
            'query': query,
            'response_text': response.get('response', ''),
            'confidence': response.get('confidence', 0.0),
            'concepts_used': response.get('concepts_used', []),
            'success': success,
            'timestamp': self._get_timestamp()
        }
        
        self.response_log.append(log_entry)
        
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
    
    
    def get_insights(self) -> Dict[str, Any]:
        """
        Obține insights din response log.
        
        Returns:
            dict: {
                'total_responses': int,
                'success_rate': float,
                'common_failures': list
            }
        """
        total = self.success_count + self.failure_count
        success_rate = self.success_count / total if total > 0 else 0.0
        
        # Identify common failure patterns
        failures = [r for r in self.response_log if not r['success']]
        
        return {
            'total_responses': total,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'success_rate': round(success_rate, 3),
            'recent_failures': failures[-5:]  # Last 5 failures
        }
    
    
    def _get_timestamp(self) -> str:
        """Get timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

---

## Λ-Zero: Logic vs Creativity Balance (CRITICAL)

### Scop

**Λ-Zero** este cel mai important modul - balanțează între **Logic** (Foundation) și **Creativitate** (Exploration).

**Formula**:
```
Λ_zero = tanh(k₁·logic_conf + k₂·creative_exp - k₃·|θ̇|)
```

### Implementare Completă

```python
"""
lambda_zero.py

Λ-Zero Module - Logic vs Creativity Balance (CRITICAL)
"""

import math
from typing import Dict, Any
from loguru import logger


class LambdaZero:
    """
    Λ-Zero Module - Balance Logic și Creativitate
    
    Formula: Λ_zero = tanh(k₁·logic_conf + k₂·creative_exp - k₃·|θ̇|)
    
    Unde:
    - logic_conf = Confidence din Foundation (0-1)
    - creative_exp = Factor de explorare creativă (0-1)
    - θ̇ = Rata de schimbare (instabilitate)
    - k₁, k₂, k₃ = Constante (default: 1.0, 0.5, 0.3)
    
    Interpretare:
    - Λ_zero > 0.5: LOGIC_DOMINANT (SPARTA în control)
    - Λ_zero < -0.5: CREATIVE_DOMINANT (Exploration mode)
    - -0.5 ≤ Λ_zero ≤ 0.5: BALANCED (Optim)
    """
    
    def __init__(self, k1=1.0, k2=0.5, k3=0.3):
        """
        Inițializează Λ-Zero.
        
        Args:
            k1: Weight pentru logic confidence
            k2: Weight pentru creative exploration
            k3: Weight pentru instabilitate
        """
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        
        self.history = []  # Pentru calculare θ̇
        
        logger.info(f"⚖️ Λ-Zero initialized (k1={k1}, k2={k2}, k3={k3})")
    
    
    def calculate_balance(
        self,
        logic_confidence: float,
        creative_exploration: float = 0.0,
        theta_dot: float = 0.0
    ) -> float:
        """
        Calculează Λ_zero balance.
        
        Args:
            logic_confidence: Confidence din Foundation (0-1)
            creative_exploration: Factor explorare (0-1), default 0
            theta_dot: Rata schimbare (instabilitate), default 0
        
        Returns:
            float: Λ_zero (-1 to +1)
        """
        # Formula
        arg = (self.k1 * logic_confidence + 
               self.k2 * creative_exploration - 
               self.k3 * abs(theta_dot))
        
        lambda_zero = math.tanh(arg)
        
        # Log în history
        self.history.append({
            'lambda_zero': lambda_zero,
            'logic_confidence': logic_confidence,
            'creative_exploration': creative_exploration,
            'theta_dot': theta_dot
        })
        
        return lambda_zero
    
    
    def interpret_balance(self, lambda_zero: float) -> Dict[str, Any]:
        """
        Interpretează valoarea Λ_zero.
        
        Args:
            lambda_zero: Valoarea Λ_zero
        
        Returns:
            dict: {
                'state': str,
                'description': str,
                'recommendation': str
            }
        """
        if lambda_zero > 0.5:
            return {
                'state': 'LOGIC_DOMINANT',
                'description': 'SPARTA în control - răspunsuri bazate strict pe Foundation',
                'recommendation': 'Optim pentru operațiuni critice (military, medical)',
                'emoji': '🛡️'
            }
        elif lambda_zero < -0.5:
            return {
                'state': 'CREATIVE_DOMINANT',
                'description': 'Exploration mode - risc halucinație crescut',
                'recommendation': 'NU recomandabil pentru operațiuni critice',
                'emoji': '🎨'
            }
        else:
            return {
                'state': 'BALANCED',
                'description': 'Balance optim între logic și creativitate',
                'recommendation': 'Stare ideală pentru majoritatea queries',
                'emoji': '⚖️'
            }
    
    
    def adjust_generation_params(
        self,
        lambda_zero: float
    ) -> Dict[str, Any]:
        """
        Ajustează parametrii de generare bazat pe Λ_zero.
        
        Args:
            lambda_zero: Valoarea Λ_zero
        
        Returns:
            dict: {
                'foundation_weight': float (0-1),
                'creative_freedom': float (0-1),
                'confidence_threshold': float (0.95-1.0)
            }
        """
        # Map Λ_zero (-1 to +1) to parameters
        
        # Foundation weight: higher când logic dominant
        foundation_weight = (lambda_zero + 1) / 2  # Map [-1,1] to [0,1]
        
        # Creative freedom: inverse
        creative_freedom = 1 - foundation_weight
        
        # Confidence threshold: mai strict când logic dominant
        confidence_threshold = 0.95 + 0.05 * foundation_weight  # [0.95, 1.0]
        
        return {
            'foundation_weight': round(foundation_weight, 3),
            'creative_freedom': round(creative_freedom, 3),
            'confidence_threshold': round(confidence_threshold, 3),
            'lambda_zero': round(lambda_zero, 3)
        }


# Example usage
if __name__ == "__main__":
    zero = LambdaZero()
    
    # Scenario 1: High confidence Foundation (logic dominant)
    lambda_zero_1 = zero.calculate_balance(
        logic_confidence=0.99,
        creative_exploration=0.1
    )
    print(f"Scenario 1: Λ_zero = {lambda_zero_1:.3f}")
    interpretation_1 = zero.interpret_balance(lambda_zero_1)
    print(f"State: {interpretation_1['state']}")
    params_1 = zero.adjust_generation_params(lambda_zero_1)
    print(f"Params: {params_1}")
    
    # Scenario 2: Low confidence, high exploration (creative dominant)
    lambda_zero_2 = zero.calculate_balance(
        logic_confidence=0.3,
        creative_exploration=0.8
    )
    print(f"\nScenario 2: Λ_zero = {lambda_zero_2:.3f}")
    interpretation_2 = zero.interpret_balance(lambda_zero_2)
    print(f"State: {interpretation_2['state']}")
    params_2 = zero.adjust_generation_params(lambda_zero_2)
    print(f"Params: {params_2}")
```

### Exemple de Calcul Λ-Zero

#### Exemplu 1: Logic Dominant (Operațiune Militară)

```
Input:
- logic_confidence = 0.99 (Foundation verified concepts)
- creative_exploration = 0.0 (zero exploration)
- theta_dot = 0.0 (stabil)

Calcul:
Λ_zero = tanh(1.0 * 0.99 + 0.5 * 0.0 - 0.3 * 0.0)
       = tanh(0.99)
       = 0.757

State: LOGIC_DOMINANT 🛡️
foundation_weight = 0.878
creative_freedom = 0.122
confidence_threshold = 0.994

→ SPARTA în control complet - perfect pentru operațiuni critice
```

#### Exemplu 2: Balanced (Query General)

```
Input:
- logic_confidence = 0.97
- creative_exploration = 0.3
- theta_dot = 0.1

Calcul:
Λ_zero = tanh(1.0 * 0.97 + 0.5 * 0.3 - 0.3 * 0.1)
       = tanh(1.10)
       = 0.802 → dar cu instabilitate

State: BALANCED ⚖️ (dacă ignorăm instabilitate) sau LOGIC_DOMINANT

→ Balance bun pentru majoritatea queries
```

---

## Integrarea Tuturor Λ-Modules

### Flow Complet cu Toate Λ-Modules

```python
def full_sparta_pipeline(query: str):
    """
    Flow complet SPARTA cu toate Λ-Modules.
    """
    # STEP 1: Λ-Guide - selectează concepts
    concepts = lambda_guide.select_best_concept(query)
    
    # STEP 2: Reflexive Generator - generează răspuns
    response = reflexive_generator.generate(query)
    
    # STEP 3: Λ-Pattern - validează (anti-hallucination)
    validation = lambda_pattern.compare_response_to_foundation(response)
    if not validation['aligned']:
        return {"error": "Response rejected - hallucination risk"}
    
    # STEP 4: Λ-Zero - check balance
    lambda_zero = lambda_zero_module.calculate_balance(
        logic_confidence=response['confidence']
    )
    params = lambda_zero_module.adjust_generation_params(lambda_zero)
    
    # STEP 5: Λ-Affect - update emotional state
    affect = lambda_affect.update_affect(response['confidence'])
    
    # STEP 6: Λ-Meta - explain reasoning
    explanation = lambda_meta.explain_reasoning(response)
    
    # STEP 7: Λ-Identity - add identity context
    identity = lambda_identity.get_identity_for_response(response)
    
    # STEP 8: Λ-Reflect - log for learning
    lambda_reflect.log_response(query, response, success=True)
    
    # STEP 9: Construiește răspuns final
    final_response = {
        'response': response['response'],
        'confidence': response['confidence'],
        'sources': response['sources'],
        'reasoning': explanation,
        'identity': identity,
        'affect': affect,
        'lambda_zero': lambda_zero,
        'parameters': params
    }
    
    return final_response
```

---

## Concluzie: Λ-Modules = Puterea SPARTA

**Cele 7 Λ-Modules** transformă SPARTA dintr-un sistem de raționament logic într-un **sistem inteligent complet**:

1. **Λ-Identity**: Știe de unde știe
2. **Λ-Pattern**: Detectează halucinații
3. **Λ-Meta**: Explică raționamentul
4. **Λ-Guide**: Selectează optim
5. **Λ-Affect**: Feedback emoțional
6. **Λ-Reflect**: Învață din erori
7. **Λ-Zero**: Balance logic/creativitate (CRITICAL)

**ΜΟΛΩΝ ΛΑΒΕ** - Vino și ia puterealambda, dacă poți! 🏛️⚡🔥

---

**Next**: [SPARTA_FLOW_EXAMPLES.md](SPARTA_FLOW_EXAMPLES.md) - Flow complet end-to-end cu exemple detaliate
