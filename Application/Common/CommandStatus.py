from __future__ import annotations

from enum import Enum, auto


class CommandStatus(Enum):
    """
    Enumeration of possible command execution statuses.
    
    Responsibility: Represents the outcome of command execution.
    Layer: Application Core (Common)
    
    This is a Value Object that encapsulates command execution results.
    Used throughout the application to communicate operation outcomes.
    
    Values:
        SUCCESS: Command executed successfully
        CANCELLED: Command was cancelled by user
        NOT_FOUND: Target resource was not found
        INVALID: Command validation failed
    """
    SUCCESS = auto()
    CANCELLED = auto()
    NOT_FOUND = auto()
    INVALID = auto()