from Application.Archive.ArchiveResult import ExtractResult
from Application.Common.CommandStatus import CommandStatus
from Application.Presenters.ResultFormatter import ResultFormatter
from Presentation.CLI.Formatters.SizeFormat import format_size
from Presentation.CLI.Formatters.ViolationText import violation_lines

_HEADER = "============ EXTRACT OPERATION ============"
_FOOTER = "==========================================="


# Architecture: CLI extract-result formatter.
# Layer: Presentation.CLI.
# Role: Renders ExtractResult statuses, counters, notes, errors and archive listings.
# Contract: ResultFormatter.
class ExtractResultFormatter(ResultFormatter[ExtractResult]):
    def format(self, result: ExtractResult) -> str:
        lines = ["", _HEADER]
        if result.status == CommandStatus.NOT_FOUND:
            lines.append("Status : NotFound")
            for violation in result.violations:
                lines += violation_lines(violation)
        elif result.status == CommandStatus.INVALID:
            lines.append("Status : REJECTED")
            for violation in result.violations:
                lines += violation_lines(violation)
        elif result.is_list_only:
            lines.append("Status : LIST")
            lines.append(f"Items  : {len(result.entries)}")
            lines.append("")
            lines.append(f"{'Size':>12} {'Packed':>12}  Name")
            for entry in result.entries:
                name = entry.name + ("/" if entry.is_dir and not entry.name.endswith("/") else "")
                lines.append(f"{format_size(entry.size):>12} {format_size(entry.compressed_size):>12}  {name}")
        else:
            labels = {
                CommandStatus.SUCCESS: "SIMULATION" if result.is_dry_run else "SUCCESS",
                CommandStatus.CANCELLED: "CANCELLED",
                CommandStatus.FAILURE: "FAILURE",
            }
            lines.append(f"Status : {labels.get(result.status, result.status.name)}")
            if result.message:
                lines.append(f"Error : {result.message}")
            if result.target_path:
                lines.append(f"Target  : {result.target_path}")
            verb = "Would extract" if result.is_dry_run else "Extracted"
            lines.append(f"{verb}: {result.files_extracted} file(s), {result.folders_created} folder(s)")
            if result.skipped:
                lines.append(f"Skipped : {result.skipped}")
            if result.notes:
                lines.append("")
                lines += [f" * {n}" for n in result.notes]
            if result.errors:
                lines.append("")
                lines.append("Errors:")
                lines += [f" - {e}" for e in result.errors]
            if result.is_dry_run:
                lines.append("")
                lines.append("No files were written.")
        if result.status == CommandStatus.FAILURE and not result.errors and result.message == "":
            lines.append("Error : extraction failed")
        lines.append(_FOOTER)
        return "\n".join(lines)
