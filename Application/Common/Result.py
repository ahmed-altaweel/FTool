from dataclasses import dataclass

from Application.Common.CommandStatus import CommandStatus

@dataclass
class CommandResult:
    status:CommandStatus
