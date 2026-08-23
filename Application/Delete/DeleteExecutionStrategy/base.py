from abc import ABC, abstractmethod

from Application.Delete.DeleteModes.base import DeleteMode
from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler


# Architecture: Delete-execution strategy contract.
# Layer: Application.Delete.
# Role: Abstracts real execution from dry-run traversal.
# Implementations: RealDeleteExecutor, DryRunDeleteExecutor.
class DeleteExecutorStrategy(ABC):
    def __init__(self, delete_handlers: list[TargetDeleteHandler]) -> None:
        self.delete_handlers: list[TargetDeleteHandler] = delete_handlers

    @abstractmethod
    def execute(self, paths: list[str], delete_mode: DeleteMode) -> None:
        ...
