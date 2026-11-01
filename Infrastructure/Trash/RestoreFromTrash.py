from pathlib import Path
import shutil

from Domain.Trash.Trash import Trash


class RestoreFromTrash(Trash):
    def move(self, path: Path, destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(path, destination)
        self._remove_container(path)
        return destination

    def _remove_container(self, trashed_path: Path) -> None:
        # MoveToTrash stores each item as entries/<uuid>/<name>.
        # Remove the <uuid> folder once it is empty.
        container = trashed_path.parent
        if container.parent != self.entries_path:
            return
        try:
            container.rmdir()
        except OSError:
            pass