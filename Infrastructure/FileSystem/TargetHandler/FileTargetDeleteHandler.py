import os
import shutil

from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler


# Architecture: File-system file target adapter.
# Layer: Infrastructure.FileSystem.
# Role: Detects, permanently deletes, or trashes regular files.
# Contract: TargetDeleteHandler.
class FileTargetDeleteHandler(TargetDeleteHandler):
    def can_handle(self, path: str) -> bool:
        return os.path.isfile(path)

    def delete(self, path: str) -> None:
        os.remove(path)

    def delete_to_trash(self, path: str) -> str:
        destination = os.path.join(self.trash_folder, os.path.basename(path))
        shutil.move(path, destination)
        return destination
