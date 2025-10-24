from .ContentUnit import ContentUnit as OrigContentUnit
from typing import ClassVar
from pydantic import Field

class ContainsContentUnit():
    ContentUnit: ClassVar[OrigContentUnit] = None

    def init_subclass(cls):
        class ContentUnit(OrigContentUnit):
            class Saved(OrigContentUnit.Saved):
                representation: str = Field(default = cls.meta.name)
                method: str = Field(default = cls.meta.name)

            saved: Saved = Field(default = Saved())

        cls.ContentUnit = ContentUnit
