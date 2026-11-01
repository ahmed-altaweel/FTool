from dataclasses import dataclass, field
from pathlib import Path

from Application.Archive.ArchiveEntry import ArchiveEntry
from Application.Common.Result import CommandResult


@dataclass
# Architecture: Validation failure DTO.
# Layer: Application.Archive.
# Role: Describes why an archive/extract request was rejected.
class ArchiveViolation:
    reason: str
    paths: list[Path] = field(default_factory=list)
    detail: str = ""


@dataclass
# Architecture: Archive use-case result DTO.
# Layer: Application.Archive.
# Role: Carries status, sizes, counts, violations and dry-run preview to presentation.
class ArchiveResult(CommandResult):
    output_path: str | None = None
    sources_count: int = 0
    files_count: int = 0
    folders_count: int = 0
    original_size: int = 0
    compressed_size: int = 0
    excluded_count: int = 0
    is_dry_run: bool = False
    preview: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    violations: list[ArchiveViolation] = field(default_factory=list)
    error_paths: list[str] = field(default_factory=list)
    message: str = ""


@dataclass
# Architecture: Extract use-case result DTO.
# Layer: Application.Archive.
# Role: Carries status, counters, notes/errors and listing entries to presentation.
class ExtractResult(CommandResult):
    target_path: str | None = None
    files_extracted: int = 0
    folders_created: int = 0
    skipped: int = 0
    is_dry_run: bool = False
    is_list_only: bool = False
    entries: list[ArchiveEntry] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    violations: list[ArchiveViolation] = field(default_factory=list)
    message: str = ""
