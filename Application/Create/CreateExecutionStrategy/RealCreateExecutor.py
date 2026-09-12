"""تنفيذ فعلي للإنشاء عبر مكيّف الهدف المناسب.

ملاحظة UC-13: سياسة تنظيف الفشل الجزئي غير مفعّلة افتراضيًا، وفق
ما ورد في SRS الحالية (سلوك غير محسوم). تُترك المجلدات الوسيطة
المنشأة إذا فشل العنصر النهائي.
"""

from __future__ import annotations

import os

from Application.Common.CommandStatus import CommandStatus  # VERIFY
from Application.Create.CreateResult import CreateResult


class RealCreateExecutor:
    def execute(self, request, handler) -> CreateResult:
        opts = request.options
        path = request.path

        try:
            handler.create(path, parents=opts.parents)
        except FileExistsError:
            return CreateResult(
                status=CommandStatus.INVALID,
                path=path,
                reason="العنصر موجود مسبقًا.",
            )
        except PermissionError:
            return CreateResult(
                status=CommandStatus.INVALID,
                path=path,
                reason="لا توجد صلاحية للكتابة في المسار.",
            )
        except FileNotFoundError:
            return CreateResult(
                status=CommandStatus.NOT_FOUND,
                path=path,
                reason="المسار الأب غير موجود.",
            )
        except OSError as exc:
            return CreateResult(
                status=CommandStatus.INVALID,
                path=path,
                reason=f"فشل الإنشاء: {exc}",
            )

        return CreateResult(
            status=CommandStatus.SUCCESS,
            path=path,
            dry_run=False,
        )