"""عقد مكيّف الهدف الخاص بعمليات الإنشاء.

لا يعاد استخدام TargetDeleteHandler هنا؛ لأن المسؤولية مختلفة:
الحذف يعرف can_handle/delete/delete_to_trash، أما الإنشاء فيعرف
can_handle/create. لذلك عقد منفصل بمكان منفصل، كما ينص دليل المطور.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class TargetCreateHandler(Protocol):
    """عقد مكيّف الإنشاء."""

    def can_handle(self, path: str) -> bool:
        ...

    def create(self, path: str, *, parents: bool = False) -> None:
        ...

    def exists(self, path: str) -> bool:
        ...