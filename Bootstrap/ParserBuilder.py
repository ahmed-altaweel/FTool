from __future__ import annotations

import argparse
from typing import Protocol, TypeAlias

from Presentation.CLI.Parsers.ParserCommandBuilder import ParserCommandBuilder, Subparsers




# Architecture: CLI parser composition helper.
# Layer: Bootstrap.
# Role: Creates the root argparse parser and attaches command builders.
class ParserBuilder:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(prog="ftool")
        self.commands: Subparsers = self.parser.add_subparsers(
            dest="command",
            required=True,
        )

    def add(self, command_builder: ParserCommandBuilder) -> ParserBuilder:
        command_builder.build(self.commands)
        return self

    def build(self) -> argparse.ArgumentParser:
        return self.parser
