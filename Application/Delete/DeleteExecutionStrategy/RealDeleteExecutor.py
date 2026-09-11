from pathlib import Path

from Application.Delete.DeleteExecutionStrategy.base import DeleteExecutorStrategy
from Application.Delete.DeleteModes.base import DeleteMode


# Architecture: Real execution strategy.
# Layer: Application.Delete.
# Role: Selects a target handler and invokes the chosen delete mode for each target.
# Contract: DeleteExecutorStrategy.
class RealDeleteExecutor(DeleteExecutorStrategy):
    def execute(self, paths: list[Path], delete_mode: DeleteMode) -> None:
        for path in paths:
            for handler in self.delete_handlers:
                if handler.can_handle(path):
                    delete_mode.execute(path, handler)
                    break

