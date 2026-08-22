import shutil
import os
from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler
class FolderTargetDeleteHandler(TargetDeleteHandler):
    def can_handle(self, path):
        return os.path.isdir(path)
    def delete(self,path):        
        return shutil.rmtree(path)
    def delete_to_trash(self,path):
        destination=os.path.join(self.trash_folder,os.path.basename(path))
        shutil.move(path,destination)
        return destination
