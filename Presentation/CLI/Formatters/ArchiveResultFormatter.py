from Application.Archive.ArchiveResult import ArchiveResult
from Application.Common.CommandStatus import CommandStatus
from Application.Presenters.ResultFormatter import ResultFormatter
from Presentation.CLI.Formatters.SizeFormat import format_size
from Presentation.CLI.Formatters.ViolationText import violation_lines

_HEADER = "============ ARCHIVE OPERATION ============"
_FOOTER = "==========================================="
_PREVIEW_LIMIT = 25


# Architecture: CLI archive-result formatter.
# Layer: Presentation.CLI.
# Role: Renders ArchiveResult statuses, sizes, violations and dry-run previews.
# Contract: ResultFormatter.
class ArchiveResultFormatter(ResultFormatter[ArchiveResult]):
    def format(self, result: ArchiveResult) -> str:
        lines = ["", _HEADER]
        if result.status == CommandStatus.NOT_FOUND:
            lines.append("Status : NotFound")
            lines.append("Error : These sources were not found:")
            lines += [f" - {p}" for p in result.error_paths]
        elif result.status == CommandStatus.INVALID:
            lines.append("Status : REJECTED")
            for violation in result.violations:
                lines += violation_lines(violation)
        elif result.status == CommandStatus.FAILURE:
            lines.append("Status : FAILURE")
            lines.append(f"Error : {result.message}")
        else:
            lines.append("Status : SIMULATION" if result.is_dry_run else "Status : SUCCESS")
            lines.append(f"Output     : {result.output_path}")
            lines.append(f"Files      : {result.files_count}")
            lines.append(f"Folders    : {result.folders_count}")
            lines.append(f"Original   : {format_size(result.original_size)}")
            if not result.is_dry_run:
                lines.append(f"Archive    : {format_size(result.compressed_size)}")
                if result.original_size:
                    lines.append(f"Ratio      : {result.compressed_size / result.original_size * 100:.1f}%")
            if result.excluded_count:
                lines.append(f"Excluded   : {result.excluded_count} item(s)")
            if result.is_dry_run:
                lines.append("")
                lines.append("Would archive:")
                lines += [f" - {name}" for name in result.preview[:_PREVIEW_LIMIT]]
                hidden = len(result.preview) - _PREVIEW_LIMIT
                if hidden > 0:
                    lines.append(f" ... and {hidden} more")
                lines.append("No archive was created.")
        if result.warnings:
            lines.append("")
            lines.append("Warnings:")
            lines += [f" - {w}" for w in result.warnings]
        lines.append(_FOOTER)
        return "\n".join(lines)
