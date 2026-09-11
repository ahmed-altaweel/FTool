from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

from Application.Common.Request import CommandRequest
from Application.Common.Result import CommandResult


RequestT_contra = TypeVar(
    "RequestT_contra",
    bound=CommandRequest[object],
    contravariant=True,
)
ResultT_co = TypeVar("ResultT_co",
                     bound=CommandResult, covariant=True)

# Architecture: Use-case handler contract.
# Layer: Application.Common.
# Role: Defines execution of a command request.
# Implementations: DeleteHandler.
class CommandHandler(ABC,Generic[RequestT_contra, ResultT_co]):
    @abstractmethod
    def execute(self, request: RequestT_contra) -> ResultT_co:
        ...

    