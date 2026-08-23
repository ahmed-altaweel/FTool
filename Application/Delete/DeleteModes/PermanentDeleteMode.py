from Application.Delete.DeleteModes.base import DeleteMode
from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler


# Architecture: Permanent-delete mode.
# Layer: Application.Delete.
# Role: Delegates final deletion to the selected target handler.
# Contract: DeleteMode.
class PermanentDeleteMode(DeleteMode):
    def execute(self, path: str, target_handler: TargetDeleteHandler) -> None:
        target_handler.delete(path)
