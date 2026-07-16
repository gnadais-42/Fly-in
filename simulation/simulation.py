from .drone import Drone
from .hub import Hub
from .connection import Connection
from .map import Map

class Simulation:
    def __init__(self, n_drones: int, hubs: list[Hub], connections: list[Connection], start: Hub, end: Hub):
        self.drones: list[Drone] = []
        self.map: Map = Map(hubs, connections, start, end)
        self.moves: dict[Drone, list[Hub, Connection]]
        self.turn: int = 0
        for i in range(n_drones):
            drone = Drone(start, f"D-{i + 1}")
            self.drones.append(drone)
            self.moves[drone] = [start]

    def run_turn(self) -> None:
        self.turn += 1
        for drone in self.drones:
            moves = self.moves[drone]
            if self.turn < len(moves):
                drone.move_to(moves[self.turn])
    
    def run_simulation(self) -> None:
        pass