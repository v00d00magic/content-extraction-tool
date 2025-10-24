from DB.Models.Content.ContentUnit import ContentUnit
from DB.Models.Content.StorageUnit import StorageUnit
from Objects.Object import Object
from typing import TypedDict, ClassVar
from enum import Enum

class ClassNameEnum(Enum):
    CONTENT_UNIT = "cu"
    STORAGE_UNIT = "su"

class FlagsDict(TypedDict):
    link_depth: int = 10

class ExportItem(Object):
    class_name: ClassVar[ClassNameEnum] = ClassNameEnum.CONTENT_UNIT
    id: int = None
    flags: ClassVar[FlagsDict] = {
        "link_depth": 10
    }

    def getLinkDepth(self):
        return self.flags.get("link_depth")

    def getModel(self):
        match (selfclass_name_str):
            case ClassNameEnum.CONTENT_UNIT.value:
                return ContentUnit.ids(self.id)
            case ClassNameEnum.STORAGE_UNIT.value:
                return StorageUnit.ids(self.id)
