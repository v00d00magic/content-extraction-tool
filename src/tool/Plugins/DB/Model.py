from Objects.Object import Object
from App import app
from pydantic import Field
from typing import ClassVar
from DB.Models.Model import Model as PeeweeModel

class Model(Object):
    uuid: int = Field(default=None)
    orm: ClassVar = None

    def flush(self) -> PeeweeModel:
        return self.toORM()

    def toORM(self) -> PeeweeModel:
        db_model = self.orm
        new = db_model()

        for name, val in self.toJson().items():
            if name in ["uuid"] or val == None:
                continue

            setattr(new, name, val)

        # todo: save links
        new.save()

        return new

    def fromORM(self, item: PeeweeModel) -> Object:
        pass
