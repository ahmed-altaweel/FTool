from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BaseCommandOptions:
    """
    Base class for all command options in the application.
    
    Responsibility: Provides common options shared across all commands.
    Layer: Application Core (Common)
    
    This is a Data Class that serves as a base for command-specific options.
    Uses the dataclass decorator for automatic __init__ generation.
    
    Attributes:
        quiet: If True, suppresses output messages.
    
    Used by: All command option classes as a base class.
    """
    quiet: bool = False
