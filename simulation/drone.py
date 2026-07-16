from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .hub import Hub
    from .connection import Connection

class Drone:
    def __init__(self, start: Hub, id: str):
        self.location: Hub | Connection = start
        self.id = id