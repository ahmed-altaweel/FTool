from __future__ import annotations

from typing import Protocol

from Application.Application import Application
from Application.Common.Dispatcher import Dispatcher
from Application.Delete.DeleteResult import DeleteResult
from Application.Presenters.ResultFormatter import ResultFormatter
from Infrastructure.Terminal.IOStream import IOStream
from Infrastructure.Terminal.Output.NormalOutputPolicy import NormalOutputPolicy
from Infrastructure.Terminal.Output.QuietOutputPolicy import QuietOutputPolicy
from Infrastructure.Terminal.Output.TerminalOutputPolicyResolver import TerminalOutputPolicyResolver
from Presentation.CLI.Presenters.CliResultPresenter import CliResultPresenter
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

    def build(self) -> Application:
        presenter = CliResultPresenter(self.formatters)
        io_stream=IOStream()
        output_resolver = TerminalOutputPolicyResolver(
        normal=NormalOutputPolicy(io_stream),
        quiet=QuietOutputPolicy(io_stream),
    )
        return  Application(
        self.dispatcher,
        self.request_factory,
        presenter,
        output_resolver,
    )
