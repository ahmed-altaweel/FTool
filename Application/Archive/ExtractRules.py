from pathlib import Path, PurePosixPath

from Application.Common.FileSystemInspector import FileSystemInspector


class UnsafeEntryError(ValueError):
    """The archive member would be written outside the target folder."""


# Architecture: Extraction safety rules.
# Layer: Application.Archive.
# Role: Blocks path traversal ("zip-slip") and builds collision-free names.
def safe_relative(name: str) -> PurePosixPath:
    normalized = PurePosixPath(name.replace("\\", "/"))
    if normalized.is_absolute():
        raise UnsafeEntryError(f"absolute path: {name}")
    for part in normalized.parts:
        if part == ".." or (len(part) >= 2 and part[1] == ":" and part[0].isalpha()):
            raise UnsafeEntryError(f"unsafe path: {name}")
    return normalized


def destination_for(target: Path, name: str) -> Path | None:
    """Returns the output path for a member, or None for empty names like './'."""
    relative = safe_relative(name)
    if not relative.parts:
        return None
    return target.joinpath(*relative.parts)


def unique_path(destination: Path, inspector: FileSystemInspector) -> Path:
    counter = 1
    while True:
        candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
        if not inspector.exists(candidate):
            return candidate
        counter += 1
