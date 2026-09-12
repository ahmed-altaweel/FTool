import argparse

class MoveParserBuilder:
    @staticmethod
    def build(subparsers: argparse._SubParsersAction):
        # تعريف الأمر "move"
        parser = subparsers.add_parser(
            "move",
            help="Move a file or folder from the source path to the destination path"
        )
        
        # الوسائط الموضعية (المطلوبة)
        parser.add_argument("source", type=str, help="Source Path")
        parser.add_argument("destination", type=str, help="Destination Path")
        
        # الخيارات الاختيارية (Flags)
        parser.add_argument(
            "--dry-run", "-d",
            action="store_true",
            dest="dry_run",
            help="Simulating the process only, without actual execution"
        )
        parser.add_argument(
            "--force", "-f",
            action="store_true",
            dest="force",
            help="Skip confirmation and replace existing files at the destination"
        )
        parser.add_argument(
            "--quiet", "-q",
            action="store_true",
            dest="quiet",
            help="Suppress success messages (error messages remain visible)"
        )
