from pathlib import Path

from Application.Archive.ArchiveRequest import ExtractRequest
from Application.Archive.ArchiveResult import ExtractResult
from Application.Archive.ExtractExecutor import ExtractExecutor
from Application.Common.Handler import CommandHandler


# Architecture: Extract command handler.
# Layer: Application.Archive.
# Role: Translates ExtractRequest into a path and delegates to the executor.
# Contract: CommandHandler[ExtractRequest, ExtractResult].
class ExtractHandler(CommandHandler[ExtractRequest, ExtractResult]):
    def __init__(self, executor: ExtractExecutor) -> None:
        self.executor = executor

    def execute(self, request: ExtractRequest) -> ExtractResult:
        args = request.request
        return self.executor.execute(Path(args.archive), args.options)
