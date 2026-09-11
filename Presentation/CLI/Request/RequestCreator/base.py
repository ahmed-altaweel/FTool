import argparse
from abc import ABC, abstractmethod


from Application.Common.Request import CommandRequest


# Architecture: CLI request-creation contract.
# Layer: Presentation.CLI.
# Role: Abstracts conversion from parsed command arguments to application requests.
# Implementations: DeleteRequestCreator.
class RequestCreator(ABC):
    @abstractmethod
    def create(self, argv: argparse.Namespace) -> CommandRequest:
        ...
