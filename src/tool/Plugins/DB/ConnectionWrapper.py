from Objects.Object import Object
from peewee import Database
from typing import Any
from pydantic import Field

class ConnectionWrapper(Object):
    name: str = Field()
    db: Any = Field()
