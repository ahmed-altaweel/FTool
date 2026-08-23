from __future__ import annotations

from typing import Any, Protocol

from Application.Common.CommandStatus import CommandStatus


class RequestFactoryProtocol(Protocol):
    """Protocol for request factory objects."""
    def create(self, argv: Any) -> Any:
        ...


class PresenterProtocol(Protocol):
    """Protocol for presenter objects."""
    def present(self, result: Any) -> str:
        ...


class OutputPolicyResolverProtocol(Protocol):
    """Protocol for output policy resolver objects."""
    def resolve(self, quiet: bool) -> Any:
        ...


class Application:
    """
    Main application coordinator that orchestrates command execution flow.
    
    Responsibility: Coordinates the entire command execution pipeline from
    parsing arguments to displaying results.
    Layer: Application Core
    
    This is a Facade that simplifies interaction with the underlying subsystems.
    It manages the flow: Parse -> Create Request -> Dispatch -> Present -> Output
    
    Architecture Pattern: Application Facade / Coordinator
    
    Dependencies (via Dependency Injection):
        - dispatcher: Routes requests to handlers
        - request_factory: Creates request objects from parsed arguments
        - presenter: Converts results to display format
        - output_policy_resolver: Selects appropriate output policy
    
    Used by: CLI entry point (main.py)
    """
    
    def __init__(
        self,
        dispatcher: Any,
        request_factory: RequestFactoryProtocol,
        presenter: PresenterProtocol,
        output_policy_resolver: OutputPolicyResolverProtocol
    ) -> None:
        """
        Initialize the application with its dependencies.
        
        Args:
            dispatcher: The command dispatcher for routing requests.
            request_factory: Factory for creating request objects.
            presenter: Presenter for formatting results.
            output_policy_resolver: Resolver for output policies.
        """
        self.dispatcher: Any = dispatcher
        self.request_factory: RequestFactoryProtocol = request_factory
        self.presenter: PresenterProtocol = presenter
        self.output_policy_resolver: OutputPolicyResolverProtocol = output_policy_resolver
    
    def run(self, args: Any) -> None:
        """
        Execute the application main loop with the provided arguments.
        
        Flow:
            1. Create request from parsed arguments
            2. Dispatch request to appropriate handler
            3. Present the result
            4. Output via selected policy
        
        Args:
            args: Parsed command-line arguments.
        """
        request: Any = self.request_factory.create(args)
        result: Any = self.dispatcher.dispatch(request)
        text: str = self.presenter.present(result)
        quiet: bool = getattr(request.request.options, 'quiet', False)
        output_policy: Any = self.output_policy_resolver.resolve(quiet)
        
        if result.status == CommandStatus.INVALID:
            output_policy.print_error(text)
        else:
            output_policy.print_result(text)
