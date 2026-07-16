from .node import Node
from .edge import Edge

class Graph:
    def __init__(self, nodes: list[Node], edges: list[Edge]):
        self._nodes: dict[str, Node] = {}
        self._edges = []

        for node in nodes:
            self.add_node(node)

        for edge in edges:
            self.add_edge(edge)

    def add_node(self, node: Node) -> None:
        self._nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        source = edge.source
        if source.id not in self._nodes:
            raise ValueError(f"Node {source} not present in graph")
        if edge.target.id not in self._nodes:
            raise ValueError(f"Node {edge.target} not present in graph")
        source.add_edge(edge)
        self._edges.append(edge)

    @property
    def nodes(self) -> dict[str, Node]:
        return self._nodes
    
    @property
    def edges(self) -> list[Edge]:
        return self._edges