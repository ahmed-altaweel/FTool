from pathlib import Path

from platformdirs import user_data_dir


class TrashPath:
    def __init__(self,trash_path:str |None=None,trash_registry_path:str |None=None):
        self.root= Path(trash_path) if trash_path is not None else self.default_root()
        self.entries_path=self.root /'entries'
        self.trash_registry_path:Path=Path(trash_registry_path) if trash_registry_path is not None else self.root/'trash_registry.json'
        print(f"Path:{self.root}")
        self._ensure_structure_exists()
    @staticmethod
    def default_root()->Path:
       return Path(user_data_dir())/"ftool"/'trash'
    
    def _ensure_structure_exists(self)->None:
      
        self.root.mkdir(parents=True,exist_ok=True)
        self.entries_path.mkdir(parents=True,exist_ok=True)
       