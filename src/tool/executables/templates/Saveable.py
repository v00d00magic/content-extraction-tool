from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit
from db.Models.Content.ThumbnailUnit import ThumbnailUnit
from app.App import logger

class Saveable:
    def ContentUnit(self):
        logger.log("Created new ContentUnit", section="Saveable")

        out = ContentUnit()
        self.selfInsert(out)

        return out

    def Collection(self):
        logger.log("Created new collection", section="Saveable")

        out = ContentUnit()
        out.is_collection = True

        self.selfInsert(out)
        self.call.collections.append(out)

        return out

    def StorageUnit(self):
        logger.log("Created new StorageUnit", section="Saveable")

        out = StorageUnit()

        return out

    def ThumbnailUnit(self):
        logger.log("Created new ThumbnailUnit", section="Saveable")

        return ThumbnailUnit()

    def selfInsert(item):
        '''
        You can append needed keys here
        '''

        return item
