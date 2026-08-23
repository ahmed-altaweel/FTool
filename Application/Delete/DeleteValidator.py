from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List


@dataclass
class DeleteValidationError:
    """
    Error object representing a validation failure.
    
    Responsibility: Encapsulates information about why a delete operation failed validation.
    Layer: Application - Delete Module
    
    This is a Value Object used to communicate validation errors.
    
    Attributes:
        reason: Error code/reason for the validation failure
        paths: List of paths that failed validation
    
    Used by: DeleteValidator, DeleteResult, Formatters
    """
    reason: str
    paths: List[str]


class DeleteValidator:
    """
    Validator for delete operations.
    
    Responsibility: Validates delete requests against business rules.
    Layer: Application - Delete Module
    
    This is a Validator Service that enforces delete operation constraints.
    Currently validates that folders cannot be deleted without explicit permission.
    
    Dependencies:
        - fs_inspector: FileSystemInspector for checking path types
    
    Used by: DeleteExecutor
    """
    
    def __init__(self, fs_inspector: Any) -> None:
        """
        Initialize the validator.
        
        Args:
            fs_inspector: Service for inspecting file system properties.
        """
        self.fs_inspector: Any = fs_inspector
    
    def validate(self, paths: List[str], options: Any) -> List[DeleteValidationError]:
        """
        Validate delete operation paths.
        
        Validation Rules:
            - If delete_folder option is True, all paths are valid
            - Otherwise, folder paths are rejected
        
        Args:
            paths: List of paths to validate.
            options: Delete options containing delete_folder flag.
            
        Returns:
            List of validation errors (empty if all paths are valid).
        """
        if options.delete_folder:
            return []
        
        folder_paths = [p for p in paths if self.fs_inspector.is_directory(p)]
        if not folder_paths:
            return []
        
        return [DeleteValidationError(reason="FOLDER_NOT_ALLOWED", paths=folder_paths)]
