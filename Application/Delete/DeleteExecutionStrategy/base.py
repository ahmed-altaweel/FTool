from abc import ABC,abstractmethod
class DeleteExecutorStrategy(ABC):
    def __init__(self,delete_strategies):
        self.delete_strategies=delete_strategies
    @abstractmethod
    def execute(self,paths,delete_type_strategy):
       pass