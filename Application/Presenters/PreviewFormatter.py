
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, TypeVar

from Application.Delete.DeleteRequest import DeleteOptions

CommandOptions=TypeVar("CommandOptions")
# Architecture: Delete-preview formatting contract.
# Layer: Application.Presenters.
# Role: Converts prospective targets and options into confirmation text.
# Implementations: DeletePreviewFormatter.
class PreviewFormatter(ABC,Generic[CommandOptions]):
    @abstractmethod
    def format(self, path: list[Path], options: CommandOptions) -> str:
        pass