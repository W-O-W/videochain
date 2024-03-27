"""
File Created: Wednesday, 27th March 2024 10:19:28 am
Author: zhangli.max (zhangli.max@bigo.com)
-----
Last Modified: Wednesday, 27th March 2024 10:24:00 am
Modified By: zhangli.max (zhangli.max@bigo.com)
"""

from typing import Type, NewType, TypeVar, List
from core.event import Event
from core.chunk import Chunk,AsyncChunk

Events = TypeVar("Events", Event, List[Event])
Chunks = TypeVar("Chunks", Chunk, List[Chunk])

ObserverResponseType = TypeVar(
    "ObserverResponseType", AsyncChunk, List[AsyncChunk]
)

AgentResponseType = TypeVar(
    "AgentResponseType", Chunk, List[Chunk]
)


