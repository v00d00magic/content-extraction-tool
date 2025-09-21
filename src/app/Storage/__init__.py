from utils.Data.Text import Text
from app.Storage.StorageItem import StorageItem
from utils.Configurable import Configurable
from declarable.Documentation import global_documentation

class StorageContainer(Configurable):
    def __init__(self, config):
        self.updateConfig()
        self.common = Text(config.get("storage.path")).cwdReplacement().srcReplacement().get()
        self.items = {}

        self.items["config"] = StorageItem(self.common, "config")
        self.items["db"] = StorageItem(self.common, "db")

        self.items["storage_units"] = StorageItem(self.common, "storage_units")
        self.items["temp_storage_units"] = StorageItem(self.common, "temp_storage_units")

        self.items["exports"] = StorageItem(self.common, "exports")
        self.items["temp_exports"] = StorageItem(self.common, "temp_exports")
        self.items["logs"] = StorageItem(self.common, "logs")
        self.items["binary"] = StorageItem(self.common, "binary")

    def get(self, name):
        return self.items.get(name)

    @classmethod
    def declareSettings(cls):
        from declarable.Arguments import StringArgument

        global_documentation.loadKeys({
            "storage.root_path.name": {
                "en_US": "Storage location",
            },
            "storage.root_path.definition": {
                "en_US": "Internal storage location. «?cwd?» is replaced with the startup directory. Edit with caution.",
            },
        })
        items = {}
        items["storage.path"] = StringArgument({
            "default": "?cwd?/storage", # cwd -> /storage
            "docs": {
                "name": global_documentation.get("storage.root_path.name"),
                "definition": global_documentation.get("storage.root_path.definition"),
            },
        })

        return items
