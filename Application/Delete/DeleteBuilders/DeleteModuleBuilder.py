from Application.Delete.DeleteModes.TrashDeleteMode import TrashDeleteMode
from Application.Delete.DeleteResult import DeleteResult
from Application.Delete.DeleteValidator import DeleteValidator
from Infrastructure.FileSystem.FileInspector.OsFileSystemInspector import OsFileSystemInspector
from Infrastructure.FileSystem.TargetHandler.FileTargetDeleteHandler import FileTargetDeleteHandler
from Infrastructure.FileSystem.TargetHandler.FolderTargetDeleteHandler import FolderTargetDeleteHandler
from Application.Delete.DeleteExecutor import DeleteExecutor
from Application.Delete.DeleteHandler import DeleteHandler
from Application.Delete.DeleteRequest import DeleteRequest
from Infrastructure.FileSystem.Reolver.TargetResolver import TargetResolver
from Infrastructure.FileSystem.Reolver.PatternResolver import PatternResolver
from Infrastructure.Trash.JsonTrashRegistry import JsonTrashRegistry
from Presentation.CLI.Formatters.DeletePreviewFormatter import DeletePreviewFormatter
from Presentation.CLI.Formatters.DeleteResultFormatter import DeleteResultFormatter
from Presentation.CLI.Request.RequestCreator.DeleteRequestCreator import DeleteRequestCreator
class DeleteModuleBuilder:
    
    def build(self,dispatcher,request_factory,formatters):
        targets_handlers=[
            FileTargetDeleteHandler("C:\\trash"),
            FolderTargetDeleteHandler("C:\\trash")
        ]
        target_resolver=TargetResolver(PatternResolver())
        preview_formatter=DeletePreviewFormatter()
        fs_inspector=OsFileSystemInspector()
        json_trash_registry=JsonTrashRegistry("C:\\trash_registry\\trash_registry.json")
        trash_mode=TrashDeleteMode(json_trash_registry)
        validator=DeleteValidator(fs_inspector)
        delete_executor=DeleteExecutor(targets_handlers,preview_formatter,validator,trash_mode)
        handler=DeleteHandler(target_resolver,delete_executor)
        dispatcher.register(DeleteRequest,handler)
        request_factory.register("del",DeleteRequestCreator().create)
        formatters[DeleteResult]=DeleteResultFormatter()