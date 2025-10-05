from .LogSection import LogSection
from .LogKind import LogKind
from Objects.Object import Object
from pydantic import Field

class LogSkipSection(Object):
    name: list = Field()
    wildcard: bool = Field(default=False)
    wildcard_all: bool = Field(default=False)
    inactive: bool = Field(default=False)
    kinda: list = Field(default=[])
    where: list = Field(default=["console"])

    def isIt(self, section: LogSection, kind: LogKind = None) -> bool:
        section_check = False

        if self.inactive == True:
            return False

        if self.wildcard == True:
            for _section in section.section:
                if _section in self.name:
                    section_check = True
        elif self.wildcard_all == True:
            section_check = True
        else:
            section_check = self.name == section.section

        if section_check == False:
            return False

        if kind != None and self.kinda != None:
            return kind.kind in self.kinda

        return True
