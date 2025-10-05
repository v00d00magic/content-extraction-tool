from Utils.Data.Random import Random
from peewee import SqliteDatabase
from DB.Export.ExportItem import ExportItem
from DB.Links.ContentUnitRelation import ContentUnitRelation
from DB.Models.Content.ContentUnit import ContentUnit
from DB.Models.Content.StorageUnit import StorageUnit
from DB.DBWrapper import DBWrapper
from App.Storage.StorageItem import StorageItem
from DB.ModelDTO import ModelDTO

from App import app

class ArchiveExport:
    EXTENSION_NAME = "units"

    def defineTemp(self):
        self.export_hash = Random().random_hash(32)
        self.tmp = app.storage.get("temp_exports").path().joinpath(self.export_hash)
        self.tmp.mkdir()

        self.storage = StorageItem(self.tmp, "storage_units", make_dir=True)

    def defineDB(self):
        models = [ContentUnit, StorageUnit, ContentUnitRelation]

        self.db_wrapper = DBWrapper(f"export_{self.export_hash}", SqliteDatabase(self.tmp.joinpath("items.db")))
        with self.db_wrapper.db_ref.bind_ctx(models):
            self.db_wrapper.db_ref.create_tables(models, safe=True)

    def end(self):
        self.db_wrapper.db_ref.close()

    def export(self, item: ExportItem):
        model = item.getModel()

        assert model != None, "item not found"

        app.logger.log(f"Exporting {model.name_db_id} to db {self.db_wrapper.db_name}", section=["Export", "Items"])

        movement = ModelDTO()
        movement.moveTo(model, 
                        self.db_wrapper, 
                        recursion_limit = item.getLinkDepth(),
                        storage_units_move_type = ModelDTO.MOVE_TYPE_COPY)

        return model
