"""
main.py - ftool entry point (composition root).

Commands: del, archive (ZIP/RAR), extract (ZIP/RAR).
"""
import sys

from Application.Common.Result import CommandResult
from Application.Presenters.ResultFormatter import ResultFormatter
from Bootstrap.ApplicationBuilder import ApplicationBuilder
from Bootstrap.ModulesBuilder.ArchiveModuleBuilder import ArchiveModuleBuilder
from Bootstrap.ModulesBuilder.DeleteModuleBuilder import DeleteModuleBuilder
from Bootstrap.ParserBuilder import ParserBuilder
from Presentation.CLI.Parsers.ArchiveParser import ArchiveParserBuilder, ExtractParserBuilder
from Presentation.CLI.Parsers.DeleteParser import DeleteParserBuilder
from Presentation.CLI.Request.RequestFactory import RequestFactory


def main(argv: list[str] | None = None) -> int:
    parser = (
        ParserBuilder()
        .add(DeleteParserBuilder)
        .add(ArchiveParserBuilder)
        .add(ExtractParserBuilder)
        .build()
    )

    request_factory = RequestFactory()
    formatters: dict[type[CommandResult], ResultFormatter] = {}
    application = (
        ApplicationBuilder(request_factory, formatters)
        .add_command(DeleteModuleBuilder())
        .add_command(ArchiveModuleBuilder())
        .build()
    )
    return application.run(parser.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
