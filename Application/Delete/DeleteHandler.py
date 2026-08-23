from Application.Common.Handler import CommandHandler
from Application.Common.TargetResolverPort import TargetResolverPort
from Application.Delete.DeleteExecutor import DeleteExecutor
from Application.Delete.DeleteRequest import DeleteRequest
from Application.Delete.DeleteResult import DeleteResult
from Infrastructure.FileSystem.Reolver.TargetResolver import TargetResolver


# Architecture: Delete command handler.
# Layer: Application.Delete.
# Role: Translates DeleteRequest into resolved targets and delegates execution.
# Contract: CommandHandler[DeleteRequest, DeleteResult].
class DeleteHandler(CommandHandler[DeleteRequest, DeleteResult]):
    def __init__(self, target_resolver: TargetResolverPort, executor: DeleteExecutor) -> None:
        self.target_resolver: TargetResolver = target_resolver
        self.executor: DeleteExecutor = executor

    def execute(self, request: DeleteRequest) -> DeleteResult:
        request_args = request.request
        target_solver = self.target_resolver.resolve(
            request_args.path,
            request_args.options.recursive_search,
        )
        return self.executor.execute(
            request_args.path,
            target_solver,
            request_args.options,
        )

