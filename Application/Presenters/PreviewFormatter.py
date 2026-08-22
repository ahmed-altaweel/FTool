
from abc import ABC,abstractmethod


class PreviewFormatter(ABC):
    @abstractmethod
    def format(self,path,options) ->str:
        pass