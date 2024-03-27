import abc
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
    def create_observer(self, context: GlobalContext) -> List[Observer]:
        """ """


class EventAgentPlugin(Plugin):
    @abc.abstractmethod
    def create_event_mapping(self, context: GlobalContext) -> List[EventMapping]:
        """ """


class FlowAgentPlugin(Plugin):
    pass


class LocalContextPlugin(FlowAgentPlugin):
    @abc.abstractmethod
    def create_local_context_modifier(self) -> LocalContextModifier:
        """ """


class ApplicationPlugin(FlowAgentPlugin):
    @abc.abstractmethod
    def create_output_builder(self, context: LocalContext) -> OutputBuilder:
        """ """


class ChunkModifierPlugin(FlowAgentPlugin):
    @abc.abstractmethod
    def create_chunk_modifier(self, context: LocalContext) -> ChunkModifier:
        """ """
