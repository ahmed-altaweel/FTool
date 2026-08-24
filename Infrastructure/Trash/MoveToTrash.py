from abc import ABC
from pathlib import Path
import shutil
import uuid
from platformdirs import use_data_dir

from Domain.Trash.TrashRegistry import TrashRegistry
class TrashPath:
    def __init__(self,trash_path:str |None=None,trash_registry:Path |None=None):
        self.root=trash_path or self.default_root()
        self.entries_path=self.root /'entries'
        self.trash_registry:Path=trash_registry or self.trash/'trash_registry.json'
        self._ensure_file_exists()
    @staticmethod
    def default_root()->Path:
       return Path(use_data_dir("ftool"))/'trash'
    def _ensure_file_exists(self)->None:
      
        self.root.mkdir(exist_ok=True)
        self.entries_path.mkdir(exist_ok=True)
       
        

    
class Trash(ABC):
    def __init__(self,trash_registry:TrashRegistry,entries_path:str):
        self.entries_path=entries_path 
        self.trash_registry:TrashRegistry=trash_registry
    def move(self,path:Path):
        destination=self.entries_path/ uuid.hex()
        shutil.move(path,destination)
        self.trash_registry.record()
    
class MoveToTrash(Trash):
    def move(self,path:Path):
        destination=ntry_path=self.trash_path/'trash'/ uuid.hex()/ path.name
        try:
            shutil.move(path,destination)
        

    def registry():
class RestoreFromTrash(Trash):