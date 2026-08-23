from abc import ABC
from typing import Generic, TypeVar


PayloadT_co = TypeVar("PayloadT_co", covariant=True)


# Architecture: Command-request envelope.
# Layer: Application.Common.
# Role: Carries the command-specific payload through dispatch.
# Implementations: DeleteRequest.
class CommandRequest(ABC, Generic[PayloadT_co]):
    def __init__(self, request: PayloadT_co) -> None:
        self.request: PayloadT_co = request
