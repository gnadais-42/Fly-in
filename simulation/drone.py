from __future__ import annotations
from typing import TYPE_CHECKING
from . import Location

if TYPE_CHECKING:
    from .hub import Hub

class Drone:
    def __init__(self, start: Hub, id: str):
        self._location: Location = start
        self._id = id
    
    def __str__(self) -> str:
        return self._id
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def location(self) -> Location:
        return self._location

    def move_to(self, destination: Location) -> None:
        self._location = destination