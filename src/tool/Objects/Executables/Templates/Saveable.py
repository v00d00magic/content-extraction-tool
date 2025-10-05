from DB.Models.Content.ContentUnit import ContentUnit
from DB.Models.Content.StorageUnit import StorageUnit
from DB.Models.Content.ThumbnailUnit import ThumbnailUnit
from App import app

class Saveable:
    def ContentUnit(self):
        app.logger.log("Created new ContentUnit", section="Saveable")

        out = ContentUnit()
        self.selfInsert(out)

        return out

    def Collection(self):
        app.logger.log("Created new collection", section="Saveable")

        out = ContentUnit()
        out.is_collection = True

        self.selfInsert(out)
        self.variable("collections").append(out)

        return out

    def StorageUnit(self):
        app.logger.log("Created new StorageUnit", section="Saveable")

        out = StorageUnit()

        return out

    def ThumbnailUnit(self):
        app.logger.log("Created new ThumbnailUnit", section="Saveable")

        return ThumbnailUnit()

    def selfInsert(item):
        '''
        You can append needed keys here
        '''

        return item
