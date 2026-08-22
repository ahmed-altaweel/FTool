from abc import ABC,abstractmethod
class ConfirmationPolicy(ABC):
    @abstractmethod
    def confirm(self,text,paths):
        pass