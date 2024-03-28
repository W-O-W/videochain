from typing import List, TypeVar, Union

T = TypeVar("T")


def flatten_and_dropduplicate(value: Union[List[List[T]], List[T], T]) -> List[T]:
    if isinstance(value, List):
        return sorted(list(set(flatten_and_dropduplicate(v) for v in value)))
    else:
        return value
