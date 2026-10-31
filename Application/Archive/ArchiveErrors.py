# Architecture: Archive error types.
# Layer: Application.Archive.
# Role: Engines translate library-specific failures into these so Application stays library-free.
class ArchiveError(Exception):
    """Base error for archive operations."""


class CorruptedArchiveError(ArchiveError):
    """The archive cannot be read (damaged or truncated)."""


class EngineUnavailableError(ArchiveError):
    """The required external program/library is missing."""
