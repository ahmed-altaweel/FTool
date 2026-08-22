from abc import ABC,abstractmethod
class CommandHandler(ABC):
    def __init__(self,executor):
        self.executor=executor
    @abstractmethod
    def execute(self,request):
        pass
    