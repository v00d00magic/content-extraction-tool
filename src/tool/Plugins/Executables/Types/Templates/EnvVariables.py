from Objects.Outer import Outer
from Plugins.Data.NameDictList import NameDictList
from typing import Any

class EnvVariables(Outer):
    items: NameDictList = NameDictList([])

    def get(self, name):
        return self.items.get(name)
