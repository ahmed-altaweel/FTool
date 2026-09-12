import os
from pathlib import Path


# Architecture: File-target create handler.
# Layer: Infrastructure.FileSystem.TargetHandler.
# Role: Creates an empty file on the local filesystem.
# Note: structurally conforms to Domain.Create.TargetCreateHandler.
class FileTargetCreateHandler:
    def can_handle(self, path: Path) -> bool:
        return True

    def create(self, path: Path, *, parents: bool = False) -> None:
        if parents:
            parent = path.parent
            if parent and str(parent) not in ("", "."):
                os.makedirs(parent, exist_ok=True)
        with open(path, "x", encoding="utf-8"):
            pass