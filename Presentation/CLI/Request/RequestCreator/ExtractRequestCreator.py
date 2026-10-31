import argparse

from Application.Archive.ArchiveRequest import ExtractOptions, ExtractRequest, ExtractRequestArgs
from Presentation.CLI.Request.RequestCreator.base import RequestCreator


# Architecture: CLI request translation adapter.
# Layer: Presentation.CLI.
# Role: Converts argparse.Namespace into an ExtractRequest.
# Contract: RequestCreator.
class ExtractRequestCreator(RequestCreator):
    def create(self, argv: argparse.Namespace) -> ExtractRequest:
        options = ExtractOptions(
            target=argv.target,
            overwrite=argv.overwrite,
            skip=argv.skip,
            rename=argv.rename,
            list_only=argv.list_only,
            dry_run=argv.dry_run,
            quiet=argv.quiet,
        )
        return ExtractRequest(ExtractRequestArgs(archive=argv.archive, options=options))
