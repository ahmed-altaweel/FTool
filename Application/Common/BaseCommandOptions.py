from dataclasses import dataclass

@dataclass
# Architecture: Shared command-options value object.
# Layer: Application.Common.
# Role: Defines options common to command requests.
class BaseCommandOptions:
    quiet: bool = False