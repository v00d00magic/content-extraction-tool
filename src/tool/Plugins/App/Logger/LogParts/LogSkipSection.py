from .LogSection import LogSection
from .LogKind import LogKind
from Objects.Object import Object
from pydantic import Field

class LogSkipSection(Object):
    name: list = Field()
    wildcard: bool = Field(default=False)
    inactive: bool = Field(default=False)
    kinda: list = Field(default=[])
    where: list = Field(default=["console"])

    def isIt(self, section: LogSection, kind: LogKind = None) -> bool:
        section_check = False

        if self.inactive == True:
            return False

        if self.wildcard == True:
            section_check = "!".join(section.section).startswith("!".join(self.name))
        else:
            section_check = "!".join(self.name) ==  "!".join(section.section)

        if section_check == False:
            return False

        if kind != None and self.kinda != None and len(self.kinda) > 0:
            return kind.kind.value in self.kinda

        return True
