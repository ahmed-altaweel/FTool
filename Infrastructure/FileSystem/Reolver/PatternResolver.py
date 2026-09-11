import glob
from pathlib import Path
# Architecture: Glob pattern adapter.
# Layer: Infrastructure.FileSystem.
# Role: Resolves a path or glob pattern into matching string paths.
class PatternResolver:
    def resolve(self, base_dir: Path ,pattern:str, recursive: bool) -> list[Path]:
       return list(base_dir.rglob(pattern)) if recursive else list(base_dir.glob(pattern))
