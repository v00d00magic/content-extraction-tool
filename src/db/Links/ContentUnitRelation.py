from peewee import CharField, AutoField, BooleanField
from db.Models.BaseModel import BaseModel
from enum import Enum

class RelationEnum(Enum):
    RELATION_NONE = 0
    RELATION_REVISION = 1
    RELATION_THUMBNAIL = 2
    RELATION_DATA = 3

class ContentUnitRelation(BaseModel):
    table_name = 'content_relations'

    parent = CharField(max_length = 100, null=True)
    child_type = CharField(max_length = 20, default='ContentUnit')
    child = CharField(max_length = 100, null=True)
    order = AutoField()

    relation_type = BooleanField(default = RelationEnum.RELATION_NONE)
