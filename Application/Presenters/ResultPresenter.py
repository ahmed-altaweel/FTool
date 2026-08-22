from abc import ABC,abstractmethod
class ResultPresenter(ABC):
    @abstractmethod
    def present(self,result)->str:
        pass