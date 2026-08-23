from pathlib import Path

from Infrastructure.FileSystem.Reolver.PatternResolver import PatternResolver
# Architecture: Delete-target resolution service.
# Layer: Infrastructure.FileSystem.
# Role: Builds direct or recursive patterns and delegates matching to PatternResolver.
class TargetResolver:
    def __init__(self, pattern_resolver: PatternResolver) -> None:
        self.pattern_resolver: PatternResolver = pattern_resolver
    def resolve(self, path: str | Path, recursive_search: bool) -> list[str]:
        path=Path(path)
        base_dir=path.parent
        target=path.name
        if base_dir== Path(""):
            base_dir=Path(".")
        if recursive_search:
            pattern=base_dir/"**"/target
            return self.pattern_resolver.resolve(pattern,recursive=recursive_search)
        # elif any(c in str(path) for c in "*?["):
        #     return self.pattern_resolver.resolve(path,recursive=recursive_search)
        else:
            return self.pattern_resolver.resolve(path,recursive=recursive_search)
    
        