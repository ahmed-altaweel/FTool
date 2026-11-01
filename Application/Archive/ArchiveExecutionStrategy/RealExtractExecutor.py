from pathlib import Path

from Application.Archive.ArchiveEngine import ArchiveReader
from Application.Archive.ArchiveErrors import ArchiveError
from Application.Archive.ArchiveExecutionStrategy.base import ExtractExecutionStrategy
from Application.Archive.ArchiveRequest import ExtractOptions
from Application.Archive.ArchiveResult import ExtractResult
from Application.Archive.ConflictPolicy import ConflictAction, ConflictPolicy
from Application.Archive.ExtractRules import UnsafeEntryError, destination_for, unique_path
from Application.Common.CommandStatus import CommandStatus
from Application.Common.FileSystemInspector import FileSystemInspector


# Architecture: Real extraction strategy.
# Layer: Application.Archive.
# Role: Extracts member by member, enforcing path safety and the conflict policy.
class RealExtractExecutor(ExtractExecutionStrategy):
    def __init__(self, fs_inspector: FileSystemInspector) -> None:
        self.fs = fs_inspector

    def execute(
        self, reader: ArchiveReader, target: Path, options: ExtractOptions, policy: ConflictPolicy
    ) -> ExtractResult:
        result = ExtractResult(CommandStatus.SUCCESS, target_path=str(target))
        for entry in reader.entries():
            try:
                destination = destination_for(target, entry.name)
            except UnsafeEntryError as error:
                result.errors.append(f"Blocked unsafe entry ({error})")
                continue
            if destination is None:
                continue

            if self.fs.exists(destination):
                if entry.is_dir and self.fs.is_directory(destination):
                    continue  # merging into an existing folder is always fine
                if entry.is_dir != self.fs.is_directory(destination):
                    result.errors.append(f"Type mismatch (file vs folder): {destination}")
                    continue
                action = policy.decide(destination)
                if action == ConflictAction.ABORT:
                    result.status = CommandStatus.CANCELLED
                    result.notes.append("Extraction stopped by user.")
                    return result
                if action == ConflictAction.SKIP:
                    result.skipped += 1
                    result.notes.append(f"Skipped existing: {destination}")
                    continue
                if action == ConflictAction.RENAME:
                    renamed = unique_path(destination, self.fs)
                    result.notes.append(f"Renamed: {destination.name} -> {renamed.name}")
                    destination = renamed

            try:
                reader.extract_to(entry, destination)
            except (ArchiveError, OSError) as error:
                result.errors.append(f"Failed to extract {entry.name}: {error}")
                continue
            if entry.is_dir:
                result.folders_created += 1
            else:
                result.files_extracted += 1

        if result.errors:
            result.status = CommandStatus.FAILURE
        return result
