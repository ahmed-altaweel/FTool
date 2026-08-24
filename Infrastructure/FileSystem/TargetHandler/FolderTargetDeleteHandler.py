import os
from pathlib import Path
import shutil

from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler


# Architecture: File-system folder target adapter.
# Layer: Infrastructure.FileSystem.
# Role: Detects, permanently deletes, or trashes directories.
# Contract: TargetDeleteHandler.
class FolderTargetDeleteHandler(TargetDeleteHandler):
    def can_handle(self, path: Path) -> bool:
        return path.is_dir()

    def delete(self, path: Path) -> None:
        shutil.rmtree(path)

    def delete_to_trash(self, path: Path) -> Path:
        return self.move_to_trash.move(path)
