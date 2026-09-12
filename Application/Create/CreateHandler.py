from pathlib import Path

from Application.Create.CreateExecutor import CreateExecutor
from Application.Create.CreateRequest import CreateRequest
from Application.Create.CreateResult import CreateResult


# Architecture: Create command handler.
# Layer: Application.Create.
# Role: Unpacks CreateRequest, invokes CreateExecutor, returns CreateResult.
class CreateHandler:
    def __init__(self, executor: CreateExecutor) -> None:
        self._executor = executor

    def execute(self, request: CreateRequest) -> CreateResult:
        payload = request.request
        path = Path(payload.path)
        return self._executor.execute(path, payload.options)