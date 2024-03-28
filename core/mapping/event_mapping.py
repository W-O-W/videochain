from typing import Any, Coroutine, Type
from core.chunk import Chunk
from core.context import LocalContext
from core.event import Event


class EventMapping:
    def is_available(self, scope: str) -> bool:
        return True

    async def map(self, chunk: Chunk, context: LocalContext) -> Event:
        return Event()


def EventMappingWrapper(*scopes, T: Type[EventMapping] = EventMapping):
    class EventMappingTmp(T):
        available_scopes = set(scopes)

        def __init__(self, func) -> None:
            super().__init__()
            self._map = func

        def is_available(self, scope: str) -> bool:
            return super().is_available(scope) and scope in self.available_scopes

        async def map(self, chunk: Chunk, context: LocalContext) -> Event:
            return self._map(self, chunk, context)

    return EventMappingTmp
