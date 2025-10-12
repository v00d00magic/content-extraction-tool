from pydantic import BaseModel, computed_field
from .classproperty import classproperty

class Object(BaseModel):
    # we can't use __init__ because of fields initialization, so we creating second constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__class__.constructor(self)

    # do not copy *args and **kwargs, ok?
    def constructor(self):
        pass

    @classproperty
    def mro(cls) -> list:
        return cls.__mro__

    def init_subclass(cls):
        pass

    def __init_subclass__(cls):
        for item in cls.mro:
            if hasattr(item, "init_subclass") == True:
                getattr(item, "init_subclass")(cls)

            if item.__name__ == "BaseModel":
                item.__init_subclass__()
