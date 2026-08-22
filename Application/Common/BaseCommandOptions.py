from dataclasses import dataclass

@dataclass
class BaseCommandOptions:
    quiet: bool = False