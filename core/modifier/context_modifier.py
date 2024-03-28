from core.context import GlobalContext, LocalContext
import abc
from typing import Type, Callable


class GlobalContextModifier(abc.ABC):
    @abc.abstractmethod
    def invoke(context: GlobalContext):
        """ """


class LocalContextModifier(abc.ABC):
    @abc.abstractmethod
    def invoke(context: LocalContext):
        """ """


def ContextModifierWrapper(T: Type = GlobalContextModifier, **kwargs):
    class ContextModifierTmp(T):
        def __init__(self, func: Callable[[T, LocalContext],]) -> None:
            super().__init__()
            self._invoke = func
            for k, v in kwargs.items():
                self.__setattr__(k, v)

        def invoke(self, context: LocalContext):
            return self._invoke(self, context)

    return ContextModifierTmp
