from __future__ import annotations

from datetime import datetime
import json
import os
import tempfile
from typing import TypedDict, TypeGuard, cast

from Domain.Trash.TrashEntry import TrashEntry
from Domain.Trash.base import TrashRegistry
from Domain.Trash.TrashRecord import TrashRecord






# Architecture: JSON trash-registry adapter.
# Layer: Infrastructure.Trash.
# Role: Persists TrashEntry records using JSON and temporary-file replacement.
# Contract: TrashRegistry.
class JsonTrashRegistry(TrashRegistry):
    def record(self, entry: TrashEntry) -> None:
        entries = self._read()
        entries.append(self._entry_to_dict(entry))
        self._write(entries)

    def restore(self, original_path: str) -> TrashEntry:
        entries = self._read()
        matching_indices = [
            index
            for index, entry in enumerate(entries)
            if entry["original_path"] == original_path
        ]
        if not matching_indices:
            raise ValueError(
                f"No trash entry found for original path: {original_path}"
            )
        latest_index = max(
            matching_indices,
            key=lambda index: datetime.fromisoformat(
                entries[index]["deleted_at"]
            ),
        )
        entry = entries.pop(latest_index)
        self._write(entries)
        return self._entry_from_dict(entry)

    def list_entries(self) -> list[TrashEntry]:
        return [self._entry_from_dict(entry) for entry in self._read()]

    def find_by_trashed_path(self, trashed_path: str) -> TrashEntry | None:
        for entry in self._read():
            if entry["trashed_path"] == trashed_path:
                return self._entry_from_dict(entry)
        return None

    def _ensure_file_exists(self) -> None:
        directory = os.path.dirname(self.registry_file)
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.registry_file):
            self._write([])

    def _read(self) -> list[TrashRecord]:
        try:
            with open(self.registry_file, "r", encoding="utf-8") as file:
                content = file.read().strip()
        except FileNotFoundError:
            return []
        if not content:
            return []

        try:
            decoded: object = json.loads(content)
        except json.JSONDecodeError:
            return []
        if not isinstance(decoded, list):
            return []

        records: list[TrashRecord] = []
        for item in cast(list[object], decoded):
            if self._is_trash_record(item):
                records.append(item)
        return records

    def _write(self, entries: list[TrashRecord]) -> None:
        directory = os.path.dirname(self.registry_file) or "."
        fd, temporary_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                json.dump(entries, file, ensure_ascii=False, indent=2)
            os.replace(temporary_path, self.registry_file)
        except Exception:
            if os.path.exists(temporary_path):
                os.remove(temporary_path)
            raise

    def _entry_to_dict(self, entry: TrashEntry) -> TrashRecord:
        return {
            "original_path": entry.original_path,
            "trashed_path": entry.trashed_path,
            "deleted_at": entry.deleted_at.isoformat(),
        }

    def _entry_from_dict(self, data: TrashRecord) -> TrashEntry:
        return TrashEntry(
            original_path=data["original_path"],
            trashed_path=data["trashed_path"],
            deleted_at=datetime.fromisoformat(data["deleted_at"]),
        )

    def _is_trash_record(self,value: object) -> TypeGuard[TrashRecord]:
        if not isinstance(value, dict):
            return False
        record = cast(dict[object, object], value)
        return (
            isinstance(record.get("original_path"), str)
            and isinstance(record.get("trashed_path"), str)
            and isinstance(record.get("deleted_at"), str)
        )

