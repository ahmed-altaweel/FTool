from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TrashEntry:
    original_path:str
    trashed_path:str
    deleted_at:datetime

