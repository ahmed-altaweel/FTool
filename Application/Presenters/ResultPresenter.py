from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from Application.Delete.DeleteResult import DeleteResult
from Application.Common.Result import CommandResult

# Architecture: Result-presentation contract.
# Layer: Application.Presenters.
# Role: Selects a formatter and exposes the final presentation text.
# Implementations: CliResultPresenter.
class ResultPresenter(ABC):
    @abstractmethod
    def present(self, result:CommandResult ) -> str:
        pass