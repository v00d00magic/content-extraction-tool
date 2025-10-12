from Objects.Object import Object
from pydantic import Field

class Outer(Object):
    thumbnail: dict = Field()
