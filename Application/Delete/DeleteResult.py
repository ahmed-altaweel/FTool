from dataclasses import dataclass, field

from Application.Common.CommandStatus import CommandStatus
from Application.Delete.DeleteValidator import DeleteValidationError
from Application.Common.Result import CommandResult


@dataclass
# Architecture: Delete use-case result DTO.
# Layer: Application.Delete.
# Role: Carries command status, affected paths, validation violations, and simulation metadata to presentation.
class DeleteResult(CommandResult):
    paths: list[str] = field(default_factory=list)
    violations: list[DeleteValidationError] = field(default_factory=list)
    is_dry_run: bool = False
    error_path: str | None = None
