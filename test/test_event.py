
from core.event import *
def test_event():
    a1 = Event(id="A",description="a",limit_scopes=["A"])
    a2 = Event(id="A",description="a",limit_scopes=["A","B"])
    assert a1 == a2

def test_event_set():
    s = set([
        Event(id="A",description="a",limit_scopes=["A"]),
        Event(id="B",description="b",limit_scopes=["A","B"])
    ])

    c1 = Event(id="A",description="a",limit_scopes=["A"])
    assert c1 in s

    c2 = Event(id="A",description="a",limit_scopes=["A","B"])
    assert c2 in s

    c3 = Event(id="C",description="a",limit_scopes=["A","B"])
    assert c3 not in s

    c4 = Event(id="B",description="b",limit_scopes=["A","B"])
    assert c4 in s