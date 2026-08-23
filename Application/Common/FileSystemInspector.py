from __future__ import annotations

from abc import ABC, abstractmethod


class FileSystemInspector(ABC):
    """
    Abstraction for file system inspection operations.
    
    Responsibility: Provides interface for checking file system properties.
    Layer: Application Core (Common)
    
    This is an Abstraction that allows the application to inspect the file system
    without depending on concrete OS implementations. Enables testing and swapping
    of file system implementations.
    
    Dependencies: None (Base abstraction)
    Used by: Validators, File system operations
    
    Implementations:
        - OsFileSystemInspector: Uses os module for real file system checks
    """
    
    @abstractmethod
    def is_directory(self, path: str) -> bool:
        """
        Check if the given path is a directory.
        
        Args:
            path: The file system path to check.
            
        Returns:
            True if the path is a directory, False otherwise.
        """
        ...