from peewee import Model
from App import app
from App.Logger.LogKind import LogKind
from DB.ModelDTO import ModelDTO

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
            self.setDb(app.db_connection.temp_db)

        super().save(**kwargs)

    def moveToDb(self, db):
        id_part = self.__class__.__name__
        if hasattr(self.__class__, "uuid") != None:
            id_part = f"{self.__class__.__name__}_{self.name_db_id}"

        app.logger.log(f"Moving {id_part} from db {self.getDbName()}", kind = LogKind.KIND_HIGHLIGHT, section = ["DB", "Moving"])

        movement = ModelDTO()
        movement.moveTo(self, db)

        app.logger.log(f"Moved {id_part} to db {self.getDbName()}", kind = LogKind.KIND_HIGHLIGHT, section = ["DB", "Moving"])

    def getDbName(self):
        if self.getDbPath() == ":memory:":
            return "temp"
        else:
            return "content"

    def getDbPath(self):
        return self._meta.database.database
