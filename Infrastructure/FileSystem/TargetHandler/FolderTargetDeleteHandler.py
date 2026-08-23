import os
import shutil

from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler


# Architecture: File-system folder target adapter.
# Layer: Infrastructure.FileSystem.
# Role: Detects, permanently deletes, or trashes directories.
# Contract: TargetDeleteHandler.
class FolderTargetDeleteHandler(TargetDeleteHandler):
    def can_handle(self, path: str) -> bool:
        return os.path.isdir(path)

    def delete(self, path: str) -> None:
        shutil.rmtree(path)

    def delete_to_trash(self, path: str) -> str:
        destination = os.path.join(self.trash_folder, os.path.basename(path))
        shutil.move(path, destination)
        return destination
