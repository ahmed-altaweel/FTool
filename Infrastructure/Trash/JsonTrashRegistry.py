from datetime import datetime
import json
import os
import tempfile
from typing import Optional

from Domain.Trash.TrashEntry import TrashEntry
from Domain.Trash.base import TrashRegistry

class JsonTrashRegistry(TrashRegistry):
    def record(self,entry:TrashEntry) ->None:
        entries=self._read()
        entries.append(entry.__dict__)
        self._write(entries)
    def restore(self,orignal_path:str) ->TrashEntry:
        entries=self._read()
        matching_indices=[
            i for i,e in enumerate(entries)
            if e["original_path"]==orignal_path
        ]
        if not matching_indices:
            raise ValueError(f"No trash entry found or orignal path:{orignal_path}")
        latest_index=max(
            matching_indices,key=lambda i:entries[i]['deleted_at']
        )
        entry_dict=entries.pop(latest_index)
        self._write(entries)
        return self._entry_from_dict(entry_dict)
    def list_entries(self):
        entries=self._read()
        return [self._entry_from_dict(e) for e in entries]
    def find_by_trashed_path(self,trashed_path:str)->Optional[TrashEntry]:
        entries=self._read()
        for e in entries:
            if e["trashed_path"] ==trashed_path:
                return self._entry_from_dict(e)
        return None
    def _ensure_file_exists(self)->None:
        directory=os.path.dirname(self.registry_file)
        if directory:
            os.makedirs(directory,exist_ok=True)
        if not os.path.exists(self.registry_file):
            self._write([])

    def _read(self):
        try:
            with open(self.registry_file,'r',encoding="utf-8") as f:
                content=f.read().strip()
                return json.loads(content) if content else []
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def _write(self,entries:list):
        directory=os.path.dirname(self.registry_file) or '.'
        fd,tmp_path=tempfile.mkstemp(dir=directory,suffix=".tmp")
        try:
            with os.fdopen(fd,'w',encoding="utf-8") as f:
                json.dump(entries,f,ensure_ascii=False,indent=2,default=self._json_default)
            os.replace(tmp_path,self.registry_file)
        except Exception:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise

    def _entry_to_dict(self,entry:TrashEntry)->dict:
            return {
                "original_path":entry.original_path,
                "trashed_path":entry.trashed_path,
                "deleted_at":entry.deleted_at
            }
    def _entry_from_dict(self,data:dict)->TrashEntry:
            return TrashEntry(
                orignial_path=data['original_path'],
                trashed_path=data['trashed_path'],
                deleted_at=data['deleted_at']
            )
    def _json_default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()

        raise TypeError(
            f"Object of type {type(obj).__name__} is not JSON serializable"
    )