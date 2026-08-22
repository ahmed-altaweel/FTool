from abc import ABC,abstractmethod

from Domain.Trash.TrashEntry import TrashEntry


class TrashRegistry(ABC):
    def __init__(self,registry_file:str):
        self.registry_file=registry_file
        self._ensure_file_exists()
    @abstractmethod
    def record(self,entry:TrashEntry) ->None:
        ...
    @abstractmethod
    def restore(self,original_path:str)->TrashEntry:
        ...
    @abstractmethod
    def list_entries(self)->list[TrashEntry]:
        ...
    @abstractmethod
    def _ensure_file_exists(self)->None:
        ...