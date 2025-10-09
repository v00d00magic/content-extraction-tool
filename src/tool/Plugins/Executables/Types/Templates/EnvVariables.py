from .Template import Template
from Plugins.Arguments.ArgumentList import ArgumentList
from typing import Any

class EnvVariables(Template):
    items: ArgumentList = ArgumentList([])

    def get(self, name):
        return self.items.get(name)
