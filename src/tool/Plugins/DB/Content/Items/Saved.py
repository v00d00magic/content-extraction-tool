from Objects.Object import Object
from pydantic import Field

class Saved(Object):
    representation: str = Field()
    method: str = Field()
