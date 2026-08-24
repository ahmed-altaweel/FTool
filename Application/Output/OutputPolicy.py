from abc import ABC, abstractmethod

from Infrastructure.Terminal.IOStream import IOStream


# Architecture: Application output policy contract.
# Layer: Application.Output.
# Role: Separates result/error presentation from the concrete output channel.
# Implementations: Terminal output policies.
class OutputPolicy(ABC):
    def __init__(self,io_stream:IOStream):
        self.io_stream=io_stream
 
    @abstractmethod
    def print_result(self, text: str) -> None:
        ...

    @abstractmethod
    def print_error(self,test:str)->None:
        ...

