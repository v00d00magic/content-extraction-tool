from Objects.Outer import Outer
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList
from Plugins.App.Arguments.Argument import Argument
from typing import List, Any
import functools

class Variables(Outer):
    items: ApplyArgumentList = ApplyArgumentList([])
    variables: dict = {}

    def get(self, name) -> Any:
        return self.variables.get(name)

    def __init__(self, outer):
        super().__init__(outer)

        for ext in self.outer.mro:
            if hasattr(ext, 'Variables'):
                for _item in ext.Variables.items.toList():
                    self.variables[_item.name] = _item.__class__(
                        name = _item.name
                    ).copy(update=_item.dict(exclude={"current"}))

                    self.variables.get(_item.name).autoApply()
