from Application.Common.Handler import CommandHandler
from Application.Move.MoveRequest import MoveRequest
from Application.Move.MoveExecutor import MoveExecutor
from Application.Move.MoveResult import MoveResult

class MoveHandler(CommandHandler):
    def execute(self, request: MoveRequest) -> MoveResult:
        executor = MoveExecutor(dry_run=request.request.options.dry_run)
        return executor.execute(request)