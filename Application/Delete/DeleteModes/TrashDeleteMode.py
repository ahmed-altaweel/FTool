from datetime import datetime

from Application.Delete.DeleteModes.base import DeleteMode
from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler
from Domain.Trash.TrashEntry import TrashEntry
from Domain.Trash.base import TrashRegistry


# Architecture: Trash-delete mode.
# Layer: Application.Delete.
# Role: Moves the target to trash and records a TrashEntry through TrashRegistry.
# Contract: DeleteMode.
class TrashDeleteMode(DeleteMode):
    def __init__(self, trash_registry: TrashRegistry) -> None:
        self.trash_registry: TrashRegistry = trash_registry

    def execute(self, path: str, target_handler: TargetDeleteHandler) -> str:
        trashed_path = target_handler.delete_to_trash(path)
        self.trash_registry.record(
            TrashEntry(
                original_path=path,
                trashed_path=trashed_path,
                deleted_at=datetime.now(),
            )
        )
        return trashed_path
