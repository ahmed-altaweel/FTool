from pathlib import Path

from Application.Archive.ArchivePlan import ArchivePlan
from Application.Archive.ArchiveResult import ArchiveViolation
from Application.Common.FileSystemInspector import FileSystemInspector


# Architecture: Archive/extract input validation service.
# Layer: Application.Archive.
# Role: Produces violations (never raises) so the presenter can explain each rejection.
class ArchiveValidator:
    def __init__(self, fs_inspector: FileSystemInspector) -> None:
        self.fs = fs_inspector

    def validate_sources(self, sources: list[Path]) -> list[ArchiveViolation]:
        unreadable = [s for s in sources if not self.fs.can_read(s)]
        violations: list[ArchiveViolation] = []
        if unreadable:
            violations.append(ArchiveViolation("SOURCE_UNREADABLE", unreadable))
        root_like = [s for s in sources if not s.name]
        if root_like:
            violations.append(ArchiveViolation("SOURCE_HAS_NO_NAME", root_like))
        return violations

    def validate_compress(self, plan: ArchivePlan, output: Path, force: bool) -> list[ArchiveViolation]:
        violations: list[ArchiveViolation] = []
        if plan.duplicates:
            violations.append(ArchiveViolation("DUPLICATE_NAME", detail=", ".join(plan.duplicates)))
        if not plan.items:
            violations.append(ArchiveViolation("NOTHING_TO_ARCHIVE"))
        if self.fs.is_directory(output):
            violations.append(ArchiveViolation("OUTPUT_IS_DIRECTORY", [output]))
        elif self.fs.exists(output) and not force:
            violations.append(ArchiveViolation("OUTPUT_EXISTS", [output]))
        if not self.fs.can_write(output):
            violations.append(ArchiveViolation("OUTPUT_NOT_WRITABLE", [output]))
        return violations

    def validate_extract(self, archive: Path, target: Path, needs_write: bool) -> list[ArchiveViolation]:
        if not self.fs.exists(archive):
            return [ArchiveViolation("ARCHIVE_NOT_FOUND", [archive])]
        if not self.fs.is_file(archive):
            return [ArchiveViolation("NOT_A_FILE", [archive])]
        if not self.fs.can_read(archive):
            return [ArchiveViolation("ARCHIVE_UNREADABLE", [archive])]
        if needs_write:
            if self.fs.exists(target) and not self.fs.is_directory(target):
                return [ArchiveViolation("TARGET_IS_FILE", [target])]
            if not self.fs.can_write(target):
                return [ArchiveViolation("TARGET_NOT_WRITABLE", [target])]
        return []
