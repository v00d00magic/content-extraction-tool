from .ContentModel import ContentModel
from peewee import TextField, BooleanField, FloatField, CharField

class ContentUnit(ContentModel):
    table_name = 'units'

    display_name = TextField(default='')
    display_description = TextField(default='')
    original_name = TextField(default='')
    original_description = TextField(default='')
    index_description = TextField(default='')

    # jsons
    content = TextField(null=True,default=None)
    source = TextField(null=True,default=None)
    outer = TextField(null=True,default=None)
    saved = TextField(null=True,default=None)

    # dates
    created_at = FloatField()
    declared_created_at = FloatField()
    edited_at = FloatField(null=True,default=None)

    # booleans
    is_collection = BooleanField(index=True,default=0)
    is_unlisted = BooleanField(index=True,default=0)
