
import argparse

from Application.Copy.CopyRequest import CopyOptions, CopyRequestArgs, CopyRequest
from Presentation.CLI.Request.RequestCreator.base import RequestCreator


class CopyRequestCreator(RequestCreator):#CopyRequest الي cli  تحويل البيانات القادمه من 
    # CopyRequest وانشي argv الداله خذ البيانات الموجده في 
    # دالة تغليف 
    def create(self, argv: argparse.Namespace) -> CopyRequest:#الداله ترجع CopyRequest
        options = CopyOptions(
           recursive=argv.recursive,#نسخ المجلدات الفرعية (-r)
            force=argv.force,#النسخ مع التجاوز(-f)
            interactive=getattr(argv, "interactive", False)# argvمن interactive  حاول الحصول على الخاصية 
           , quiet=argv.quiet#وضع التنفيذ الصامت
        )#argparse كائن من مكتبةargv

        args = CopyRequestArgs(
            source=argv.source,
            destination=argv.destination,
            options=options
        )
        return CopyRequest(args)