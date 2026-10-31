from abc import ABC, abstractmethod
from enum import Enum, auto
from pathlib import Path


class ConflictAction(Enum):
    OVERWRITE = auto()
    SKIP = auto()
    RENAME = auto()
    ABORT = auto()


# Architecture: Extraction conflict-policy contract.
# Layer: Application.Archive.
# Role: Decides what to do when an extracted file already exists.
# Implementations: Overwrite/Skip/Rename (below), PromptConflictPolicy (Infrastructure.Terminal).
class ConflictPolicy(ABC):
    interactive: bool = False

    @abstractmethod
    def decide(self, destination: Path) -> ConflictAction:
        ...


class OverwriteConflictPolicy(ConflictPolicy):
    def decide(self, destination: Path) -> ConflictAction:
        return ConflictAction.OVERWRITE


class SkipConflictPolicy(ConflictPolicy):
    def decide(self, destination: Path) -> ConflictAction:
        return ConflictAction.SKIP


class RenameConflictPolicy(ConflictPolicy):
    def decide(self, destination: Path) -> ConflictAction:
        return ConflictAction.RENAME
