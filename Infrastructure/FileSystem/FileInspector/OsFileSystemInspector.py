
import os

from Application.Common.FileSystemInspector import FileSystemInspector


class OsFileSystemInspector(FileSystemInspector):
    def is_directory(slef,path)->bool:
        return os.path.isdir(path)
