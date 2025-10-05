from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase, DatabaseProxy, Database
from Objects.Object import Object
from Plugins.Data.Text.Text import Text
from pydantic import Field
from enum import Enum

class ConnectionEnum(Enum):
    sqlite = "sqlite"

class ConnectionConfig(Object):
    protocol: ConnectionEnum = Field(default=ConnectionEnum.sqlite)
    content: str = Field()

    def getConnection(self):
        db = None

        match(self.protocol):
            case "sqlite":
                _t = Text()
                _t = _t.cwdReplacement(self.content)
                db = SqliteDatabase(_t)

        return db
