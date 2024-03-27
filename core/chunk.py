"""

[SCOPE][COMMAND][DATA][SEP]
"""

import asyncio
from dataclasses import dataclass, field
from typing import TypeVar,List

DataType = TypeVar("DataType",str,List[str])

@dataclass(unsafe_hash=True)
class Chunk:
    scope: str = ""
    command: str = ""
    data: DataType = field(default_factory=str)


def new_none_chunk():
    chunk = Chunk()
    chunk.scope = "FLOW"
    chunk.command = ""
    chunk.data = ""
    return chunk

# @dataclass(unsafe_hash=True)
# class AsyncChunk(Chunk):
#     def set_task(self, async_task: asyncio.Task) -> None:
#         async_task.add_done_callback(lambda x:self.init_from(x.result()))
#         self.__async_task__ = async_task

#     def init_from(self, chunk: Chunk):
#         self.command = chunk.command
#         self.scope = chunk.scope
#         self.data = chunk.data