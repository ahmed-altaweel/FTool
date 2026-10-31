from pathlib import Path

from Application.Archive.ArchiveEngine import ArchiveEngine
from Application.Archive.ArchiveExecutionStrategy.base import ArchiveExecutionStrategy
from Application.Archive.ArchivePlan import ArchivePlan
from Application.Archive.ArchiveRequest import ArchiveOptions
from Application.Archive.ArchiveResult import ArchiveResult
from Application.Common.CommandStatus import CommandStatus


# Architecture: Simulated compression strategy.
# Layer: Application.Archive.
# Role: Reports exactly what would be archived without touching the disk.
class DryRunArchiveExecutor(ArchiveExecutionStrategy):
    def execute(
        self, engine: ArchiveEngine, plan: ArchivePlan, output: Path, options: ArchiveOptions
    ) -> ArchiveResult:
        return ArchiveResult(
            CommandStatus.SUCCESS,
            output_path=str(output),
            sources_count=plan.sources_count,
            files_count=len(plan.files),
            folders_count=len(plan.folders),
            original_size=plan.total_size,
            excluded_count=plan.excluded_count,
            is_dry_run=True,
            preview=[i.arcname + ("/" if i.is_dir else "") for i in plan.items],
            warnings=plan.warnings,
        )
