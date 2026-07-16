from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .edge import Edge

class Node:
    count: int = 0

    def __init__(self):
        Node.count += 1
        self._id: str = f"N-{Node.count}"
        self._edges: dict[Node, Edge] = {}

    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.target] = edge

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def edges(self) -> dict[Node, Edge]:
        return self._edges
    
    def __str__(self) -> str:
        return f"Node-{self.id}"
    
    def __repr__(self) -> str:
        return f"Node-{self.id}"
