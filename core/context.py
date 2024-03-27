class GlobalContext:
    def __init__(self,plugins) -> None:
        self.global_enable_plugins = plugins
        self.MAX_CHUNK_WAIT_TIME = 100

    def init(self)->bool:
        pass

    

class LocalContext:
    def __init__(self,global_context:GlobalContext) -> None:
        self.global_context = global_context
        self.MAX_CHUNK_WAIT_TIME = global_context.MAX_CHUNK_WAIT_TIME
        self.phase = 0