from .Model import Model
from snowflake import SnowflakeGenerator

class ContentModel(Model):
    def generateId(self):
        gen = SnowflakeGenerator(0)
        return str(next(gen))

    def save(self, to_temp = False, **kwargs):
        if hasattr(self.__class__, "uuid") == True:
            self.uuid = self.generateId()

        kwargs["force_insert"] = True

        super().save(**kwargs)
