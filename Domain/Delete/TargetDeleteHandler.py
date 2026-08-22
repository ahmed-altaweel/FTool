from abc import ABC,abstractmethod
class TargetDeleteHandler(ABC):
    def __init__(self,trash_folder:str):
        self.trash_folder=trash_folder
    @abstractmethod
    def can_handle(self,path):
        ...
    @abstractmethod
    #final delete
    def delete(self,path):
        ...
    # move the folders or files to trash folder
    @abstractmethod
    def delete_to_trash(self,path):
        ...
    