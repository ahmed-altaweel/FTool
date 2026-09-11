import argparse

from Application.Delete.DeleteRequest import DeleteOptions, DeleteRequestArgs, DeleteRequest
from Presentation.CLI.Request.RequestCreator.base import RequestCreator
from Application.Common.Request import CommandRequest
# Architecture: CLI request translation adapter.
# Layer: Presentation.CLI.
# Role: Converts argparse.Namespace into the DeleteRequest payload.
# Contract: RequestCreator.
class DeleteRequestCreator(RequestCreator):
 def create(self, argv: argparse.Namespace) -> DeleteRequest:
        options = DeleteOptions(
            final_delete=argv.final_delete,
            recursive_search=argv.recursive_search,
            delete_folder=argv.delete_folder,
            force=argv.force,
            quiet=argv.quiet,
            dry_run=argv.dry_run
            
        )

        args = DeleteRequestArgs(
            path=argv.path,
            options=options
        )
        return DeleteRequest(args)