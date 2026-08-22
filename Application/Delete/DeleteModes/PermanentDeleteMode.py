from Application.Delete.DeleteModes.base import DeleteMode
class PermanentDeleteMode(DeleteMode):
    def execute(self,path,target_handler):
        return target_handler.delete(path)