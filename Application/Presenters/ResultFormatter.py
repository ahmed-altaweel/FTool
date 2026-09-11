from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from Application.Delete.DeleteResult import DeleteResult
from Application.Common.Result import CommandResult
TResult=TypeVar("TResult_f",bound=[CommandResult])
# Architecture: Result-formatting contract.
# Layer: Application.Presenters.
# Role: Converts a use-case result DTO into display text.
# Implementations: DeleteResultFormatter.
class ResultFormatter(ABC,Generic[TResult]):
    @abstractmethod
    def format(self, result: TResult) -> str:
        pass