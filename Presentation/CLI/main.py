from Application.Application import Application
from Application.Delete.DeleteBuilders.DeleteModuleBuilder import DeleteModuleBuilder
from Application.Delete.DeleteResult import DeleteResult
from Application.Presenters.ResultFormatter import ResultFormatter
from Bootsrap.ApplicationBuilder import ApplicationBuilder
from Bootsrap.ParserBuilder import ParserBuilder
from Infrastructure.Terminal.Output.NormalOutputPolicy import NormalOutputPolicy
from Infrastructure.Terminal.Output.QuietOutputPolicy import QuietOutputPolicy
from Infrastructure.Terminal.Output.TerminalOutputPolicyResolver import TerminalOutputPolicyResolver
from Presentation.CLI.Parsers.DeleteParser import DeleteParserBuilder
from Presentation.CLI.Presenters.CliResultPresenter import CliResultPresenter
from Presentation.CLI.Request.RequestFactory import RequestFactory
from Application.Common.Result import CommandResult


def main() -> None:
    request_factory = RequestFactory()
    formatters: dict[type[CommandResult], ResultFormatter] = {}
    dispatcher = (
        ApplicationBuilder(request_factory, formatters)
        .add_command(DeleteModuleBuilder())
        .build()
    )
    parser = ParserBuilder().add(DeleteParserBuilder).build()

    presenter = CliResultPresenter(formatters)
    output_resolver = TerminalOutputPolicyResolver(
        normal=NormalOutputPolicy(),
        quiet=QuietOutputPolicy(),
    )

    application = Application(
        dispatcher,
        request_factory,
        presenter,
        output_resolver,
    )
    application.run(parser.parse_args())


if __name__ == "__main__":
    main()
