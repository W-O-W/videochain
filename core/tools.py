from collections import Iterable
from typing import List, TypeVar, Union

T = TypeVar("T")


def flatten_and_dropduplicate(value: Union[List[List[T]], List[T], T]) -> List[T]:
    if isinstance(value, Iterable):
        return list(set(map(flatten_and_dropduplicate, value)))
    else:
        return [value]
