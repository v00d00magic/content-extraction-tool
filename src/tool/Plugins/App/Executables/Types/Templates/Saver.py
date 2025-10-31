from Plugins.App.DB.Content.ContentUnit import ContentUnit
from Objects.Outer import Outer
from App import app

class Saver(Outer):
    def ContentUnit(self, *args, **kwargs):
        do_flush = kwargs.get('_do_flush', True)
        db = None
        db_name = None

        out: ContentUnit = self.outer.ContentUnit(*args, **kwargs)
        out.saved = self.outer.ContentUnit.Saved(
            representation = self.outer.meta.name_str,
            method = self.outer.meta.name_str,
        )

        app.Logger.log(f"Created new ContentUnit {out}", section=["Saveable"])

        if do_flush == True:
            if kwargs.get('db', None) != None:
                db = kwargs.get('db')
            else:
                db_name = self.outer.call.db
                if kwargs.get('save', None) != None:
                    db_name = kwargs.get('save')

                db = app.DbConnection.getConnectionByName(db_name)

            out.flush(db)

            app.Logger.log(f"Flushed ContentUnit to db {db_name} (id {out.uuid})", section=["Saveable"])

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
