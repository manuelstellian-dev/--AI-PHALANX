"""
Λ-Logos Benchmark - retrieval quality on the SPARTA Foundation.

Each query is a paraphrase written *without* the target concept's key wording;
the model must rank the intended concept near the top among all active
concepts. Reported metrics:

- MRR      mean reciprocal rank of the target (1.0 = always first)
- R@1/R@5  share of queries whose target is ranked first / in the top 5

The benchmark is fixed, so every model version is measured against the same
reference (compare with the untrained, lexical-only baseline).
"""

from typing import Dict, List, Tuple

import numpy as np

from logos.corpus import concept_text
from logos.model import LogosEmbedder

# (paraphrased query, target concept id)
QUERIES: List[Tuple[str, str]] = [
    ("energy can neither appear nor vanish, it only changes form", "energy_conservation"),
    ("disorder in an isolated system tends to grow", "entropy"),
    ("a body keeps its state of motion unless something pushes it", "newton_first_law"),
    ("organisms better suited to their environment leave more offspring", "natural_selection"),
    ("a procedure that invokes itself on a smaller version of the problem", "recursion"),
    ("a learner that memorizes its examples and fails on new data", "overfitting"),
    ("act only on rules you could want everyone to follow", "categorical_imperative"),
    ("making sure stored information was not tampered with", "data_integrity"),
    ("physical laws look identical to every observer moving at constant velocity", "special_relativity"),
    ("a substance that speeds up a reaction without being used up", "catalysis"),
    ("how triplets of nucleotides map to amino acids", "genetic_code"),
    ("approximating a function by an infinite polynomial around a point", "taylor_series"),
    ("the hardest problems whose solutions can be checked quickly", "np_completeness"),
    ("how society should share goods and burdens fairly", "distributive_justice"),
    ("upper limit on how well a heat engine converts heat to work", "carnot_efficiency"),
    ("twisting effect of a force about an axis", "torque"),
    ("waves bending as they pass the edge of an obstacle", "diffraction"),
    ("properties that survive stretching and bending but not tearing", "topology"),
    ("algebra of true and false values with and, or, not", "boolean_algebra"),
    ("traits are inherited through segregating factors from each parent", "mendelian_genetics"),
    ("split a task into parts, solve each, then combine the answers", "divide_conquer"),
    ("a logic where proofs must construct their witnesses", "intuitionistic_logic"),
    ("government taxing and spending to steer the economy", "fiscal_policy"),
    ("computing close to where data is produced instead of a distant cloud", "edge_computing"),
    ("the study of how speech sounds are produced and heard", "phonetics"),
    ("turning spoken audio into written words automatically", "speech_recognition"),
    ("what a speaker suggests without saying it outright", "implicature"),
    ("why physical processes give rise to subjective experience", "consciousness_hard_problem"),
]


def evaluate(model: LogosEmbedder, concepts: Dict[str, Dict]) -> Dict[str, float]:
    """
    Run the benchmark.

    Args:
        model: Model to evaluate (trained or untrained)
        concepts: Active SPARTA concepts (id -> concept)

    Returns:
        Metrics: queries, mrr, recall_at_1, recall_at_5, mean_rank
    """
    ids = sorted(concepts)
    matrix = model.embed_batch([concept_text(concepts[cid]) for cid in ids])
    queries = [(q, t) for q, t in QUERIES if t in concepts]
    query_vecs = model.embed_batch([q for q, _ in queries])

    ranks = []
    for (query, target), vec in zip(queries, query_vecs):
        order = np.argsort(-(matrix @ vec), kind="stable")
        ranks.append(int(np.where(np.asarray(ids)[order] == target)[0][0]) + 1)

    ranks_arr = np.asarray(ranks, dtype=float)
    return {
        "queries": len(ranks),
        "mrr": float(np.mean(1.0 / ranks_arr)),
        "recall_at_1": float(np.mean(ranks_arr <= 1)),
        "recall_at_5": float(np.mean(ranks_arr <= 5)),
        "mean_rank": float(np.mean(ranks_arr)),
    }
