from typing import TypedDict


class TrashRecord(TypedDict):
    original_path: str
    trashed_path: str
    deleted_at: str
