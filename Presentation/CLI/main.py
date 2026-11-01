
from Application.Create.CreateBuilders.CreateModuleBuilder import CreateModuleBuilder
from Application.Move.MoveModuleBuilder import MoveModuleBuilder
from Bootstrap.ModulesBuilder.DeleteModuleBuilder import DeleteModuleBuilder

import sys

from Application.Common.Result import CommandResult

from Application.Presenters.ResultFormatter import ResultFormatter
from Bootstrap.ApplicationBuilder import ApplicationBuilder
from Bootstrap.ModulesBuilder.ArchiveModuleBuilder import ArchiveModuleBuilder
from Bootstrap.ModulesBuilder.DeleteModuleBuilder import DeleteModuleBuilder
from Bootstrap.ParserBuilder import ParserBuilder
from Presentation.CLI.Parsers.CreateParser import CreateParserBuilder

from Presentation.CLI.Parsers.ArchiveParser import ArchiveParserBuilder, ExtractParserBuilder

from Presentation.CLI.Parsers.DeleteParser import DeleteParserBuilder
from Presentation.CLI.Parsers.MoveParserBuilder import MoveParserBuilder
from Presentation.CLI.Request.RequestFactory import RequestFactory

from Application.Common.Result import CommandResult
from Bootstrap.ModulesBuilder.CopyModuleBuilder import CopyModuleBuilder 
from Presentation.CLI.Parsers.CopyParser import CopyParserBuilder  

from Bootstrap.ModulesBuilder.RestoreModuleBuilder import RestoreModuleBuilder
from Presentation.CLI.Parsers.RestoreParser import RestoreParserBuilder

def main(argv: list[str] | None = None) -> int:
    parser = (
        ParserBuilder()
        .add(DeleteParserBuilder)
        .add(ArchiveParserBuilder)
        .add(ExtractParserBuilder)
        .add(MoveParserBuilder)
        .add(CopyParserBuilder)
        .add(CreateParserBuilder)
        .add(RestoreParserBuilder())
        .build()
    )
    
    request_factory = RequestFactory()
    formatters: dict[type[CommandResult], ResultFormatter] = {}
    application = (
        ApplicationBuilder(request_factory, formatters)
        .add_command(DeleteModuleBuilder())

        .add_command(CopyModuleBuilder())  
        .add_command(CreateModuleBuilder())
        .add_command(MoveModuleBuilder())
        .add_command(RestoreModuleBuilder())
        .add_command(ArchiveModuleBuilder())
        .build()
    )


   


    application.run(parser.parse_args())







if __name__ == "__main__":
    sys.exit(main())

