"""طلب أمر الإنشاء.

يحمل بيانات typed (Options + Args) ولا يعرف argparse.
"""

from __future__ import annotations

from dataclasses import dataclass

from Application.Common.BaseCommandOptions import BaseCommandOptions  # VERIFY
from Application.Common.Request import CommandRequest  # VERIFY


@dataclass
class CreateOptions(BaseCommandOptions):
    """خيارات خاصة بأمر create. لا نعيد استخدام DeleteOptions."""

    # نوع العنصر: أحدهما إلزامي
    create_file: bool = False
    create_folder: bool = False

    # عند إنشاء مجلد: إنشاء المجلدات الوسيطة
    parents: bool = False

    # تجاوز وجود عنصر بنفس الاسم (سلوك افتراضي: رفض)
    force: bool = False

    # تشغيل تجريبي: محاكاة دون تنفيذ
    dry_run: bool = False


@dataclass
class CreateRequestArgs:
    path: str
    options: CreateOptions


class CreateRequest(CommandRequest[CreateRequestArgs]):
    """الطلب الكامل الذي يستقبله CreateHandler."""

    # VERIFY: نتبع نمط DeleteRequest(CommandRequest[DeleteRequestArgs])
    pass