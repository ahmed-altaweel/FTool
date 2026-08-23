from Application.Common.CommandStatus import CommandStatus
from Application.Delete.DeleteResult import DeleteResult
from Application.Presenters.ResultFormatter import ResultFormatter


# Architecture: CLI delete-result formatter.
# Layer: Presentation.CLI.
# Role: Renders DeleteResult statuses, violations, and target counts.
# Contract: ResultFormatter.
class DeleteResultFormatter(ResultFormatter[DeleteResult]):
    def format(self, result: DeleteResult) -> str:
        if result.status == CommandStatus.NOT_FOUND:
            return (
                "\n"
                "============ DELETE OPERATION ============\n"
                "Status : NotFound\n"
                f"Error : The file or directory ({result.error_path}) not found in current path.\n"
                "==========================================="
            )

        elif result.status == CommandStatus.CANCELLED:
            return (
                "\n"
                "============ DELETE OPERATION ============\n"
                "Status : CANCELLED\n"
                "No files were deleted.\n"
                "==========================================="
            )

        elif result.is_dry_run:
            return (
                "\n"
                "============ DELETE OPERATION ============\n"
                "Status : SIMULATION\n"
                "No files were deleted.\n"
                f"Targets: {len(result.paths)}\n"
                "==========================================="
            )
        if result.status == CommandStatus.INVALID:
            lines = [
                "",
                "============ DELETE OPERATION ============",
                "Status : REJECTED",
            ]
            for violation in result.violations:
                if violation.reason == "FOLDER_NOT_ALLOWED":
                    lines.append(
                        "Error : The following are directories, but --delete-folder was not specified:"
                    )
                    lines += [f" - {p}" for p in violation.paths]
            lines.append("===========================================")
            return "\n".join(lines)
        
        return (
            "\n"
            "============ DELETE OPERATION ============\n"
            "Status : SUCCESS\n"
            f"Deleted: {len(result.paths)} target(s)\n"
            "==========================================="
        )
