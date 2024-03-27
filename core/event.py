from typevar import Chunks
from plugins.plugin import Plugin
from typing import List
from abc import ABC
class Event:
    id = "EMPTY"
    description = "do nothing"
    def __init__(self,limit_scopes = []) -> None:
        self.limit_scopes = limit_scopes

class EmptyEvent(Event):
    pass

class FinalEvent(Event):
    id = "FINAL"
    description = "stop flow invoke signal"

class KillEvent(Event):
    id = "KILL"
    description = "kill flow"

def has_final_event(events:List[Event])->bool:
    for event in events:
        if isinstance(event,FinalEvent):
            return True
    return False