from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from Application.Archive.ArchiveEngine import ArchiveEngineRegistry
from Application.Archive.ArchiveExecutionStrategy.base import ArchiveExecutionStrategy
from Application.Archive.ArchivePlanner import ArchivePlanner
from Application.Archive.ArchiveRequest import ArchiveOptions
from Application.Archive.ArchiveResult import ArchiveResult, ArchiveViolation
from Application.Archive.ArchiveValidator import ArchiveValidator
from Application.Common.CommandStatus import CommandStatus


# Architecture: Compression use-case coordinator.
# Layer: Application.Archive.
# Role: Picks engine and output name, plans, validates, then delegates to a real or dry-run strategy.
class ArchiveExecutor:
    def __init__(
        self,
        registry: ArchiveEngineRegistry,
        planner: ArchivePlanner,
        validator: ArchiveValidator,
        real_strategy: ArchiveExecutionStrategy,
        dry_run_strategy: ArchiveExecutionStrategy,
        clock: Callable[[], datetime] = datetime.now,
    ) -> None:
        self.registry = registry
        self.planner = planner
        self.validator = validator
        self.real_strategy = real_strategy
        self.dry_run_strategy = dry_run_strategy
        self.clock = clock

    def execute(self, sources: list[Path], options: ArchiveOptions) -> ArchiveResult:
        engine = self.registry.by_name(options.format)
        if engine is None:
            return self._invalid("UNSUPPORTED_FORMAT", detail=options.format)
        reason = engine.write_unavailable_reason()
        if reason:
            return ArchiveResult(CommandStatus.FAILURE, message=reason)

        output = self._resolve_output(sources, options, engine.extension)
        other = self.registry.extensions().get(output.suffix.lower())
        if other is not None and other != engine.name:
            return self._invalid(
                "FORMAT_MISMATCH", [output], f"'{output.name}' looks like {other} but format is {engine.name}"
            )

        plan = self.planner.plan(sources, options.exclude, output)
        violations = self.validator.validate_compress(plan, output, options.force)
        if violations:
            return ArchiveResult(
                CommandStatus.INVALID, violations=violations, output_path=str(output), warnings=plan.warnings
            )

        strategy = self.dry_run_strategy if options.dry_run else self.real_strategy
        return strategy.execute(engine, plan, output, options)

    def _resolve_output(self, sources: list[Path], options: ArchiveOptions, extension: str) -> Path:
        if options.output:
            output = Path(options.output)
            return output if output.suffix else output.with_name(output.name + extension)
        if len(sources) == 1:
            return Path(sources[0].name + extension)
        return Path(f"archive_{self.clock():%Y%m%d_%H%M%S}{extension}")

    @staticmethod
    def _invalid(reason: str, paths: list[Path] | None = None, detail: str = "") -> ArchiveResult:
        return ArchiveResult(
            CommandStatus.INVALID, violations=[ArchiveViolation(reason, paths or [], detail)]
        )
