from db.Models.BaseModel import BaseModel
from peewee import AutoField, TextField
from utils.Data.JSON import JSON

class ArgumentsDump(BaseModel):
    table_name = 'dumps'
    self_name = 'argument_dump'

    id = AutoField()
    executable = TextField(null=True)
    data = TextField(default="{}")

    @property
    def args(self):
        return JSON(self.data).parse()

    def getStructure(self):
        return {
            "id": self.id,
            "executable": self.executable,
            "data": self.args
        }
