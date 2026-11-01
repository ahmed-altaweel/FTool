import os
import zipfile
from datetime import datetime
from pathlib import Path

from Application.Archive.ArchiveEngine import ArchiveEngine, ArchiveReader
from Application.Archive.ArchiveEntry import ArchiveEntry
from Application.Archive.ArchiveErrors import ArchiveError, CorruptedArchiveError
from Application.Archive.ArchivePlan import ArchiveItem
from Infrastructure.Compression.StreamWriter import write_stream

_SIGNATURES = (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")


class _ZipReader(ArchiveReader):
    def __init__(self, archive: Path) -> None:
        try:
            self._zip = zipfile.ZipFile(archive, "r")
        except (zipfile.BadZipFile, OSError) as error:
            raise CorruptedArchiveError(f"Cannot read ZIP: {error}") from error

    def entries(self) -> list[ArchiveEntry]:
        result: list[ArchiveEntry] = []
        for info in self._zip.infolist():
            try:
                modified = datetime(*info.date_time)
            except ValueError:
                modified = None
            result.append(
                ArchiveEntry(info.filename, info.file_size, info.compress_size, modified, info.is_dir())
            )
        return result

    def extract_to(self, entry: ArchiveEntry, destination: Path) -> None:
        try:
            if entry.is_dir:
                destination.mkdir(parents=True, exist_ok=True)
                return
            with self._zip.open(entry.name, "r") as stream:
                write_stream(stream, destination)
        except (zipfile.BadZipFile, RuntimeError, NotImplementedError) as error:
            raise ArchiveError(str(error)) from error

    def close(self) -> None:
        self._zip.close()


# Architecture: ZIP format adapter.
# Layer: Infrastructure.Compression.
# Role: Implements ArchiveEngine with the standard-library zipfile module.
# Contract: ArchiveEngine.
class ZipEngine(ArchiveEngine):
    name = "zip"
    extension = ".zip"

    def matches(self, archive: Path) -> bool:
        try:
            with open(archive, "rb") as file:
                return file.read(4) in _SIGNATURES
        except OSError:
            return False

    def compress(self, items: list[ArchiveItem], output: Path, level: int) -> int:
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_name(f"{output.stem}.ftool-tmp{output.suffix}")
        method = zipfile.ZIP_STORED if level == 0 else zipfile.ZIP_DEFLATED
        try:
            with zipfile.ZipFile(
                temporary, "w", method,
                compresslevel=None if level == 0 else level,
                strict_timestamps=False,
            ) as archive:
                for item in items:
                    archive.write(item.source, item.arcname)
            os.replace(temporary, output)
        except (OSError, zipfile.BadZipFile, ValueError) as error:
            raise ArchiveError(f"ZIP compression failed: {error}") from error
        finally:
            if temporary.exists():
                temporary.unlink()
        return output.stat().st_size

    def open(self, archive: Path) -> ArchiveReader:
        return _ZipReader(archive)
