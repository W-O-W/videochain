"""

[SCOPE][COMMAND][DATA][SEP]
"""

import asyncio
class Chunk:
    def __init__(self) -> None:
        self.scope = ""
        self.command = ""
        self.data = ""
    

def new_none_chunk():
    chunk = Chunk()
    chunk.scope = "FLOW"
    chunk.command = ""
    chunk.data = ""
    return chunk
    

class AsyncChunk(Chunk):
    def __init__(self,task:asyncio.Task) -> None:
        super().__init__()
        self.task = task
    
    def init_from(self,chunk:Chunk):
        self.command = chunk.command
        self.scope = chunk.scope
        self.data = chunk.data
        
    async def get(self) -> Chunk:
        if self.task is not None:
            await self.task
            self.init_from(self.task.result())
            self.task = None
        return self
        