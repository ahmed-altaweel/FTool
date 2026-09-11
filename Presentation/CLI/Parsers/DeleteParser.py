from __future__ import annotations

import argparse

from Presentation.CLI.Parsers.ParserCommandBuilder import Subparsers




# Architecture: CLI delete-command parser builder.
# Layer: Presentation.CLI.
# Role: Defines the del command and its argparse flags without executing the use case.
class DeleteParserBuilder:
    @staticmethod
    def build(
        commands: Subparsers,
    ) -> None:
        parser=commands.add_parser(
            "del",
            help="Delete files or directories"
        )
        parser.add_argument(
            "-d",
            "--delete-folder",
            dest="delete_folder",
            action="store_true",
            help="Delete Folder"
        )
        parser.add_argument(
            "-r",
            "--recursive",
            dest="recursive_search",
            action="store_true",
            help="search the file or directories recursively"

        )
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Delete without confimation message"
        )
        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="Delete without output message or status"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be delete without actually deleteing"
        )
        parser.add_argument(
            "--final",
            dest="final_delete",
            action="store_true",
            help="Permanently deleted the target"
        )
        parser.add_argument(
            "path"
        )
