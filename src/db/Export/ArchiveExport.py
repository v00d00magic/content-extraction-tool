from utils.Data.Random import Random
from db.Models.Content.ContentModel import BaseModel
from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Relations.ContentUnitRelation import ContentUnitRelation
from db.Models.Content.StorageUnit import StorageUnit
from peewee import Model, SqliteDatabase
from db.LinkManager import LinkManager
from app.App import storage

class ExportItem():
    def __init__(self, element_item, flags):
        self.item = element_item
        self.flags = flags

    def export(self):
        item_type = self.item.short_name
        save_at_db = True
        save_files = True

        if save_at_db == True:
            with override_db([ContentUnit, StorageUnit], self.db):
                item_data = self.item.__dict__["__data__"]
                self.item.insert(item_data).execute()

        match (item_type):
            case "su":
                pass

class ArchiveExport:
    EXTENSION_NAME = "units"

    @classmethod
    def create_manager(cls):
        return ArchiveExport()

    def define_temp(self):
        _storage = storage.sub("tmp_exports")
        storage_path = _storage.path()

        self.tmp_path = storage_path.joinpath(Random().random_hash(32))
        self.tmp_path.mkdir()

        self.content_path = self.tmp_path.joinpath("content")
        self.content_path.mkdir()

        # self.cu_path = self.content_path.joinpath("content_units")
        # self.cu_path.mkdir()

        self.su_path = self.content_path.joinpath("storage_units")
        self.su_path.mkdir()

    def define_db(self):
        self.db = SqliteDatabase(self.tmp_path.joinpath("items.db"))
        _models = [ContentUnit, StorageUnit, ContentUnitRelation]

        with override_db(_models, self.db):
            self.db.connect()
            self.db.create_tables(_models, safe=True)
            print(self.db)

    def end(self):
        self.db.close()

    def getByTypeAndId(self, type: str, id: int):
        '''
        type: cu or su
        id: id of model
        '''
        element_class = None

        match(type):
            case "cu":
                element_class = ContentUnit.ids(int(id))
            case "su":
                element_class = StorageUnit.ids(int(id))

        return element_class

    def getExportItem(self, item: BaseModel, flags):
        return ExportItem(item, flags)
