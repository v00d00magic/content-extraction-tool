from peewee import Model
from App.Logger.LogKind import LogKind
from DB.DBWrapper import DBWrapper
from DB.ModelDTO import ModelDTO
from App import app

class BaseModel(Model):
    @classmethod
    def setWrapperToModel(cls, wrapper: DBWrapper):
        cls.wrapper = wrapper
        cls.bind(cls.wrapper.db_ref)

        app.logger.log(f"Class: {cls.__name__}; Set wrapper to {cls.wrapper.db_name} (cls)", section = ["Saveable", "DB"])

    def setWrapper(self, wrapper: DBWrapper):
        self.wrapper = wrapper
        #self.bind(self.wrapper.db_ref)

        app.logger.log(f"Class: {self.__class__.__name__}; Set wrapper to {self.wrapper.db_name} (self)", section = ["Saveable", "DB"])

    @classmethod
    def setProxy(self, db):
        self._meta.database = db

    def save(self, to_temp = False, **kwargs):
        if hasattr(self.__class__, "uuid") == True:
            self.uuid = self.generateId()

        kwargs["force_insert"] = True
        if to_temp == True:
            self.setWrapper(app.db_connection.temp_db)

        super().save(**kwargs)

    def changeWrapper(self, wrapper):
        id_part = self.__class__.__name__
        if hasattr(self.__class__, "uuid") != None:
            id_part = self.name_db_id

        app.logger.log(f"Moving {id_part} from db {self.getDbName()}", kind = LogKind.KIND_HIGHLIGHT, section = ["DB", "Moving"])

        movement = ModelDTO()
        movement.moveTo(item = self, db_wrapper = wrapper, storage_units_move_storage = app.storage.get("storage_units"))

        app.logger.log(f"Moved {id_part} to db {self.getDbName()}", kind = LogKind.KIND_HIGHLIGHT, section = ["DB", "Moving"])

    def getDbName(self):
        return self.wrapper.db_name
