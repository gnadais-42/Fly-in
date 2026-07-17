from .hub import Hub
from graph import Edge

class Connection(Edge):
    def __init__(self, source: Hub, target: Hub, capacity: int):
        super().__init__(source, target)
        
        self._name = f"{source}-{target}"
        self._capacity = capacity

    @property
    def capacity(self) -> int:
        return self._capacity

        

