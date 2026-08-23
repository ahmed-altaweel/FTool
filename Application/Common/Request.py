from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CommandRequest(ABC):
    """
    Base abstraction for all command requests in the application.
    
    Responsibility: Encapsulates request data for command execution.
    Layer: Application Core (Common)
    
    This is an Abstraction that defines the contract for all request types.
    Concrete implementations should inherit from this class and add specific
    request data.
    
    Dependencies: None (Base class)
    Used by: Dispatcher, CommandHandler implementations
    """
    
    def __init__(self, request: Any) -> None:
        """
        Initialize the command request with request data.
        
        Args:
            request: The request data object containing command-specific arguments.
        """
        self.request: Any = request
