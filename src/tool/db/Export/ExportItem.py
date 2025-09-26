from utils.Wrap import Wrap
from typing import TypedDict, ClassVar
from enum import Enum

class ClassNameEnum(Enum):
    CONTENT_UNIT = "cu"
    STORAGE_UNIT = "su"

class FlagsDict(TypedDict):
    link_depth: int = 10

class ExportItem(Wrap):
    class_name: ClassVar[ClassNameEnum] = ClassNameEnum.CONTENT_UNIT
    id: int
    flags: ClassVar[FlagsDict] = {
        "link_depth": 10
    }
