from enum import Enum, auto

class CommandStatus(Enum):
    SUCCESS = auto()
    CANCELLED = auto()
    NOT_FOUND = auto()
    INVALID=auto()