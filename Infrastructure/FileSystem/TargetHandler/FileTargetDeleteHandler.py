import os
from pathlib import Path
import shutil

from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler


# Architecture: File-system file target adapter.
# Layer: Infrastructure.FileSystem.
# Role: Detects, permanently deletes, or trashes regular files.
# Contract: TargetDeleteHandler.
class FileTargetDeleteHandler(TargetDeleteHandler):
    def can_handle(self, path: Path) -> bool:
        return path.is_file()

    def delete(self, path: Path) -> None:
        path.unlink()

    def delete_to_trash(self, path: Path) -> Path:
        return self.move_to_trash.move(path)
