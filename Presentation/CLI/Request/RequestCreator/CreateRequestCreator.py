import argparse

from Application.Create.CreateRequest import (
    CreateOptions,
    CreateRequest,
    CreateRequestArgs,
)


# Architecture: Create request creator.
# Layer: Presentation.CLI.Request.RequestCreator.
# Role: Converts an argparse Namespace into a typed CreateRequest.
class CreateRequestCreator:
    def create(self, args: argparse.Namespace) -> CreateRequest:
        options = CreateOptions(
            quiet=getattr(args, "quiet", False),
            create_file=getattr(args, "create_file", False),
            create_folder=getattr(args, "create_folder", False),
            parents=getattr(args, "parents", False),
            force=getattr(args, "force", False),
            dry_run=getattr(args, "dry_run", False),
        )
        payload = CreateRequestArgs(path=args.path, options=options)
        return CreateRequest(payload)