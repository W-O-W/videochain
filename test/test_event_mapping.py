
from core.context import GlobalContext
from core.mapping.event_mapping import *
import asyncio


def test_event_mapping_wrapper():
    @EventMappingWrapper("A")
    def map_test(self, chunk: Chunk, context: LocalContext) -> Event:
        return Event(id=list(self.available_scopes)[0])

    assert map_test.is_available("A")
    assert not map_test.is_available("B")

    e = asyncio.run(
        map_test.map(Chunk(), LocalContext(global_context=GlobalContext([])))
    )
    assert e.id == "A"
