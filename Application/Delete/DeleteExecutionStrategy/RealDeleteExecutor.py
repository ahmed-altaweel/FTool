from Application.Delete.DeleteExecutionStrategy.base import DeleteExecutorStrategy
class RealDeleteExecutor(DeleteExecutorStrategy):
    def execute(self,paths,delete_type_strategy):  
        for r in paths:
            for strategy in self.delete_strategies:
                if strategy.can_handle(r):
                    delete_type_strategy.execute(r,strategy)
                    break

