
from abc import ABCMeta,abstractmethod
from context import GlobalContext,LocalContext
from typevar import Chunks,Events
from typing import List
from event import Event,EmptyEvent
from core.chunk import Chunk
from plugins.plugin import EventAgentPlugin,FlowAgentPlugin,ApplicationPlugin,ChunkModifierPlugin,LocalContextPlugin

class Agent(metaclass = ABCMeta):
    @abstractmethod
    def invoke(self,context:LocalContext,chunks:Chunks)->Events | Chunks:
        """
        """

class EventAgent(Agent):
    def __init__(self,context:GlobalContext,plugins:List[EventAgentPlugin]) -> None:
        super().__init__()
        self.event_mapping_list = []
        
        for plugin in plugins:
            for mapping in plugin.create_event_mapping():
                self.register_mapping(mapping)

    def invoke(self,context: LocalContext, chunk: Chunk) -> List[Event]:
        return_events = []
        for mapping in self.event_mapping_list:
            if mapping.is_available(chunk.scope):
                event = mapping.map(chunk)
                if event is not None or not isinstance(event,EmptyEvent):
                    return_events.append(event)
                else:
                    # TODO LOG
                    pass
                    
        return return_events
                    


class FlowAgent(Agent):
    def __init__(self,context:LocalContext) -> None:
        super().__init__()
        self.application_plugin:ApplicationPlugin = None
        self.chunk_modifier_list = []
        effect_plugins = set()

        # 初始化 local context
        for plugin in context.global_context.global_enable_plugins:
            if isinstance(plugin,FlowAgentPlugin):
                if isinstance(plugin,LocalContextPlugin):
                    plugin.create_context_modifer().invoke(context)
                    effect_plugins.add(plugin)
        
        # 生效不同的 plugins
        for plugin in context.global_context.global_enable_plugins:
            if isinstance(plugin,FlowAgentPlugin):
                if isinstance(plugin,ApplicationPlugin):
                    self.application_plugin = plugin
                    effect_plugins.add(plugin)
                    
                if isinstance(plugin,ChunkModifierPlugin):
                    self.chunk_modifier_list.append(plugin.create_chunk_modifer(context))
                    effect_plugins.add(plugin)

        assert self.application_plugin is not None,"application plugin must enable"
        self.output_builder = self.application_plugin.create_output_builder(context)

        # TODO effect_plugin logs


    def invoke(self, context: LocalContext, chunks: List[Chunk]) -> Chunk:
        phase = context.phase
        num_built_chunk = 0
        before_chunk = chunks[0]
        fix_chunks = chunks[1:]
        for chunk in fix_chunks:
            if self.output_builder.match_and_append(chunk):
                #TODO LOG
                num_built_chunk += 1

        return_chunk = before_chunk
        for modifier in self.chunk_modifier_list:
            if modifier.phase == phase:
                return_chunk = modifier.invoke(return_chunk,[chunk for chunk in fix_chunks if modifier.match(chunk)])
                #TODO LOG
        return return_chunk
    