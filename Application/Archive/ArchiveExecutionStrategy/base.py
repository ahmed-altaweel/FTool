from abc import ABC, abstractmethod
from pathlib import Path

from Application.Archive.ArchiveEngine import ArchiveEngine, ArchiveReader
from Application.Archive.ArchivePlan import ArchivePlan
from Application.Archive.ArchiveRequest import ArchiveOptions, ExtractOptions
from Application.Archive.ArchiveResult import ArchiveResult, ExtractResult
from Application.Archive.ConflictPolicy import ConflictPolicy


# Architecture: Compression execution strategy contract.
# Layer: Application.Archive.
# Implementations: RealArchiveExecutor, DryRunArchiveExecutor.
class ArchiveExecutionStrategy(ABC):
    @abstractmethod
    def execute(
        self, engine: ArchiveEngine, plan: ArchivePlan, output: Path, options: ArchiveOptions
    ) -> ArchiveResult:
        ...


# Architecture: Extraction execution strategy contract.
# Layer: Application.Archive.
# Implementations: RealExtractExecutor, DryRunExtractExecutor.
class ExtractExecutionStrategy(ABC):
    @abstractmethod
    def execute(
        self,
        reader: ArchiveReader,
        target: Path,
        options: ExtractOptions,
        policy: ConflictPolicy,
    ) -> ExtractResult:
        ...
