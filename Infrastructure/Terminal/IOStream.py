import sys
from typing import TextIO


# Architecture: Terminal I/O adapter.
# Layer: Infrastructure.Terminal.
# Role: Wraps stdin/stdout so output never crashes on non-UTF-8 consoles (e.g. Windows cp1252).
class IOStream:
    def __init__(
        self,
        input_stream: TextIO | None = None,
        output_stream: TextIO | None = None,
    ) -> None:
        self.input_stream = input_stream or sys.stdin
        self.output_stream = output_stream or sys.stdout
        reconfigure = getattr(self.output_stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(errors="replace")
            except (ValueError, OSError):
                pass

    def print_text(self, message: str) -> None:
        self.output_stream.write(message)
        self.output_stream.flush()

    def read_text(self) -> str:
        return self.input_stream.readline().strip()
