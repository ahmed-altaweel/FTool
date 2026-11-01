from abc import ABC, abstractmethod
from pathlib import Path


# Architecture: File-system inspection contract.
# Layer: Application.Common.
# Role: Abstracts file-system queries from validation and execution logic.
# Implementations: OsFileSystemInspector.
class FileSystemInspector(ABC):
    @abstractmethod
    def is_directory(self, path: Path) -> bool:
        ...

    @abstractmethod
    def is_file(self, path: Path) -> bool:
        ...

    @abstractmethod
    def exists(self, path: Path) -> bool:
        ...

    @abstractmethod
    def can_read(self, path: Path) -> bool:
        ...

    @abstractmethod
    def can_write(self, path: Path) -> bool:
        """True if `path` (existing or not) can be created/written."""
