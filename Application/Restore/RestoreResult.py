from dataclasses import dataclass, field

from Application.Common.Result import CommandResult
from Domain.Trash.TrashEntry import TrashEntry


@dataclass
class RestoreResult(CommandResult):
    entries: list[TrashEntry] = field(default_factory=list)
    restored_path: str | None = None
    error_path: str | None = None
    reason: str | None = None
    is_dry_run: bool = False
    is_listing: bool = False