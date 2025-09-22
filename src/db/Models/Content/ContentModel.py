from db.Models.BaseModel import BaseModel
from peewee import IntegerField
from playhouse.sqlite_ext import fn

from snowflake import SnowflakeGenerator

from app.Logger.LogSection import LogSection
from app.Logger.LogKind import LogKind
from app.App import logger

class ContentModel(BaseModel):
    uuid = IntegerField(unique=True, primary_key=True)

    @classmethod
    def ids(cls, id):
        logger.log(f"Searching {cls.self_name} by ids {str(id)}", section = ["DB", "Models"])

        if type(id) in [str, int]:
            _query = cls.select().where(cls.uuid == int(id))

            return _query.first()

        if type(id) in [list]:
            res = []
            _query = cls.select().where(cls.uuid.in_(id))

            for _e in _query:
                res.append(_e)

            return res

    @property
    def id(self) -> str:
        return self.uuid

    @property
    def name_id(self) -> str:
        return f"{self.short_name}_{self.uuid}"

    def isSaved(self) -> bool:
        return self.uuid != None

    def generateId(self):
        gen = SnowflakeGenerator(0)
        return str(next(gen))

    def getDbName(self):
        if self._meta.database.database == ":memory:":
            return "temp"
        else:
            return "content"

    def sign(self)->str:
        return f"__$|{self.short_name}_{self.uuid}"

    @classmethod
    def json_search(cls, query, property, key, value):
        return query.where(fn.json_extract(property, key) == value)

    async def beforeSave(self):
        pass

    async def postSave(self):
        logger.log(f"Saved {self.__class__.self_name} to db {self.getDbName()}, id: {self.uuid}", kind=LogKind.KIND_SUCCESS, section=["Saveable"])

    async def flush(self, **kwargs):
        await self.beforeSave()
        kwargs["to_temp"] = True

        self.save(**kwargs)
        await self.postSave()
