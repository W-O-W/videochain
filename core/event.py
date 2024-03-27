from typing import List
from dataclasses import dataclass,field
@dataclass(unsafe_hash=True)
class Event:
    id:str = "EMPTY"
    description:str = field(default_factory=str,compare=False,hash=False) 
    limit_scopes:List[str] = field(default_factory=list,compare=False,hash=False) 

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