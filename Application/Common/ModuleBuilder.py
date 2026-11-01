from abc import ABC, abstractmethod

from Application.Common.Dispatcher import Dispatcher
from Application.Common.Result import CommandResult
from Application.Presenters.ResultFormatter import ResultFormatter
from Presentation.CLI.Request.RequestFactory import RequestFactory


# Architecture: Command-module composition contract.
# Layer: Application.Common.
# Role: Lets each command module register its handler, request creator and formatter.
# Implementations: DeleteModuleBuilder, ArchiveModuleBuilder.
class ModuleBuilder(ABC):
    @abstractmethod
    def build(
        self,
        dispatcher: Dispatcher,
        request_factory: RequestFactory,
        formatters: dict[type[CommandResult], ResultFormatter],
    ) -> None:
        ...
