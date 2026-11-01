import os
from pathlib import Path

from Application.Common.FileSystemInspector import FileSystemInspector


# Architecture: Operating-system file-system adapter.
# Layer: Infrastructure.FileSystem.
# Role: Implements file-system inspection using the host operating system.
# Contract: FileSystemInspector.
class OsFileSystemInspector(FileSystemInspector):
    def is_directory(self, path: Path) -> bool:
        return Path(path).is_dir()

    def is_file(self, path: Path) -> bool:
        return Path(path).is_file()

    def exists(self, path: Path) -> bool:
        return os.path.lexists(path)

    def can_read(self, path: Path) -> bool:
        return os.access(path, os.R_OK)

    def can_write(self, path: Path) -> bool:
        target = Path(os.path.abspath(path))
        if os.path.lexists(target):
            return os.access(target, os.W_OK)
        current = target.parent
        while not os.path.lexists(current):
            if current.parent == current:
                return False
            current = current.parent
        return current.is_dir() and os.access(current, os.W_OK)
