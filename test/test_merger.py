from typing import List
from core.builder.chunk_merger import DEFALT_CHUNK_MERGER,ChunkMerger,ChunkMergerWrapper
from core.chunk import Chunk

def test_default_chunk_merger():
    assert isinstance(DEFALT_CHUNK_MERGER,ChunkMerger)
    assert DEFALT_CHUNK_MERGER.merge([
        Chunk(data = "A"),
        Chunk(data = "B"),
        Chunk(data = "C"),
        Chunk(data = "D"),
    ]) == Chunk(data = "ABCD")


def test_chunk_merger():
    @ChunkMergerWrapper(sep = ".",end_signal = "!")
    def MergeA(self, chunks: List[Chunk]) -> Chunk:
        return Chunk(data = self.sep.join(chunk.data for chunk in chunks) + self.end_signal)
    
    assert MergeA.merge([
        Chunk(data = "A"),
        Chunk(data = "B"),
        Chunk(data = "C"),
        Chunk(data = "D"),
    ]) == Chunk(data="A.B.C.D!")