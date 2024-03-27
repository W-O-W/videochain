
from core.context import GlobalContext, LocalContext
import abc

class GlobalContextModifier(abc.ABC):
    @abc.abstractmethod
    def invoke(context:GlobalContext):
        """
        """
        

class LocalContextModifier(abc.ABC):
    @abc.abstractmethod
    def invoke(context:LocalContext):
        """
        """