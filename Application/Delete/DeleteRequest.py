from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from Application.Common.BaseCommandOptions import BaseCommandOptions
from Application.Common.Request import CommandRequest


class DeleteRequest(CommandRequest):
    """
    Request object for delete operations.
    
    Responsibility: Encapsulates all data needed to execute a delete command.
    Layer: Application - Delete Module
    
    This is a Concrete Implementation of CommandRequest for delete operations.
    It wraps DeleteRequestArgs which contains the path and options.
    
    Dependencies:
        - CommandRequest: Base abstraction
        - DeleteRequestArgs: Data container for delete arguments
    
    Used by: DeleteHandler, Dispatcher
    """
    pass


@dataclass
class DeleteOptions(BaseCommandOptions):
    """
    Options specific to delete operations.
    
    Responsibility: Contains configuration flags for delete command behavior.
    Layer: Application - Delete Module
    
    This is a Data Class that extends BaseCommandOptions with delete-specific settings.
    
    Attributes:
        quiet: Inherited from BaseCommandOptions - suppress output
        final_delete: If True, permanently delete instead of moving to trash
        recursive_search: If True, search recursively for matching files
        delete_folder: If True, allow deletion of folders
        force: If True, skip confirmation prompts
        dry_run: If True, simulate without actual deletion
        exclude: List of patterns to exclude from operation
    
    Used by: DeleteHandler, DeleteExecutor, ConfirmationPolicy, PreviewFormatter
    """
    final_delete: bool = False
    recursive_search: bool = False
    delete_folder: bool = False
    force: bool = False
    dry_run: bool = False
    exclude: Optional[list[str]] = None


@dataclass
class DeleteRequestArgs:
    """
    Data container for delete request arguments.
    
    Responsibility: Holds the path and options for a delete operation.
    Layer: Application - Delete Module
    
    This is a Value Object that groups related delete operation parameters.
    
    Attributes:
        path: The target path to delete
        options: DeleteOptions instance with operation settings
    
    Used by: DeleteRequest
    """
    path: str
    options: DeleteOptions
