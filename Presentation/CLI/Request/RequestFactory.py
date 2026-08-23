import argparse
from collections.abc import Callable
from typing import TypeVar

from Application.Delete.DeleteRequest import DeleteRequest
from Application.Common.Request import CommandRequest
from Presentation.CLI.Request.RequestCreator.base import RequestCreator


# Architecture: CLI request-factory registry.
# Layer: Presentation.CLI.
# Role: Maps command names to request creators and invokes the selected creator.
class RequestFactory:
    def __init__(self) -> None:
        self.factories: dict[str, RequestCreator] = {}

    def register(self, command_name: str, creator: RequestCreator) -> None:
        self.factories[command_name] = creator

    def create(self, argv: argparse.Namespace) -> CommandRequest:
        command = getattr(argv, "command", None)
        if not isinstance(command, str):
            raise ValueError("Parsed arguments do not contain a command name")
        creator = self.factories.get(command)
        if creator is None:
            raise ValueError(f"Unknown command: {command}")
        return creator.create(argv)
