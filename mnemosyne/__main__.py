"""
Mnemosyne CLI.

    python -m mnemosyne boot                       session boot pack
    python -m mnemosyne check [--strict]           validate the memory graph
    python -m mnemosyne query "question" [-k N]    semantic recall (Λ-Logos)
    python -m mnemosyne checkpoint TITLE --gates G --agent A
    python -m mnemosyne graph [--format mermaid|edges]
    python -m mnemosyne stats
"""

import argparse
import sys
from collections import Counter

from mnemosyne import checkpoint as chk
from mnemosyne.graph import load_graph
from mnemosyne.recall import boot_pack, query
from mnemosyne.validate import validate


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m mnemosyne",
                                     description="Mnemosyne - project memory graph")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("boot", help="print the session boot pack")
    p_check = sub.add_parser("check", help="validate .memory/")
    p_check.add_argument("--strict", action="store_true", help="checkpoint drift is an error")
    p_query = sub.add_parser("query", help="semantic recall")
    p_query.add_argument("text")
    p_query.add_argument("-k", type=int, default=5)
    p_chk = sub.add_parser("checkpoint", help="append a verified checkpoint")
    p_chk.add_argument("title")
    p_chk.add_argument("--gates", required=True, help="evidence: tests, lint, checks")
    p_chk.add_argument("--agent", required=True, help="who verified this state")
    p_graph = sub.add_parser("graph", help="export entry-to-entry edges")
    p_graph.add_argument("--format", choices=["mermaid", "edges"], default="edges")
    sub.add_parser("stats", help="graph statistics")
    args = parser.parse_args(argv)

    if args.cmd == "boot":
        print(boot_pack())
    elif args.cmd == "check":
        report = validate(strict=args.strict)
        for line in report.errors:
            print(f"ERROR   {line}")
        for line in report.warnings:
            print(f"WARNING {line}")
        graph = load_graph()
        print(f"{'OK' if report.ok else 'FAILED'}: {len(graph.entries)} entries, {len(graph.edges)} edges, "
              f"{len(report.errors)} errors, {len(report.warnings)} warnings")
        return 0 if report.ok else 1
    elif args.cmd == "query":
        for hit in query(args.text, args.k):
            print(f"{hit['score']:.3f}  {hit['id']} · {hit['title']}  ({hit['file']})")
            for kind, other in hit["neighbors"][:6]:
                print(f"         {kind} {other}")
    elif args.cmd == "checkpoint":
        report = validate(strict=False)
        if not report.ok:
            print("Refusing to checkpoint an invalid memory:\n  " + "\n  ".join(report.errors))
            return 1
        print(f"Created {chk.create(args.title, args.gates, args.agent)}")
    elif args.cmd == "graph":
        graph = load_graph()
        edges = [e for e in graph.edges if e.target in graph.entries]
        if args.format == "mermaid":
            print("graph TD")
            for e in edges:
                print(f"  {e.source.replace('-', '_')} -->|{e.kind}| {e.target.replace('-', '_')}")
        else:
            for e in edges:
                print(f"{e.source}\t{e.kind}\t{e.target}")
    elif args.cmd == "stats":
        graph = load_graph()
        print("entries by kind:", dict(Counter(e.kind for e in graph.entries.values())))
        print("edges by kind:  ", dict(Counter(e.kind for e in graph.edges)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
