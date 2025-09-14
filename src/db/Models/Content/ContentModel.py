from peewee import Model, IntegerField
from snowflake import SnowflakeGenerator
from playhouse.sqlite_ext import fn

class BaseModel(Model):
    uuid = IntegerField(unique=True, primary_key=True)

    @classmethod
    def ids(cls, id):
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

    def is_saved(self) -> bool:
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
