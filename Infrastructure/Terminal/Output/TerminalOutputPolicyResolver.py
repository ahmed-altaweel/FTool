from Application.Output.OutputPolicy import OutputPolicy
from Application.Output.OutputPolicyResolver import OutputPolicyResolver


# Architecture: Terminal output-policy adapter.
# Layer: Infrastructure.Terminal.
# Role: Selects normal or quiet terminal output implementation.
# Contract: Application.Output.OutputPolicyResolver.
class TerminalOutputPolicyResolver(OutputPolicyResolver):
    def __init__(self, normal: OutputPolicy, quiet: OutputPolicy) -> None:
        self._normal: OutputPolicy = normal
        self._quiet: OutputPolicy = quiet

    def resolve(self, quiet: bool) -> OutputPolicy:
        return self._quiet if quiet else self._normal
