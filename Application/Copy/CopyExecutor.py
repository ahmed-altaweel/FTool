import os
from Application.Common.CommandStatus import CommandStatus
from Application.Copy.CopyRequest import CopyOptions
from Application.Copy.CopyResult import CopyResult
from Infrastructure.FileSystem.TargetHandler.FileTargetCopyHandler import (
    FileTargetCopyHandler,
)


class CopyExecutor:

    def __init__(self, copy_handler: FileTargetCopyHandler) -> None:
        self.copy_handler = copy_handler

    def execute(
        self, source: str, destination: str, options: CopyOptions
    ) -> CopyResult:

        result = CopyResult(status=CommandStatus.SUCCESS)
        result.destination_path = destination

        # 1. تحويل المسارات إلى مسارات مطلقة
        source = os.path.abspath(source)
        destination = os.path.abspath(destination)

        # 2. التحقق من وجود المصدر
        if not os.path.exists(source):
            result.status = CommandStatus.NOT_FOUND
            result.error_path = source
            result.violations.append(f"Source Path'{source}' dose not exist .")
            return result

        # 3. منع النسخ داخل المجلد نفسه (UC-13)
        if os.path.isdir(source) and destination.startswith(source):
            result.status = CommandStatus.INVALID
            result.error_path = source
            result.violations.append(
                f"Cannot copy directory'{source}'in to a subdirectory of itself!"
            )
            return result

        # 4. تحديد المسار النهائي للوجهة
        dest_path = destination
        if os.path.isdir(destination):
            dest_path = os.path.join(destination, os.path.basename(source))

        # 5. التأكد من عدم نسخ الملف فوق نفسه
        if os.path.exists(dest_path) and os.path.samefile(source, dest_path):
            result.status = CommandStatus.INVALID
            result.error_path = source
            result.violations.append("Source and destination are the exact same file.")
            return result

        # 6. معالجة التعارض والتأكيد (-i / -f / UC-10 & UC-11)
        if os.path.exists(dest_path):
            if options.interactive and not options.force:
                confirm = (
                    input(
                        f"File '{dest_path}'already exists. Overwrite ؟  [y/N]: "
                    )
                    .strip()
                    .lower()
                )
                if confirm != "y":
                    result.status = CommandStatus.INVALID
                    result.violations.append(
                     "Overwrite operation cancelled by user."
                    )
                    return result

        # 7. التنفيذ حسب نوع المصدر وخيار -r
        try:
            if os.path.isfile(source):
                self.copy_handler.copy_file(source, dest_path)
                result.source_paths.append(source)

            elif os.path.isdir(source):
                # فحص خيار النسخ التكراري -r
                if not options.recursive:
                    result.status = CommandStatus.INVALID
                    result.error_path = source
                    result.violations.append(
                        f"'{source}' is a directory . Use -r option to copy directories."
                    )
                    return result

                self.copy_handler.copy_directory(
                    source, dest_path, overwrite=options.force
                )
                result.source_paths.append(source)

        except Exception as e:
            result.status = CommandStatus.INVALID
            result.error_path = source
            result.violations.append(str(e))

        return result