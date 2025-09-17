from peewee import SmallIntegerField, TextField, AutoField, TimestampField
from db.Models.BaseModel import BaseModel
from utils.Data.JSON import JSON
import time

class ServiceInstance(BaseModel):
    table_name = 'services'
    self_name = 'service'

    id = AutoField()
    service_name = TextField()
    display_name = TextField(null=True)
    frontend_data = TextField(default="{}")
    data = TextField(default="{}")
    interval = SmallIntegerField(default=60) # in seconds
    created_at = TimestampField(default=time.time())
    edited_at = TimestampField(null=True)

    def data_json(self):
        __data = self.data

        return JSON(__data).parse()

    def frontend_data_json(self):
        __data = self.frontend_data
        if __data != None:
            return {}

        return JSON(__data).parse() 

    def getStructure(self):
        payload = {}

        payload['id'] = self.id
        payload['service_name'] = self.service_name
        payload['display_name'] = self.display_name
        payload['data'] = self.data_json()
        payload['frontend_data'] = self.frontend_data_json()
        payload['interval'] = self.interval
        payload['created_at'] = int(self.created_at)

        return payload

    @staticmethod
    def get(id):
        return ServiceInstance.select().where(ServiceInstance.id == id).first()

    def setData(self, json):
        self.data = JSON(json).dump()
        #self.save()

    def updateData(self, json):
        orig = self.data_json()
        orig.update(json)

        self.data = JSON.dump(orig)
