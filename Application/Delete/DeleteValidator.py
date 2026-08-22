
from dataclasses import dataclass


@dataclass
class DeleteValidationError:
    reason:str
    paths: list[str]
class DeleteValidator:
    def __init__(self,fs_inspector):
        self.fs_inspector=fs_inspector
    def validate(self,paths,options):
        if options.delete_folder:
            return []
        folder_paths=[p for p in paths if self.fs_inspector.is_directory(p)]
        if not folder_paths:
            return []
        return [DeleteValidationError(reason="FOLDER_NOT_ALLOWED",paths=folder_paths)]