from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase, DatabaseProxy, Database
from .ConnectionWrapper import ConnectionWrapper
from Objects.Object import Object
from Plugins.Data.Text.Text import Text
from pydantic import Field
from enum import Enum

class ConnectionEnum(Enum):
    sqlite = "sqlite"

class ConnectionConfig(Object):
    protocol: ConnectionEnum = Field(default=ConnectionEnum.sqlite)
    content: str = Field()

    def getConnection(self) -> Database:
        db = None

        match(self.protocol.value):
            case ConnectionEnum.sqlite.value:
                _t = Text()
                _t = _t.cwdReplacement(self.content)
                db = SqliteDatabase(_t)

        return db

    def getWrapper(self, name):
        return ConnectionWrapper(
            name = name,
            db = self.getConnection()
        )
