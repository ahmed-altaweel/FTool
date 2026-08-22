from abc import ABC, abstractmethod


class OutputPolicy(ABC):
 
    @abstractmethod
    def print_result(self, text: str) -> None:
        ...

    @abstractmethod
    def print_error(self,test:str)->None:
        ...

