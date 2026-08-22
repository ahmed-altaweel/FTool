from abc import ABC, abstractmethod

class ResultFormatter(ABC):
    @abstractmethod
    def format(self, result) -> str:
        pass