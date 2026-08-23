from abc import ABC, abstractmethod

from Domain.Trash.TrashEntry import TrashEntry


# Architecture: Trash persistence contract.
# Layer: Domain.Trash.
# Role: Defines recording, restoring, listing, and initialization of TrashEntry records.
# Implementations: JsonTrashRegistry.
class TrashRegistry(ABC):
   
    @abstractmethod
    def record(self,entry:TrashEntry) ->None:
        ...
    @abstractmethod
    def restore(self, original_path: str) -> TrashEntry:
        ...
    @abstractmethod
    def list_entries(self) -> list[TrashEntry]:
        ...
 