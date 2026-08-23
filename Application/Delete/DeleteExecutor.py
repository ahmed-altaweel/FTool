from __future__ import annotations

from typing import Any, List

from Application.Common.CommandStatus import CommandStatus
from Application.Delete.DeleteExecutionStrategy.DryRunDeleteExecutor import DryRunDeleteExecutor
from Application.Delete.DeleteExecutionStrategy.RealDeleteExecutor import RealDeleteExecutor
from Application.Delete.DeleteModes.PermanentDeleteMode import PermanentDeleteMode
from Application.Delete.DeleteModes.TrashDeleteMode import TrashDeleteMode
from Application.Delete.DeleteModes.base import DeleteMode
from Application.Delete.DeleteRequest import DeleteOptions
from Application.Delete.DeleteResult import DeleteResult
from Application.Delete.DeleteValidator import DeleteValidator
from Application.Presenters.PreviewFormatter import PreviewFormatter
from Infrastructure.Terminal.Confirmation.RequiredConfirmationPolicy import RequiredConfirmationPolicy
from Infrastructure.Terminal.Confirmation.SkippedConfirmationPolicy import SkippedConfirmationPolicy
from Infrastructure.Terminal.Confirmation.base import ConfirmationPolicy


class DeleteExecutor:
    """
    Orchestrator for delete operations.
    
    Responsibility: Coordinates the complete delete workflow including validation,
    confirmation, strategy selection, and execution.
    Layer: Application - Delete Module
    
    This is a Service class that implements the core delete operation logic.
    It uses Strategy Pattern for both execution mode (real vs dry-run) and
    delete mode (permanent vs trash).
    
    Architecture Patterns:
        - Service Layer
        - Strategy Pattern (execution and delete modes)
    
    Dependencies:
        - delete_handlers: List of TargetDeleteHandler implementations
        - preview_formatter: Formats preview for user confirmation
        - validator: Validates delete operations
        - trash_delete_mode: Pre-configured trash mode instance
    
    Used by: DeleteHandler
    """
    
    def __init__(
        self,
        delete_handlers: List[Any],
        preview_formatter: PreviewFormatter,
        validator: DeleteValidator,
        trash_delete_mode: TrashDeleteMode
    ) -> None:
        """
        Initialize the delete executor.
        
        Args:
            delete_handlers: List of handlers for different target types.
            preview_formatter: Formatter for showing preview to user.
            validator: Validator for checking operation validity.
            trash_delete_mode: Mode for trash-based deletion.
        """
        self.delete_handlers: List[Any] = delete_handlers
        self.preview_formatter: PreviewFormatter = preview_formatter
        self.validator: DeleteValidator = validator
        self.trash_delete_mode: DeleteMode = trash_delete_mode
    
    def execute(
        self,
        path: str,
        paths: List[str],
        options: DeleteOptions
    ) -> DeleteResult:
        """
        Execute the delete operation.
        
        Flow:
            1. Check if any targets were found
            2. Validate the paths against rules
            3. Select appropriate executor strategy (real/dry-run)
            4. Select delete mode (permanent/trash)
            5. Get user confirmation
            6. Execute the deletion
        
        Args:
            path: Original target path.
            paths: List of resolved paths to delete.
            options: Delete operation options.
            
        Returns:
            DeleteResult with operation outcome.
        """
        if len(paths) <= 0:
            return DeleteResult(CommandStatus.NOT_FOUND, paths=[], error_path=path)
        
        violations = self.validator.validate(paths, options)
        if violations:
            return DeleteResult(CommandStatus.INVALID, paths=paths, violations=violations)
        
        delete_executor = self.select_delete_executor(options)
        delete_mode = self.select_delete_mode(options)
        
        if not self.confirm(options, paths):
            return DeleteResult(CommandStatus.CANCELLED, paths=paths)
        
        delete_executor.execute(paths, delete_mode)
        return DeleteResult(CommandStatus.SUCCESS, paths=paths, is_dry_run=options.dry_run)
    
    def select_delete_executor(self, options: DeleteOptions) -> Any:
        """
        Select the appropriate executor based on options.
        
        Args:
            options: Delete operation options.
            
        Returns:
            Either RealDeleteExecutor or DryRunDeleteExecutor.
        """
        delete_executor: Any = RealDeleteExecutor(self.delete_handlers)
        if options.dry_run:
            delete_executor = DryRunDeleteExecutor(self.delete_handlers)
        return delete_executor
    
    def select_delete_mode(self, options: DeleteOptions) -> DeleteMode:
        """
        Select the delete mode based on options.
        
        Args:
            options: Delete operation options.
            
        Returns:
            Either PermanentDeleteMode or TrashDeleteMode.
        """
        delete_mode: DeleteMode = PermanentDeleteMode()
        if not options.final_delete:
            delete_mode = self.trash_delete_mode
        return delete_mode
    
    def confirm(self, options: DeleteOptions, paths: List[str]) -> bool:
        """
        Get user confirmation for the delete operation.
        
        Args:
            options: Delete operation options.
            paths: List of paths to be deleted.
            
        Returns:
            True if confirmed, False if cancelled.
        """
        confirm: ConfirmationPolicy = RequiredConfirmationPolicy()
        if options.force:
            confirm = SkippedConfirmationPolicy()
        return confirm.confirm(paths, options, self.preview_formatter)
