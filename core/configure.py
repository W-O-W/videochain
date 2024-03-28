
from dataclasses import dataclass


@dataclass
class configure:
    DEFAULT_CHUNK_DATA_SEP:str = ""
    DEFAULT_SCOPE_SEP:str = "|"

def get_configure():
    return configure()