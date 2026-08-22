from abc import ABC,abstractmethod
class CommandRequest(ABC):
    def __init__(self,request):
        self.request=request 
