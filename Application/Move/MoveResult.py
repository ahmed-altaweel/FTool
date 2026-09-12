from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List

@dataclass
class MoveResult:
    status: str                     # SUCCESS, FAILED, CANCELLED, SOURCE_NOT_FOUND...
    source: Path
    destination: Path
    message: str = ""
    error_path: Optional[Path] = None  # المسار الذي تسبب في الفشل
    moved_items: List[Path] = field(default_factory=list)  # ا  لعناصر التي نُقلت فعلياً

