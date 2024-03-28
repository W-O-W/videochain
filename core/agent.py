from abc import ABCMeta, abstractmethod
from core.context import GlobalContext, LocalContext
from core.modifier.chunk_modifier import ChunkModifier
from core.constants import Chunks, Events
from typing import List, Union
from core.event import Event, EmptyEvent
from core.chunk import Chunk
from plugins.plugin import (
    EventAgentPlugin,
    FlowAgentPlugin,
    ApplicationPlugin,
    ChunkModifierPlugin,
    LocalContextPlugin,
)
from core.mapping.event_mapping import EventMapping
import asyncio


class Agent(metaclass=ABCMeta):
    @abstractmethod
    def invoke(self, context: LocalContext, chunks: Chunks) -> Union[Events, Chunks]:
        """ """


class EventAgent(Agent):
    def __init__(self, context: GlobalContext, plugins: List[EventAgentPlugin]) -> None:
        super().__init__()
        self.event_mapping_list: List[EventMapping] = []

        for plugin in plugins:
            for mapping in plugin.create_event_mappings():
                self.register_mapping(mapping)

    def register_mapping(self, mapping: EventMapping):
        self.event_mapping_list.append(mapping)

    async def invoke(self, context: LocalContext, chunk: Chunk) -> List[Event]:
        await_events = []
        for mapping in self.event_mapping_list:
            if mapping.is_available(chunk.scope):
                event = mapping.map(chunk, context)
                await_events.append(event)

        await_events_result = await asyncio.gather(*await_events)
        return_events: List[Event] = []
        for event in await_events_result:
            if event is None or event == EmptyEvent():
                # TODO LOG
                pass
            else:
                return_events.append(event)
        return return_events


class FlowAgent(Agent):
    def __init__(self, context: LocalContext) -> None:
        super().__init__()
        self.application_plugin: ApplicationPlugin = None
        self.chunk_modifier_plugins: List[ChunkModifierPlugin] = []
        effect_plugins = set()

        # 初始化 local context
        for plugin in context.global_context.global_enable_plugins:
            if isinstance(plugin, LocalContextPlugin):
                plugin.create_local_context_modifier(
                    context=context.global_context
                ).invoke(context)
                effect_plugins.add(plugin)

        # 生效不同的 plugins
        for plugin in context.global_context.global_enable_plugins:
            if isinstance(plugin, FlowAgentPlugin):
                if isinstance(plugin, ApplicationPlugin):
                    self.application_plugin = plugin
                    effect_plugins.add(plugin)

                if isinstance(plugin, ChunkModifierPlugin):
                    self.chunk_modifier_plugins.append(plugin)
                    effect_plugins.add(plugin)

        assert self.application_plugin is not None, "application plugin must enable"
        self.output_builder = self.application_plugin.create_output_builder(context)

        # TODO effect_plugin logs

    async def invoke(self, context: LocalContext, chunks: List[Chunk]) -> Chunk:
        num_built_chunk = 0
        before_chunk = chunks[0]
        fix_chunks = chunks[1:]
        for chunk in fix_chunks:
            if self.output_builder.match_and_append(chunk):
                # TODO LOG
                num_built_chunk += 1

        if self.output_builder.is_completed():
            # TODO LOG
            return self.output_builder.build()

        return_chunk = before_chunk
        for plugin in self.chunk_modifier_plugins:
            modifier = plugin.create_chunk_modifier(context, return_chunk)
            if modifier is not None:
                return_chunk = modifier.invoke(return_chunk, fix_chunks)
                # TODO LOG
        return return_chunk
