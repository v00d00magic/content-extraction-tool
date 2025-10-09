from Objects.Object import Object
from pydantic import Field

class Model(Object):
    uuid: int = Field(default=None)

