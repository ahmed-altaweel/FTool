from dataclasses import dataclass

from Application.Common.BaseCommandOptions import BaseCommandOptions
from Application.Common.Request import CommandRequest


@dataclass
# Architecture: Delete command options value object.
# Layer: Application.Delete.
# Role: Captures deletion, traversal, confirmation, output, and simulation flags.
# Contract: BaseCommandOptions.
class DeleteOptions(BaseCommandOptions):
    final_delete: bool = False
    recursive_search: bool = False
    delete_folder: bool = False
    force: bool = False
    dry_run: bool = False
    exclude: list[str] | None = None


@dataclass
# Architecture: Delete request payload value object.
# Layer: Application.Delete.
# Role: Couples the target path with DeleteOptions.
class DeleteRequestArgs:
    path: str
    options: DeleteOptions


# Architecture: Delete command request envelope.
# Layer: Application.Delete.
# Role: Carries DeleteRequestArgs through the common request contract.
# Contract: CommandRequest[DeleteRequestArgs].
class DeleteRequest(CommandRequest[DeleteRequestArgs]):
    pass


