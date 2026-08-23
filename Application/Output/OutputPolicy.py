from abc import ABC, abstractmethod


# Architecture: Application output policy contract.
# Layer: Application.Output.
# Role: Separates result/error presentation from the concrete output channel.
# Implementations: Terminal output policies.
class OutputPolicy(ABC):
 
    @abstractmethod
    def print_result(self, text: str) -> None:
        ...

    @abstractmethod
    def print_error(self,test:str)->None:
        ...

