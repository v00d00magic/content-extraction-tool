from Plugins.App.Storage.StorageItem import StorageItem
from Objects.Configurable import Configurable
from Plugins.Data.NameDictList import NameDictList
from Objects.Object import Object
from Objects.ClassProperty import classproperty
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
    def options(cls) -> NameDictList:
        from Plugins.Arguments.Types.StringArgument import StringArgument

        return NameDictList([
            StringArgument(
                name = "storage.path",
                default = "?cwd?/storage",
            )
        ])
