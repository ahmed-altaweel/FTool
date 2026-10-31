from Presentation.CLI.Parsers.ParserCommandBuilder import Subparsers


# Architecture: CLI archive-command parser builder.
# Layer: Presentation.CLI.
# Role: Defines `ftool archive` and its argparse flags without executing the use case.
class ArchiveParserBuilder:
    @staticmethod
    def build(commands: Subparsers) -> None:
        parser = commands.add_parser("archive", help="Compress files/folders into a ZIP or RAR archive")
        parser.add_argument("sources", nargs="+", help="Files, folders or wildcards (e.g. *.txt) to compress")
        parser.add_argument("-o", "--output", help="Output archive path (default: <name>.zip or archive_<time>.zip)")
        parser.add_argument(
            "-f", "--format", choices=["zip", "rar"], default=None,
            help="Archive format. Default: taken from the --output extension, otherwise zip",
        )
        parser.add_argument(
            "-l", "--level", type=int, default=6, choices=range(0, 10), metavar="0-9",
            help="Compression level: 0 = store only, 9 = maximum (default: 6)",
        )
        parser.add_argument(
            "-e", "--exclude", action="append", default=[], metavar="PATTERN",
            help="Exclude names matching a pattern (e.g. *.tmp, node_modules). Can be repeated",
        )
        parser.add_argument("--force", action="store_true", help="Replace the output archive if it already exists")
        parser.add_argument("-d", "--dry-run", action="store_true", help="Show what would be archived, change nothing")
        parser.add_argument("-q", "--quiet", action="store_true", help="Hide success output (errors stay visible)")


# Architecture: CLI extract-command parser builder.
# Layer: Presentation.CLI.
# Role: Defines `ftool extract` and its argparse flags without executing the use case.
class ExtractParserBuilder:
    @staticmethod
    def build(commands: Subparsers) -> None:
        parser = commands.add_parser("extract", help="Extract a ZIP or RAR archive")
        parser.add_argument("archive", help="Archive file to extract")
        parser.add_argument("-t", "--target", help="Destination folder (default: current folder)")
        parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite existing files")
        parser.add_argument("-s", "--skip", action="store_true", help="Skip files that already exist")
        parser.add_argument("-r", "--rename", action="store_true", help="Keep both: save as name_1.ext, name_2.ext ...")
        parser.add_argument("-l", "--list", dest="list_only", action="store_true", help="List contents only, extract nothing")
        parser.add_argument("-d", "--dry-run", action="store_true", help="Show what would happen, change nothing")
        parser.add_argument("-q", "--quiet", action="store_true", help="Hide success output (errors stay visible)")
