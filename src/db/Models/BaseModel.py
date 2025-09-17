from peewee import Model

class BaseModel(Model):
    def setDb(self, db):
        self.old_db = self._meta.database
        self._meta.database = db

    @classmethod
    def setDbAtClass(self, db):
        self._meta.database = db
