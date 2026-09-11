from Application.Output.OutputPolicy import OutputPolicy
# Architecture: Quiet terminal output adapter.
# Layer: Infrastructure.Terminal.
# Role: Suppresses normal result text while retaining error output.
# Contract: Infrastructure.Terminal.Output.OutputPolicy.
class QuietOutputPolicy(OutputPolicy):
    def print_result(self, text: str) -> None:
        return
    def print_error(self, text: str) -> None:
        self.io_stream.print_text(text)