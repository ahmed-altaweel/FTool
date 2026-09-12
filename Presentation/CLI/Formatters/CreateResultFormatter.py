from Application.Common.CommandStatus import CommandStatus
from Application.Common.Result import CommandResult
from Application.Create.CreateResult import CreateResult


# Architecture: Create result formatter.
# Layer: Presentation.CLI.Formatters.
# Role: Converts a CreateResult into a user-facing string.
# Contract: ResultFormatter.
class CreateResultFormatter:
    def format(self, result: CommandResult) -> str:
        if result.status == CommandStatus.SUCCESS:
            if getattr(result, "is_dry_run", False):
                target = result.paths[0] if result.paths else "?"
                return f"[dry-run] would create: {target}"
            target = result.paths[0] if result.paths else "?"
            return f"created: {target}"

        if result.status == CommandStatus.NOT_FOUND:
            target = result.error_path or (result.paths[0] if result.paths else "?")
            return f"not found: {target}"

        if result.status == CommandStatus.INVALID:
            if result.violations:
                reasons = ", ".join(v.reason for v in result.violations)
                return f"invalid: {reasons}"
            return f"invalid: {result.error_path or 'unknown'}"

        return f"status: {result.status}"