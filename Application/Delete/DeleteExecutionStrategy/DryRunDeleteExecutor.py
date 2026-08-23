from __future__ import annotations

from typing import Any, List

from Application.Delete.DeleteExecutionStrategy.base import DeleteExecutorStrategy
from Application.Delete.DeleteModes.base import DeleteMode


class DryRunDeleteExecutor(DeleteExecutorStrategy):
    """
    Dry-run implementation of delete execution strategy.
    
    Responsibility: Simulates delete operations without making actual changes.
    Layer: Application - Delete Module (Execution Strategy)
    
    This is a Concrete Implementation of DeleteExecutorStrategy that provides
    safe simulation of delete operations. It checks which handlers would handle
    each path but performs no actual deletion.
    
    Architecture Pattern: Strategy Pattern (Concrete Strategy)
    
    Dependencies:
        - delete_strategies: Inherited from base class
    
    Used by: DeleteExecutor when dry_run option is enabled
    """
    
    def execute(self, paths: List[str], delete_type_strategy: DeleteMode) -> None:
        """
        Simulate delete operation without making changes.
        
        Flow:
            1. Iterate through all target paths
            2. For each path, find the appropriate handler
            3. Skip actual execution (dry run)
        
        Args:
            paths: List of paths that would be deleted.
            delete_type_strategy: The delete mode (unused in dry run).
        """
        for path in paths:
            for strategy in self.delete_strategies:
                if strategy.can_handle(path):
                    # Dry run - no actual operation performed
                    pass
