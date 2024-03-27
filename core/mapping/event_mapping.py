from core.chunk import Chunk
from core.context import LocalContext
from core.event import Event


class EventMapping:
    def is_available(self, scope: str) -> bool:
        return True

    async def map(self, chunk: Chunk,context:LocalContext) -> Event:
        return Event()
