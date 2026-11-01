import os
from pathlib import Path

from Application.Common.CommandStatus import CommandStatus
from Application.Common.Handler import CommandHandler
from Application.Restore.RestoreRequest import RestoreRequest
from Application.Restore.RestoreResult import RestoreResult
from Domain.Trash.Trash import Trash
from Domain.Trash.TrashEntry import TrashEntry
from Domain.Trash.TrashRegistry import TrashRegistry


class RestoreHandler(CommandHandler[RestoreRequest, RestoreResult]):
    def __init__(self, trash_registry: TrashRegistry, restorer: Trash) -> None:
        self.trash_registry: TrashRegistry = trash_registry
        self.restorer: Trash = restorer

    def execute(self, request: RestoreRequest) -> RestoreResult:
        args = request.request
        options = args.options

        if options.list_only:
            entries = sorted(
                self.trash_registry.list_entries(),
                key=lambda entry: entry.deleted_at,
                reverse=True,
            )
            return RestoreResult(CommandStatus.SUCCESS, entries=entries, is_listing=True)

        if not args.path:
            return RestoreResult(CommandStatus.INVALID, reason="MISSING_PATH")

        entry = self._find_latest_entry(args.path)
        if entry is None:
            return RestoreResult(
                CommandStatus.NOT_FOUND,
                error_path=args.path,
                reason="NO_TRASH_ENTRY",
            )

        trashed_path = Path(entry.trashed_path)
        destination = Path(entry.original_path)

        if not trashed_path.exists():
            return RestoreResult(
                CommandStatus.NOT_FOUND,
                entries=[entry],
                error_path=entry.trashed_path,
                reason="TRASHED_ITEM_MISSING",
            )

        if destination.exists():
            return RestoreResult(
                CommandStatus.INVALID,
                entries=[entry],
                error_path=entry.original_path,
                reason="DESTINATION_EXISTS",
            )

        if options.dry_run:
            return RestoreResult(
                CommandStatus.SUCCESS,
                entries=[entry],
                restored_path=entry.original_path,
                is_dry_run=True,
            )

        # The registry entry is removed first and put back if the move fails.
        self.trash_registry.restore(entry.original_path)
        try:
            self.restorer.move(trashed_path, destination)
        except OSError as error:
            self.trash_registry.record(entry)
            return RestoreResult(
                CommandStatus.INVALID,
                entries=[entry],
                error_path=entry.original_path,
                reason=f"MOVE_FAILED: {error}",
            )

        return RestoreResult(
            CommandStatus.SUCCESS,
            entries=[entry],
            restored_path=entry.original_path,
        )

    def _find_latest_entry(self, path: str) -> TrashEntry | None:
        # Compare by absolute path so older entries stored as relative paths still match.
        wanted = os.path.abspath(path)
        matches = [
            entry
            for entry in self.trash_registry.list_entries()
            if os.path.abspath(entry.original_path) == wanted
        ]
        if not matches:
            return None
        return max(matches, key=lambda entry: entry.deleted_at)