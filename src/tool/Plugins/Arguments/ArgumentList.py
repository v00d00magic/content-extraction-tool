from Objects.Object import Object
from pydantic.dataclasses import dataclass
from pydantic import Field

@dataclass
class ArgumentList:
    items: list

    def toDict(self) -> dict:
        dicts = {}
        for item in self.items:
            dicts[item.name] = item

        return dicts
