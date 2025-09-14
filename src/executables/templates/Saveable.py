from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit
from app.App import logger

class Saveable:
    @classmethod
    def ContentUnit(cls):
        logger.log("Created new ContentUnit", section="Saveable")

        out = ContentUnit()
        cls.selfInsert(out)

        return out

    @classmethod
    def StorageUnit(cls):
        logger.log("Created new StorageUnit", section="Saveable")

        out = StorageUnit()

        return out

    def selfInsert(item):
        '''
        You can append needed keys here
        '''

        return item
