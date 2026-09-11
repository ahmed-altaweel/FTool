from abc import ABC
from datetime import datetime
from pathlib import Path
import shutil
import uuid 
from platformdirs import  user_data_dir

from Domain.Trash.Trash import Trash
from Domain.Trash.TrashEntry import TrashEntry
from Domain.Trash.TrashRegistry import TrashRegistry

        


    
class MoveToTrash(Trash):
    def move(self,path:Path)->Path:
        destination=self.entries_path/ uuid.uuid4().hex/ path.name
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.move(path,destination)
        return destination
