from pydantic.dataclasses import dataclass
from typing import Any, List
from Objects.Object import Object

@dataclass
class NameDictList:
    items: List[Object] # name-field-containing

    def toList(self) -> list:
        return self.items

    def toNames(self) -> list:
        names = []

        for val in self.toList():
            names.append(val.name)

        return names

    def toDict(self) -> dict:
        dicts = {}
        for item in self.items:
            dicts[item.name] = item

        return dicts

    def get(self, name: str) -> Any:
        return self.toDict().get(name)

    def append(self, item: Any):
        self.items.append(item)
