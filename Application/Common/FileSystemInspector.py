from abc import ABC,abstractmethod


# Architecture: File-system inspection contract.
# Layer: Application.Common.
# Role: Abstracts directory detection from validation logic.
# Implementations: OsFileSystemInspector.
class FileSystemInspector(ABC):
    @abstractmethod
    def is_directory(self, path: str) -> bool:
        ...