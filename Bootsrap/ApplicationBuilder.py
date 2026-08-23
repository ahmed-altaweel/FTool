from __future__ import annotations

from typing import Protocol

from Application.Common.Dispatcher import Dispatcher
from Application.Delete.DeleteResult import DeleteResult
from Application.Presenters.ResultFormatter import ResultFormatter
from Presentation.CLI.Request.RequestFactory import RequestFactory
from Application.Common.ModuleBuilder import ModuleBuilder
from Application.Common.Result import CommandResult




# Architecture: Generic application composition helper.
# Layer: Bootstrap.
# Role: Registers command modules in the Dispatcher and exposes the assembled registry.
class ApplicationBuilder:
    def __init__(
        self,
        request_factory: RequestFactory,
        formatters: dict[type[CommandResult], ResultFormatter],
    ) -> None:
        self.dispatcher = Dispatcher()
        self.request_factory = request_factory
        self.formatters = formatters

    def add_command(self, module: ModuleBuilder) -> ApplicationBuilder:
        module.build(self.dispatcher, self.request_factory, self.formatters)
        return self

    def build(self) -> Dispatcher:
        return self.dispatcher
