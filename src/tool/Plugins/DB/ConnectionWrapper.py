from Objects.Object import Object
from peewee import Database
from pydantic import Field

class ConnectionWrapper(Object):
    name: str = Field()
    db: Database = Field()
