from .DownloadItem import DownloadItem
from Objects.Object import Object
from pydantic import Field

class DownloadManagerItems(Object):
    manager: Object = Field(default=None)
    items: list = []

    def append(self, item: DownloadItem):
        item.manager = self.manager
        item._constuctor()

        self.items.append(item)

    def remove(self, item: DownloadItem):
        pass

    def getById(self, id: int):
        for item in self.items:
            if item.id == id:
                return item
