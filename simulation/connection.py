from .hub import Hub
from graph import Edge
from .drone import Drone

class Connection(Edge):
    def __init__(self, source: Hub, target: Hub, capacity: int):
        super.__init__(source, target)

        self._capacity = capacity
        self._drones: list[Drone] = []

    @property
    def capacity(self) -> int:
        return self._capacity

