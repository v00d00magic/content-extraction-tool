from peewee import TextField, TimestampField, BigIntegerField, AutoField
from db.Models.BaseModel import BaseModel
import time

class Stat(BaseModel):
    table_name = 'stats'
    id = AutoField()
    name = TextField(default='Untitled')
    type = TextField(default='default')
    linked_id = BigIntegerField(default=0)
    timestamp = TimestampField(default=time.time)
