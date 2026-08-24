from pathlib import Path

from Domain.Trash.Trash import Trash


class RestoreFromTrash(Trash):
    def move(self,path:Path):
        ...