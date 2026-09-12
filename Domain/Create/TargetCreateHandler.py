from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
# Architecture: Target create handler contract.
# Layer: Domain.Create.
# Role: Declares how a concrete handler recognises and creates its target kind.
class TargetCreateHandler(Protocol):
    def can_handle(self, path: Path) -> bool:
        ...

    def create(self, path: Path, *, parents: bool = False) -> None:
        ...