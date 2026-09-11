from abc import ABC, abstractmethod

from Application.Output.OutputPolicy import OutputPolicy

# Architecture: Output-policy resolver contract.
# Layer: Application.Output.
# Role: Chooses the output policy from command-level quiet mode.
# Implementations: TerminalOutputPolicyResolver.
class OutputPolicyResolver(ABC):

    @abstractmethod
    def resolve(self, quiet: bool) -> OutputPolicy:
        ...
