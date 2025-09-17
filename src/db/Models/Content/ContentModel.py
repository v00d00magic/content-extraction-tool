from peewee import IntegerField
from db.Models.BaseModel import BaseModel
from snowflake import SnowflakeGenerator
from app.App import logger
from playhouse.sqlite_ext import fn

class ContentModel(BaseModel):
    uuid = IntegerField(unique=True, primary_key=True)

    @classmethod
    def ids(cls, id):
        logger.log(f"Searching {cls.self_name} by ids {str(id)}", section=logger.SECTION_DB)

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

    def isSaved(self) -> bool:
        return self.uuid != None

    def save(self, **kwargs):
        gen = SnowflakeGenerator(0)
        self.uuid = str(next(gen))

        super().save(**kwargs)

    def sign(self)->str:
        return f"__$|{self.short_name}_{self.uuid}"

    @classmethod
    def json_search(cls, query, property, key, value):
        return query.where(fn.json_extract(property, key) == value)

    async def beforeSave(self):
        pass

    async def flush(self):
        await self.beforeSave()
        self.save()

    def moveToDb(self):
        pass
