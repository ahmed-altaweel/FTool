from pathlib import Path

from Application.Delete.DeleteExecutionStrategy.base import DeleteExecutorStrategy
from Application.Delete.DeleteModes.base import DeleteMode


# Architecture: No-op execution strategy.
# Layer: Application.Delete.
# Role: Traverses eligible targets without invoking a delete mode.
# Contract: DeleteExecutorStrategy.
class DryRunDeleteExecutor(DeleteExecutorStrategy):
    def execute(self, paths: list[Path], delete_mode: DeleteMode) -> None:
        for path in paths:
            for handler in self.delete_handlers:
                if handler.can_handle(path):
                    break

