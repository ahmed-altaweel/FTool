import shutil
import os
from pathlib import Path
from Application.Move.MoveResult import MoveResult
from Application.Move.MoveRequest import MoveRequest

class MoveExecutor:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

    def execute(self, request: MoveRequest) -> MoveResult:
        src = request.request.source
        dst = request.request.destination
        options = request.request.options

        # 1. التحقق من وجود المصدر
        if not src.exists():
            return MoveResult(
                status="SOURCE_NOT_FOUND",
                source=src,
                destination=dst,
                message=f"Source not found: {src}"
            )

        # 2. منع النقل إلى نفس المسار أو داخله
        try:
            src_resolved = src.resolve()
            dst_resolved = dst.resolve()
            if src_resolved == dst_resolved:
                return MoveResult(
                    status="SAME_PATH",
                    source=src,
                    destination=dst,
                    message="The file cannot be moved to the same path"
                )
            if src.is_dir() and dst_resolved.is_relative_to(src_resolved):
                return MoveResult(
                    status="SAME_PATH",
                    source=src,
                    destination=dst,
                    message="A folder cannot be moved into itself or into one of its subfolders"
                )
        except Exception:
            return MoveResult(
                status="PERMISSION_DENIED",
                source=src,
                destination=dst,
                message="Unable to verify the path due to permissions or a file system issue"
            )

        # 3. معالجة الوجهة الموجودة
        if dst.exists() and not options.force:
            return MoveResult(
                status="DESTINATION_EXISTS",
                source=src,
                destination=dst,
                message=f"The destination already exists: {dst}. Use --force to replace."
            )

        # 4. المحاكاة (Dry Run)
        if self.dry_run or options.dry_run:
            return MoveResult(
                status="SUCCESS",
                source=src,
                destination=dst,
                message=f"[Simulation] Relocated{src} to {dst} (No actual change occurred)",
                moved_items=[src] if src.is_file() else list(src.rglob("*"))
            )

        # 5. التنفيذ الفعلي
        try:
            if src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            elif src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                return MoveResult(
                    status="FAILED",
                    source=src,
                    destination=dst,
                    message="The source is neither a file nor a known folder"
                )

            if not dst.exists():
                raise Exception("Verification of the destination's existence after copying failed.")

            if src.is_file():
                os.remove(src)
            else:
                shutil.rmtree(src)

            return MoveResult(
                status="SUCCESS",
                source=src,
                destination=dst,
                message=f"Has been moved{src} to {dst} Successfully",
                moved_items=[src]
            )

        except PermissionError as e:
            return MoveResult(
                status="PERMISSION_DENIED",
                source=src,
                destination=dst,
                message=f"Permission error:{e}",
                error_path=src
            )
        except Exception as e:
            return MoveResult(
                status="FAILED",
                source=src,
                destination=dst,
                message=f"Transfer failed: {e}",
                error_path=src
            )