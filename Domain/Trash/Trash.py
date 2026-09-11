    
from abc import ABC
from pathlib import Path


class Trash(ABC):
    def __init__(self,entries_path:Path):
        self.entries_path=entries_path 
        
    def move(self,path:Path):
       ...