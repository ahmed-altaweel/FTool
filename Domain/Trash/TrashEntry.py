from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
# Architecture: Trash record domain entity.
# Layer: Domain.Trash.
# Role: Immutable value describing an original path, its trashed path, and deletion time.
class TrashEntry:
    original_path:str
    trashed_path:str
    deleted_at:datetime

