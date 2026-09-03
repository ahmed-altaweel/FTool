from __future__ import annotations#تاجيل تفسير البيانات

import argparse#المسؤوله عن قراءة وتحليل الاوامر 

from Presentation.CLI.Parsers.ParserCommandBuilder import Subparsers# تعريف نوع البيانات الذي نضيف امر النسخ داخله


class CopyParserBuilder:
    @staticmethod#تجعل الداله سكونية 
    def build(
        commands: Subparsers,
    ) -> None:#تستقبل الاوامر ولاترجع قيمة
        parser = commands.add_parser(
            "copy",
            help="Copy files or directories from source to destination"
        )#با مجرد كتابة الامر النسخ  سوف يبدا بتطبيق الخيارات المحدده اسفلة
        parser.add_argument(
            "-r",
            "--recursive",#نسخ بشكل متكرر
            dest="recursive",
            action="store_true",
            help="Copy directories recursively"
        )
        parser.add_argument(
            "-f",
            "--force",#الكتابة فوق ملفات الوجهة
            action="store_true",
            help="Overwrite destination files without confirmation"
        )
        parser.add_argument(
            "-q",
            "--quiet",#تنفيذ الامر بدون رساله اخراج
            action="store_true",
            help="Copy without output message or status"
        )
        parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Propmt for confirmation before overwriting an existing file"
)
        parser.add_argument(
            "source",
            help="Source file or directory path"
        )
        parser.add_argument(
            "destination",
            help="Destination path"
        )