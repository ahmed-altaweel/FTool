
# Architecture: Normal terminal output adapter.
# Layer: Infrastructure.Terminal.
# Role: Writes result and error text to standard output.
# Contract: Infrastructure.Terminal.Output.OutputPolicy.
from Application.Output.OutputPolicy import OutputPolicy


class NormalOutputPolicy(OutputPolicy):
    def print_result(self, text: str) -> None:
        self.io_stream.print_text(text)
    def print_error(self, text: str) -> None:
        self.io_stream.print_text(text)