from Objects.Object import Object
from pydantic import Field

class ArgumentList(Object):
    items: list = Field()

    def toDict(self):
        dicts = {}
        for item in self.items:
            dicts[item.name] = item

        return dicts
