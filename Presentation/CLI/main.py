from Application.Create.CreateBuilders.CreateModuleBuilder import CreateModuleBuilder
from Application.Move.MoveModuleBuilder import MoveModuleBuilder
from Bootstrap.ModulesBuilder.DeleteModuleBuilder import DeleteModuleBuilder
from Application.Presenters.ResultFormatter import ResultFormatter
from Bootstrap.ApplicationBuilder import ApplicationBuilder
from Bootstrap.ParserBuilder import ParserBuilder
from Presentation.CLI.Parsers.CreateParser import CreateParserBuilder
from Presentation.CLI.Parsers.DeleteParser import DeleteParserBuilder
from Presentation.CLI.Parsers.MoveParserBuilder import MoveParserBuilder
from Presentation.CLI.Request.RequestFactory import RequestFactory
from Application.Common.Result import CommandResult
from Bootstrap.ModulesBuilder.CopyModuleBuilder import CopyModuleBuilder 
from Presentation.CLI.Parsers.CopyParser import CopyParserBuilder  


def main() -> None:
    request_factory = RequestFactory()
    formatters: dict[type[CommandResult], ResultFormatter] = {}
    application = (
        ApplicationBuilder(request_factory, formatters)
        .add_command(DeleteModuleBuilder())
        .add_command(CopyModuleBuilder())  
        .add_command(CreateModuleBuilder())
        .add_command(MoveModuleBuilder())
        .build()
    )

    parser = (ParserBuilder().add(DeleteParserBuilder())
              .add(CopyParserBuilder()).add(MoveParserBuilder())
              .add(CreateParserBuilder()).build()
    )

    application.run(parser.parse_args())


if __name__ == "__main__":
    main()