from datetime import datetime

from Application.Delete.DeleteModes.base import DeleteMode
from Domain.Trash.TrashEntry import TrashEntry
from Domain.Trash.base import TrashRegistry
class TrashDeleteMode(DeleteMode):
    def __init__(self,trash_registry):
        self.trash_registry=trash_registry
    def execute(self, path,target_handler):
        trashed_path=target_handler.delete_to_trash(path)
        self.trash_registry.record(
            TrashEntry(original_path=path,trashed_path=trashed_path,deleted_at=datetime.now())
        )
        return trashed_path
