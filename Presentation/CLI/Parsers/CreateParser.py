from Presentation.CLI.Parsers.ParserCommandBuilder import Subparsers


# Architecture: CLI parser builder for the create command.
# Layer: Presentation.CLI.Parsers.
# Role: Declares the create subcommand, its positional path, and its flags.
# Contract: ParserCommandBuilder (structural).
class CreateParserBuilder:
    @staticmethod
    def build(commands: Subparsers) -> None:
        parser = commands.add_parser(
            "create",
            help="Create a new file or folder.",
            description=(
                "Create a new empty file or a new folder at the given path. "
                "Exactly one of --file or --folder must be provided."
            ),
        )

        parser.add_argument(
            "path",
            help="Target path to create.",
        )

        kind = parser.add_mutually_exclusive_group(required=True)
        kind.add_argument(
            "--file",
            dest="create_file",
            action="store_true",
            help="Create a new empty file.",
        )
        kind.add_argument(
            "--folder",
            dest="create_folder",
            action="store_true",
            help="Create a new folder.",
        )

        parser.add_argument(
            "--parents",
            dest="parents",
            action="store_true",
            help="Create missing intermediate folders (folder only).",
        )
        parser.add_argument(
            "--force",
            dest="force",
            action="store_true",
            help="Allow replacing an existing element with the same name.",
        )
        parser.add_argument(
            "--dry-run",
            dest="dry_run",
            action="store_true",
            help="Simulate the operation without touching the filesystem.",
        )
        parser.add_argument(
            "-q",
            "--quiet",
            dest="quiet",
            action="store_true",
            help="Suppress success messages.",
        )