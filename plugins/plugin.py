import abc
from core.chunk import Chunk
from core.context import GlobalContext, LocalContext
from typing import List
from core.observer.observer import Observer
from core.modifier.context_modifier import GlobalContextModifier, LocalContextModifier
from core.modifier.chunk_modifier import ChunkModifier
from core.mapping.event_mapping import EventMapping
from core.builder.output_builder import OutputBuilder


class Plugin(abc.ABC):
    def init(self, scope, context: GlobalContext) -> bool:
        self.scope = scope
        return True


class GlobalContextPlugin(Plugin):
    @abc.abstractmethod
    def create_global_context_modifier(self) -> GlobalContextModifier:
        """ """


class ObserverPlugin(Plugin):
    @abc.abstractmethod
    def create_observers(self, context: GlobalContext) -> List[Observer]:
        """ """


class EventAgentPlugin(Plugin):
    @abc.abstractmethod
    def create_event_mappings(self, context: GlobalContext) -> List[EventMapping]:
        """ """


class LocalContextPlugin(Plugin):
    @abc.abstractmethod
    def create_local_context_modifier(
        self, context: GlobalContext
    ) -> LocalContextModifier:
        """ """


class FlowAgentPlugin(Plugin):
    pass


class ApplicationPlugin(FlowAgentPlugin):
    @abc.abstractmethod
    def create_output_builder(self, context: LocalContext) -> OutputBuilder:
        """ """


class ChunkModifierPlugin(FlowAgentPlugin):
    @abc.abstractmethod
    def create_chunk_modifier(self, context: LocalContext,chunk:Chunk) -> ChunkModifier:
        """ """
