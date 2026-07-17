from graph import Node

class Hub(Node):
    count: int = 0

    def __init__(self, name: str, attributes: dict):
        super().__init__()

        self._name: str = name
        self._coordinates: tuple[int, int] = attributes["coordinates"]
        self._color: str = attributes["color"]
        self._type: str = attributes["zone"]
        self._max_drones: int | None = attributes["max_drones"]

        Hub.count += 1
        print(f"Hub created: {self.name} {self.coordinates} [{self.type}, {self.color}, n_drones={self.max_drones}]")

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self._name