from peewee import CharField, AutoField, BigIntegerField
from db.Models.BaseModel import BaseModel
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
