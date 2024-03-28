from typing import Callable, List, Type
from core.chunk import Chunk
from core.context import LocalContext


class ChunkModifier:
    def invoke(self, chunk: Chunk, fix_chunks: List[Chunk]) -> Chunk:
        return chunk


def ChunkModifierWrapper(T: Type = ChunkModifier, **kwargs):
    class ContextModifierTmp(T):
        def __init__(self, func: Callable[[T, Chunk, List[Chunk]],]) -> None:
            super().__init__()
            self._invoke = func
            for k, v in kwargs.items():
                self.__setattr__(k, v)

        def invoke(self, chunk: Chunk, fix_chunks: List[Chunk]) -> Chunk:
            return self._invoke(self, chunk, fix_chunks)

    return ContextModifierTmp
