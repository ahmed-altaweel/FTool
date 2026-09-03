import os
import shutil
from Application.Copy.CopyRequest import CopyOptions


class FileTargetCopyHandler:

    def copy_file(self, source: str, destination: str) -> None:
        """نسخ ملف فردي مع حفظ البيانات الوصفية."""
        shutil.copy2(source, destination)

    def copy_directory(
        self, source: str, destination: str, overwrite: bool = False
    ) -> None:
        """نسخ مجلد بكافة محتوياته."""
        shutil.copytree(source, destination, dirs_exist_ok=overwrite)

    def copy(self, source: str, destination: str, options: CopyOptions) -> dict:
        """الدالة الرئيسية للتحقق وتنفيذ عملية النسخ حسب الخيارات."""
        source = os.path.abspath(source)
        destination = os.path.abspath(destination)

        # 1. فحص وجود المصدر
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source not found: '{source}'")

        # 2. منع النسخ داخل نفسه (UC-13)
        if os.path.isdir(source) and destination.startswith(source):
            raise ValueError(
                f"Cannot copy directory'{source}'into a subdirectory of itself '{destination}'!"
            )

        # 3. تحديث مسار الوجهة إذا كانت مجلداً قائماً
        final_dest = destination
        if os.path.isdir(destination):
            final_dest = os.path.join(destination, os.path.basename(source))

        # 4. التأكد من أن المصدر والوجهة ليسا نفس الملف تماماً
        if os.path.exists(final_dest) and os.path.samefile(source, final_dest):
            raise ValueError(
                f"Source and destination are the exact same file : '{source}'"
            )

        # 5. معالجة التعارض والخيارات (-i / -f)
        if os.path.exists(final_dest):
            if options.interactive and not options.force:
                confirm = (
                    input(
                        f"File '{final_dest}' already exists. Overwrite? [y/N]: "
                    )
                    .strip()
                    .lower()
                )
                if confirm != "y":
                    return {
                        "status": "SKIPPED",
                        "message": "Overwrite operation cancelled by user",
                    }

        # 6. التوجيه والدعوة للدوال الخاصة بك بناءً على نوع المصدر والخيار -r
        if os.path.isdir(source):
            if not options.recursive:
                raise IsADirectoryError(
                    f"'{source}'is a directory. Use -r option to copy directories."
                )

            self.copy_directory(
                source, final_dest, overwrite=options.force
            )
            return {"status": "SUCCESS", "destination": final_dest}
        else:
            self.copy_file(source, final_dest)
            return {"status": "SUCCESS", "destination": final_dest}