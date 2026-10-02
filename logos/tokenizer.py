"""
Λ-Logos Tokenizer - deterministic text → sparse feature extraction.

Features (all hashed into a fixed space, no vocabulary file needed):
- ``w:`` word unigrams        - lexical meaning
- ``b:`` word bigrams         - local phrase structure ("energy conservation")
- ``c:`` character n-grams    - morphology; robust to inflection, typos,
                                 Romanian diacritics and Greek terms (Λ-TAS)

Hashing uses BLAKE2b (stable across processes and platforms), never Python's
salted ``hash()``, so the same text always yields the same features.
"""

import hashlib
import math
import re
import unicodedata
from collections import Counter
from typing import Dict, Iterable, List, Tuple

# Word = run of Unicode letters/digits (covers Latin, Romanian, Greek)
_WORD_RE = re.compile(r"[^\W_]+", re.UNICODE)

# Feature-group weights: words carry most meaning, char n-grams add robustness
GROUP_WEIGHTS = {"w": 1.0, "b": 0.7, "c": 0.35}
CHAR_NGRAM_RANGE = (3, 5)


def normalize(text: str) -> str:
    """
    Normalize text: NFKD, strip combining marks (ă→a, ș→s, ά→α), lowercase.

    Args:
        text: Raw text

    Returns:
        Normalized text
    """
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return stripped.lower()


def words(text: str) -> List[str]:
    """Split normalized text into word tokens."""
    return _WORD_RE.findall(normalize(text))


def raw_features(text: str) -> Counter:
    """
    Extract un-hashed features with their counts.

    Args:
        text: Raw text

    Returns:
        Counter of feature strings (prefixed by group: w:, b:, c:)
    """
    tokens = words(text)
    feats: Counter = Counter()
    for tok in tokens:
        feats["w:" + tok] += 1
        padded = f"<{tok}>"
        lo, hi = CHAR_NGRAM_RANGE
        for n in range(lo, hi + 1):
            for i in range(len(padded) - n + 1):
                feats["c:" + padded[i:i + n]] += 1
    for a, b in zip(tokens, tokens[1:]):
        feats[f"b:{a}_{b}"] += 1
    return feats


def _hash(feature: str, n_features: int) -> Tuple[int, float]:
    """Stable signed hash: (bucket index, ±1 sign)."""
    digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
    value = int.from_bytes(digest, "little")
    return value % n_features, (1.0 if (value >> 63) & 1 else -1.0)


def hashed_features(text: str, n_features: int) -> Dict[int, float]:
    """
    Hash features into a fixed space with sublinear TF and group weights.

    Args:
        text: Raw text
        n_features: Size of the hashed feature space

    Returns:
        Mapping bucket index → signed weighted value
    """
    out: Dict[int, float] = {}
    for feat, count in raw_features(text).items():
        weight = GROUP_WEIGHTS[feat[0]]
        tf = 1.0 + math.log(count)  # sublinear term frequency (count >= 1)
        idx, sign = _hash(feat, n_features)
        out[idx] = out.get(idx, 0.0) + sign * weight * tf
    return out


def batch_hashed_features(texts: Iterable[str], n_features: int) -> List[Dict[int, float]]:
    """Hash a batch of texts."""
    return [hashed_features(t, n_features) for t in texts]
