from graph import Edge, Graph, Node
from .simulation import Simulation
from .drone import Drone
from .connection import Connection
from .hub import Hub
from typing import TypeAlias

Location: TypeAlias = Hub | Connection
