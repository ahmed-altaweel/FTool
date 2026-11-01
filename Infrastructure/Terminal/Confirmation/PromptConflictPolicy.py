from pathlib import Path

from Application.Archive.ConflictPolicy import ConflictAction, ConflictPolicy
from Infrastructure.Terminal.IOStream import IOStream

_ANSWERS = {
    "o": ConflictAction.OVERWRITE,
    "s": ConflictAction.SKIP,
    "r": ConflictAction.RENAME,
    "q": ConflictAction.ABORT,
}


# Architecture: Interactive conflict adapter.
# Layer: Infrastructure.Terminal.
# Role: Asks the user what to do with an existing file; empty/unknown input (or no stdin) means skip.
# Contract: ConflictPolicy.
class PromptConflictPolicy(ConflictPolicy):
    interactive = True

    def __init__(self, io_stream: IOStream) -> None:
        self.io_stream = io_stream

    def decide(self, destination: Path) -> ConflictAction:
        self.io_stream.print_text(
            f"\nFile exists: {destination}\n[o]verwrite / [s]kip / [r]ename / [q]uit (default s): "
        )
        answer = self.io_stream.read_text().lower()[:1]
        return _ANSWERS.get(answer, ConflictAction.SKIP)
