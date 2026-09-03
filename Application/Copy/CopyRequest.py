from dataclasses import dataclass
from Application.Common.Request import CommandRequest
from Application.Common.BaseCommandOptions import BaseCommandOptions

@dataclass
class CopyOptions(BaseCommandOptions):
    recursive: bool = False
    force: bool = False
    interactive: bool = False
    quiet: bool = False  


@dataclass
class CopyRequestArgs:
    source: str
    destination: str
    options: CopyOptions


class CopyRequest(CommandRequest[CopyRequestArgs]):
    """طلب النسخ الذي يحمل المسارات والخيارات بشكل منظّم."""
    pass#لايوجد شي نريد كتابتة داخل الكلاس