import argparse

from Application.Restore.RestoreRequest import RestoreOptions, RestoreRequest, RestoreRequestArgs
from Presentation.CLI.Request.RequestCreator.base import RequestCreator


class RestoreRequestCreator(RequestCreator):
    def create(self, argv: argparse.Namespace) -> RestoreRequest:
        options = RestoreOptions(
            list_only=argv.list_only,
            dry_run=argv.dry_run,
            quiet=argv.quiet,
        )
        return RestoreRequest(RestoreRequestArgs(path=argv.path, options=options))