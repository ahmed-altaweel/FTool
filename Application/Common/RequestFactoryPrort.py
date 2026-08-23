from abc import ABC, abstractmethod
import argparse

from Application.Common.Request import CommandRequest


class RequestFactoryPort(ABC):
    @abstractmethod
    def create(self, argv: argparse.Namespace) -> CommandRequest:
        ...