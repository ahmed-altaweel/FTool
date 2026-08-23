from typing import Generic, Protocol, TypeVar

from Application.Common.Handler import CommandHandler
from Application.Common.Request import CommandRequest
from Application.Common.Result import CommandResult


RequestT = TypeVar("RequestT", bound=CommandRequest[object])
ResultT = TypeVar("ResultT",bound=CommandResult)


class _RegisteredHandler(Protocol):
    def execute(self, request: object) -> object:
        ...


class _HandlerAdapter(Generic[RequestT, ResultT]):
    def __init__(
        self,
        request_type: type[RequestT],
        handler: CommandHandler[RequestT, ResultT],
    ) -> None:
        self.request_type = request_type
        self.handler = handler

    def execute(self, request: object) -> object:
        if not isinstance(request, self.request_type):
            raise TypeError(
                f"Handler expected {self.request_type.__name__}, "
                f"got {type(request).__name__}"
            )
        return self.handler.execute(request)


# Architecture: Request-to-handler dispatch registry.
# Layer: Application.Common.
# Role: Routes a request to the handler registered for its concrete type.
class Dispatcher:
    def __init__(self) -> None:
        self.handlers: dict[type[object], CommandHandler[RequestT,ResultT]] = {}

    def register(
        self,
        request_type: type[RequestT],
        handler: CommandHandler[RequestT, ResultT],
    ) -> None:
        self.handlers[request_type] = _HandlerAdapter(request_type, handler)

    def dispatch(self, request: CommandRequest[object]) -> object:
        handler = self.handlers.get(type(request))
        if handler is None:
            raise ValueError(
                f"No handler registered for {type(request).__name__}"
            )
        return handler.execute(request)

