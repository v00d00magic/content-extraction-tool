from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit
from db.Models.Content.ThumbnailUnit import ThumbnailUnit
from app.App import logger

class Saveable:
    @classmethod
    def ContentUnit(cls):
        logger.log("Created new ContentUnit", section="Saveable")

        out = ContentUnit()
        cls.selfInsert(out)

        return out

    @classmethod
    def Collection(cls):
        logger.log("Created new collection", section="Saveable")

        out = ContentUnit()
        out.is_collection = True

        cls.selfInsert(out)
        cls.call.collections.append(out)

        return out

    @classmethod
    def StorageUnit(cls):
        logger.log("Created new StorageUnit", section="Saveable")

        out = StorageUnit()

        return out

    @classmethod
    def ThumbnailUnit(cls):
        logger.log("Created new ThumbnailUnit", section="Saveable")

        return ThumbnailUnit()

    def selfInsert(item):
        '''
        You can append needed keys here
        '''

        return item
