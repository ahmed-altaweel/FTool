from dataclasses import dataclass, field
from typing import Optional

from Application.Common.CommandStatus import CommandStatus
from Application.Delete.DeleteValidator import DeleteValidationError


@dataclass
class DeleteResult:
    status: CommandStatus
    paths: list[str]=field(default_factory=list)
    violations:list[DeleteValidationError]=field(default=list)
    is_dry_run: bool = False
    error_path: Optional[str] = None