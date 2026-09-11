from abc import ABC, abstractmethod
from pathlib import Path

from Infrastructure.Trash import MoveToTrash


# Architecture: Target deletion capability contract.
# Layer: Domain.Delete.
# Role: Defines how a supported target is detected, deleted, or moved to trash.
# Implementations: FileTargetDeleteHandler, FolderTargetDeleteHandler.
class TargetDeleteHandler(ABC):
    def __init__(self, move_to_trash: MoveToTrash) -> None:
        self.move_to_trash: MoveToTrash = move_to_trash

    @abstractmethod
    def can_handle(self, path: Path) -> bool:
        ...

    @abstractmethod
    def delete(self, path: Path) -> None:
        """Permanently delete the target."""
        ...

    @abstractmethod
    def delete_to_trash(self, path: Path) -> Path:
        """Move the target into the configured trash folder."""
        ...
