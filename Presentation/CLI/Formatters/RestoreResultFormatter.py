from Application.Common.CommandStatus import CommandStatus
from Application.Presenters.ResultFormatter import ResultFormatter
from Application.Restore.RestoreResult import RestoreResult


class RestoreResultFormatter(ResultFormatter[RestoreResult]):
    HEADER = "\n============ RESTORE OPERATION ============"
    FOOTER = "==========================================="

    def format(self, result: RestoreResult) -> str:
        if result.is_listing:
            return self._format_listing(result)

        if result.status == CommandStatus.SUCCESS:
            status = "SIMULATION" if result.is_dry_run else "SUCCESS"
            note = (
                "No files were restored."
                if result.is_dry_run
                else "Restored the item to its original location."
            )
            return self._block(status, f"Path   : {result.restored_path}", note)

        if result.status == CommandStatus.NOT_FOUND:
            if result.reason == "TRASHED_ITEM_MISSING":
                error = f"The trashed item is missing from the trash: {result.error_path}"
            else:
                error = f"No deleted item was found in the trash for: {result.error_path}"
            return self._block("NotFound", f"Error  : {error}")

        return self._block("REJECTED", f"Error  : {self._describe(result)}")

    def _format_listing(self, result: RestoreResult) -> str:
        if not result.entries:
            return self._block("EMPTY", "The trash is empty.")
        lines = [f"Items  : {len(result.entries)}", ""]
        for entry in result.entries:
            lines.append(
                f" - {entry.original_path}  "
                f"(deleted {entry.deleted_at.strftime('%Y-%m-%d %H:%M:%S')})"
            )
        return self._block("TRASH", *lines)

    def _describe(self, result: RestoreResult) -> str:
        reason = result.reason or ""
        if reason == "MISSING_PATH":
            return "Provide the path of the deleted item, or use --list to see the trash."
        if reason == "DESTINATION_EXISTS":
            return (
                f"The original location already exists: {result.error_path}. "
                "Move or rename it first, then restore again."
            )
        if reason.startswith("MOVE_FAILED"):
            return f"Could not restore {result.error_path} ({reason.removeprefix('MOVE_FAILED: ')})."
        return reason or "Unknown error."

    def _block(self, status: str, *lines: str) -> str:
        return "\n".join([self.HEADER, f"Status : {status}", *lines, self.FOOTER, ""])