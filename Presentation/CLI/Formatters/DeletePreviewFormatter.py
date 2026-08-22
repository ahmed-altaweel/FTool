from Application.Presenters.PreviewFormatter import PreviewFormatter


class DeletePreviewFormatter(PreviewFormatter):
    def format(self, paths, options) -> str:
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