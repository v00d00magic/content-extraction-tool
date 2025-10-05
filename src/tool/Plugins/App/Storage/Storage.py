from Plugins.App.Storage.StorageItem import StorageItem
from Objects.Configurable import Configurable
from Plugins.Arguments.ArgumentList import ArgumentList
from Objects.Object import Object
from pydantic import Field
from pathlib import Path

class Storage(Object, Configurable):
    items: dict = Field(default={})
    common: str = Field(default=None)

    def __init__(self):
        super().__init__()

        for name in ["config", "db", "storage_units", "temp_storage_units", "exports", "temp_exports", "logs", "binary"]:
            self.register(name)

    def register(self, name):
        self.items[name] = StorageItem(self.common, name)

    def get(self, name):
        return self.items.get(name)

    @property
    def options() -> ArgumentList:
        from Plugins.Arguments.Types.StringArgument import StringArgument

        return ArgumentList([
            StringArgument(
                name = "storage.path",
                default = "?cwd?/storage",
            )
        ])
