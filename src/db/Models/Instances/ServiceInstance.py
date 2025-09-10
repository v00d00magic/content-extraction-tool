from peewee import SmallIntegerField, TextField, AutoField, TimestampField, Model
from utils.MainUtils import parse_json, dump_json
import time

class ServiceInstance(Model):
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

        return parse_json(__data)

    def frontend_data_json(self):
        __data = self.frontend_data
        if __data != None:
            return {}

        return parse_json(__data) 

    def getStructure(self):
        obj = {}

        obj['id'] = self.id
        obj['service_name'] = self.service_name
        obj['display_name'] = self.display_name
        obj['data'] = self.data_json()
        obj['frontend_data'] = self.frontend_data_json()
        obj['interval'] = self.interval
        obj['created_at'] = int(self.created_at)

        return obj

    @staticmethod
    def get(id):
        return ServiceInstance.select().where(ServiceInstance.id == id).first()

    def setData(self, json):
        self.data = dump_json(json)
        #self.save()

    def updateData(self, json):
        orig = self.data_json()
        orig.update(json)

        self.data = dump_json(orig)
