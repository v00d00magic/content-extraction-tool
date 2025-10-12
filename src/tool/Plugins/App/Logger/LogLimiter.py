from Objects.Object import Object
from .LogParts.LogSkipSection import LogSkipSection
from typing import List
from pydantic import Field

class LogLimiter(Object):
    skip_categories: List[LogSkipSection] = Field()
    silent: list = Field(default=[])

    def shouldBeDisplayed(self, msg, where):
        if where in self.silent:
            return False

        for _section in self.skip_categories:
            if _section.isIt(msg.section, msg.kind) == True:
                return where not in _section.where

        return True
