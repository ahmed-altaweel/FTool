from pathlib import Path

from Application.Archive.ArchiveEngine import ArchiveEngineRegistry
from Application.Archive.ArchiveErrors import ArchiveError
from Application.Archive.ArchiveExecutionStrategy.base import ExtractExecutionStrategy
from Application.Archive.ArchiveRequest import ExtractOptions
from Application.Archive.ArchiveResult import ArchiveViolation, ExtractResult
from Application.Archive.ArchiveValidator import ArchiveValidator
from Application.Archive.ConflictPolicy import (
    ConflictPolicy,
    OverwriteConflictPolicy,
    RenameConflictPolicy,
    SkipConflictPolicy,
)
from Application.Common.CommandStatus import CommandStatus


# Architecture: Extraction use-case coordinator.
# Layer: Application.Archive.
# Role: Validates, sniffs the format, opens the archive, then lists or extracts via a strategy.
class ExtractExecutor:
    def __init__(
        self,
        registry: ArchiveEngineRegistry,
        validator: ArchiveValidator,
        real_strategy: ExtractExecutionStrategy,
        dry_run_strategy: ExtractExecutionStrategy,
        prompt_policy: ConflictPolicy,
    ) -> None:
        self.registry = registry
        self.validator = validator
        self.real_strategy = real_strategy
        self.dry_run_strategy = dry_run_strategy
        self.prompt_policy = prompt_policy

    def execute(self, archive: Path, options: ExtractOptions) -> ExtractResult:
        target = Path(options.target) if options.target else Path(".")
        writes = not (options.list_only or options.dry_run)
        violations = self.validator.validate_extract(archive, target, writes)
        if violations:
            missing = violations[0].reason == "ARCHIVE_NOT_FOUND"
            status = CommandStatus.NOT_FOUND if missing else CommandStatus.INVALID
            return ExtractResult(status, violations=violations)

        engine = self.registry.detect(archive)
        if engine is None:
            return self._invalid("UNSUPPORTED_FORMAT", [archive], ", ".join(self.registry.names()))
        reason = engine.read_unavailable_reason()
        if reason:
            return ExtractResult(CommandStatus.FAILURE, message=reason)

        try:
            with engine.open(archive) as reader:
                if options.list_only:
                    return ExtractResult(
                        CommandStatus.SUCCESS, target_path=str(target), is_list_only=True, entries=reader.entries()
                    )
                strategy = self.dry_run_strategy if options.dry_run else self.real_strategy
                return strategy.execute(reader, target, options, self._policy(options))
        except ArchiveError as error:
            return self._invalid("CORRUPTED_ARCHIVE", [archive], str(error))

    def _policy(self, options: ExtractOptions) -> ConflictPolicy:
        if options.overwrite:
            return OverwriteConflictPolicy()
        if options.skip:
            return SkipConflictPolicy()
        if options.rename:
            return RenameConflictPolicy()
        return self.prompt_policy

    @staticmethod
    def _invalid(reason: str, paths: list[Path], detail: str = "") -> ExtractResult:
        return ExtractResult(CommandStatus.INVALID, violations=[ArchiveViolation(reason, paths, detail)])
