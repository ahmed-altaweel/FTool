from dataclasses import dataclass
from pathlib import Path

from Application.Common.FileSystemInspector import FileSystemInspector
from Application.Create.CreateRequest import CreateOptions


@dataclass
# Architecture: Validation failure DTO.
# Layer: Application.Create.
# Role: Describes why a create request was rejected.
class CreateValidationError:
    reason: str
    paths: list[Path]


# Architecture: Create-input validation service.
# Layer: Application.Create.
# Role: Applies create policy using the FileSystemInspector contract.
class CreateValidator:
    def __init__(self, fs_inspector: FileSystemInspector) -> None:
        self.fs_inspector: FileSystemInspector = fs_inspector

    def validate(
        self, path: Path, options: CreateOptions
    ) -> list[CreateValidationError]:
        errors: list[CreateValidationError] = []

        # 1) يجب تحديد نوع العنصر (أحدهما فقط)
        if options.create_file == options.create_folder:
            errors.append(
                CreateValidationError(reason="KIND_REQUIRED", paths=[path])
            )
            return errors

        # 2) --parents لا يُستخدم مع الملفات
        if options.create_file and options.parents:
            errors.append(
                CreateValidationError(
                    reason="PARENTS_FILE_NOT_ALLOWED", paths=[path]
                )
            )
            return errors

        # 3) العنصر موجود مسبقًا (ما لم يُطلب --force)
        if not options.force and path.exists():
            errors.append(
                CreateValidationError(reason="ALREADY_EXISTS", paths=[path])
            )
            return errors

        # 4) تحقق من المجلد الأب (إن لم يُطلب --parents)
        if not options.parents:
            parent = path.parent
            if str(parent) not in ("", "."):
                if not parent.exists():
                    errors.append(
                        CreateValidationError(
                            reason="PARENT_NOT_FOUND", paths=[parent]
                        )
                    )
                elif not self.fs_inspector.is_directory(str(parent)):
                    errors.append(
                        CreateValidationError(
                            reason="PARENT_NOT_A_DIRECTORY", paths=[parent]
                        )
                    )

        return errors