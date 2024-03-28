from dataclasses import dataclass, field
from typing import List, Set
from core.chunk import Chunk
import abc
from core.builder.chunk_merger import DEFALT_CHUNK_MERGER
from core.tools import flatten_and_dropduplicate
from core.configure import get_configure

confgure = get_configure()
class OutputBuilder(abc.ABC):
    def match_and_append(self, append_chunk: Chunk) -> bool:
        return True

    @abc.abstractmethod
    def is_completed(self) -> bool:
        """ """

    @abc.abstractmethod
    def build(self) -> Chunk:
        """ """


@dataclass
class DefaultOutputBuilder(OutputBuilder):
    last_plugin_signal: str = field()
    accept_plugin_signal: Set[str] = field(default_factory=set, compare=False)
    chunks: List[Chunk] = field(default_factory=list, compare=False, init=False)
    completed: bool = field(default=False, init=False, compare=False)

    def match_and_append(self, append_chunk: Chunk) -> bool:
        accept_flag = False
        for signal in append_chunk.producer_signals:
            if signal in self.accept_plugin_signal:
                self.chunks.append(append_chunk)
                accept_flag = True
            if self.last_plugin_signal == signal:
                self.completed = True
        return accept_flag

    def is_completed(self) -> bool:
        return self.completed

    def build(self) -> Chunk:
        assert self.is_completed(), "can't build when not completed"
        chunk = DEFALT_CHUNK_MERGER.merge(self.chunks)
        chunk.scope = confgure.DEFAULT_SCOPE_SEP.join(flatten_and_dropduplicate([c.scope for c in self.chunks]))
        chunk.command = "OUTPUT"
        return chunk
