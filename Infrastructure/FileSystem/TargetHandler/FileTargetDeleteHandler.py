
import os,shutil
from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler
class FileTargetDeleteHandler(TargetDeleteHandler):
    def can_handle(self, path):
        return os.path.isfile(path)
    def delete(self,path):
        return os.remove(path)
    def delete_to_trash(self,path):
        destination=os.path.join(self.trash_folder,os.path.basename(path))
        shutil.move(path,destination)
        return destination