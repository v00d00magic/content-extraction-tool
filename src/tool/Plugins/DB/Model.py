from Objects.Object import Object
from App import app
from pydantic import Field
from typing import ClassVar
from DB.Models.Model import Model as PeeweeModel
from Plugins.DB.ConnectionWrapper import ConnectionWrapper

class Model(Object):
    uuid: str = Field(default=None) # actually int but using str because of js JSON.parse int issues
    orm_model: ClassVar = None

    def flush(self, connection: ConnectionWrapper) -> PeeweeModel:
        new = self.toORM(connection)
        new.save()

        self.uuid = str(new.uuid)

        return new

    def toORM(self, connection: ConnectionWrapper) -> PeeweeModel:
        db_model = self.orm_model
        new = db_model()

        for name, val in self.toJson().items():
            if name in ["uuid"] or val == None:
                continue

            setattr(new, name, val)

        new.setDb(connection.db)

        return new

    def fromORM(self, item: PeeweeModel) -> Object:
        pass
