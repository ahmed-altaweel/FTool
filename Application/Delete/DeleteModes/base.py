from abc import ABC,abstractmethod
class DeleteMode(ABC):
    @abstractmethod
    def execute(self,paths,target_handler):
        pass