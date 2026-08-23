from typing import Any

from Application.Confirmation.ConfirmaitonPolicy import ConfirmationPolicy
from Application.Delete.DeleteRequest import DeleteOptions
from Application.Presenters.PreviewFormatter import PreviewFormatter

# Architecture: Interactive confirmation adapter.
# Layer: Infrastructure.Terminal.
# Role: Presents the delete preview and accepts an affirmative terminal response.
# Contract: ConfirmationPolicy as currently defined.
class RequiredConfirmationPolicy(ConfirmationPolicy):
    def confirm(self, paths: list[str], options: Any, preview_formatter: PreviewFormatter) -> bool:
        preview = preview_formatter.format(paths, options)
        print(preview)
        return input("Are you sure?[Y/N]").strip().upper()=='Y'