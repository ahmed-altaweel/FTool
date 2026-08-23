from Application.Delete.DeleteResult import DeleteResult
from Application.Presenters.ResultFormatter import ResultFormatter
from Application.Presenters.ResultPresenter import ResultPresenter
from Application.Common.Result import CommandResult


# Architecture: CLI result presentation adapter.
# Layer: Presentation.CLI.
# Role: Selects a formatter by concrete result type and returns its text.
# Contract: ResultPresenter.
class CliResultPresenter(ResultPresenter):
    def __init__(self, formatters: dict[type[CommandResult], ResultFormatter]) -> None:
        self.formatters: dict[type[CommandResult], ResultFormatter] = formatters

    def present(self, result: CommandResult) -> str:
        formatter = self.formatters.get(type(result))
        if formatter is None:
            return f"...Unknown result type: {type(result).__name__}..."
        return formatter.format(result)
