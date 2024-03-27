
from typing import List
from core.context import GlobalContext
from core.mapping.event_mapping import EventMapping
from core.modifier.context_modifier import GlobalContextModifier, LocalContextModifier
from core.observer.observer import Observer
from plugins.plugin import (
    GlobalContextPlugin,
    LocalContextPlugin,
    EventAgentPlugin,
    ObserverPlugin,
)


class ChatBot(
    GlobalContextPlugin, EventAgentPlugin, ObserverPlugin, LocalContextPlugin
):
    def create_event_mapping(self, context: GlobalContext) -> List[EventMapping]:
        return super().create_event_mapping(context)

    def create_observer(self, context: GlobalContext) -> List[Observer]:
        return super().create_observer(context)

    def create_global_context_modifier(self) -> GlobalContextModifier:
        return super().create_global_context_modifier()

    def create_local_context_modifier(self) -> LocalContextModifier:
        return super().create_local_context_modifier()
    
    def init(self, scope, context: GlobalContext) -> bool:
        return super().init(scope, context)


BASIC_LLM_PLUGINS = {
    "QWEN":[ChatBot()]
}