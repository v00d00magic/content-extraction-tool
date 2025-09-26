from DB.Models.BaseModel import BaseModel
from peewee import IntegerField
from playhouse.sqlite_ext import fn

from snowflake import SnowflakeGenerator

from App.Logger.LogKind import LogKind


class ContentModel(BaseModel):
    uuid = IntegerField(unique=True, primary_key=True)

    @classmethod
    def ids(cls, id):
        app.logger.log(f"Searching {cls.self_name} by ids {str(id)}", section = ["DB", "Models"])

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

    @property
    def name_db_id(self) -> str:
        parts = [self.getDbName(), self.short_name, str(self.uuid)]

        if self.uuid == None:
            parts[2] = "None"

        return "_".join(parts)

    def isSaved(self) -> bool:
        return self.uuid != None

    def generateId(self):
        gen = SnowflakeGenerator(0)
        return str(next(gen))

    def sign(self)->str:
        return f"__$|{self.short_name}_{self.uuid}"

    @classmethod
    def json_search(cls, query, property, key, value):
        return query.where(fn.json_extract(property, key) == value)

    async def beforeSave(self):
        pass

    async def postSave(self):
        app.logger.log(f"Saved {self.__class__.self_name} to db {self.getDbName()}, id: {self.uuid}", kind=LogKind.KIND_SUCCESS, section=["Saveable"])

    async def flush(self, **kwargs):
        '''Runs beforeSave(), saves model to temporary db
        '''
        await self.beforeSave()
        kwargs["to_temp"] = True

        self.save(**kwargs)
        await self.postSave()
