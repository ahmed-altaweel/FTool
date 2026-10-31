from abc import ABC, abstractmethod
from pathlib import Path
from types import TracebackType

from Application.Archive.ArchiveEntry import ArchiveEntry
from Application.Archive.ArchivePlan import ArchiveItem


# Architecture: Open-archive reading contract.
# Layer: Application.Archive.
# Role: Lists and extracts members of one opened archive.
class ArchiveReader(ABC):
    @abstractmethod
    def entries(self) -> list[ArchiveEntry]:
        ...

    @abstractmethod
    def extract_to(self, entry: ArchiveEntry, destination: Path) -> None:
        """Writes one member (file or folder) to `destination`. Raises ArchiveError."""

    @abstractmethod
    def close(self) -> None:
        ...

    def __enter__(self) -> "ArchiveReader":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()


# Architecture: Archive-format contract.
# Layer: Application.Archive.
# Role: Abstracts one archive format (zip, rar, ...) from the use case.
# Implementations: ZipEngine, RarEngine.
class ArchiveEngine(ABC):
    name: str = ""
    extension: str = ""

    @abstractmethod
    def matches(self, archive: Path) -> bool:
        """True if the file's signature (magic bytes) belongs to this format."""

    def read_unavailable_reason(self) -> str | None:
        """None if reading is possible, otherwise a user-facing explanation."""
        return None

    def write_unavailable_reason(self) -> str | None:
        """None if writing is possible, otherwise a user-facing explanation."""
        return None

    @abstractmethod
    def compress(self, items: list[ArchiveItem], output: Path, level: int) -> int:
        """Creates `output` atomically and returns its size in bytes. Raises ArchiveError."""

    @abstractmethod
    def open(self, archive: Path) -> ArchiveReader:
        """Opens an archive. Raises CorruptedArchiveError if unreadable."""


# Architecture: Engine registry.
# Layer: Application.Archive.
# Role: Finds an engine by format name or by sniffing an existing archive.
class ArchiveEngineRegistry:
    def __init__(self, engines: list[ArchiveEngine]) -> None:
        self._engines = list(engines)

    def names(self) -> list[str]:
        return [e.name for e in self._engines]

    def extensions(self) -> dict[str, str]:
        return {e.extension: e.name for e in self._engines}

    def by_name(self, name: str) -> ArchiveEngine | None:
        return next((e for e in self._engines if e.name == name), None)

    def detect(self, archive: Path) -> ArchiveEngine | None:
        return next((e for e in self._engines if e.matches(archive)), None)
