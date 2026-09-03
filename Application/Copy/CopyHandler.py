from Application.Common.Handler import CommandHandler
from Application.Copy.CopyExecutor import CopyExecutor
from Application.Copy.CopyRequest import CopyRequest
from Application.Copy.CopyResult import CopyResult


class CopyHandler(CommandHandler[CopyRequest, CopyResult]):

    def __init__(self, executor: CopyExecutor) -> None:
        self.executor = executor

    def execute(self, request: CopyRequest) -> CopyResult:
        request_args = request.request

        return self.executor.execute(
            request_args.source,
            request_args.destination,
            request_args.options,
        )