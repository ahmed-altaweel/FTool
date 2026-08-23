from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from Application.Common.CommandStatus import CommandStatus
from Application.Delete.DeleteValidator import DeleteValidationError


@dataclass
class DeleteResult:
    """
    Result object for delete operations.
    
    Responsibility: Encapsulates the outcome of a delete command execution.
    Layer: Application - Delete Module
    
    This is a Data Class that serves as a Result/Response object for delete operations.
    It contains status, affected paths, and any validation errors.
    
    Attributes:
        status: CommandStatus indicating success/failure/cancellation
        paths: List of paths that were processed
        violations: List of validation errors if status is INVALID
        is_dry_run: True if this was a simulation run
        error_path: The path that caused an error (if applicable)
    
    Used by: DeleteHandler, DeleteExecutor, Formatters, Presenters
    """
    status: CommandStatus
    paths: list[str] = field(default_factory=list)
    violations: list[DeleteValidationError] = field(default_factory=list)
    is_dry_run: bool = False
    error_path: Optional[str] = None
