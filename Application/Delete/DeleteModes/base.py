from abc import ABC, abstractmethod

from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler


# Architecture: Target-deletion mode contract.
# Layer: Application.Delete.
# Role: Abstracts the action applied to a selected target handler.
# Implementations: PermanentDeleteMode, TrashDeleteMode.
class DeleteMode(ABC):
    @abstractmethod
    def execute(self, path: str, target_handler: TargetDeleteHandler) -> str | None:
        ...
