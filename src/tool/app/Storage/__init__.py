from utils.Data.Text import Text
from app.Storage.StorageItem import StorageItem
from utils.Configurable import Configurable
from declarable.Documentation import global_documentation
from pathlib import Path

class StorageContainer(Configurable):
    def __init__(self, config):
        self.updateConfig()
        self.common = Text(config.get("storage.path")).cwdReplacement().get()
        self.items = {}

        for name in ["config", "db", "storage_units", "temp_storage_units", "exports", "temp_exports", "logs", "binary"]:
            self.register(name)

    def register(self, name):
        self.items[name] = StorageItem(self.common, name)

    def get(self, name):
        return self.items.get(name)

    @classmethod
    def declareSettings(cls):
        from declarable.Arguments import StringArgument

        items = {}
        items["storage.path"] = StringArgument({
            "default": "?cwd?/storage", # cwd -> /storage
        })

        return items
