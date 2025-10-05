from Utils.Data.List import List
from Objects.Object import Object
from pydantic import Field

class LogSection(Object):
    section: list = Field(repr=True)

    def join(self) -> str:
        return "!".join(self.section)

    def toString(self) -> str:
        return f"[{self.join()}]"
