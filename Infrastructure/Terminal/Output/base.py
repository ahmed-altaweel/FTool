from abc import ABC,abstractmethod
class OutputPolicy(ABC):
    @abstractmethod
    def print_result(self,text):
        pass