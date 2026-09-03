from Application.Common.CommandStatus import CommandStatus
from Application.Copy.CopyResult import CopyResult


class CopyResultFormatter:

    def format(self, result: CopyResult) -> str:

        if result.status == CommandStatus.SUCCESS:
            return (
                f"Copied : "
                f"{', '.join(result.source_paths)} "
                f"← {result.destination_path}"
            )

        if result.status == CommandStatus.NOT_FOUND:
            return (
                f"Error : Source not found  "
                f"({result.error_path})"
            )

        if result.status == CommandStatus.CANCELLED:
            return "Copy operation cancelled."

        if result.status == CommandStatus.INVALID:
            return "\n".join(result.violations)

        return "Failed to execute copy operation."