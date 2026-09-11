import os
from pathlib import Path


# Architecture: Folder-target create handler.
# Layer: Infrastructure.FileSystem.TargetHandler.
# Role: Creates a directory on the local filesystem.
# Note: structurally conforms to Domain.Create.TargetCreateHandler.
class FolderTargetCreateHandler:
    def can_handle(self, path: Path) -> bool:
        return True

    def create(self, path: Path, *, parents: bool = False) -> None:
        if parents:
            os.makedirs(path, exist_ok=False)
        else:
            os.mkdir(path)
