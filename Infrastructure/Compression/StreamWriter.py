import os
import shutil
from pathlib import Path
from typing import BinaryIO


# Architecture: Safe file-writing helper.
# Layer: Infrastructure.Compression.
# Role: Streams data to a temp file then renames it, so a failed extraction never leaves half-written files.
def write_stream(source: BinaryIO, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".ftool-part")
    try:
        with open(temporary, "wb") as target:
            shutil.copyfileobj(source, target, length=1024 * 1024)
        os.replace(temporary, destination)
    except BaseException:
        try:
            temporary.unlink()
        except OSError:
            pass
        raise
