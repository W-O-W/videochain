
from core.context import LocalContext
from core.event import Event
import asyncio
import abc
from typing import Mapping,Callable
from core.chunk import new_none_chunk
from core.typevar import Chunks
class Observer:
    def __init__(self,event:Event) -> None:
        self.event = event
    def observe(self,event:Event)->bool:
        return event == self.event

    async def invoke(self,context:LocalContext,event:Event)->Chunks:
        return new_none_chunk()