from abc import ABC, abstractmethod
from typing import Callable, List, Type
from core.chunk import Chunk
from core.configure import get_configure

configure = get_configure()


class ChunkMerger(ABC):
    @abstractmethod
    def merge(self, chunks: List[Chunk]) -> Chunk:
        """ """


def ChunkMergerWrapper(T: Type = ChunkMerger, **kwargs):
    class ChunkMergerTmp(T):
        def __init__(self, func: Callable[[T, List[Chunk]], Chunk]) -> None:
            super().__init__()
            self._merge = func
            for k, v in kwargs.items():
                self.__setattr__(k, v)

        def merge(self, chunks: List[Chunk]) -> Chunk:
            return self._merge(self, chunks)

    return ChunkMergerTmp


@ChunkMergerWrapper(sep=configure.DEFAULT_CHUNK_DATA_SEP)
def DEFALT_CHUNK_MERGER(self, chunks: List[Chunk]) -> Chunk:
    return Chunk(data=self.sep.join([chunk.to_natural_language() for chunk in chunks]))
