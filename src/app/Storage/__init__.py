from utils.Data.Text import Text
from app.Storage.StorageItem import StorageItem
from app.Storage.StorageItemHashList import StorageItemHashList

class StorageContainer:
    def __init__(self, config):
        self.common = Text(config.get("storage.root_path")).cwdReplacement().srcReplacement().get()
        self.items = {}

        self.items["config"] = StorageItem(self.common, "config")
        self.items["db"] = StorageItem(self.common, "db")

        self.items["storage_units"] = StorageItemHashList(self.common, "storage_units")
        self.items["temp_storage_units"] = StorageItemHashList(self.common, "temp_storage_units")

        self.items["exports"] = StorageItem(self.common, "exports")
        self.items["temp_exports"] = StorageItem(self.common, "temp_exports")
        self.items["logs"] = StorageItem(self.common, "logs")
        self.items["binary"] = StorageItem(self.common, "binary")

    def get(self, name):
        return self.items.get(name)
