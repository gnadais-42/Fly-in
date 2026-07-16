from .node import Node

class Edge:
    def __init__(self, source: Node, target: Node):
        self._source = source
        self._target = target
    
    @property
    def source(self) -> Node:
        return self._source
    
    @property
    def target(self) -> Node:
        return self._target