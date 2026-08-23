from abc import ABC, abstractmethod

from Application.Common.Dispatcher import Dispatcher
from Application.Delete.DeleteResult import CommandResult, DeleteResult
from Application.Presenters.ResultFormatter import ResultFormatter
from Presentation.CLI.Request.RequestFactory import RequestFactory


class ModuleBuilder(ABC):
    @abstractmethod
    def build(
        self,
        dispatcher: Dispatcher,
        request_factory: RequestFactory,
        formatters: dict[type[CommandResult], ResultFormatter],
    ) -> None:
        ...