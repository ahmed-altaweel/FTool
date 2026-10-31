from abc import ABC, abstractmethod
from pathlib import Path


# Architecture: Target-resolution contract.
# Layer: Application.Common.
# Role: Expands a path or glob pattern into the matching paths.
# Implementations: TargetResolver.
class TargetResolverPort(ABC):
    @abstractmethod
    def resolve(self, path: str | Path, recursive_search: bool) -> list[Path]:
        ...
