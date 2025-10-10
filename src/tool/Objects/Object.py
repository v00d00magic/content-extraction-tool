from pydantic import BaseModel

class Object(BaseModel):
    # we can't use __init__ because of fields initialization, so we creating second constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__class__.constructor(self)

    # do not copy *args and **kwargs, ok?
    def constructor(self):
        pass
