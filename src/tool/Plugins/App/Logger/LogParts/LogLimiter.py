from Objects.Object import Object
from pydantic import Field

class LogLimiter(Object):
    skip_categories: list = Field()
    silent: list = Field(default=[])

    def shouldBeDisplayed(self, msg, where):
        if where in self.silent:
            return False

        for _section in self.skip_categories:
            if _section.isIt(msg.section, msg.kind) == True:
                return _section.where != where

        return True
