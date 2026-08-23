from __future__ import annotations

from typing import Any

from Application.Common.Handler import CommandHandler
from Application.Common.Request import CommandRequest


class DeleteHandler(CommandHandler[CommandRequest]):
    """
    Handler for delete command requests.
    
    Responsibility: Processes delete requests by resolving targets and
    coordinating with the delete executor.
    Layer: Application - Delete Module
    
    This is a Concrete Implementation of CommandHandler for delete operations.
    It follows the Command Handler pattern by delegating actual execution to
    an executor after resolving target paths.
    
    Architecture Pattern: Command Handler
    
    Dependencies:
        - target_resolver: Resolves target paths from request (can include wildcards)
        - executor: Performs the actual delete operation
    
    Used by: Dispatcher for routing DeleteRequest commands
    """
    
    def __init__(self, target_resolver: Any, executor: Any) -> None:
        """
        Initialize the delete handler.
        
        Args:
            target_resolver: Service for resolving target paths.
            executor: Executor for performing delete operations.
        """
        super().__init__(executor)
        self.target_resolver: Any = target_resolver
    
    def execute(self, request: CommandRequest) -> Any:
        """
        Execute a delete request.
        
        Flow:
            1. Extract request data from wrapper
            2. Resolve target paths using target resolver
            3. Delegate execution to executor
        
        Args:
            request: The delete request to execute.
            
        Returns:
            DeleteResult containing the outcome of the operation.
        """
        request_data = request.request
        target_solver = self.target_resolver.resolve(
            request_data.path,
            request_data.options.recursive_search
        )
        return self.executor.execute(request_data.path, target_solver, request_data.options)
