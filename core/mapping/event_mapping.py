from typing import Type, Callable
from core.chunk import Chunk
from core.context import LocalContext
from core.event import Event


class EventMapping:
    def is_available(self, scope: str) -> bool:
        return True

    async def map(self, chunk: Chunk, context: LocalContext) -> Event:
        return Event()


def EventMappingWrapper(*scopes, T: Type[EventMapping] = EventMapping, **kwargs):
    class EventMappingTmp(T):
        def __init__(self, func: Callable[[T, Chunk, LocalContext], Event]) -> None:
            super().__init__()
            self._map = func
            self.available_scopes = set(scopes)
            for k, v in kwargs.items():
                self.__setattr__(k, v)

        def is_available(self, scope: str) -> bool:
            return super().is_available(scope) and scope in self.available_scopes

        async def map(self, chunk: Chunk, context: LocalContext) -> Event:
            return self._map(self, chunk, context)

    return EventMappingTmp
