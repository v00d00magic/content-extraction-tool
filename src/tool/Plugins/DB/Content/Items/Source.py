from Objects.Object import Object
from pydantic import Field

class Source(Object):
    types: str = Field()
    content: str = Field()
