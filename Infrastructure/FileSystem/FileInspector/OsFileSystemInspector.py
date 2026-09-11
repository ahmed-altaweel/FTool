import os
from pathlib import Path

from Application.Common.FileSystemInspector import FileSystemInspector


# Architecture: Operating-system file-system adapter.
# Layer: Infrastructure.FileSystem.
# Role: Implements directory inspection using the host operating system.
# Contract: FileSystemInspector.
class OsFileSystemInspector(FileSystemInspector):
    def is_directory(self, path: Path) -> bool:
        return path.is_dir()
