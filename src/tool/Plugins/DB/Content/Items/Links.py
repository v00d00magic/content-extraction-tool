from Objects.Object import Object
from pydantic import Field

class Links(Object):
    items: list = Field()
