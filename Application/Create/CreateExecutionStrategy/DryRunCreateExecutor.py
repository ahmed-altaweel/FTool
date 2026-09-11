"""تشغيل تجريبي: يحاكي العملية دون تعديل نظام الملفات."""

from __future__ import annotations

from Application.Common.CommandStatus import CommandStatus  # VERIFY
from Application.Create.CreateResult import CreateResult


class DryRunCreateExecutor:
    def execute(self, request, handler) -> CreateResult:
        kind = "ملف" if request.options.create_file else "مجلد"
        return CreateResult(
            status=CommandStatus.SUCCESS,
            path=request.path,
            dry_run=True,
            reason=f"[محاكاة] سيُنشأ {kind} في: {request.path}",
        )