import fnmatch
import os
from pathlib import Path

from Application.Archive.ArchivePlan import ArchiveItem, ArchivePlan
from Application.Archive.SourceScannerPort import SourceScannerPort


# Architecture: Compression planner.
# Layer: Application.Archive.
# Role: Turns sources + exclusion patterns into the exact list of archive members.
class ArchivePlanner:
    def __init__(self, scanner: SourceScannerPort) -> None:
        self.scanner = scanner

    def plan(self, sources: list[Path], exclude: list[str], output: Path | None) -> ArchivePlan:
        plan = ArchivePlan(sources_count=len(sources))
        seen: set[str] = set()
        output_key = self._key(output) if output else None
        temp_key = self._key(output.with_name(f"{output.stem}.ftool-tmp{output.suffix}")) if output else None

        for source in sources:
            root_name = source.name

            def skip(relative: tuple[str, ...], is_dir: bool, _root: str = root_name) -> bool:
                excluded = self._is_excluded((_root, *relative), exclude)
                if excluded:
                    plan.excluded_count += 1
                return excluded

            for entry in self.scanner.scan(source, skip):
                if entry.skipped_reason:
                    plan.warnings.append(f"Skipped {entry.path}: {entry.skipped_reason}")
                    continue
                if output_key and self._key(entry.path) in (output_key, temp_key):
                    continue  # never put the archive inside itself
                arcname = "/".join((root_name, *entry.relative))
                if arcname in seen:
                    plan.duplicates.append(arcname)
                    continue
                seen.add(arcname)
                plan.items.append(ArchiveItem(entry.path, arcname, entry.is_dir, entry.size))
        return plan

    @staticmethod
    def _key(path: Path) -> str:
        return os.path.normcase(os.path.normpath(os.path.abspath(path)))

    @staticmethod
    def _is_excluded(parts: tuple[str, ...], patterns: list[str]) -> bool:
        joined = "/".join(parts)
        for pattern in patterns:
            pattern = pattern.replace("\\", "/").strip("/")
            if not pattern:
                continue
            if "/" in pattern:
                if fnmatch.fnmatch(joined, pattern) or fnmatch.fnmatch(joined, f"*/{pattern}"):
                    return True
            elif any(fnmatch.fnmatch(part, pattern) for part in parts):
                return True
        return False
