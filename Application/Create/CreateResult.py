from dataclasses import dataclass, field

from Application.Common.CommandStatus import CommandStatus
from Application.Common.Result import CommandResult


@dataclass
# Architecture: Create use-case result DTO.
# Layer: Application.Create.
# Role: Carries command status, affected paths, validation notes, and simulation metadata to presentation.
class CreateResult(CommandResult):
    paths: list[str] = field(default_factory=list)
    violations: list["CreateValidationError"] = field(default_factory=list)
    is_dry_run: bool = False
    error_path: str | None = None