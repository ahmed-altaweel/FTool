from abc import ABC, abstractmethod

from Application.Output import OutputPolicy

class OutputPolicyResolver(ABC):

    @abstractmethod
    def resolve(self, quiet: bool) -> OutputPolicy:
        ...
