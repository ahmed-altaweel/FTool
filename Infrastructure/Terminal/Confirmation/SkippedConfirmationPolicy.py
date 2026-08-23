from typing import Any

from Application.Confirmation.ConfirmaitonPolicy import ConfirmationPolicy
from Application.Delete.DeleteRequest import DeleteOptions
from Application.Presenters.PreviewFormatter import PreviewFormatter


# Architecture: Non-interactive confirmation adapter.
# Layer: Infrastructure.Terminal.
# Role: Bypasses the confirmation prompt for forced execution.
# Contract: ConfirmationPolicy.
class SkippedConfirmationPolicy(ConfirmationPolicy):
    def confirm(
        self,
        paths: list[str],
        options: Any,
        preview_formatter: PreviewFormatter,
    ) -> bool:
        return True

