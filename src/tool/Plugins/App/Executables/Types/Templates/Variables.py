from Objects.Outer import Outer
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList
from Plugins.App.Arguments.Argument import Argument
from typing import List, Any
import functools

class Variables(Outer):
    items: ApplyArgumentList = ApplyArgumentList([])

    def get(self, name) -> Any:
        return self.all_variables.get(name)

    @functools.cached_property
    def all_variables(self) -> List[Argument]:
        items: dict = {}

        for ext in self.outer.mro:
            if hasattr(ext, 'variables'):
                for _item in ext.variables.items.toList():
                    items[_item.name] = _item

        return items
