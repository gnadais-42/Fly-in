from .drone import Drone
from .hub import Hub
from .connection import Connection
from .map import Map

class Simulation:
    def __init__(self, n_drones: int, hubs: list[Hub], connections: list[Connection], start: Hub, end: Hub):
        self.drones: list[Drone] = []
        self.map: Map = Map(hubs, connections, start, end)

        for i in range(n_drones):
            self.drones.append(Drone(start, f"D-{i + 1}"))
        