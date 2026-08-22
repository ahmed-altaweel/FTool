from abc import ABC,abstractmethod
class RequestCreator(ABC):
   @abstractmethod
   def create(self,argv):
         pass
      