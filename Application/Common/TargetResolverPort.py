from abc import ABC, abstractmethod
from pathlib import Path


class TargetResolverPort(ABC):
    @abstractmethod
    def resolve(self, path: str | Path, recursive_search: bool) -> list[str]:
        ...