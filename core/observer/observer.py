from core.context import LocalContext
from core.event import Event
import asyncio
import abc
from typing import Type, Callable
from core.chunk import new_none_chunk
from core.constants import Chunks


class Observer:
    def __init__(self, event: Event) -> None:
        self.event = event

    def observe(self, event: Event) -> bool:
        return event == self.event

    async def invoke(self, context: LocalContext, event: Event) -> Chunks:
        return new_none_chunk()


def ObserverWrapper(T: Type = Observer, **kwargs):
    class ObserverTmp(T):
        def __init__(
            self, func: Callable[[T, LocalContext, Event], Chunks]
        ) -> None:
            super().__init__()
            self._invoke = func
            for k, v in kwargs.items():
                self.__setattr__(k, v)

        async def invoke(self, context: LocalContext, event: Event) -> Chunks:
            return self._invoke(self, context, event)

    return ObserverTmp
