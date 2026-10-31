import argparse
from pathlib import Path

from Application.Archive.ArchiveRequest import ArchiveOptions, ArchiveRequest, ArchiveRequestArgs
from Presentation.CLI.Request.RequestCreator.base import RequestCreator

_EXTENSIONS = {".zip": "zip", ".rar": "rar"}


# Architecture: CLI request translation adapter.
# Layer: Presentation.CLI.
# Role: Converts argparse.Namespace into an ArchiveRequest (format: -f > output extension > zip).
# Contract: RequestCreator.
class ArchiveRequestCreator(RequestCreator):
    def create(self, argv: argparse.Namespace) -> ArchiveRequest:
        fmt = argv.format
        if fmt is None and argv.output:
            fmt = _EXTENSIONS.get(Path(argv.output).suffix.lower())
        options = ArchiveOptions(
            format=fmt or "zip",
            level=argv.level,
            exclude=list(argv.exclude or []),
            output=argv.output,
            force=argv.force,
            dry_run=argv.dry_run,
            quiet=argv.quiet,
        )
        return ArchiveRequest(ArchiveRequestArgs(sources=list(argv.sources), options=options))
