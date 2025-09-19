from .LogSection import LogSection
from .LogKind import LogKind
from utils.Wrap import Wrap
from typing import List

class LogSkipSection(Wrap):
    name: str
    wildcard: bool = False
    inactive: bool = False
    kinda: List = None
    where: List = "console"

    def isIt(self, section: LogSection, kind: LogKind = None):
        section_check = False

        if self.inactive == True:
            return False

        if self.wildcard == True:
            for _section in section.section:
                if _section in self.name:
                    section_check = True
        else:
            section_check = self.name == section.section

        if section_check == False:
            return False

        if kind != None and self.kinda != None:
            return kind.kind in self.kinda

        return True
