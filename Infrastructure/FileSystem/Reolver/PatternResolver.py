import glob
from pathlib import Path
# Architecture: Glob pattern adapter.
# Layer: Infrastructure.FileSystem.
# Role: Resolves a path or glob pattern into matching string paths.
class PatternResolver:
    def resolve(self, path: str | Path, recursive: bool) -> list[str]:
       return glob.glob(str(path),recursive=recursive)
