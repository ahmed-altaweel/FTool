from __future__ import annotations

from Presentation.CLI.Parsers.ParserCommandBuilder import Subparsers


class RestoreParserBuilder:
    @staticmethod
    def build(commands: Subparsers) -> None:
        parser = commands.add_parser(
            "restore",
            help="Restore a deleted file or directory from the ftool trash",
        )
        parser.add_argument(
            "path",
            nargs="?",
            help="Original path of the deleted item (the latest deleted version is restored)",
        )
        parser.add_argument(
            "-l", "--list",
            dest="list_only",
            action="store_true",
            help="List the items currently in the trash",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be restored without actually restoring",
        )
        parser.add_argument(
            "-q", "--quiet",
            action="store_true",
            help="Restore without output message or status",
        )