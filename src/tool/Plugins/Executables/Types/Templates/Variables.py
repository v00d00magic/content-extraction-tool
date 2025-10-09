from .Template import Template
from Plugins.Arguments.ArgumentList import ArgumentList
from Plugins.Arguments.Argument import Argument
from typing import List, Any

class Variables(Template):
    items: ArgumentList = ArgumentList([])

    def get(self, name) -> Any:
        return self.items.get(name)

    def all_variables(self) -> List[Argument]:
        items: list = []

        for ext in self.outer.__mro__:
            if hasattr(ext, 'variables'):
                for _item in ext.variables.items.toList():
                    items.append(_item)

        return items
