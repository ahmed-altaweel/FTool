from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
# Architecture: Archive member DTO.
# Layer: Application.Archive.
# Role: Describes one file/folder stored inside an archive.
class ArchiveEntry:
    name: str
    size: int = 0
    compressed_size: int = 0
    modified: datetime | None = None
    is_dir: bool = False

    @property
    def ratio(self) -> float:
        return (self.compressed_size / self.size * 100) if self.size else 0.0
