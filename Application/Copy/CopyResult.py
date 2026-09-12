from dataclasses import dataclass, field

from Application.Common.CommandStatus import CommandStatus
from Application.Common.Result import CommandResult
# سنستخدم الكلاس الخاص بأخطاء التحقق للنسخ لاحقاً إذا وجد، أو يمكنك استيراد كلاس الأخطاء العام/الخاص بالنسخ
# from Application.Copy.CopyValidator import CopyValidationError


@dataclass
class CopyResult(CommandResult):
    source_paths: list[str] = field(default_factory=list)#قائمة بامسارات المصدر
    destination_path: str | None = None#مسار الوجهة
    violations: list[str] = field(default_factory=list)#قائمة المشكلات
    is_dry_run: bool = False#dry_run هل العملية     
    error_path: str | None = None#مسار الملف الذي صار عنده حطاء