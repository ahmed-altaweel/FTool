from dataclasses import dataclass, field

from Application.Common.BaseCommandOptions import BaseCommandOptions
from Application.Common.Request import CommandRequest

SUPPORTED_FORMATS: tuple[str, ...] = ("zip", "rar")
MIN_LEVEL = 0
MAX_LEVEL = 9


@dataclass
# Architecture: Archive (compress) command options value object.
# Layer: Application.Archive.
# Role: Captures format, level, exclusion, output and simulation flags.
# Contract: BaseCommandOptions.
class ArchiveOptions(BaseCommandOptions):
    format: str = "zip"
    level: int = 6
    exclude: list[str] = field(default_factory=list)
    output: str | None = None
    force: bool = False
    dry_run: bool = False

    def __post_init__(self) -> None:
        if self.format not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format '{self.format}'. "
                f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
            )
        if not MIN_LEVEL <= self.level <= MAX_LEVEL:
            raise ValueError(
                f"Compression level must be between {MIN_LEVEL} and {MAX_LEVEL}, got {self.level}"
            )


@dataclass
# Architecture: Extract command options value object.
# Layer: Application.Archive.
# Role: Captures destination, conflict policy, listing and simulation flags.
# Contract: BaseCommandOptions.
class ExtractOptions(BaseCommandOptions):
    target: str | None = None
    overwrite: bool = False
    skip: bool = False
    rename: bool = False
    list_only: bool = False
    dry_run: bool = False

    def __post_init__(self) -> None:
        chosen = [n for n, v in (("--overwrite", self.overwrite), ("--skip", self.skip), ("--rename", self.rename)) if v]
        if len(chosen) > 1:
            raise ValueError(f"Choose only one conflict option, got: {', '.join(chosen)}")


@dataclass
class ArchiveRequestArgs:
    sources: list[str]
    options: ArchiveOptions


@dataclass
class ExtractRequestArgs:
    archive: str
    options: ExtractOptions


# Architecture: Archive command request envelope.
# Layer: Application.Archive.
# Contract: CommandRequest[ArchiveRequestArgs].
class ArchiveRequest(CommandRequest[ArchiveRequestArgs]):
    pass


# Architecture: Extract command request envelope.
# Layer: Application.Archive.
# Contract: CommandRequest[ExtractRequestArgs].
class ExtractRequest(CommandRequest[ExtractRequestArgs]):
    pass
