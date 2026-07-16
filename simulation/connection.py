from .hub import Hub
from graph import Edge
from .drone import Drone

class Connection(Edge):
    def __init__(self, source: Hub, target: Hub, capacity: int):
        super.__init__(source, target)
        
        self._name = f"{source}-{target}"
        self._capacity = capacity
        self._drones: list[Drone] = []
        self._drone_count: int = 0

    @property
    def capacity(self) -> int:
        return self._capacity
    
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
        

