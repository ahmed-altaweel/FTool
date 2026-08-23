import argparse

from Application.Common.CommandStatus import CommandStatus
from Application.Common.Dispatcher import Dispatcher
from Application.Delete.DeleteRequest import DeleteRequest
from Application.Delete.DeleteResult import DeleteResult
from Application.Output.OutputPolicyResolver import OutputPolicyResolver
from Application.Presenters.ResultPresenter import ResultPresenter
from Presentation.CLI.Request.RequestFactory import RequestFactory


# Architecture: Application orchestration boundary.
# Layer: Application.
# Role: Coordinates request creation, dispatch, presentation, and output policy selection.
class Application:
    def __init__(
        self,
        dispatcher: Dispatcher,
        request_factory: RequestFactory,
        presenter: ResultPresenter,
        output_policy_resolver: OutputPolicyResolver,
    ) -> None:
        self.dispatcher: Dispatcher = dispatcher
        self.request_factory: RequestFactory = request_factory
        self.presenter: ResultPresenter = presenter
        self.output_policy_resolver: OutputPolicyResolver = output_policy_resolver

    def run(self, args: argparse.Namespace) -> None:
        request: DeleteRequest = self.request_factory.create(args)
        result = self.dispatcher.dispatch(request)
        text = self.presenter.present(result)
        quiet = request.request.options.quiet
        output_policy = self.output_policy_resolver.resolve(quiet)
        if result.status == CommandStatus.INVALID:
            output_policy.print_error(text)
        else:
            output_policy.print_result(text)
