from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
# Architecture: One planned archive member.
# Layer: Application.Archive.
# Role: Maps a file-system path to its name inside the archive (always '/'-separated).
class ArchiveItem:
    source: Path
    arcname: str
    is_dir: bool
    size: int = 0


@dataclass
# Architecture: Compression plan.
# Layer: Application.Archive.
# Role: The exact, already-filtered list of members an engine will write.
class ArchivePlan:
    items: list[ArchiveItem] = field(default_factory=list)
    excluded_count: int = 0
    sources_count: int = 0
    warnings: list[str] = field(default_factory=list)
    duplicates: list[str] = field(default_factory=list)

    @property
    def files(self) -> list[ArchiveItem]:
        return [i for i in self.items if not i.is_dir]

    @property
    def folders(self) -> list[ArchiveItem]:
        return [i for i in self.items if i.is_dir]

    @property
    def total_size(self) -> int:
        return sum(i.size for i in self.items if not i.is_dir)
