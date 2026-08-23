from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List


class DeleteExecutorStrategy(ABC):
    """
    Abstract base for delete execution strategies.
    
    Responsibility: Defines the contract for executing delete operations.
    Layer: Application - Delete Module (Execution Strategy)
    
    This is an Abstraction that implements the Strategy Pattern for delete execution.
    Different implementations can provide real deletion, dry-run simulation, or
    other execution behaviors.
    
    Architecture Pattern: Strategy Pattern
    
    Dependencies:
        - delete_strategies: List of TargetDeleteHandler implementations
    
    Implementations:
        - RealDeleteExecutor: Performs actual deletion
        - DryRunDeleteExecutor: Simulates deletion without changes
    
    Used by: DeleteExecutor
    """
    
    def __init__(self, delete_strategies: List[Any]) -> None:
        """
        Initialize the strategy with target handlers.
        
        Args:
            delete_strategies: List of handlers for different target types.
        """
        self.delete_strategies: List[Any] = delete_strategies
    
    @abstractmethod
    def execute(self, paths: List[str], delete_type_strategy: Any) -> None:
        """
        Execute the delete operation on the given paths.
        
        Args:
            paths: List of paths to process.
            delete_type_strategy: The delete mode strategy to use.
        """
        pass
