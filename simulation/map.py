from .hub import Hub
from .connection import Connection
from graph import Graph

class Map(Graph):
    def __init__(self, hubs: list[Hub], connections: list[Connection], start: Hub, end: Hub):
        super.__init__(hubs, connections)

        self._start = start
        self._end = end

    @property
    def start(self) -> Hub:
        return self._start
    
    @property
    def end(self) -> Hub:
        return self._end