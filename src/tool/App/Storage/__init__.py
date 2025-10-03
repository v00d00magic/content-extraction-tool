from Utils.Data.Text import Text
from App.Storage.StorageItem import StorageItem
from Objects.Configurable import Configurable
from Declarable.Documentation import global_documentation
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
        from Declarable.Arguments import StringArgument

        items = {}
        items["storage.path"] = StringArgument({
            "default": "?cwd?/storage", # cwd -> /storage
        })

        return items
