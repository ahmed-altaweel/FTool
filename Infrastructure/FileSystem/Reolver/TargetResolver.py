from dataclasses import dataclass
from pathlib import Path
class TargetResolver:
    def __init__(self,pattern_resolver):
        self.pattern_resolver=pattern_resolver
    def resolve(self,path,recursive_search):
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
    
        