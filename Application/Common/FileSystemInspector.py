from abc import ABC,abstractmethod


class FileSystemInspector(ABC):
    @abstractmethod
    def is_directory(self,path)->bool:
        ...