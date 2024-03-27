
from core.observer.observer import *
def test_observer():
    observerA = Observer(Event("A"))
    observerB = Observer(Event("A"))
    e = Event("A",limit_scopes="B")
    assert observerA.observe(e)

    async def run():
        return [await observerA.invoke(None,e), await observerB.invoke(None,e)]
    
    print(asyncio.run(run()))