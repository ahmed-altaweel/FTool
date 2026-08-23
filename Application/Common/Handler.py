from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar('T')


class CommandHandler(ABC, Generic[T]):
    """
    Base abstraction for all command handlers in the application.
    
    Responsibility: Executes commands of a specific type and returns results.
    Layer: Application Core (Common)
    
    This is an Abstraction that defines the contract for command execution.
    Concrete implementations handle specific request types and coordinate
    with executors to perform the actual work.
    
    Architecture Pattern: Command Handler
    
    Dependencies:
        - Executor: Performs the actual operation
        - Request: The command request to execute
    
    Used by: Dispatcher for routing requests to appropriate handlers
    """
    
    def __init__(self, executor: Any) -> None:
        """
        Initialize the handler with an executor.
        
        Args:
            executor: The executor responsible for performing the operation.
        """
        self.executor: Any = executor
    
    @abstractmethod
    def execute(self, request: T) -> Any:
        """
        Execute the command and return the result.
        
        Args:
            request: The command request to execute.
            
        Returns:
            The result of the command execution.
        """
        pass