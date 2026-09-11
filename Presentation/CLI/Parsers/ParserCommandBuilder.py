import argparse
from typing import Protocol, TypeAlias


Subparsers: TypeAlias = "argparse._SubParsersAction[argparse.ArgumentParser]"


class ParserCommandBuilder(Protocol):
    @staticmethod
    def build(commands: Subparsers) -> None:
        ...
