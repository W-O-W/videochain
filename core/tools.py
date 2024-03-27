from collections import Iterable

def flatten_and_dropduplicate(value):
    if isinstance(value,Iterable):
        return list(set(map(flatten_and_dropduplicate,value)))
    else:
        return value    

