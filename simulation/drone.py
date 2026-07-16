from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .hub import Hub
    from .connection import Connection

class Drone:
    def __init__(self, start: Hub, id: str):
        self._location: Hub | Connection = start
        self._id = id
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def location(self) -> Hub | Connection:
        return self._location

    def move_to(self, destination: Hub | Connection) -> None:
        self._location = destination