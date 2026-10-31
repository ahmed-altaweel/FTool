import os
from pathlib import Path

from Application.Archive.ArchiveExecutor import ArchiveExecutor
from Application.Archive.ArchiveRequest import ArchiveRequest
from Application.Archive.ArchiveResult import ArchiveResult
from Application.Archive.ArchiveValidator import ArchiveValidator
from Application.Common.CommandStatus import CommandStatus
from Application.Common.FileSystemInspector import FileSystemInspector
from Application.Common.Handler import CommandHandler
from Application.Common.TargetResolverPort import TargetResolverPort

_GLOB_CHARS = "*?["


# Architecture: Archive command handler.
# Layer: Application.Archive.
# Role: Expands wildcards (cmd.exe does not), checks sources exist, then delegates to the executor.
# Contract: CommandHandler[ArchiveRequest, ArchiveResult].
class ArchiveHandler(CommandHandler[ArchiveRequest, ArchiveResult]):
    def __init__(
        self,
        target_resolver: TargetResolverPort,
        fs_inspector: FileSystemInspector,
        validator: ArchiveValidator,
        executor: ArchiveExecutor,
    ) -> None:
        self.target_resolver = target_resolver
        self.fs = fs_inspector
        self.validator = validator
        self.executor = executor

    def execute(self, request: ArchiveRequest) -> ArchiveResult:
        args = request.request
        resolved: list[Path] = []
        missing: list[str] = []
        for raw in args.sources:
            matches = self._expand(raw)
            if not matches:
                missing.append(raw)
            resolved.extend(Path(os.path.normpath(os.path.abspath(m))) for m in matches)
        if missing:
            return ArchiveResult(CommandStatus.NOT_FOUND, error_paths=missing)

        resolved = list(dict.fromkeys(resolved))
        violations = self.validator.validate_sources(resolved)
        if violations:
            return ArchiveResult(CommandStatus.INVALID, violations=violations)
        return self.executor.execute(resolved, args.options)

    def _expand(self, raw: str) -> list[Path]:
        path = Path(raw)
        if self.fs.exists(path):
            return [path]
        if any(c in raw for c in _GLOB_CHARS):
            return self.target_resolver.resolve(raw, False)
        return []
