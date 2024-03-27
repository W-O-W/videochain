from typing import List
from core.chunk import Chunk


class ChunkModifier:
    def is_available(self, phase) -> bool:
        return self.phase == phase

    def match(self, chunk: Chunk) -> bool:
        return True

    def invoke(self, chunk: Chunk, fix_chunks: List[Chunk]) -> Chunk:
        return chunk
