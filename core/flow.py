from core.chunk import Chunk, new_none_chunk
from typing import List
from core.context import LocalContext, GlobalContext
from plugins.plugin import (
    Plugin,
    ObserverPlugin,
    EventAgentPlugin,
    GlobalContextPlugin,
)
from plugins.demo import BASIC_LLM_PLUGINS
from core.agent import FlowAgent, EventAgent
import logging
from core.constants import Events, Chunks
from core.tools import flatten_and_dropduplicate
from core.event import has_final_event
import asyncio

# logging.config.fileConfig("conf/logging.conf")

"""
flow:一个具有一定生命周期的流，在生命周期内，通过 invoke 函数进行交互，并提供 checkpoint 功能，类似于消息队列
context:flow 的上下文，保存 flow 的全局变量、日志信息、持久化信息
observers:监听 Event 的实例，当对应的 Event 进入到 Flow 后触发
main_agent:根据 observers 的返回结果，对 flow 的输入进行加工
event_agent:对 chunk 进行转化，生成 event

一个典型的 Demo：
observers:为 RAG 的 retriever
invoke chunk 为：中国首都是哪里？
1. event_agent: 判断是否需要 RAG
2. 假设需要 RAG 则会产生一个 RAG event: [Q][中国首都是哪里？][P0][RAG]
3. RAG event 会触发 RAG observer -> 产生 RAG 一种结果：[百度百科][北京是中华人民共和国首都]
4. main_agent: 组织成[Q][中国首都是哪里？][P0][RAG][百度百科][北京是中华人民共和国首都] 形式的输入请求 LLM 得到 [根据百度百科的文档，中国首都是北京]
5. main_agent: 对结果组织成 [Q][中国首都是哪里？][P0][RAG][百度百科][北京是中华人民共和国首都][P1][LLM][根据百度百科的文档，中国首都是北京] 形式，继续 invoke flow
6. 当没有新的 event 触发或者出发 [FINAL] event 的时候，返回最终的结果

"""


class Flow:
    def __init__(self, plugins: List[Plugin] = BASIC_LLM_PLUGINS["QWEN"]) -> None:
        self.context = GlobalContext(plugins)
        for modifier in [
            plugin.create_global_context_modifier()
            for plugin in plugins
            if isinstance(plugin, GlobalContextPlugin)
        ]:
            modifier.invoke(self.context)

        # 初始化全局上下文和插件
        if not self.context.init():
            # TODO LOG
            pass

        for plugin in plugins:
            if not plugin.init(self.context):
                # TODO LOG
                pass

        self.context.global_enable_plugins = plugins
        self.observers = flatten_and_dropduplicate(
            [
                plugin.create_observers(self.context)
                for plugin in plugins
                if isinstance(plugin, ObserverPlugin)
            ]
        )
        self.event_agent = EventAgent(
            self.context,
            [plugin for plugin in plugins if isinstance(plugin, EventAgentPlugin)],
        )

    async def invoke(self, chunk: Chunk) -> Chunks:
        local_context = LocalContext(self.context)

        flow_agent = FlowAgent(local_context)

        request_events = self.event_agent.invoke(local_context, chunk)
        response_chunk = new_none_chunk()
        while request_events and not has_final_event(request_events):
            async_chunks = self.notify_all_observers(local_context, request_events)
            response_chunks: List[Chunk] = [
                await async_chunk
                for async_chunk in async_chunks
                if async_chunk is not None
            ]
            response_chunk = flow_agent.invoke(local_context, [chunk] + response_chunks)
            request_events = self.event_agent.invoke(local_context, chunk)
            chunk = response_chunk

        return response_chunk

    def notify_all_observers(
        self, local_context: LocalContext, events: List[Events]
    ) -> List:
        async_chunks = []
        events = flatten_and_dropduplicate(events)
        for event in events:
            for observer in self.observers:
                if observer.observe(event):
                    async_chunks.append(observer.invoke(local_context, event))

        return flatten_and_dropduplicate(async_chunks)
