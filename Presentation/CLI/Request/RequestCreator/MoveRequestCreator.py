from pathlib import Path
from argparse import Namespace
from Application.Move.MoveRequest import MoveRequest, MoveRequestArgs, MoveOptions
from Presentation.CLI.Request.RequestCreator.base import RequestCreator

class MoveRequestCreator(RequestCreator):
    def create(self, argv: Namespace) -> MoveRequest:
        # 1. استخراج الخيارات
        options = MoveOptions(
            dry_run=argv.dry_run,
            force=argv.force,
            quiet=argv.quiet
        )
        
        # 2. استخراج المسارات (تحويلها إلى كائنات Path)
        source = Path(argv.source)
        destination = Path(argv.destination)
        
        # 3. بناء الوسائط
        args = MoveRequestArgs(
            source=source,
            destination=destination,
            options=options
        )
        
        # 4. إرجاع الطلب النهائي
        return MoveRequest(request=args)
    