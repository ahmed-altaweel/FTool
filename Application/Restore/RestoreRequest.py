from dataclasses import dataclass

from Application.Common.BaseCommandOptions import BaseCommandOptions
from Application.Common.Request import CommandRequest


@dataclass
class RestoreOptions(BaseCommandOptions):
    list_only: bool = False
    dry_run: bool = False


@dataclass
class RestoreRequestArgs:
    path: str | None
    options: RestoreOptions


class RestoreRequest(CommandRequest[RestoreRequestArgs]):
    pass