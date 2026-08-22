from Application.Delete.DeleteExecutionStrategy.base import DeleteExecutorStrategy
class DryRunDeleteExecutor(DeleteExecutorStrategy):
    def execute(self, paths,delete_type_strategy):
          for r in paths:
            for strategy in self.delete_strategies:
                if strategy.can_handle(r):
                    pass

