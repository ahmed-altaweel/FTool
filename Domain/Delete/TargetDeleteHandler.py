from abc import ABC, abstractmethod


# Architecture: Target deletion capability contract.
# Layer: Domain.Delete.
# Role: Defines how a supported target is detected, deleted, or moved to trash.
# Implementations: FileTargetDeleteHandler, FolderTargetDeleteHandler.
class TargetDeleteHandler(ABC):
    def __init__(self, trash_folder: str) -> None:
        self.trash_folder: str = trash_folder

    @abstractmethod
    def can_handle(self, path: str) -> bool:
        ...

    @abstractmethod
    def delete(self, path: str) -> None:
        """Permanently delete the target."""
        ...

    @abstractmethod
    def delete_to_trash(self, path: str) -> str:
        """Move the target into the configured trash folder."""
        ...
