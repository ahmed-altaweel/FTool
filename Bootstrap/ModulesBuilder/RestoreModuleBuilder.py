from Application.Common.Dispatcher import Dispatcher
from Application.Common.ModuleBuilder import ModuleBuilder
from Application.Common.Result import CommandResult
from Application.Presenters.ResultFormatter import ResultFormatter
from Application.Restore.RestoreHandler import RestoreHandler
from Application.Restore.RestoreRequest import RestoreRequest
from Application.Restore.RestoreResult import RestoreResult
from Infrastructure.Trash.JsonTrashRegistry import JsonTrashRegistry
from Infrastructure.Trash.RestoreFromTrash import RestoreFromTrash
from Infrastructure.Trash.TrashPath import TrashPath
from Presentation.CLI.Formatters.RestoreResultFormatter import RestoreResultFormatter
from Presentation.CLI.Request.RequestCreator.RestoreRequestCreator import RestoreRequestCreator
from Presentation.CLI.Request.RequestFactory import RequestFactory


class RestoreModuleBuilder(ModuleBuilder):
    def build(
        self,
        dispatcher: Dispatcher,
        request_factory: RequestFactory,
        formatters: dict[type[CommandResult], ResultFormatter],
    ) -> None:
        trash_path = TrashPath()
        trash_registry = JsonTrashRegistry(trash_path.trash_registry_path)
        restorer = RestoreFromTrash(trash_path.entries_path)
        handler = RestoreHandler(trash_registry, restorer)
        dispatcher.register(RestoreRequest, handler)
        request_factory.register("restore", RestoreRequestCreator())
        formatters[RestoreResult] = RestoreResultFormatter()