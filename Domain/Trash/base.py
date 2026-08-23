from abc import ABC, abstractmethod

from Domain.Trash.TrashEntry import TrashEntry


# Architecture: Trash persistence contract.
# Layer: Domain.Trash.
# Role: Defines recording, restoring, listing, and initialization of TrashEntry records.
# Implementations: JsonTrashRegistry.
class TrashRegistry(ABC):
    def __init__(self, registry_file: str) -> None:
        self.registry_file: str = registry_file
        self._ensure_file_exists()
    @abstractmethod
    def record(self,entry:TrashEntry) ->None:
        ...
    @abstractmethod
    def restore(self, original_path: str) -> TrashEntry:
        ...
    @abstractmethod
    def list_entries(self) -> list[TrashEntry]:
        ...
    @abstractmethod
    def _ensure_file_exists(self)->None:
        ...