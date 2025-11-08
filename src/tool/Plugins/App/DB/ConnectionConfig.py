from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase, DatabaseProxy, Database
from .ConnectionWrapper import ConnectionWrapper
from Objects.Object import Object
from Plugins.Data.Text import Text
from pydantic import Field
from typing import Any
from enum import Enum

class ConnectionEnum(Enum):
    sqlite = "sqlite"

class ConnectionConfig(Object):
    protocol: ConnectionEnum = Field(default=ConnectionEnum.sqlite)
    content: str = Field()
    name: str = Field()
    storage: str = Field(default=None)

    db: Any = None # Database

    def connect(self) -> Database:
        db = None
        match(self.protocol.value):
            case ConnectionEnum.sqlite.value:
                text = Text.use(
                    text = self.content
                )
                text.replaceCwd()
                db = SqliteDatabase(text.content.text)

        return db

    def create_tables(self, items: list) -> None:
        for item in items:
            item.setClsDB(self.db)
            item.setClsTableName(item.table_name)

        self.db.create_tables(items)
