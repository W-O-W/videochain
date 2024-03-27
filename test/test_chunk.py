
from core.chunk import *
def test_chunk():
    chunk = Chunk()
    chunk.data = "T1"
    print(chunk)
async def new_chunk():
     print("A")
     return Chunk(scope="A")
