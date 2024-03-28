
from typing import Type, NewType, TypeVar, List
from core.event import Event
from core.chunk import Chunk

Events = TypeVar("Events", Event, List[Event])
Chunks = TypeVar("Chunks", Chunk, List[Chunk])

