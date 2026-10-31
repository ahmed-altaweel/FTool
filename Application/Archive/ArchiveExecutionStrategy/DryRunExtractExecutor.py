from pathlib import Path

from Application.Archive.ArchiveEngine import ArchiveReader
from Application.Archive.ArchiveExecutionStrategy.base import ExtractExecutionStrategy
from Application.Archive.ArchiveRequest import ExtractOptions
from Application.Archive.ArchiveResult import ExtractResult
from Application.Archive.ConflictPolicy import ConflictAction, ConflictPolicy
from Application.Archive.ExtractRules import UnsafeEntryError, destination_for
from Application.Common.CommandStatus import CommandStatus
from Application.Common.FileSystemInspector import FileSystemInspector


# Architecture: Simulated extraction strategy.
# Layer: Application.Archive.
# Role: Reports what would be extracted/skipped/blocked without writing anything.
class DryRunExtractExecutor(ExtractExecutionStrategy):
    def __init__(self, fs_inspector: FileSystemInspector) -> None:
        self.fs = fs_inspector

    def execute(
        self, reader: ArchiveReader, target: Path, options: ExtractOptions, policy: ConflictPolicy
    ) -> ExtractResult:
        result = ExtractResult(CommandStatus.SUCCESS, target_path=str(target), is_dry_run=True)
        for entry in reader.entries():
            try:
                destination = destination_for(target, entry.name)
            except UnsafeEntryError as error:
                result.errors.append(f"Would block unsafe entry ({error})")
                continue
            if destination is None:
                continue
            exists = self.fs.exists(destination)
            if entry.is_dir:
                result.folders_created += 0 if exists else 1
                continue
            if not exists:
                result.files_extracted += 1
            elif policy.interactive:
                result.notes.append(f"Would ask what to do (already exists): {destination}")
            else:
                action = policy.decide(destination)
                if action == ConflictAction.SKIP:
                    result.skipped += 1
                    result.notes.append(f"Would skip existing: {destination}")
                else:
                    result.files_extracted += 1
                    verb = "overwrite" if action == ConflictAction.OVERWRITE else "rename"
                    result.notes.append(f"Would {verb}: {destination}")
        if result.errors:
            result.status = CommandStatus.FAILURE
        return result
