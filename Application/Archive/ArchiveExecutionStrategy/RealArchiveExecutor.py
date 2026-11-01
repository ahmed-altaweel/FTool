from pathlib import Path

from Application.Archive.ArchiveEngine import ArchiveEngine
from Application.Archive.ArchiveErrors import ArchiveError
from Application.Archive.ArchiveExecutionStrategy.base import ArchiveExecutionStrategy
from Application.Archive.ArchivePlan import ArchivePlan
from Application.Archive.ArchiveRequest import ArchiveOptions
from Application.Archive.ArchiveResult import ArchiveResult
from Application.Common.CommandStatus import CommandStatus


# Architecture: Real compression strategy.
# Layer: Application.Archive.
# Role: Asks the engine to write the archive and reports sizes.
class RealArchiveExecutor(ArchiveExecutionStrategy):
    def execute(
        self, engine: ArchiveEngine, plan: ArchivePlan, output: Path, options: ArchiveOptions
    ) -> ArchiveResult:
        base = dict(
            output_path=str(output),
            sources_count=plan.sources_count,
            files_count=len(plan.files),
            folders_count=len(plan.folders),
            original_size=plan.total_size,
            excluded_count=plan.excluded_count,
            warnings=plan.warnings,
        )
        try:
            compressed = engine.compress(plan.items, output, options.level)
        except (ArchiveError, OSError) as error:
            return ArchiveResult(CommandStatus.FAILURE, message=str(error), **base)
        return ArchiveResult(
            CommandStatus.SUCCESS, compressed_size=compressed, message="Archive created", **base
        )
