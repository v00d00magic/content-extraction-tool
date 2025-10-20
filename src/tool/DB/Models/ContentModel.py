from .Model import Model
from snowflake import SnowflakeGenerator
from peewee import IntegerField

class ContentModel(Model):
    uuid = IntegerField(unique=True, primary_key=True)

    def generateId(self):
        gen = SnowflakeGenerator(0)
        return str(next(gen))

    def save(self, to_temp = False, **kwargs):
        if hasattr(self.__class__, "uuid") == True:
            self.uuid = self.generateId()

        kwargs["force_insert"] = True

        super().save(**kwargs)
