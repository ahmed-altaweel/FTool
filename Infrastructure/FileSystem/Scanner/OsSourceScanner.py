import os
from collections.abc import Callable, Iterator
from pathlib import Path

from Application.Archive.SourceScannerPort import ScannedEntry, SourceScannerPort


# Architecture: Operating-system source scanner.
# Layer: Infrastructure.FileSystem.
# Role: Walks files/folders (sorted, no symlink-following) and reports what cannot be archived.
# Contract: SourceScannerPort.
class OsSourceScanner(SourceScannerPort):
    def scan(
        self,
        source: Path,
        skip: Callable[[tuple[str, ...], bool], bool],
    ) -> Iterator[ScannedEntry]:
        is_dir = os.path.isdir(source) and not os.path.islink(source)
        if skip((), is_dir):
            return
        if not is_dir:
            yield self._file_entry(source, ())
            return

        yield ScannedEntry(source, (), True)
        errors: list[OSError] = []
        for dirpath, dirnames, filenames in os.walk(source, onerror=errors.append):
            yield from self._flush(errors)
            base = Path(dirpath)
            relative_dir = self._relative(source, base)
            dirnames.sort()
            filenames.sort()
            kept: list[str] = []
            for name in dirnames:
                child = base / name
                relative = (*relative_dir, name)
                if skip(relative, True):
                    continue
                if os.path.islink(child):
                    yield ScannedEntry(child, relative, True, skipped_reason="folder symlink (not followed)")
                    continue
                kept.append(name)
                yield ScannedEntry(child, relative, True)
            dirnames[:] = kept
            for name in filenames:
                relative = (*relative_dir, name)
                if skip(relative, False):
                    continue
                yield self._file_entry(base / name, relative)
        yield from self._flush(errors)

    @staticmethod
    def _relative(root: Path, current: Path) -> tuple[str, ...]:
        parts = Path(os.path.relpath(current, root)).parts
        return () if parts == (".",) else parts

    @staticmethod
    def _file_entry(path: Path, relative: tuple[str, ...]) -> ScannedEntry:
        try:
            size = os.path.getsize(path)
            if not os.access(path, os.R_OK):
                return ScannedEntry(path, relative, False, skipped_reason="no read permission")
            return ScannedEntry(path, relative, False, size)
        except OSError as error:
            return ScannedEntry(path, relative, False, skipped_reason=error.strerror or "unreadable")

    @staticmethod
    def _flush(errors: list[OSError]) -> Iterator[ScannedEntry]:
        while errors:
            error = errors.pop()
            yield ScannedEntry(
                Path(error.filename or "?"), (), True, skipped_reason=error.strerror or "unreadable folder"
            )
