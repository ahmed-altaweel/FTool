from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScannedEntry:
    path: Path
    relative: tuple[str, ...]          # () for the scanned root itself
    is_dir: bool
    size: int = 0
    skipped_reason: str | None = None  # set when the entry cannot be archived


# Architecture: Source-tree scanning contract.
# Layer: Application.Archive.
# Role: Walks a file/folder, pruning anything `skip` rejects. Implementations: OsSourceScanner.
class SourceScannerPort(ABC):
    @abstractmethod
    def scan(
        self,
        source: Path,
        skip: Callable[[tuple[str, ...], bool], bool],
    ) -> Iterator[ScannedEntry]:
        ...
