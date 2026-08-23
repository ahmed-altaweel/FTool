from Application.Delete.DeleteRequest import DeleteOptions
from Application.Presenters.PreviewFormatter import PreviewFormatter


# Architecture: CLI delete-preview formatter.
# Layer: Presentation.CLI.
# Role: Renders targets and delete options for interactive confirmation.
# Contract: PreviewFormatter.
class DeletePreviewFormatter(PreviewFormatter[DeleteOptions]):
    def format(self, paths: list[str], options: DeleteOptions) -> str:
        execution = "SIMULATION" if options.dry_run else "Real"
        destination = "Permanent deletion" if options.final_delete else "Trash"

        lines = [
            "",
            "============ DELETE OPERATION ==========",
            f"Execution   : {execution}",
            f"Destination : {destination}",
            f"Targets     : {len(paths)}",
            "",
            "Files:",
        ]
        lines += [f" - {p}" for p in paths]
        lines.append("=========================================")
        return "\n".join(lines)