from Plugins.App.Storage.StorageItem import StorageItem
from Objects.Configurable import Configurable
from Plugins.Arguments.ArgumentList import ArgumentList
from Objects.Object import Object
from Objects.classproperty import classproperty
from pydantic import Field
from pathlib import Path

class Storage(Object, Configurable):
    items: dict = Field(default={})
    common: Path = Field(default=None)

    def register(self):
        for name in ["config", "db", "storage_units", "temp_storage_units", "exports", "temp_exports", "logs", "binary"]:
            self.items[name] = StorageItem(
                root = self.common, 
                dir_name = name
            )

    def get(self, name):
        return self.items.get(name)

    @classproperty
    def options(cls) -> ArgumentList:
        from Plugins.Arguments.Types.StringArgument import StringArgument

        return ArgumentList([
            StringArgument(
                name = "storage.path",
                default = "?cwd?/storage",
            )
        ])
