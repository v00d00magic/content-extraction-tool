from peewee import Model
from app.App import db_connection
from app.Logger.LogSection import LogSection
from app.App import logger
from db.ModelDTO import ModelDTO

class BaseModel(Model):
    def setDb(self, db):
        self.old_db = self._meta.database
        self._meta.database = db

    @classmethod
    def setDbAtClass(self, db):
        self._meta.database = db

    def save(self, to_temp = False, **kwargs):
        if hasattr(self.__class__, "uuid") == True:
            self.uuid = self.generateId()

        kwargs["force_insert"] = True
        if to_temp == True:
            self.setDb(db_connection.temp_db)

        super().save(**kwargs)

    def moveToDb(self, db):
        to_message = f"Moving {self.__class__.__name__} to another db"
        if hasattr(self.__class__, "uuid") != None:
            to_message = f"Moving {self.__class__.__name__}_{self.uuid} to another db"

        logger.log(to_message, section = ["DB", "Moving"])

        movement = ModelDTO()
        movement.moveTo(self, db)
