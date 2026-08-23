from Application.Common.Dispatcher import Dispatcher
from Application.Delete.DeleteExecutor import DeleteExecutor
from Application.Delete.DeleteHandler import DeleteHandler
from Application.Delete.DeleteModes.PermanentDeleteMode import PermanentDeleteMode
from Application.Delete.DeleteModes.TrashDeleteMode import TrashDeleteMode
from Application.Delete.DeleteRequest import DeleteRequest
from Application.Delete.DeleteResult import CommandResult, DeleteResult
from Application.Delete.DeleteValidator import DeleteValidator
from Application.Presenters.ResultFormatter import ResultFormatter
from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler
from Infrastructure.FileSystem.FileInspector.OsFileSystemInspector import OsFileSystemInspector
from Infrastructure.FileSystem.Reolver.PatternResolver import PatternResolver
from Infrastructure.FileSystem.Reolver.TargetResolver import TargetResolver
from Infrastructure.FileSystem.TargetHandler.FileTargetDeleteHandler import FileTargetDeleteHandler
from Infrastructure.FileSystem.TargetHandler.FolderTargetDeleteHandler import FolderTargetDeleteHandler
from Infrastructure.Terminal.Confirmation.RequiredConfirmationPolicy import RequiredConfirmationPolicy
from Infrastructure.Terminal.Confirmation.SkippedConfirmationPolicy import SkippedConfirmationPolicy
from Infrastructure.Trash.JsonTrashRegistry import JsonTrashRegistry
from Presentation.CLI.Formatters.DeletePreviewFormatter import DeletePreviewFormatter
from Presentation.CLI.Formatters.DeleteResultFormatter import DeleteResultFormatter
from Presentation.CLI.Request.RequestFactory import RequestFactory
from Presentation.CLI.Request.RequestCreator.DeleteRequestCreator import DeleteRequestCreator
from Application.Common.ModuleBuilder import ModuleBuilder


# Architecture: Delete-module composition root.
# Layer: Application.Delete.
# Role: Wires existing contracts to concrete infrastructure implementations and registers the module.
class DeleteModuleBuilder(ModuleBuilder):
    def build(
        self,
        dispatcher: Dispatcher,
        request_factory: RequestFactory,
        formatters: dict[type[CommandResult], ResultFormatter],
    ) -> None:
        target_handlers: list[TargetDeleteHandler] = [
            FileTargetDeleteHandler("C:\\trash"),
            FolderTargetDeleteHandler("C:\\trash"),
        ]
        target_resolver = TargetResolver(PatternResolver())
        preview_formatter = DeletePreviewFormatter()
        fs_inspector = OsFileSystemInspector()
        json_trash_registry = JsonTrashRegistry(
            "C:\\trash_registry\\trash_registry.json"
        )
        trash_mode = TrashDeleteMode(json_trash_registry)
        validator = DeleteValidator(fs_inspector)
        delete_executor = DeleteExecutor(
            target_handlers,
            preview_formatter,
            validator,
            trash_mode,
            PermanentDeleteMode(),
            RequiredConfirmationPolicy(),
            SkippedConfirmationPolicy()
        )
        handler = DeleteHandler(target_resolver, delete_executor)
        dispatcher.register(DeleteRequest, handler)
        request_factory.register("del", DeleteRequestCreator())
        formatters[DeleteResult] = DeleteResultFormatter()
