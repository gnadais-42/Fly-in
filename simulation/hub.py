from graph import Node
from .drone import Drone


class Hub(Node):
    count: int = 0

    def __init__(self, name: str, attributes: dict):
        super.__init__()

        self._name: str = name
        self.coordinates: tuple[int, int] = attributes["coordinates"]
        self.color: str = attributes["color"]
        self.type: str = attributes["zone"]
        self.max_drones: int = attributes["max_drones"]
        self.drones: list[Drone] = []
        Hub.count += 1
        print(f"Hub created: {self.name} {self.coordinates} [{self.type}, {self.color}, n_drones={self.max_drones}]")

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self._name