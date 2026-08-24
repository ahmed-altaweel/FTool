from abc import ABC, abstractmethod
from typing import Any

from Application.Delete.DeleteRequest import DeleteOptions
from Application.Presenters.PreviewFormatter import PreviewFormatter
from Infrastructure.Terminal.IOStream import IOStream


# Architecture: Confirmation policy contract.
# Layer: Infrastructure.Terminal.
# Role: Abstracts whether a delete operation is accepted by the user or execution mode.
# Implementations: RequiredConfirmationPolicy, SkippedConfirmationPolicy.
class ConfirmationPolicy(ABC):
    def __init__(self,io_stream:IOStream):
        self.io_stream=io_stream
    def confirm(
        self,
        paths: list[str],
        options: Any,
        preview_formatter: PreviewFormatter,
    ) -> bool:
        ...
