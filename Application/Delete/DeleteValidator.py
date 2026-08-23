
from dataclasses import dataclass

from Application.Common.FileSystemInspector import FileSystemInspector
from Application.Delete.DeleteRequest import DeleteOptions


@dataclass
# Architecture: Validation failure DTO.
# Layer: Application.Delete.
# Role: Describes why a collection of delete targets was rejected.
class DeleteValidationError:
    reason:str
    paths: list[str]
# Architecture: Delete-input validation service.
# Layer: Application.Delete.
# Role: Applies delete-folder policy using the FileSystemInspector contract.
class DeleteValidator:
    def __init__(self, fs_inspector: FileSystemInspector) -> None:
        self.fs_inspector: FileSystemInspector = fs_inspector
    def validate(self, paths: list[str], options: DeleteOptions) -> list[DeleteValidationError]:
        if options.delete_folder:
            return []
        folder_paths=[p for p in paths if self.fs_inspector.is_directory(p)]
        if not folder_paths:
            return []
        return [DeleteValidationError(reason="FOLDER_NOT_ALLOWED",paths=folder_paths)]