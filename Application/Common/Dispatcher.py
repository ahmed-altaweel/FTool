from __future__ import annotations

from typing import Any, Dict, Type


class Dispatcher:
    """
    Central dispatcher for routing command requests to their handlers.
    
    Responsibility: Maintains a registry of request types and their corresponding
    handlers, and dispatches incoming requests to the appropriate handler.
    Layer: Application Core (Common)
    
    This is a Core Infrastructure component that implements a simple Command Pattern
    dispatcher. It uses runtime type inspection to route requests.
    
    Architecture Pattern: Command Dispatcher / Request Router
    
    Dependencies:
        - CommandHandler: Handlers that execute specific request types
        - CommandRequest: Request objects that are dispatched
    
    Used by: Application entry point for executing commands
    """
    
    def __init__(self) -> None:
        """Initialize the dispatcher with an empty handler registry."""
        self.handlers: Dict[Type[Any], Any] = {}
    
    def register(self, request_type: Type[Any], handler: Any) -> None:
        """
        Register a handler for a specific request type.
        
        Args:
            request_type: The class type of the request to handle.
            handler: The handler instance that will process this request type.
        """
        self.handlers[request_type] = handler
    
    def dispatch(self, request: Any) -> Any:
        """
        Dispatch a request to its registered handler.
        
        Args:
            request: The request object to dispatch.
            
        Returns:
            The result from executing the handler.
            
        Note:
            Uses runtime type inspection (type(request)) to find the handler.
        """
        handler: Any = self.handlers[type(request)]
        return handler.execute(request)
