

from Application.Common.BaseCommandOptions import BaseCommandOptions
from Application.Common.Request import CommandRequest
from dataclasses import dataclass


class DeleteRequest(CommandRequest):
    pass

@dataclass
class DeleteOptions(BaseCommandOptions):
    final_delete:bool=False
    recursive_search:bool=False
    delete_folder:bool=False
    force:bool=False
    dry_run:bool=False
    exclude:list[str] |None =None

@dataclass
class DeleteRequestArgs:
    path:str
    options:DeleteOptions



