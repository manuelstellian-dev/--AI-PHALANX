"""
Λ-Logos CLI.

    python -m logos train [--force] [--out PATH]   train on the project corpus
    python -m logos info                           describe the current model
    python -m logos similar "text a" "text b"      cosine similarity
    python -m logos explain AXIS                   words that define a latent axis
"""

import argparse
import json
import os
import sys

from logos.corpus import build_corpus
from logos.model import top_terms
from logos.runtime import artifact_path, get_model, train_default


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m logos", description="Λ-Logos - own embedding model")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_train = sub.add_parser("train", help="train on the project corpus")
    p_train.add_argument("--force", action="store_true", help="retrain even if the artifact exists")
    p_train.add_argument("--out", default=None, help="artifact path")
    sub.add_parser("info", help="describe the current model")
    p_sim = sub.add_parser("similar", help="cosine similarity of two texts")
    p_sim.add_argument("a")
    p_sim.add_argument("b")
    p_exp = sub.add_parser("explain", help="top words of a latent axis")
    p_exp.add_argument("axis", type=int)
    args = parser.parse_args(argv)

    if args.cmd == "train":
        out = args.out or artifact_path()
        if os.path.exists(out) and not args.force:
            print(f"Artifact exists: {out} (use --force to retrain; then re-index the vault)")
            return 0
        model = train_default(out)
        print(json.dumps(model.info(), indent=2))
    elif args.cmd == "info":
        print(json.dumps(get_model().info(), indent=2))
    elif args.cmd == "similar":
        print(f"{get_model().similarity(args.a, args.b):.4f}")
    elif args.cmd == "explain":
        texts = [t for _, t in build_corpus()]
        print(", ".join(top_terms(get_model(), texts, args.axis)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
