from graph import Node
from .drone import Drone


class Hub(Node):
    count: int = 0

    def __init__(self, name: str, attributes: dict):
        super.__init__()

        self._name: str = name
        self._coordinates: tuple[int, int] = attributes["coordinates"]
        self._color: str = attributes["color"]
        self._type: str = attributes["zone"]
        self._max_drones: int | None = attributes["max_drones"]
        self._drones: list[Drone] = []
        self._drone_count: int = 0
        Hub.count += 1
        print(f"Hub created: {self.name} {self.coordinates} [{self.type}, {self.color}, n_drones={self.max_drones}]")

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def drone_count(self) -> int:
        return self._drone_count
    
    def receive_drone(self, drone: Drone) -> None:
        if drone in self._drones:
            raise ValueError(f"{drone} can't be sent to {self.name}, it is already there")
        self._drone_count += 1
        self._drones.append(drone)
    
    def dispatch_drone(self, drone: Drone) -> None:
        if drone not in self._drones:
            raise ValueError(f"{drone} can't leave {self.name}, it is not there")
        self._drone_count -= 1
        self._drones.remove(drone)

    def __str__(self) -> str:
        return self._name