from Application.Common.Dispatcher import Dispatcher
from Application.Common.ModuleBuilder import ModuleBuilder
from Application.Common.Result import CommandResult
from Application.Create.CreateExecutor import CreateExecutor
from Application.Create.CreateHandler import CreateHandler
from Application.Create.CreateRequest import CreateRequest
from Application.Create.CreateResult import CreateResult
from Application.Create.CreateValidator import CreateValidator
from Application.Presenters.ResultFormatter import ResultFormatter
from Infrastructure.FileSystem.FileInspector.OsFileSystemInspector import (
    OsFileSystemInspector,
)
from Infrastructure.FileSystem.TargetHandler.FileTargetCreateHandler import (
    FileTargetCreateHandler,
)
from Infrastructure.FileSystem.TargetHandler.FolderTargetCreateHandler import (
    FolderTargetCreateHandler,
)
from Presentation.CLI.Formatters.CreateResultFormatter import CreateResultFormatter
from Presentation.CLI.Request.RequestCreator.CreateRequestCreator import (
    CreateRequestCreator,
)
from Presentation.CLI.Request.RequestFactory import RequestFactory


# Architecture: Create-module composition root.
# Layer: Application.Create.
# Role: Wires existing contracts to concrete infrastructure implementations and registers the module.
class CreateModuleBuilder(ModuleBuilder):
    def build(
        self,
        dispatcher: Dispatcher,
        request_factory: RequestFactory,
        formatters: dict[type[CommandResult], ResultFormatter],
    ) -> None:
        fs_inspector = OsFileSystemInspector()
        file_handler = FileTargetCreateHandler()
        folder_handler = FolderTargetCreateHandler()
        validator = CreateValidator(fs_inspector)
        executor = CreateExecutor(file_handler, folder_handler, validator)
        handler = CreateHandler(executor)

        dispatcher.register(CreateRequest, handler)
        request_factory.register("create", CreateRequestCreator())
        formatters[CreateResult] = CreateResultFormatter()