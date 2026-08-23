from enum import Enum, auto

# Architecture: Command outcome enumeration.
# Layer: Application.Common.
# Role: Provides stable statuses consumed by use cases and presenters.
class CommandStatus(Enum):
    SUCCESS = auto()
    CANCELLED = auto()
    NOT_FOUND = auto()
    INVALID=auto()