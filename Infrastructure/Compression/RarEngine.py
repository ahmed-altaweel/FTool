import os
import shutil
import subprocess
from pathlib import Path, PurePosixPath

from Application.Archive.ArchiveEngine import ArchiveEngine, ArchiveReader
from Application.Archive.ArchiveEntry import ArchiveEntry
from Application.Archive.ArchiveErrors import ArchiveError, CorruptedArchiveError
from Application.Archive.ArchivePlan import ArchiveItem
from Infrastructure.Compression.StreamWriter import write_stream

_SIGNATURE = b"Rar!\x1a\x07"
_MAX_ARGS_CHARS = 6000


def _winrar_dirs() -> list[Path]:
    dirs: list[Path] = []
    for variable in ("ProgramFiles", "ProgramFiles(x86)", "ProgramW6432"):
        base = os.environ.get(variable)
        if base:
            dirs.append(Path(base) / "WinRAR")
    return dirs


def _find_tool(names: list[str]) -> str | None:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    for folder in _winrar_dirs():
        for name in names:
            for candidate in (folder / name, folder / f"{name}.exe"):
                if candidate.is_file():
                    return str(candidate)
    return None


class _RarReader(ArchiveReader):
    def __init__(self, archive: Path, rarfile_module) -> None:
        self._rarfile = rarfile_module
        try:
            self._rar = rarfile_module.RarFile(str(archive))
        except rarfile_module.Error as error:
            raise CorruptedArchiveError(f"Cannot read RAR: {error}") from error

    def entries(self) -> list[ArchiveEntry]:
        try:
            infos = self._rar.infolist()
        except self._rarfile.Error as error:
            raise CorruptedArchiveError(f"Cannot read RAR: {error}") from error
        result = []
        for info in infos:
            try:
                from datetime import datetime
                modified = datetime(*info.date_time)
            except (ValueError, TypeError):
                modified = None
            result.append(ArchiveEntry(info.filename, info.file_size, info.compress_size, modified, info.is_dir()))
        return result

    def extract_to(self, entry: ArchiveEntry, destination: Path) -> None:
        try:
            if entry.is_dir:
                destination.mkdir(parents=True, exist_ok=True)
                return
            with self._rar.open(entry.name) as stream:
                write_stream(stream, destination)
        except self._rarfile.Error as error:
            raise ArchiveError(str(error)) from error

    def close(self) -> None:
        self._rar.close()


# Architecture: RAR format adapter.
# Layer: Infrastructure.Compression.
# Role: Reads via the optional `rarfile` package (+ unrar/WinRAR); writes via the `rar` program.
# Contract: ArchiveEngine.
class RarEngine(ArchiveEngine):
    name = "rar"
    extension = ".rar"

    def matches(self, archive: Path) -> bool:
        try:
            with open(archive, "rb") as file:
                return file.read(6) == _SIGNATURE
        except OSError:
            return False

    # ---- availability ------------------------------------------------
    def _rarfile(self):
        try:
            import rarfile
        except ImportError:
            return None
        unrar = _find_tool(["unrar", "UnRAR"])
        if unrar:
            rarfile.UNRAR_TOOL = unrar
        return rarfile

    def read_unavailable_reason(self) -> str | None:
        rarfile = self._rarfile()
        if rarfile is None:
            return "Reading RAR needs the 'rarfile' package: pip install rarfile (and WinRAR/unrar installed)."
        try:
            rarfile.tool_setup()
        except rarfile.RarCannotExec:
            return "Reading RAR needs WinRAR/unrar (or 7-Zip) installed and available in PATH."
        return None

    def write_unavailable_reason(self) -> str | None:
        if _find_tool(["rar", "Rar"]) is None:
            return "Creating RAR needs the 'rar' program (WinRAR). Install WinRAR or use --format zip."
        return None

    # ---- writing -------------------------------------------------------
    def compress(self, items: list[ArchiveItem], output: Path, level: int) -> int:
        executable = _find_tool(["rar", "Rar"])
        if executable is None:
            raise ArchiveError(self.write_unavailable_reason() or "rar not found")
        output = Path(os.path.abspath(output))
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_name(f"{output.stem}.ftool-tmp{output.suffix}")
        method = round(level * 5 / 9)  # map 0-9 onto rar's -m0..-m5

        # RAR stores the names exactly as given, so run it from each member's base folder.
        groups: dict[Path, list[str]] = {}
        for item in items:
            if item.is_dir:
                continue  # folders are created implicitly by the files they contain
            base = item.source
            for _ in PurePosixPath(item.arcname).parts:
                base = base.parent
            groups.setdefault(base, []).append(item.arcname)
        if not groups:
            raise ArchiveError("RAR cannot store an archive that contains only empty folders.")

        try:
            for base, names in groups.items():
                for chunk in self._chunks(names):
                    command = [executable, "a", f"-m{method}", "-y", "-idq", str(temporary), "--", *chunk]
                    completed = subprocess.run(command, cwd=base, capture_output=True, text=True, check=False)
                    if completed.returncode != 0:
                        detail = (completed.stderr or completed.stdout or "").strip()[-500:]
                        raise ArchiveError(f"rar failed (exit {completed.returncode}): {detail}")
            os.replace(temporary, output)
        except OSError as error:
            raise ArchiveError(f"RAR compression failed: {error}") from error
        finally:
            if temporary.exists():
                temporary.unlink()
        return output.stat().st_size

    @staticmethod
    def _chunks(names: list[str]):
        chunk: list[str] = []
        size = 0
        for name in names:
            if chunk and size + len(name) > _MAX_ARGS_CHARS:
                yield chunk
                chunk, size = [], 0
            chunk.append(name)
            size += len(name) + 1
        if chunk:
            yield chunk

    # ---- reading -------------------------------------------------------
    def open(self, archive: Path) -> ArchiveReader:
        rarfile = self._rarfile()
        if rarfile is None:
            raise ArchiveError(self.read_unavailable_reason() or "rarfile missing")
        return _RarReader(archive, rarfile)
