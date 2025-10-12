from Objects.Outer import Outer
from App import app

class Saver(Outer):
    def ContentUnit(self):
        app.logger.log("Created new ContentUnit", section="Saveable")

        out = ContentUnit()
        self.outer.meta.selfInsert(out)

        return out

    def Collection(self):
        app.logger.log("Created new collection", section="Saveable")

        out = ContentUnit()
        out.is_collection = True

        self.outer.meta.selfInsert(out)
        self.variable("collections").append(out)

        return out

    def StorageUnit(self):
        app.logger.log("Created new StorageUnit", section="Saveable")

        out = StorageUnit()

        return out

    def ThumbnailUnit(self):
        app.logger.log("Created new ThumbnailUnit", section="Saveable")

        return ThumbnailUnit()
