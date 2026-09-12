from Application.Common.ModuleBuilder import ModuleBuilder
from Application.Copy.CopyExecutor import CopyExecutor
from Application.Copy.CopyHandler import CopyHandler
from Application.Copy.CopyRequest import CopyRequest
from Application.Copy.CopyResult import CopyResult
from Infrastructure.FileSystem.TargetHandler.FileTargetCopyHandler import FileTargetCopyHandler
from Presentation.CLI.Formatters.CopyResultFormatter import CopyResultFormatter
from Presentation.CLI.Request.RequestCreator.CopyRequestCreator import CopyRequestCreator


class CopyModuleBuilder(ModuleBuilder):
    """
    مسؤول عن تجميع كافة المكونات والاعتماديات الخاصة بأمر النسخ (ftool copy)
    وتسجيلها في النظام (Dispatcher, RequestFactory, FormatterRegistry).
    """

    def build(self, dispatcher, request_factory, formatters) -> None:
        # 1. إنشاء معالج عمليات النسخ للملفات والمجلدات
        copy_handler = FileTargetCopyHandler()

        # 2. إنشاء المنفذ الرئيسي وتزويده بمعالج النسخ
        executor = CopyExecutor(copy_handler=copy_handler)

        # 3. إنشاء المعالج المسؤول عن استقبال واستدعاء المنفذ
        handler = CopyHandler(executor=executor)

        # 4. ربط وتسجيل المكونات في الموزع والمصانع الرئيسية
        dispatcher.register(CopyRequest, handler)
        request_factory.register("copy", CopyRequestCreator())
        formatters[CopyResult]=CopyResultFormatter()