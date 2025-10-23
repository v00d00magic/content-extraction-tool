from peewee import Model
from App import app

class Model(Model):
    @classmethod
    def setClsDB(cls, db):
        cls._meta.database = db

    @classmethod
    def setClsTableName(cls, name: str):
        cls._meta.table_name = name

    def setDb(self, db):
        self._meta.database = db
