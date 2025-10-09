from Objects.Object import Object
from typing import Any
from pydantic.dataclasses import dataclass
from pydantic import Field

@dataclass
class ArgumentList:
    items: list

    def toList(self) -> list:
        return self.items

    def toDict(self) -> dict:
        dicts = {}
        for item in self.items:
            dicts[item.name] = item

        return dicts

    def get(self, name: str) -> Any:
        return self.toDict().get(name)
