from peewee import CharField, AutoField, BigIntegerField
from DB.Models.BaseModel import BaseModel
from DB.Models.Content.ContentUnit import ContentUnit
from DB.Models.Content.StorageUnit import StorageUnit
from enum import Enum

class RelationEnum():
    RELATION_NONE = 0
    RELATION_MAIN = 1
    RELATION_THUMBNAIL = 2
    RELATION_REVISION = 3

class ContentUnitRelation(BaseModel):
    table_name = 'relations'

    parent = CharField(max_length = 100, null=True)
    child_type = CharField(max_length = 20, default='ContentUnit')
    child = CharField(max_length = 100, null=True)
    order = AutoField()

    relation_type = BigIntegerField(default = 0)

    def getModel(self):
        item = None

        _c = ContentUnit()
        _s = StorageUnit()
        _c.setWrapper(self.wrapper)
        _s.setWrapper(self.wrapper)

        with self.wrapper.db_ref.bind_ctx([_c, _s]):
            if self.child_type == "ContentUnit":
                item = _c.select().where(ContentUnit.uuid == self.child)
            elif self.child_type == "StorageUnit":
                item = _s.select().where(StorageUnit.uuid == self.child)

            return item.get()

    def getStructure(self):
        model = self.getModel()
        item_append = {
            "type": self.relation_type,
            "item": None,
        }

        if model != None:
            item_append["item"] = model

        return item_append

    def getStructureWithModel(self):
        structure = self.getStructure()

        if structure.get("item") != None:
            structure["item"] = structure.get("item").getStructure()

        return structure
