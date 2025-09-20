from peewee import BigIntegerField, CharField, AutoField, Model, BooleanField
from db.Models.BaseModel import BaseModel

class ContentUnitRelation(BaseModel):
    RELATION_NONE = 0
    RELATION_REVISION = 1
    RELATION_THUMBNAIL = 2
    RELATION_DATA = 3

    table_name = 'content_relations'

    parent = CharField(max_length=100, null=True)
    child_type = CharField(max_length=20, default='ContentUnit')
    child = CharField(max_length=100, null=True)
    order = AutoField()
    #is_main = BooleanField(default=0)

    relation_type = BooleanField(default=0)
