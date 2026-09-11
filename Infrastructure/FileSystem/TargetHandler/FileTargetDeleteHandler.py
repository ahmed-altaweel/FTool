import os
from pathlib import Path

from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler


# Architecture: File-system file target adapter.
# Layer: Infrastructure.FileSystem.
# Role: Detects, permanently deletes, or trashes files.
# Contract: TargetDeleteHandler.
class FileTargetDeleteHandler(TargetDeleteHandler):
    def can_handle(self, path: Path) -> bool:
        return path.is_file()

    def delete(self, path: Path) -> None:
        os.remove(path)

    def delete_to_trash(self, path: Path) -> Path:
        return self.move_to_trash.move(path)