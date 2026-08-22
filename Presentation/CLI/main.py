from Bootsrap.ApplicationBuilder import ApplicationBuilder
from Bootsrap.ParserBuilder import ParserBuilder
from Application.Application import Application
from Application.Delete.DeleteBuilders.DeleteModuleBuilder import DeleteModuleBuilder
from Infrastructure.Terminal.Output.NormalOutputPolicy import NormalOutputPolicy
from Infrastructure.Terminal.Output.QuietOutputPolicy import QuietOutputPolicy
from Infrastructure.Terminal.Output.TerminalOutputPolicyResolver import TerminalOutputPolicyResolver
from Presentation.CLI.Parsers.DeleteParser import DeleteParserBuilder
from Presentation.CLI.Presenters.CliResultPresenter import CliResultPresenter
from Presentation.CLI.Request.RequestCreator.base import RequestCreator
from Presentation.CLI.Request.RequestFactory import RequestFactory
from Application.Common.Dispatcher import Dispatcher
from Presentation.CLI.Request.RequestCreator.DeleteRequestCreator import DeleteRequestCreator

def main():
    dispatcher=Dispatcher()
    request_factory=RequestFactory()
    formatters={}
    parser=(
        ParserBuilder()
        .add(DeleteParserBuilder)
        .build()
    )

    DeleteModuleBuilder().build(dispatcher,request_factory,formatters)
    presenter=CliResultPresenter(formatters)
    output_resolver=TerminalOutputPolicyResolver(
        normal=NormalOutputPolicy(),
        quiet=QuietOutputPolicy(),
    )

    application=Application(dispatcher,request_factory,presenter,output_resolver)
    args=parser.parse_args()
    application.run(args)


if __name__ == "__main__":
    main()