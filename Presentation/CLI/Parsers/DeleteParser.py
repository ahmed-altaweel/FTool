class DeleteParserBuilder:
    @staticmethod
    def build(commands):
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
