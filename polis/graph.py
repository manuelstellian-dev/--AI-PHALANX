"""
polis.graph — directed graph (replaces networkx for SPARTA's concept graph).
"""

from typing import Any, Dict, Iterator, List, Set


class GraphError(KeyError):
    """Raised when a node is not in the graph."""


class DiGraph:
    """
    Directed graph with node attributes.

    Attributes:
        nodes: node -> attribute dict (``graph.nodes[n]['confidence']``)
    """

    def __init__(self):
        self.nodes: Dict[Any, Dict[str, Any]] = {}
        self._succ: Dict[Any, Set[Any]] = {}
        self._pred: Dict[Any, Set[Any]] = {}

    def add_node(self, node: Any, **attrs: Any) -> None:
        if node not in self.nodes:
            self.nodes[node] = {}
            self._succ[node] = set()
            self._pred[node] = set()
        self.nodes[node].update(attrs)

    def add_edge(self, u: Any, v: Any) -> None:
        self.add_node(u)
        self.add_node(v)
        self._succ[u].add(v)
        self._pred[v].add(u)

    def has_node(self, node: Any) -> bool:
        return node in self.nodes

    def has_edge(self, u: Any, v: Any) -> bool:
        return u in self._succ and v in self._succ[u]

    def remove_node(self, node: Any) -> None:
        if node not in self.nodes:
            raise GraphError(f"Node {node!r} is not in the graph")
        for v in self._succ.pop(node):
            self._pred[v].discard(node)
        for u in self._pred.pop(node):
            self._succ[u].discard(node)
        del self.nodes[node]

    def successors(self, node: Any) -> Iterator[Any]:
        if node not in self._succ:
            raise GraphError(f"Node {node!r} is not in the graph")
        return iter(sorted(self._succ[node], key=str))

    def predecessors(self, node: Any) -> Iterator[Any]:
        if node not in self._pred:
            raise GraphError(f"Node {node!r} is not in the graph")
        return iter(sorted(self._pred[node], key=str))

    def number_of_nodes(self) -> int:
        return len(self.nodes)

    def number_of_edges(self) -> int:
        return sum(len(s) for s in self._succ.values())

    def edges(self) -> List[tuple]:
        return [(u, v) for u in self._succ for v in sorted(self._succ[u], key=str)]
