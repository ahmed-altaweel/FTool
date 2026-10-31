import argparse

from Application.Common.CommandStatus import CommandStatus
from Application.Common.Dispatcher import Dispatcher
from Application.Common.RequestFactoryPrort import RequestFactoryPort
from Application.Output.OutputPolicyResolver import OutputPolicyResolver
from Application.Presenters.ResultPresenter import ResultPresenter


# Architecture: Application orchestration boundary.
# Layer: Application.
# Role: Coordinates request creation, dispatch, presentation, and output policy selection.
class Application:
    EXIT_OK = 0
    EXIT_FAILED = 1
    EXIT_BAD_USAGE = 2

    def __init__(
        self,
        dispatcher: Dispatcher,
        request_factory: RequestFactoryPort,
        presenter: ResultPresenter,
        output_policy_resolver: OutputPolicyResolver,
    ) -> None:
        self.dispatcher: Dispatcher = dispatcher
        self.request_factory: RequestFactoryPort = request_factory
        self.presenter: ResultPresenter = presenter
        self.output_policy_resolver: OutputPolicyResolver = output_policy_resolver

    def run(self, args: argparse.Namespace) -> int:
        """Runs one command and returns a process exit code."""
        try:
            request = self.request_factory.create(args)
        except ValueError as error:
            policy = self.output_policy_resolver.resolve(False)
            policy.print_error(f"Error: {error}\n")
            return self.EXIT_BAD_USAGE

        result = self.dispatcher.dispatch(request)
        text = self.presenter.present(result)
        quiet = request.request.options.quiet
        output_policy = self.output_policy_resolver.resolve(quiet)

        if result.status.is_error:
            output_policy.print_error(text + "\n")
            return self.EXIT_FAILED
        output_policy.print_result(text + "\n")
        if result.status == CommandStatus.CANCELLED:
            return self.EXIT_FAILED
        return self.EXIT_OK
